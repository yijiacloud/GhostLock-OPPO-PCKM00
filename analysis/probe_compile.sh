#!/bin/bash
cd /root/ksrc/linux-4.14.180 || exit 1
ls include/generated/ 2>&1 | head
echo "--- test compile ---"
cat > /tmp/t.c <<'EOF'
#include <linux/task_struct.h>
#include <stddef.h>
#include <stdio.h>
int main(void) {
  printf("pid=%zu\n", offsetof(struct task_struct, pid));
  return 0;
}
EOF
/opt/ndk/android-ndk-r29/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android30-clang \
  -D__KERNEL__ -Iinclude -Iarch/arm64/include -O0 -o /tmp/t /tmp/t.c 2>&1 | head -20
echo "compile exit: $?"
