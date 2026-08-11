#!/bin/bash
echo "=== PSELECT / SHIFT defines ==="
grep -n 'PSELECT_WAITER_WORD_SHIFT\|SLIDE_PSELECT_WORD_SHIFT\|PSELECT_ROUTE_NFDS\|SLIDE_PSELECT_NFDS' \
  /mnt/d/opporoot/exploit/src/common.h \
  /mnt/d/opporoot/exploit/src/slide.c \
  /mnt/d/opporoot/exploit/src/fops.c \
  /mnt/d/opporoot/exploit/targets/oppo-pckm00/target.h
