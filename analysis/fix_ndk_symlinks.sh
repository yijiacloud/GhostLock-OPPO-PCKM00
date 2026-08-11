#!/bin/bash
# Fix symlinks that were flattened to text files during drvfs copy
set -u
NDK=/opt/ndk/android-ndk-r29
BIN=$NDK/toolchains/llvm/prebuilt/linux-x86_64/bin
cd "$BIN" || exit 1

fix_file() {
  local f="$1"
  if [ -L "$f" ]; then return 0; fi
  if [ -f "$f" ]; then
    local first
    first=$(head -c 200 "$f")
    # If it's a tiny text file (1-2 lines, no shebang), treat as flattened symlink
    local lines
    lines=$(wc -l < "$f" 2>/dev/null)
    local size
    size=$(wc -c < "$f" 2>/dev/null)
    if [ "$size" -lt 300 ] && [ "$lines" -le 2 ]; then
      local target
      target=$(cat "$f" | tr -d '\n\r')
      if [ -n "$target" ] && [ "$target" != "#!/bin/sh" ] && [[ "$target" != \#* ]]; then
        if [ -e "$target" ]; then
          rm -f "$f"
          ln -s "$target" "$f"
          echo "FIXED: $f -> $target"
        else
          echo "WARN: target missing for $f -> $target"
        fi
      fi
    fi
  fi
}

count=0
for f in "$BIN"/*; do
  [ -f "$f" ] || continue
  fix_file "$(basename "$f")"
  count=$((count+1))
done
echo "scanned $count files"
echo "=== verify ==="
ls -la clang clang++ ld.lld lld 2>&1
echo "=== clang version ==="
./clang --version 2>&1 | head -2
