#include <linux/rbtree.h>
#include <stddef.h>

/* 4.14 rt_mutex_waiter layout (rtmutex_common.h, CONFIG_DEBUG_RT_MUTEXES off) */
struct mock_rt_mutex_waiter {
    struct rb_node tree_entry;
    struct rb_node pi_tree_entry;
    struct task_struct *task;
    struct rt_mutex *lock;
    int prio;
    u64 deadline;
};

#define PACK(label, val) \
  const unsigned long label[] __attribute__((used)) = { (unsigned long)(val) };

PACK(k_w_size, sizeof(struct mock_rt_mutex_waiter))
PACK(k_w_tree, offsetof(struct mock_rt_mutex_waiter, tree_entry))
PACK(k_w_pi_tree, offsetof(struct mock_rt_mutex_waiter, pi_tree_entry))
PACK(k_w_task, offsetof(struct mock_rt_mutex_waiter, task))
PACK(k_w_lock, offsetof(struct mock_rt_mutex_waiter, lock))
PACK(k_w_prio, offsetof(struct mock_rt_mutex_waiter, prio))
PACK(k_w_deadline, offsetof(struct mock_rt_mutex_waiter, deadline))
