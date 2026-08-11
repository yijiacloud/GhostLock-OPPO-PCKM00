#!/bin/bash
cd /root/ksrc/linux-4.14.180 || exit 1
CC=/opt/ndk/android-ndk-r29/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android30-clang
cat > /tmp/off.c <<'EOF'
#define __KERNEL__
#define CONFIG_64BIT 1
#define CONFIG_ARM64 1
#include <linux/sched.h>
#include <stddef.h>
#include <stdio.h>
int main(void) {
  printf("struct task_struct size=%zu\n", sizeof(struct task_struct));
  printf("pid=%zu\n", offsetof(struct task_struct, pid));
  printf("tgid=%zu\n", offsetof(struct task_struct, tgid));
  printf("real_cred=%zu\n", offsetof(struct task_struct, real_cred));
  printf("cred=%zu\n", offsetof(struct task_struct, cred));
  printf("comm=%zu\n", offsetof(struct task_struct, comm));
  printf("tasks=%zu\n", offsetof(struct task_struct, tasks));
  printf("thread_group=%zu\n", offsetof(struct task_struct, thread_group));
  printf("real_parent=%zu\n", offsetof(struct task_struct, real_parent));
  return 0;
}
EOF
$CC -DCONFIG_ARM64_VA_BITS=48 -Iinclude -Iarch/arm64/include -Iarch/arm64/include/generated \
    -Iinclude/generated -Iinclude/uapi -Iarch/arm64/include/uapi \
    -Iinclude/generated/uapi -Iarch/arm64/include/generated/uapi \
    -nostdinc -isystem /opt/ndk/android-ndk-r29/toolchains/llvm/prebuilt/linux-x86_64/lib/clang/21/include \
    -O0 -o /tmp/off /tmp/off.c 2>&1 | head -40
echo "exit: ${PIPESTATUS[0]}"
