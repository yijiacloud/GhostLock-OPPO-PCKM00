#!/bin/bash
NDK=/opt/ndk/android-ndk-r29/toolchains/llvm/prebuilt/linux-x86_64
# mm_init vaddr from kallsyms
grep -E ' mm_init$' /mnt/d/opporoot/analysis/kallsyms_v2e.txt
# text file offset = 0x20000. mm_init kallsyms? find it
