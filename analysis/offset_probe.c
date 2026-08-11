#include <stddef.h>
#include <stdio.h>

/* Minimal kernel-compatible typedefs needed for offsetof on the structs */
typedef struct { int counter; } atomic_t;
typedef struct { long long counter; } atomic_long_t;
typedef struct { unsigned int val; } spinlock_t;
typedef struct { unsigned int tail; } optimistic_spin_queue_t;
typedef struct list_head { struct list_head *next, *prev; } list_head_t;
typedef struct rb_node { unsigned long __rb_parent_color; struct rb_node *rb_right; struct rb_node *rb_left; } rb_node_t;
typedef unsigned int umode_t;
typedef int pid_t_k;
typedef struct { atomic_long_t owner; spinlock_t wait_lock; optimistic_spin_queue_t osq; list_head_t wait_list; } mutex_t;
typedef struct { unsigned int flags; atomic_t count; } wait_queue_head_t_placeholder;

int main(void) {
  return 0;
}
