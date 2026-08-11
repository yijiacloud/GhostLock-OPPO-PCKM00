#!/usr/bin/env python3
import re

BASE = 0xffffff8008080000
symtab = {}
with open(r'D:\opporoot\analysis\kallsyms_v2e.txt', 'r', encoding='utf-8', errors='replace') as f:
    for line in f:
        line = line.strip()
        m = re.match(r'^(0x[0-9a-f]+)\s+(\S+)$', line)
        if m:
            addr = int(m.group(1), 16)
            name = m.group(2)
            if name not in symtab:
                symtab[name] = addr

need = [
    'ashmem_fops','ashmem_misc','ashmem_ioctl','compat_ashmem_ioctl','ashmem_mmap',
    'ashmem_open','ashmem_release','ashmem_read_iter','ashmem_llseek','ashmem_show_fdinfo',
    'configfs_read_bin_file','configfs_write_bin_file','configfs_open_bin_file',
    'configfs_release_bin_file','generic_file_splice_read','noop_llseek','init_task',
    'init_uts_ns','empty_zero_page','root_task_group','selinux_state','selinux_enforcing_boot',
    'security_hook_heads','kmalloc_caches','anon_pipe_buf_ops','nfulnl_logger','sysctl_bootid',
    'init_cred','init_user_ns','init_groups','memstart_addr','module_alloc_base',
    'kallsyms_lookup_name','remove_waiter','rt_mutex_start_proxy_lock','futex_requeue',
    'futex_lock_pi','futex_wake','commit_creds','prepare_kernel_cred',
    'selinux_cred_blob_sizes','selinux_blob_sizes','cred_sid','init_user_ns',
    'futex','futex_global_futex','runtime_lock'
]
for s in need:
    if s in symtab:
        off = symtab[s] - BASE
        print(f"{s:32s} 0x{off:x}")
    else:
        print(f"{s:32s} MISSING")

# also check some extra ones for SELinux / configfs buffer
extra = ['configfs_open_file','configfs_buffer','configfs_bin_attribute',
         'selinux_state','selinux_enforcing_boot','selinux_cred_blob_sizes']
for s in extra:
    if s in symtab:
        off = symtab[s] - BASE
        print(f"{s:32s} 0x{off:x}")
