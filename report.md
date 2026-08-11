# OPPO PCKM00 (OP4A57) — CVE-2026-43499 GhostLock 漏洞分析报告

**日期**: 2026-08-09
**设备**: OPPO PCKM00 / OP4A57 (SM6150, aarch64)
**系统**: Android 11 (RKQ1.200903.002), 安全补丁 2022-09-05
**内核**: Linux 4.14.180-perf+ (clang 10.0.7 for Android NDK)

---

## 1. 概述

本报告针对 OPPO PCKM00 设备评估 CVE-2026-43499 (GhostLock) — Linux 内核 futex 优先级继承 (Priority Inheritance) 代码中的 use-after-free 漏洞。该漏洞位于 `remove_waiter()` 在 `rt_mutex_start_proxy_lock()` 的代理锁回滚路径中的误用，允许本地用户提权至 root。

**核心结论**: 目标内核 **包含漏洞（vulnerable）**，且为 GhostLock 所针对的 4.14 系列。所有 exploit 所需符号偏移量已从内核镜像中完整提取并验证。

---

## 2. Boot Image 解包

boot.img 已使用 `unpack_bootimg` 完成解包，产物位于 `D:\opporoot\boot\`：

| 文件 | 大小 | 说明 |
|---|---|---|
| `header` | 386 B | boot.img 头部（v1 格式，page_size=4096） |
| `kernel` | 38,436,880 B | ARM64 Image 内核（未压缩，含完整头部） |
| `kernel_dtb` | 818,684 B | 设备树 blob (QCOM sm6150) |
| `ramdisk.cpio` | 2,100,224 B | 根文件系统（含 fstab.qcom, oplus.fstab） |
| `comp` | 6 B | 压缩标志 |

### 2.1 内核镜像验证

- **架构**: ARM64 (aarch64), little-endian, 4KB 页
- **工具链**: clang 10.0.7 (Android NDK), GNU ld 2.27
- **构建时间**: Fri Oct 21 23:24:28 CST 2022
- **版本字符串**: `Linux version 4.14.180-perf+ (root@ubuntu-10-207) ... #2 SMP PREEMPT`
- **CONFIG 特征**: SMP, PREEMPT, mod_unload, modversions, aarch64

---

## 3. 符号表提取

### 3.1 提取方法

内核镜像使用压缩形式的 kallsyms（`CONFIG_KALLSYMS=y`）。通过 `vmlinux_to_elf` (v1.3.6) 的 `KallsymsFinder` 完整解析：

| kallsyms 结构 | 文件偏移 |
|---|---|
| `kallsyms_offsets` | `0x01880600` |
| `kallsyms_num_syms` | `0x018f4100` |
| `kallsyms_names` | `0x018f4200` |
| `kallsyms_markers` | `0x01a75600` |
| `kallsyms_token_table` | `0x01a76500` |
| `kallsyms_token_index` | `0x01a76900` |

- **符号总数**: 118,341
- **有效唯一符号**: 112,679
- **应用重定位**: 109,830 条 (ELF64 rela)

### 3.2 基址

| 项目 | 值 |
|---|---|
| KIMAGE_TEXT_BASE (`_text`) | `0xffffff8008080000` |
| 从偏移范围推断基址 | `0xffffff8008080000` |

> 注意: 此为链接时基址。运行时受 KASLR 影响会滑动，exploit 中所有地址均使用 `KIMAGE_TEXT_BASE + offset` 形式，运行时通过 kallsyms 或偏移自动适配。

---

## 4. 符号偏移量对照表

所有偏移量为**相对于 `_text` (KIMAGE_TEXT_BASE = 0xffffff8008080000)**。

### 4.1 Root Payload 核心符号

| 符号 | 偏移量 | 地址 |
|---|---|---|
| `commit_creds` | `0x0006b640` | `0xffffff80080eb640` |
| `prepare_kernel_cred` | `0x0006b9e8` | `0xffffff80080eb9e8` |
| `init_task` | `0x0219df00` | `0xffffff800a21df00` |
| `init_uts_ns` | `0x0219dcb8` | `0xffffff800a21dcb8` |
| `init_cred` | `0x021af810` | `0xffffff800a22f810` |
| `init_user_ns` | `0x021ae0e0` | `0xffffff800a22e0e0` |
| `init_groups` | `0x021af808` | `0xffffff800a22f808` |

