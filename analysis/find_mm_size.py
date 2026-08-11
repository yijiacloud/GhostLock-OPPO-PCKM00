#!/usr/bin/env python3
import struct
d = open('/mnt/d/opporoot/boot/kernel','rb').read()
TFO = 0x20000
TEXT_VADDR = 0xffffff8008080000
str_vaddr = 0xffffff8009adc654

def vaddr_to_off(v):
    return (v - TEXT_VADDR) + TFO

# Find adrp for page 0xffffff8009adc000 in the init text region (after start_kernel)
page = str_vaddr & ~0xfff
lo = page & 0xfff  # 0x654

# scan full text for adrp page then nearby add imm to reach 0x654
for off in range(TFO, vaddr_to_off(0xffffff8009e80000), 4):
    w = struct.unpack_from('<I', d, off)[0]
    if (w & 0x9f000000) == 0x90000000:
        immhi = (w >> 5) & 0x7ffff
        immlo = (w >> 29) & 0x3
        imm = (immhi << 2) | immlo
        if imm & 0x1000000: imm -= 0x2000000
        addr = (off - TFO) + TEXT_VADDR
        base = (addr & ~0xfff) + (imm << 12)
        if base == page:
            # look at next few instructions for add x, x, #0x654 (low12)
            for j in range(1, 5):
                off2 = off + j*4
                if off2+4 > len(d): break
                w2 = struct.unpack_from('<I', d, off2)[0]
                # add imm12: 0x91000000 | imm12<<10 | rn<<5 | rd ; lsl 0
                if (w2 & 0xff800000) == 0x91000000:
                    imm12 = (w2 >> 10) & 0xfff
                    if imm12 == lo:
                        print("MATCH adrp@%#x add@%#x vaddr=%#x" % (off, off2, TEXT_VADDR+(off2-TFO)))
                        # print the instruction after (mov size / bl kmem_cache_create)
                        for k in range(1, 8):
                            off3 = off2 + k*4
                            if off3+4 > len(d): break
                            w3 = struct.unpack_from('<I', d, off3)[0]
                            # movz/movk
                            if (w3 & 0x7fe00000) in (0x72800000, 0xd2800000, 0x72a00000, 0xd2a00000):
                                imm16 = (w3 >> 5) & 0xffff
                                hw = (w3 >> 21) & 0x3
                                rd = w3 & 0x1f
                                print("   +%d movz/movk x%d imm16=%#x hw=%d" % (k, rd, imm16, hw))
                            elif (w3 & 0x7f000000) == 0x94000000:  # bl
                                print("   +%d bl" % k)
print("done")
