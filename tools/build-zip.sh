#!/bin/sh
# Build the installable Kodi zip: a top-level folder named after the add-on id.
set -e
cd "$(dirname "$0")/.."
ID=skin.xelp
VER=$(sed -n 's/.*<addon id="skin.xelp" version="\([^"]*\)".*/\1/p' addon.xml)
rm -rf dist/.stage && mkdir -p dist/.stage/$ID
git ls-files -z | grep -zv -e '^dist/' -e '^tools/' -e '^docs/' -e '^\.gitignore$' | xargs -0 -I{} cp --parents {} dist/.stage/$ID/
(cd dist/.stage && zip -qr ../$ID-$VER.zip $ID)
rm -rf dist/.stage
echo "built dist/$ID-$VER.zip"
