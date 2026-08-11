#!/bin/bash
cp /mnt/d/opporoot/analysis/mm_size_probe.c /root/ksrc/mm_size_probe.c
cp /mnt/d/opporoot/analysis/probe_mm_size.sh /root/ksrc/probe_mm_size.sh
bash /root/ksrc/probe_mm_size.sh
NDK=/opt/ndk/android-ndk-r29/toolchains/llvm/prebuilt/linux-x86_64
echo "=== .rodata hex (each field = 8 bytes LE) ==="
"$NDK/bin/llvm-objdump" -s -j .rodata /root/ksrc/mmprobe.o
