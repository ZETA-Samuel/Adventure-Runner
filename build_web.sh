#!/bin/sh
set -eu

cd "$(dirname "$0")"
.venv/bin/pygbag --build main.py

index="build/web/index.html"
if ! grep -Fq "browserfs.min.js" "$index"; then
    printf "pygbag template did not include browserfs.min.js in %s\n" "$index" >&2
    exit 1
fi

sed -i 's#<script src="[^"]*browserfs.min.js"></script>#<script src="https://pygame-web.github.io/pygbag/0.0/browserfs.min.js"></script>#' "$index"
