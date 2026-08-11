#!/usr/bin/env python3
import struct
d = open('/mnt/d/opporoot/boot/kernel','rb').read()
TFO = 0x20000
TEXT_VADDR = 0xffffff8008080000
kmem_cache_create = 0xffffff800823f308

def vaddr_to_off(v):
    return (v - TEXT_VADDR) + TFO

# find all bl kmem_cache_create in init text (start_kernel area)
start = vaddr_to_off(0xffffff8009e00000)
end = vaddr_to_off(0xffffff8009e60000)
bls=[]
for off in range(start, end, 4):
    w = struct.unpack_from('<I', d, off)[0]
    if (w & 0x7f000000) == 0x94000000:
        off24 = w & 0x3ffffff
        if off24 & 0x2000000: off24 -= 0x4000000
        tgt = (off - TFO) + TEXT_VADDR + off24*4
        if tgt == kmem_cache_create:
            bls.append(off)
print("bl kmem_cache_create in start_kernel window:", [hex(TEXT_VADDR+(o-TFO)) for o in bls])

# For each, disassemble preceding ~30 instrs, look for movz/movk x1 with imm in [0x300,0x500]
for b in bls:
    print("== call at %#x ==" % (TEXT_VADDR+(b-TFO)))
    for off in range(b-40*4, b, 4):
        w = struct.unpack_from('<I', d, off)[0]
        if (w & 0x7fe00000) in (0x72800000, 0xd2800000):  # movz
            imm16, rd = (w>>5)&0xffff, w&0x1f
            if rd == 1 and imm16:
                print("  movz x1, #0x%x  (size?)" % imm16)
        elif (w & 0x7fe00000) in (0x72a00000, 0xd2a00000):  # movk
            imm16, rd, hw = (w>>5)&0xffff, w&0x1f, (w>>21)&0x3
            if rd == 1:
                print("  movk x1, #0x%x lsl#%d" % (imm16, hw*16))
