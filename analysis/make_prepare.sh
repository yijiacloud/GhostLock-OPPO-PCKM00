#!/bin/bash
cd /root/ksrc/linux-4.14.180 || exit 1
export PATH=/root/mk/usr/bin:/usr/bin:/bin:$PATH
MUSL=/opt/musl/x86_64-linux-musl-cross/bin/x86_64-linux-musl
CC=/opt/ndk/android-ndk-r29/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android30-clang

echo '=== prepare (full) ==='
TARGET="${1:-prepare}"
make ARCH=arm64 \
  CC=$CC \
  HOSTCC=$MUSL-gcc HOSTAR=$MUSL-ar HOSTLD=$MUSL-ld \
  HOSTCFLAGS=-static HOSTLDFLAGS=-static \
  $TARGET 2>&1 | tail -25
echo "=== exit: $? ==="