import struct
d = open(r'D:\opporoot\boot\kernel','rb').read()
N = len(d)

def parse_names(pos, count, maxlen=0x80):
    """parse 'count' symbols at file offset pos; return (total_len, list of byte offsets of symbols at multiples of 256)"""
    p = pos
    marks = [0]
    for i in range(count):
        if p >= N:
            return None
        ln = d[p]
        if ln >= maxlen:
            return None
        p += 1
        if p + ln > N:
            return None
        p += ln
        if (i + 1) % 256 == 0:
            marks.append(p - pos)
    return (p - pos, marks)

candidates = []
# scan 4-byte aligned
for p in range(0, N - 8, 4):
    v = struct.unpack_from('<I', d, p)[0]
    if not (20000 <= v <= 600000):
        continue
    # quick sanity: parse first 8 symbols
    q = p + 4
    ok = True
    for i in range(8):
        if q >= N:
            ok = False; break
        ln = d[q]
        if ln >= 0x80:
            ok = False; break
        q += 1 + ln
    if not ok:
        continue
    candidates.append((p, v))

print('num_syms candidates:', len(candidates))

for p, v in candidates[:400]:
    res = parse_names(p + 4, v)
    if res is None:
        continue
    total, marks = res
    names_end = p + 4 + total
    # markers at names_end aligned to 4
    mstart = (names_end + 3) & ~3
    nm = (v + 255) // 256
    if mstart + nm * 4 > N:
        continue
    if mstart + nm*4 > 0x1d25000:   # must be near/within .rodata region
        continue
    mvals = struct.unpack_from('<%dI' % nm, d, mstart)
    if mvals[0] != 0:
        continue
    inc = all(mvals[i+1] > mvals[i] for i in range(nm-1))
    if not inc:
        continue
    # compare with parse offsets (marks)
    if marks != list(mvals):
        continue
    print('MATCH  num_syms at 0x%x  count=%d  names 0x%x-0x%x  markers 0x%x (n=%d)' % (
        p, v, p+4, names_end, mstart, nm))
