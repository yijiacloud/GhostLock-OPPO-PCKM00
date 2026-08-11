#!/bin/bash
# Compile-time size probe: read values from symbol names
cd /root/ksrc/linux-4.14.180 || exit 1
NDK=/opt/ndk/android-ndk-r29/toolchains/llvm/prebuilt/linux-x86_64
RESDIR="$NDK/lib/clang/21/include"
"$NDK/bin/aarch64-linux-android30-clang" -c \
  -D__KERNEL__ -DCC_HAVE_ASM_GOTO -ffreestanding -DCONFIG_64BIT \
  -DCONFIG_ARM64_VA_BITS=39 -DCONFIG_ARM64_PAGE_SHIFT=12 \
  -DCONFIG_ARM64_4K_PAGES=1 -DCONFIG_PGTABLE_LEVELS=3 \
  -DCONFIG_CPUMASK_OFFSTACK=1 \
  -U__linux__ -Ulinux -U__unix__ -Uunix \
  -include /root/ksrc/linux-4.14.180/include/generated/autoconf.h \
  -include /root/ksrc/linux-4.14.180/include/linux/kconfig.h \
  -nostdinc \
  -isystem "$RESDIR" \
  -Iarch/arm64/include -Iarch/arm64/include/generated \
  -Iinclude -Iinclude/generated \
  -Iarch/arm64/include/uapi -Iarch/arm64/include/generated/uapi \
  -Iinclude/uapi -Iinclude/generated/uapi \
  -O0 -o /root/ksrc/mmprobe.o /root/ksrc/mm_size_probe.c 2> /root/ksrc/mmprobe.err
echo "RC=$?"
grep -E "error:" /root/ksrc/mmprobe.err | head -15
echo "--- symbol-encoded sizes ---"
"$NDK/bin/llvm-nm" /root/ksrc/mmprobe.o 2>/dev/null | grep 'sz_'
