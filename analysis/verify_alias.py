#!/usr/bin/env python3
KBT=0xffffff8008080000
PO=0xffffff8000000000
PHYS_OFF=0x80000000
LOAD=0x88080000
DELTA=(LOAD-PHYS_OFF)&0xffffffffffffffff
def alias(img):
    return (PO | ((img-KBT+DELTA)&0xffffffffffffffff))
tests={
 "_text":0xffffff8008080000,
 "loggers":0xffffff800a213888,
 "bootid":0xffffff800a6a36c0,
 "init_task":0xffffff800a21df00,
 "root_tg":0xffffff800a52ff00,
 "sysctl_bootid":0xffffff800a6a36c0,
 "ashmem_fops":0xffffff8009879fd0,
 "kmalloc_caches":0xffffff8009d226a8,
}
print("DELTA=%016x"%DELTA)
for n,a in tests.items():
    al=alias(a)
    ok = (0xffffff8000000000 <= al < 0xffffffc000000000)
    print("%-14s img=%016x alias=%016x %s"%(n,a,al,"OK" if ok else "BAD"))
