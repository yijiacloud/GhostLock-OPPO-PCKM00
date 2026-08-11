#include <stdio.h>
#include <stddef.h>
#include <linux/fs.h>

int main(void) {
  printf("file_operations (4.14.180 arm64)\n");
  printf("  owner          %zu\n", offsetof(struct file_operations, owner));
  printf("  llseek         %zu\n", offsetof(struct file_operations, llseek));
  printf("  read           %zu\n", offsetof(struct file_operations, read));
  printf("  write          %zu\n", offsetof(struct file_operations, write));
  printf("  read_iter      %zu\n", offsetof(struct file_operations, read_iter));
  printf("  write_iter     %zu\n", offsetof(struct file_operations, write_iter));
  printf("  unlocked_ioctl %zu\n", offsetof(struct file_operations, unlocked_ioctl));
  printf("  compat_ioctl   %zu\n", offsetof(struct file_operations, compat_ioctl));
  printf("  mmap           %zu\n", offsetof(struct file_operations, mmap));
  printf("  open           %zu\n", offsetof(struct file_operations, open));
  printf("  release        %zu\n", offsetof(struct file_operations, release));
  printf("  splice_read    %zu\n", offsetof(struct file_operations, splice_read));
  printf("  show_fdinfo    %zu\n", offsetof(struct file_operations, show_fdinfo));
  return 0;
}
