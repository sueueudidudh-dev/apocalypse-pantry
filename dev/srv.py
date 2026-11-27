"""Dedicated-server self-test for one Apocalypse Delight build.

  py dev/srv.py <target>        target like 1.21.1-fabric, 1.20.1-forge, 1.21.1-neoforge

Reuses the test servers in D:/minecraft mods razrab/_test/srv-<target>/ (installed for Stardew Delight). For the run,
every other mod except Fabric API and Farmer's Delight is moved to mods_off/ and put back afterwards. The server starts with
-Dapocalypsedelight.selftest=true and gets "stop" after SELFTEST DONE. Prints the result lines and suspicious log lines.
"""
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEST = r'D:\minecraft mods razrab\_test'
_TMP = os.path.join(TEST, 'tmp')
os.makedirs(_TMP, exist_ok=True)
os.environ['TMP'] = os.environ['TEMP'] = _TMP
JDK = {17: r'C:\Users\Karasik\.gradle\jdks\eclipse_adoptium-17-amd64-windows.2',
       21: r'C:\Users\Karasik\.gradle\jdks\eclipse_adoptium-21-amd64-windows.2',
       25: r'C:\Users\Karasik\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2'}
JAVA = {'1.18.2-forge': 17, '1.19.2-forge': 17, '1.20.1-forge': 17, '1.20.1-fabric': 17, '1.21.1-neoforge': 21,
        '1.21.1-fabric': 21, '1.21.5-fabric': 21, '1.21.8-fabric': 21, '1.21.10-fabric': 21, '1.21.11-fabric': 21,
        '26.1-fabric': 25, '26.2-fabric': 25, '26.3-fabric': 25}
LOADER = {'1.18.2-forge': '1.18.2-40.3.0', '1.19.2-forge': '1.19.2-43.5.0', '1.20.1-forge': '1.20.1-47.4.0',
          '1.21.1-neoforge': '21.1.267'}


def mod_version():
    m = re.search(r'^mod\.version\s*=\s*"([^"]+)"', open(os.path.join(ROOT, 'stonecutter.properties.toml'), encoding='utf-8').read(), re.M)
    return m.group(1)


def command(target, d):
    jv = os.path.join(JDK[JAVA[target]], 'bin', 'java.exe')
    flag = '-Dapocalypsedelight.selftest=true'
    if target.endswith('fabric'):
        return [jv, flag, '-Xmx2G', '-jar', 'fabric-server-launch.jar', 'nogui']
    lv = LOADER[target]
    if target.endswith('neoforge'):
        return [jv, flag, '-Xmx2G', f'@libraries/net/neoforged/neoforge/{lv}/win_args.txt', 'nogui']
    return [jv, flag, '-Xmx2G', f'@libraries/net/minecraftforge/forge/{lv}/win_args.txt', 'nogui']


def main():
    target = sys.argv[1]
    d = os.path.join(TEST, f'srv-{target}')
    if not os.path.isdir(d):
        raise SystemExit(f'no test server in {d}')
    mods, off = os.path.join(d, 'mods'), os.path.join(d, 'mods_off')
    os.makedirs(off, exist_ok=True)
    moved = []
    for f in os.listdir(mods):
        if f.endswith('.jar') and not f.startswith(('fabric-api', 'FarmersDelight')):
            shutil.move(os.path.join(mods, f), os.path.join(off, f))
            if not f.startswith('apocalypsedelight'):
                moved.append(f)
    mc, loader = target.split('-')
    v = mod_version()
    jar = os.path.join(ROOT, 'build', 'libs', v, f'apocalypsedelight-{loader}-{mc}-{v}.jar')
    shutil.copy(jar, mods)
    shutil.rmtree(os.path.join(d, 'world'), ignore_errors=True)
    log = os.path.join(d, 'ap-server.log')
    try:
        with open(log, 'w', encoding='utf-8', errors='replace') as out:
            p = subprocess.Popen(command(target, d), cwd=d, stdin=subprocess.PIPE, stdout=out, stderr=subprocess.STDOUT)
            deadline, done_at, stopped, code = time.time() + 900, None, False, None
            while code is None:
                code = p.poll()
                if code is not None:
                    break
                if time.time() > deadline:
                    p.kill()
                    code = 'TIMEOUT'
                    break
                if not stopped:
                    txt = open(log, encoding='utf-8', errors='replace').read()
                    if done_at is None and 'Done (' in txt:
                        done_at = time.time()
                    if 'SELFTEST DONE' in txt or (done_at and time.time() - done_at > 90):
                        time.sleep(2)
                        p.stdin.write(b'stop\n')
                        p.stdin.flush()
                        stopped = True
                time.sleep(1)
    finally:
        for f in os.listdir(mods):
            if f.startswith('apocalypsedelight'):
                os.remove(os.path.join(mods, f))
        for f in moved:
            shutil.move(os.path.join(off, f), os.path.join(mods, f))
        shutil.rmtree(os.path.join(d, 'world'), ignore_errors=True)
    text = open(log, encoding='utf-8', errors='replace').read()
    print(f'== {target}: exit {code}, {len(text.splitlines())} lines, log {log}')
    for pat in (r'Done \(', r'Apocalypse Delight: \d+ foods', r'SELFTEST \d+ recipes', r'SELFTEST DONE'):
        m = re.findall(r'.*' + pat + r'.*', text)
        print('  ' + (m[-1].strip()[:200] if m else f'MISSING: {pat}'))
    for l in re.findall(r'.*SELFTEST FAIL.*', text)[:30]:
        print('  X ' + l.strip()[:300])
    bad = [l for l in text.splitlines() if re.search(r'/(WARN|ERROR|FATAL)\]|\[(WARN|ERROR)\]|Exception|Caused by', l)
           and re.search(r'apocalypse|recipe|advancement|mixin|Exception|Caused by|Missing|Failed|parse', l, re.I)]
    for l in bad[:40]:
        print('  ! ' + l.strip()[:300])
    print(f'  {len(bad)} suspicious lines')


if __name__ == '__main__':
    main()
