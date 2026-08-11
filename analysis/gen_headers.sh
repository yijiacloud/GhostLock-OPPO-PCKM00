#!/bin/bash
# Manually create minimal generated headers needed to compile offsetof program
cd /root/ksrc/linux-4.14.180 || exit 1

mkdir -p include/generated/uapi/linux
mkdir -p arch/arm64/include/generated/uapi/asm
mkdir -p arch/arm64/include/generated/asm
mkdir -p include/generated/asm

# Minimal autoconf.h with key CONFIGs for task_struct layout
cat > include/generated/autoconf.h <<'EOF'
#define CONFIG_ARM64 1
#define CONFIG_64BIT 1
#define CONFIG_SMP 1
#define CONFIG_PREEMPT 1
#define CONFIG_THREAD_INFO_IN_TASK 1
#define CONFIG_SCHED_INFO 1
#define CONFIG_KEYS 1
#define CONFIG_SECURITY 1
#define CONFIG_AUDIT 1
#define CONFIG_FUTEX 1
#define CONFIG_EPOLL 1
#define CONFIG_SIGNALFD 1
#define CONFIG_TIMERFD 1
#define CONFIG_EVENTFD 1
#define CONFIG_SHMEM 1
#define CONFIG_AIO 1
#define CONFIG_IO_URING 1
#define CONFIG_BLOCK 1
#define CONFIG_CGROUPS 1
#define CONFIG_MEMCG 1
#define CONFIG_BLK_CGROUP 1
#define CONFIG_CPUSETS 1
#define CONFIG_USER_NS 1
#define CONFIG_PID_NS 1
#define CONFIG_NET_NS 1
#define CONFIG_IPC_NS 1
#define CONFIG_UTS_NS 1
#define CONFIG_TIME_NS 1
#define CONFIG_SECCOMP 1
#define CONFIG_SECCOMP_FILTER 1
#define CONFIG_SECURITY_SELINUX 1
#define CONFIG_PERF_EVENTS 1
#define CONFIG_FTRACE 1
#define CONFIG_STACKTRACE 1
#define CONFIG_DEBUG_BUGVERBOSE 1
#define CONFIG_VMAP_STACK 1
#define CONFIG_MMU 1
#define CONFIG_SCHED_MUQSS 1
#define CONFIG_HAVE_ARM64_CPU_SUSPEND 1
#define CONFIG_ARM64_PAGE_SHIFT 12
#define CONFIG_ARM64_VA_BITS_39 1
#define CONFIG_ARM64_VA_BITS 39
#define CONFIG_PGTABLE_LEVELS 3
EOF

# utsrelease.h
cat > include/generated/utsrelease.h <<'EOF'
#define UTS_RELEASE "4.14.180-perf"
EOF

# asm/types.h via asm-generic
ln -sf ../../../../../include/uapi/asm-generic/types.h arch/arm64/include/generated/uapi/asm/types.h 2>/dev/null
ln -sf ../../../../../include/uapi/asm-generic/bitsperlong.h arch/arm64/include/generated/uapi/asm/bitsperlong.h 2>/dev/null

# bound.h (NR_CPUS etc)
cat > include/generated/bounds.h <<'EOF'
#define __NR_CPUS_BITS 8
#define NR_CPUS_BITS 8
EOF

# compile.h
cat > include/generated/compile.h <<'EOF'
EOF

echo "generated headers created"
ls -la arch/arm64/include/generated/uapi/asm/
echo "---"
ls include/generated/
