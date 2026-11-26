"""Builds every target, then runs the dedicated-server self-test for each one and prints a summary.

  py dev/check_all.py            all targets
  py dev/check_all.py 1.21.1-fabric 26.3-fabric
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_all  # noqa: E402


def main():
    wanted = sys.argv[1:] or build_all.targets()
    print('== build', flush=True)
    subprocess.call([sys.executable, os.path.join(HERE, 'build_all.py')] + wanted, cwd=ROOT)
    print('== self-test', flush=True)
    summary = []
    for t in wanted:
        out = subprocess.run([sys.executable, os.path.join(HERE, 'srv.py'), t], cwd=ROOT, capture_output=True, text=True,
                             encoding='utf-8', errors='replace')
        text = out.stdout + out.stderr
        m = re.search(r'SELFTEST DONE: (\d+) ok, (\d+) failed', text)
        res = f'{m.group(1)} ok, {m.group(2)} failed' if m else 'NO RESULT'
        summary.append((t, res))
        print(f'{t:16} {res}', flush=True)
        for line in text.splitlines():
            if ' X ' in line or 'MISSING' in line or 'Traceback' in line or 'Error' in line:
                print('    ' + line.strip()[:300], flush=True)
    good = sum(1 for _, r in summary if r.endswith(' 0 failed'))
    print(f'\nself-test passed on {good} of {len(summary)}')


if __name__ == '__main__':
    main()
