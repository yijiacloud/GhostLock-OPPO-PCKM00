import struct
d = open(r'D:\opporoot\boot\kernel','rb').read()
N = len(d)

def is_kernel_addr(v):
    return (v >> 40) == 0xffffff80 or ((v >> 40) == 0xffffffc0 and v < 0xffffffc000000000)

results = []
for p in range(4, N - 8, 4):
    nsyms = struct.unpack_from('<I', d, p)[0]
    if not (20000 <= nsyms <= 600000):
        continue
    # relative_base at p-8
    rb = struct.unpack_from('<Q', d, p - 8)[0]
    if not (0xffffff8000000000 <= rb < 0xffffffc000000000):
        continue
    # offsets array: from p-12 backwards, strictly decreasing, length nsyms, ending at 0
    # last offset = value at p-12
    last = struct.unpack_from('<I', d, p - 12)[0]
    if not (0 < last <= 0x20000000):
        continue
    # walk back nsyms entries: offsets[k] = d[p-12 - (nsyms-1-k)*4]
    start = p - 12 - (nsyms - 1) * 4
    if start < 0:
        continue
    first = struct.unpack_from('<I', d, start)[0]
    if first != 0:
        continue
    # verify increasing: check the whole array quickly (vectorized-ish)
    offs = struct.unpack_from('<%dI' % nsyms, d, start)
    if offs[-1] != last:
        continue
    if any(offs[i+1] <= offs[i] for i in range(nsyms - 1)):
        continue
    # names at p+4
    q = p + 4
    ok = True
    marks = [0]
    for i in range(nsyms):
        if q >= N:
            ok = False; break
        ln = d[q]
        if ln >= 0x80:
            ok = False; break
        q += 1 + ln
        if (i + 1) % 256 == 0:
            marks.append(q - (p + 4))
    if not ok:
        continue
    total = q - (p + 4)
    names_end = p + 4 + total
    nm = (nsyms + 255) // 256
    mstart = (names_end + 3) & ~3
    if mstart + nm * 4 > N:
        continue
    mvals = struct.unpack_from('<%dI' % nm, d, mstart)
    if mvals[0] != 0 or list(mvals) != marks:
        continue
    if any(mvals[i+1] <= mvals[i] for i in range(nm - 1)):
        continue
    # token table should follow markers
    tts = mstart + nm * 4
    results.append((p, nsyms, rb, start, mstart, tts))

print('MATCHES:', len(results))
for r in results:
    print('  num_syms@0x%x nsyms=%d relbase=0x%x offsets@0x%x markers@0x%x token_table_cand@0x%x' % r)
