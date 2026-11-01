#!/usr/bin/env python3
"""Build the installable Kodi zip: dist/skin.xelp-<version>.zip with a top-level skin.xelp/ folder.
Only git-tracked files are packaged, minus the development folders (tools/, docs/, dist/)."""
import os, re, subprocess, zipfile
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)
ver = re.search(r'<addon id="skin\.xelp" version="([^"]+)"', open("addon.xml", encoding="utf-8").read()).group(1)
files = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
skip = ("dist/", "tools/", "docs/")
files = [f for f in files if f and not f.startswith(skip) and f != ".gitignore"]
os.makedirs("dist", exist_ok=True)
out = "dist/skin.xelp-%s.zip" % ver
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(files):
        z.write(f, "skin.xelp/" + f)
print("built %s (%d files, %.1f MB)" % (out, len(files), os.path.getsize(out) / 1e6))
