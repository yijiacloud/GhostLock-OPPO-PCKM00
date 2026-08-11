#!/bin/bash
grep -n 'CONFIG_DEBUG_RT_MUTEXES\|CONFIG_DEBUG_MUTEXES' /root/ksrc/linux-4.14.180/include/generated/autoconf.h
echo "exit=$?"
echo "=== all DEBUG_LOCK ==="
grep -n 'CONFIG_DEBUG' /root/ksrc/linux-4.14.180/include/generated/autoconf.h | head