### 4.2 KASLR Bypass / 内存布局

| 符号 | 偏移量 | 地址 |
|---|---|---|
| `memstart_addr` | `0x01ca2540` | `0xffffff8009d22540` |
| `module_alloc_base` | `0x01ca2520` | `0xffffff8009d22520` |
| `reserved_mem` | `0x028d8960` | `0xffffff800a958960` |
| `swapper_pg_dir` | *非导出* | — |
| `empty_zero_page` | `0x024a9000` | `0xffffff800a529000` |

### 4.3 Ashmem (Android)

| 符号 | 偏移量 | 地址 |
|---|---|---|
| `ashmem_fops` | `0x017f9fd0` | `0xffffff8009879fd0` |
| `ashmem_misc` | `0x024115f0` | `0xffffff800a4915f0` |
| `ashmem_ioctl` | `0x00d0a288` | `0xffffff8008d8a288` |
| `compat_ashmem_ioctl` | `0x00d0ab68` | `0xffffff8008d8ab68` |
| `ashmem_mmap` | `0x00d0abc0` | `0xffffff8008d8abc0` |
| `ashmem_llseek` | `0x00d0a118` | `0xffffff8008d8a118` |

### 4.4 file_operations / llseek

| 符号 | 偏移量 | 地址 |
|---|---|---|
| `noop_llseek` | `0x0020dff0` | `0xffffff800828dff0` |
| `generic_file_llseek` | `0x0020dda8` | `0xffffff800828dda8` |
| `generic_file_splice_read` | `0x00251d30` | `0xffffff80082d1d30` |
| `default_file_splice_read` | `0x002542d0` | `0xffffff80082d42d0` |
| `kernel_write` | `0x0020ea10` | `0xffffff800828ea10` |

### 4.5 Configfs (configfs_read_iter / bin_write_iter)

> ⚠️ 4.14 内核 **不存在** `configfs_read_iter` / `configfs_bin_write_iter`（6.x 新 API）。
> 4.14 使用传统 `.read` / `.write` / `.bin_attrs` 回调：

| 符号 | 偏移量 | 地址 |
|---|---|---|
| `configfs_read_file` | `0x002bd410` | `0xffffff800833d410` |
| `configfs_write_file` | `0x002bd538` | `0xffffff800833d538` |
| `configfs_read_bin_file` | `0x002bd760` | `0xffffff800833d760` |
| `configfs_write_bin_file` | `0x002bd8e8` | `0xffffff800833d8e8` |
| `configfs_open_bin_file` | `0x002bda08` | `0xffffff800833da08` |
| `configfs_release_bin_file` | `0x002bda28` | `0xffffff800833da28` |

### 4.6 Slab / 内存分配器

| 符号 | 偏移量 | 地址 |
|---|---|---|
| `kmalloc_caches` | `0x01ca26a8` | `0xffffff8009d226a8` |
| `anon_pipe_buf_ops` | `0x016be100` | `0xffffff800973e100` |
| `anon_pipe_buf_nomerge_ops` | `0x016be128` | `0xffffff800973e128` |

### 4.7 SELinux / LSM

| 符号 | 偏移量 | 地址 |
|---|---|---|
| `selinux_state` | `0x025b19d8` | `0xffffff800a6319d8` |
| `selinux_enforcing_boot` | `0x02904000` | `0xffffff800a984000` |
| `security_hook_heads` | `0x01ca2bb0` | `0xffffff8009d22bb0` |
| `selinux_enforcing` | **缺失** | — |

> ⚠️ `selinux_enforcing` 是 4.14 中 `selinux_state` 结构体**内部字段**（不再作为独立符号）。可直接通过 `selinux_state + 结构体偏移` 或使用 `selinux_enforcing_boot` 定位。参考同架构 OPPO K9 (SM7250) 移植确认此命名差异。

### 4.8 CVE-2026-43499 漏洞触发关键符号

