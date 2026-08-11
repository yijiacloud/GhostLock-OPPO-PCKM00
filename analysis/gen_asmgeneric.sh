#!/bin/bash
# Copy all asm-generic uapi headers to arch/arm64/include/generated/uapi/asm
# and non-uapi to arch/arm64/include/generated/asm
cd /root/ksrc/linux-4.14.180 || exit 1

GEN_UAPI=arch/arm64/include/generated/uapi/asm
GEN_ASM=arch/arm64/include/generated/asm

mkdir -p "$GEN_UAPI" "$GEN_ASM"

# uapi asm-generic headers
for f in include/uapi/asm-generic/*.h; do
  base=$(basename "$f")
  # skip some that have arch-specific versions
  case "$base" in
    int-ll64.h|int-l64.h|types.h|bitsperlong.h|posix_types.h|fcntl.h|ioctl.h|stat.h|statfs.h|termios.h|ioctls.h|poll.h|errno.h|param.h|resource.h|siginfo.h|signal.h|socket.h|sockios.h|swab.h|ucontext.h|unistd.h|auxvec.h|byteorder.h)
      cp "$f" "$GEN_UAPI/$base"
      ;;
  esac
done

# kernel (non-uapi) asm-generic headers
for f in include/asm-generic/*.h; do
  base=$(basename "$f")
  cp "$f" "$GEN_ASM/$base"
done

echo "copied uapi: $(ls $GEN_UAPI | wc -l) headers"
echo "copied asm: $(ls $GEN_ASM | wc -l) headers"
