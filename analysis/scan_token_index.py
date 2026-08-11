import struct
d = open(r'D:\opporoot\boot\kernel','rb').read()
N = len(d)

def check_window(p):
    a = struct.unpack_from('<256H', d, p)
    if a[0] > 0x20:
        return None
    if not (250 <= a[255] <= 0x20000):
        return None
    for i in range(255):
        if a[i+1] <= a[i]:
            return None
    return a

hits = []
step = 2
for p in range(0, N - 512, step):
    # fast prefilter: first, second, last entries
    v0 = d[p] | (d[p+1] << 8)
    v1 = d[p+2] | (d[p+3] << 8)
    vl = d[p+510] | (d[p+511] << 8)
    if v0 > 0x20:
        continue
    if v1 <= v0:
        continue
    if not (250 <= vl <= 0x20000):
        continue
    a = check_window(p)
    if a is not None:
        ts = p - a[255] - 1
        hits.append((p, a[255], ts))

print('token_index hits (step 2):', len(hits))
for p, last, ts in hits[:20]:
    print('  idx=0x%x last=%d token_table=0x%x' % (p, last, ts))

if not hits:
    print('--- retry step 1 ---')
    for p in range(0, N - 512, 1):
        v0 = d[p] | (d[p+1] << 8)
        v1 = d[p+2] | (d[p+3] << 8)
        vl = d[p+510] | (d[p+511] << 8)
        if v0 > 0x20:
            continue
        if v1 <= v0:
            continue
        if not (250 <= vl <= 0x20000):
            continue
        a = check_window(p)
        if a is not None:
            ts = p - a[255] - 1
            hits.append((p, a[255], ts))
    print('token_index hits (step 1):', len(hits))
    for p, last, ts in hits[:20]:
        print('  idx=0x%x last=%d token_table=0x%x' % (p, last, ts))