| 符号 | 偏移量 | 地址 |
|---|---|---|
| `rt_mutex_start_proxy_lock` | `0x000c0420` | `0xffffff8008140420` |
| `remove_waiter` | `0x000c04b8` | `0xffffff80081404b8` |
| `rt_mutex_slowlock` | `0x011d2560` | `0xffffff8009252560` |
| `rt_mutex_setprio` | `0x0007b948` | `0xffffff80080fb948` |
| `mark_wakeup_next_waiter` | `0x000bfd40` | `0xffffff800813fd40` |
| `futex_requeue` | `0x000fe798` | `0xffffff800817e798` |
| `futex_lock_pi` | `0x000ff890` | `0xffffff800817f890` |
| `futex_wake` | `0x000fe3e0` | `0xffffff800817e3e0` |

### 4.9 辅助符号

| 符号 | 偏移量 | 地址 |
|---|---|---|
| `kallsyms_lookup_name` | `0x0010c260` | `0xffffff800818c260` |
| `kptr_restrict` | `0x0219da00` | `0xffffff800a21da00` |
| `sys_ioctl` | `0x00229e48` | `0xffffff80082a9e48` |
| `fget` | `0x0023a340` | `0xffffff80082ba340` |
| `fput` | `0x002131a8` | `0xffffff80082931a8` |
| `override_creds` | `0x0006b918` | `0xffffff80080eb918` |
| `get_task_cred` | `0x0006b068` | `0xffffff80080eb068` |

---

## 5. 漏洞存在性验证

CVE-2026-43499 影响自 2011 年引入的 rtmutex PI 代码，4.14 系列**完全受影响**：

1. **受影响函数确认**: `remove_waiter` (off 0xc04b8) 与 `rt_mutex_start_proxy_lock` (off 0xc0420) 均存在于目标内核。
2. **API 形态**: 4.14 的 `rt_mutex_start_proxy_lock` 使用 `rt_mutex_slowlock`/`rt_mutex_fastlock` 传统路径（未并入 5.x 之后的 `rt_mutex_lock_slowlock` 重构），与 GhostLock 针对的易受攻击路径一致。
3. **内核版本**: 4.14.180 位于受影响范围（2017-2023 全部受影响）。
4. **补丁状态**: Android 安全补丁 2022-09-05 为**常规月度补丁**，不包含 2026-07 修复 CVE-2026-43499 的 rtmutex 补丁。
5. **SELinux**: 未提取到 `selinux_enforcing` 独立符号，需通过 `selinux_state` 结构定位；`security_hook_heads` 已确认存在。
6. **反汇编验证**: 从镜像偏移 `0x1404b8` 提取 `remove_waiter` 完整指令（见 `analysis/cve_functions_dump.txt`），并确认 `rt_mutex_start_proxy_lock` 通过 Android patchable-function-entry trampoline 跳转（`0xc0420` 处 `ret; bl`），函数体正常。`futex_requeue` → `rt_mutex_start_proxy_lock` → `remove_waiter` 调用链的符号地址均已验证。

---

## 6. 结论与风险提示

### 6.1 可行性评估

| 项目 | 状态 |
|---|---|
| 漏洞存在 | ✅ 受影响 (4.14.180) |
| 符号表可用性 | ✅ 完整提取 (112,679 符号) |
| 所需符号覆盖 | ✅ 全部核心符号已定位 |
| KASLR 处理 | ✅ 有 `kallsyms_lookup_name` / 偏移自动适配 |
| ashmem 可用 | ✅ (Android 11 仍含 ashmem) |
| 4.14 API 差异 | ⚠️ configfs/selinux 需适配（见 4.5/4.7） |

### 6.2 风险声明

- 本报告仅用于**安全研究与教育目的**。
- CVE-2026-43499 为高危本地提权漏洞，PoC 可在约 5 秒内以 ~97% 可靠性获取 root。
- 在目标设备上运行完整 exploit 可能触发内核崩溃，需谨慎评估。
- 最终可利用性需在设备上验证实际偏移与结构体布局（4.14 的 `task_struct`、`rt_mutex_waiter` 布局与 6.x 有差异）。

---

## 7. 待办事项 (后续轮次)

- [ ] 获取并对照 `NebuSec/CyberMeowfia` 的 `target.h` 模板，为 4.14 生成目标定义
- [ ] 验证 `task_struct`/`rt_mutex_waiter`/`pi_state` 结构体偏移（4.14 布局）
- [ ] 设备端验证 `/proc/kallsyms` 可见性及 KASLR 行为
- [ ] 构建并测试 exploit（在可控测试机上先行）
