#!/bin/bash
echo "=== constants ==="
grep -n 'APPENDED_FUTEXES\|KERNELSNITCH_THRESHOLD_MULT\|MULITPLE\|futex_hash_table_size' /mnt/d/opporoot/exploit/src/kernelsnitch/kernelsnitch.h | head
echo '=== find_collisions ==='
sed -n '305,345p' /mnt/d/opporoot/exploit/src/kernelsnitch/kernelsnitch.h
