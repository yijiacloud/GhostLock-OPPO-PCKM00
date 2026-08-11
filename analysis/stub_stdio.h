#ifndef _STUB_STDIO_H
#define _STUB_STDIO_H
#define NULL ((void*)0)
typedef unsigned long size_t;
typedef long ssize_t;
struct _IO_FILE;
typedef struct _IO_FILE FILE;
extern FILE *stdout;
int printf(const char *fmt, ...);
#endif
