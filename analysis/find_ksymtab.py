import struct
d = open(r'D:\opporoot\boot\kernel','rb').read()
N = len(d)

POOL_OFF = 0x1ceae68
POOL_LEN = 0x1d24640 - 0x1ceae68
TEXT_OFF = 0x80000

# candidate kernel image bases (KIMAGE_VADDR)
bases = {
    'va39': 0xffffff8000000000,
    'va48': 0xffff000000000000,
    'va48b': 0xffffffc000000000,
}

for name, base in bases.items():
    X = base + (POOL_OFF - TEXT_OFF)
    hits = []
    for w in range(0, N - 8, 8):
        v = struct.unpack_from('<Q', d, w)[0]
        off = v - X
        if 0 <= off < POOL_LEN:
            if d[POOL_OFF + off] != 0:
                hits.append(w)
    print('%s: pool_vaddr=0x%x  name-pointer hits=%d' % (name, X, len(hits)))
    if hits:
        print('   first few at:', [hex(x) for x in hits[:8]])
