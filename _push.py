import base64, os, subprocess
REPO = r"D:\minecraft mods razrab\ZombieFood"
tok = None
for line in open(r"D:\minecraft mods razrab\secrets\github_token.env", encoding="utf-8-sig"):
    if line.strip().startswith("GITHUB_TOKEN="):
        tok = line.strip().split("=", 1)[1].strip().strip('"').strip("'")
basic = base64.b64encode(f"x-access-token:{tok}".encode()).decode()
env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_CONFIG_COUNT="1",
           GIT_CONFIG_KEY_0="http.https://github.com/.extraheader", GIT_CONFIG_VALUE_0="AUTHORIZATION: basic " + basic)
def git(*a):
    p = subprocess.run(["git", "-c", "user.name=sueueudidudh-dev", "-c", "user.email=359911170+sueueudidudh-dev@users.noreply.github.com", *a],
                       cwd=REPO, env=env, capture_output=True, text=True, timeout=300)
    print("$ git", a[0], p.returncode, (p.stdout + p.stderr).replace(tok, "***").replace(basic, "***").strip()[-600:])
git("add", "-A")
git("commit", "-q", "-m", "Mod page: image links point to page/docs on GitHub")
git("push", "-q", "origin", "main")
git("status", "-sb")
