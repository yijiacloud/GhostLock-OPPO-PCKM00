#!/usr/bin/env python3
import struct
d = open('/mnt/d/opporoot/boot/kernel','rb').read()
TFO = 0x20000
TEXT_VADDR = 0xffffff8008080000

def vaddr_to_off(v):
    return (v - TEXT_VADDR) + TFO

# disassemble around 0xffffff80085e248c to see kmem_cache_create("mm_struct", SIZE,...)
start = vaddr_to_off(0xffffff80085e2400)
end = start + 0x300
for off in range(start, end, 4):
    w = struct.unpack_from('<I', d, off)[0]
    v = TEXT_VADDR + (off - TFO)
    desc = ""
    if (w & 0xff800000) == 0x91000000:
        rd, rn, imm12 = w&0x1f, (w>>5)&0x1f, (w>>10)&0xfff
        desc = "add x%d, x%d, #0x%x" % (rd, rn, imm12)
    elif (w & 0x7fe00000) in (0x72800000, 0xd2800000):
        imm16, rd = (w>>5)&0xffff, w&0x1f
        desc = "movz x%d, #0x%x" % (rd, imm16)
    elif (w & 0x7fe00000) in (0x72a00000, 0xd2a00000):
        imm16, rd, hw = (w>>5)&0xffff, w&0x1f, (w>>21)&0x3
        desc = "movk x%d, #0x%x, lsl#%d" % (rd, imm16, hw*16)
    elif (w & 0x7f000000) == 0x94000000:
        off24 = (w & 0x3ffffff)
        if off24 & 0x2000000: off24 -= 0x4000000
        tgt = v + off24*4
        desc = "bl %#x" % tgt
    elif (w & 0xff000000) == 0xf9400000:
        rt, rn, imm12 = w&0x1f, (w>>5)&0x1f, (w>>10)&0xfff
        desc = "ldr x%d, [x%d, #0x%x]" % (rt, rn, imm12<<3)
    if desc:
        print("%#x: %s" % (v, desc))
