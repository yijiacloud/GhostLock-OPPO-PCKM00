#include <linux/mm_types.h>
#include <linux/sched.h>
#include <stddef.h>

#define PACK(label, val) \
  const unsigned long label[] __attribute__((used)) = { (unsigned long)(val) };

PACK(k_mm_struct_size, sizeof(struct mm_struct))
PACK(k_rb_node_size, sizeof(struct rb_node))
PACK(k_rb_root_cached, sizeof(struct rb_root_cached))
PACK(k_mm_mmap_off, offsetof(struct mm_struct, mmap))
PACK(k_mm_count_off, offsetof(struct mm_struct, mm_count))
PACK(k_mm_pgd_off, offsetof(struct mm_struct, pgd))
PACK(k_mm_owner_off, offsetof(struct mm_struct, owner))
PACK(k_mm_rss_off, offsetof(struct mm_struct, rss_stat))
PACK(k_task_pid_off, offsetof(struct task_struct, pid))
PACK(k_task_tgid_off, offsetof(struct task_struct, tgid))
PACK(k_task_cred_off, offsetof(struct task_struct, cred))
PACK(k_task_real_cred_off, offsetof(struct task_struct, real_cred))
PACK(k_task_comm_off, offsetof(struct task_struct, comm))
PACK(k_task_seccomp_off, offsetof(struct task_struct, seccomp))
PACK(k_task_atomic_off, offsetof(struct task_struct, atomic_flags))
PACK(k_task_prio_off, offsetof(struct task_struct, prio))
PACK(k_task_pi_waiters_off, offsetof(struct task_struct, pi_waiters))
PACK(k_task_tasks_off, offsetof(struct task_struct, tasks))
