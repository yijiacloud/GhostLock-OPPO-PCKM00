#!/bin/bash
cd /root/ksrc/linux-4.14.180 || exit 1
export PATH=/root/mk/usr/bin:/usr/bin:/bin:$PATH
MUSL=/opt/musl/x86_64-linux-musl-cross/bin/x86_64-linux-musl
MAKECMD="make ARCH=arm64 HOSTCC=$MUSL-gcc HOSTAR=$MUSL-ar HOSTLD=$MUSL-ld HOSTCFLAGS=-static HOSTLDFLAGS=-static"

echo '=== defconfig ==='
$MAKECMD defconfig 2>&1 | tail -15
echo "=== exit: $? ==="
