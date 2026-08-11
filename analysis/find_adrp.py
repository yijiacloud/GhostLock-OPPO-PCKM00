#!/usr/bin/env python3
import struct
d = open('/mnt/d/opporoot/boot/kernel','rb').read()
TFO = 0x20000
TEXT_VADDR = 0xffffff8008080000
TEXT_END = 0xffffff8009400000  # __start_rodata
str_vaddr = 0xffffff8009adc654
page = str_vaddr & ~0xfff
print("searching adrp loading page %#x" % page)

# adrp: immhi:imm lo encoding. Scan text range.
found = []
for off in range(TFO, TFO + (TEXT_END - TEXT_VADDR), 4):
    w = struct.unpack_from('<I', d, off)[0]
    if (w & 0x9f000000) == 0x90000000:  # adrp
        immhi = (w >> 5) & 0x7ffff
        immlo = (w >> 29) & 0x3
        imm = (immhi << 2) | immlo
        if imm & 0x1000000:
            imm -= 0x2000000
        addr = (off - TFO) + TEXT_VADDR
        base = (addr & ~0xfff) + (imm << 12)
        if base == page:
            found.append((off, addr))
print("adrp hits:", [(hex(o), hex(a)) for o, a in found])
