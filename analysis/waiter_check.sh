#!/bin/bash
echo "=== 4.14 rt_mutex_waiter ==="
grep -n 'struct rt_mutex_waiter {' -A 18 /root/ksrc/linux-4.14.180/kernel/locking/rtmutex_common.h
echo "=== 6.x (frankel) WAITER offsets ==="
grep -n 'WAITER_' /mnt/d/opporoot/exploit/src/../targets/oppo-pckm00/target.h | head -20
