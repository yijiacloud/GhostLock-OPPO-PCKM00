# GhostLock — OPPO PCKM00 (4.14.180) PoC

**CVE-2026-43499 (GhostLock)** — Linux kernel `futex` priority-inheritance
use-after-free local privilege escalation PoC, ported to the **OPPO PCKM00
(OP4A57, SM6150, Android 11, kernel 4.14.180-perf+)**.

> **DISCLAIMER / 免责声明**
> This project is for **authorized security research and educational purposes
> only**. Do not use it on any device you do not own or are not explicitly
> authorized to test. Running the exploit may crash the kernel. The author
> assumes no liability for any misuse or damage.
>
> 本项目仅用于**授权的安全研究与教育目的**。请勿在非本人所有或未获明确授权的设备上使用。运行利用可能导致内核崩溃，作者不承担任何滥用或损失的责任。

---

## 1. Vulnerability

CVE-2026-43499 (GhostLock) is a use-after-free in the Linux kernel futex
priority-inheritance code. The bug lives in `remove_waiter()` being misused in
the proxy-lock rollback path of `rt_mutex_start_proxy_lock()`. The free'd
`rt_mutex_waiter` (allocated on the kernel stack) is re-interpreted as an
attacker-controlled `fd_set` copied in by `pselect()`, which yields an
arbitrary-write primitive.

**Affected range:** Linux 4.x–6.x (introduced 2011). 4.14 series fully
affected. See `report.md` for the full analysis and verified symbol offsets.

### Exploit chain

```
futex requeue-pi UAF
   └─> pselect fd_set stack copy (fake rt_mutex_waiter / fake task)
         └─> arbitrary write (rt_mutex tree ops / sched_setattr)
               └─> overwrite ashmem_fops -> configfs bin read/write
                     └─> pipe_buffer page rewrite (physical RW primitive)
                           └─> patch current task cred -> root
```

The PoC runs entirely in userspace via `LD_PRELOAD` — no device reboot
required (unless the kernel panics).

---

## 2. Target

| Field         | Value                                    |
|---------------|------------------------------------------|
| Device        | OPPO PCKM00 / OP4A57                     |
| SoC           | Qualcomm SM6150                          |
| Android       | 11 (RKQ1.200903.002)                     |
| Security patch| 2022-09-05                               |
| Kernel        | 4.14.180-perf+ (arm64, clang 10.0.7)     |
| Build         | `OPPO/PCKM00/PCKM00:11/RKQ1.200903.002/1635513065:user/release-keys` |

> Porting to other 4.14 devices: copy `exploit/targets/oppo-pckm00/target.h`
> and regenerate the symbol offsets from your kernel image (see `analysis/`).

---

## 3. Repository layout

```
.
├── report.md                    # Full vulnerability analysis & verified offsets
├── exploit/
│   ├── Makefile                 # Build preload.so (Windows NDK / WSL)
│   ├── src/
│   │   ├── preload.c            # LD_PRELOAD entry + forced disk logging + su
│   │   ├── main.c               # Orchestration (waiter/owner/consumer threads)
│   │   ├── slide.c              # KASLR leak (boot_id / nfulnl loggers)
│   │   ├── fops.c               # ashmem_fops overwrite + configfs primitive
│   │   ├── pipe.c               # pipe_buffer physrw primitive
│   │   ├── root.c               # task walk + cred patch + seccomp/selinux
│   │   ├── util.c               # kernelsnitch, skb page prep, kernel RW
│   │   ├── su_daemon.c          # embedded su server (drop-in)
│   │   ├── su_blob.S            # .incbin of su_daemon
│   │   └── wallpaper_blob.S     # .incbin of wallpaper payload
│   ├── targets/oppo-pckm00/target.h   # 4.14.180 symbol/struct offsets
│   └── assets/wallpaper.webp    # embedded wallpaper payload
├── analysis/                    # kernel image / kallsyms extraction scripts
└── LICENSE                      # Apache-2.0 (same as upstream GhostLock)
```

---

## 4. Build

Requires Android NDK r29 (`aarch64-linux-android30-clang`).

### Windows NDK

```bat
set NDK=C:\path\to\android-ndk-r29
make NDK=%NDK%
```

### WSL (recommended)

```bash
# put NDK at /opt/ndk/android-ndk-r29 (linux-x86_64 toolchain)
cd exploit
make wsl
# or directly:
bash ../analysis/build_preload.sh
```

Output: `exploit/preload.so` (64-bit aarch64 ELF shared object).

The build also compiles `su_daemon.c` to a PIE binary and embeds it (plus the
wallpaper) into the `.so` via the `.S` blobs.

---

## 5. Usage

```bash
adb push exploit/preload.so /data/local/tmp/preload.so
adb shell LD_PRELOAD=/data/local/tmp/preload.so id
```

On success the shell reports `uid=0(root)`. A `su` daemon is installed to
`/apex/com.android.virt/bin/su` (falling back to `/data/local/tmp/su`) and an
embedded wallpaper is applied as a persistence/verification artifact.

### Forced real-time disk logging

All `pr_*` diagnostics are also written to
**`/sdcard/Download/log_<timestamp>.txt`** (falling back to
`/data/local/tmp/log_<timestamp>.txt`), with `O_SYNC` + `fsync()` on every
line so logs survive a kernel panic / reboot — pull them with:

```bash
adb pull /sdcard/Download/log_*.txt
```

---

## 6. Notes & Limitations

- **KASLR**: the PoC leaks the slide via the `boot_id`/nfulnl logger path
  (`slide.c`) plus an ashmem_fops verification pass (`fops.c`).
- **4.14 vs 6.x differences handled** in this port:
  - configfs uses legacy `.read`/`.write` (no `read_iter`/`write_iter`),
  - `ashmem_fops` has no `show_fdinfo`,
  - `generic_file_splice_read` replaces `copy_splice_read`,
  - `selinux_enforcing` lives inside `struct selinux_state`,
  - 4.14 `rt_mutex_waiter` / `pipe_inode_info` / `cred` layouts.
- Some struct offsets (e.g. `task_struct.seccomp`) are best-effort; failure to
  patch seccomp does **not** block the cred-overwrite root.
- Running the exploit may trigger a kernel panic (~97% reliability in ~5s on
  the target); use an isolated device.

---

## 7. Credits

- **NebuSec** — original GhostLock research & exploit framework
  (`IonStack/CVE-2026-43499`), Apache-2.0.
  https://github.com/NebuSec/CyberMeowfia
- KernelSnitch (futex hash side-channel) is embedded under its upstream terms.

## License

Apache-2.0 — see [LICENSE](LICENSE).
