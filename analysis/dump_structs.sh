#!/bin/bash
cd /root/ksrc/linux-4.14.180
echo "=== struct pipe_buffer ==="
sed -n '/^struct pipe_buffer {/,/^};/p' include/linux/pipe_fs_i.h
echo ""
echo "=== struct pipe_inode_info ==="
sed -n '/^struct pipe_inode_info {/,/^};/p' include/linux/pipe_fs_i.h
echo ""
echo "=== struct configfs_bin_attribute ==="
sed -n '/^struct configfs_bin_attribute {/,/^};/p' fs/configfs/configfs_internal.h include/linux/configfs.h 2>/dev/null
echo ""
echo "=== struct configfs_attribute ==="
sed -n '/^struct configfs_attribute {/,/^};/p' include/linux/configfs.h
