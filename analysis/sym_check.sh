#!/bin/bash
echo "=== mm_init / related symbols ==="
grep -E ' mm_init$| do_basic_setup| kernel_init_freeable| start_kernel$| rest_init$| fork_init$' /mnt/d/opporoot/analysis/kallsyms_v2e.txt
echo "=== mm_cachep context: symbols near it ==="
grep -E 'mm_cachep|kmem_cache' /mnt/d/opporoot/analysis/kallsyms_v2e.txt | head
