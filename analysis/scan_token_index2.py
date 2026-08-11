import struct
d = open(r'D:\opporoot\boot\kernel','rb').read()
N = len(d)

def validate(p):
    a = struct.unpack_from('<256H', d, p)
    # strict increasing
    for i in range(255):
        if a[i+1] <= a[i]:
            return None
    last = a[255]
    ts = p - last - 1
    if ts < 0:
        return None
    # token_table = d[ts : p-1] ; each token ends with NUL, content printable
    for i in range(256):
        s = ts + a[i]
        if i == 255:
            e = p - 1
        else:
            e = ts + a[i+1] - 1
        if e < s:
            return None
        if d[e] != 0:
            return None
        for b in d[s:e]:
            if not (0x20 <= b <= 0x7e):
                return None
    return (p, last, ts)

results = []
# scan step 2 first
for p in range(0, N - 512, 2):
    v0 = d[p] | (d[p+1] << 8)
    v1 = d[p+2] | (d[p+3] << 8)
    vl = d[p+510] | (d[p+511] << 8)
    if v0 > 0x20:
        continue
    if v1 <= v0:
        continue
    if not (200 <= vl <= 0x10000):
        continue
    r = validate(p)
    if r:
        results.append(r)

print('step2 validated:', len(results))
for r in results[:10]:
    print('  idx=0x%x last=%d token_table=0x%x' % r)

if not results:
    for p in range(0, N - 512, 1):
        v0 = d[p] | (d[p+1] << 8)
        v1 = d[p+2] | (d[p+3] << 8)
        vl = d[p+510] | (d[p+511] << 8)
        if v0 > 0x20:
            continue
        if v1 <= v0:
            continue
        if not (200 <= vl <= 0x10000):
            continue
        r = validate(p)
        if r:
            results.append(r)
    print('step1 validated:', len(results))
    for r in results[:10]:
        print('  idx=0x%x last=%d token_table=0x%x' % r)
