import struct
d = open(r'D:\opporoot\boot\kernel','rb').read()
N = len(d)

def is_printable_or_nul(b):
    return b == 0 or (0x20 <= b <= 0x7e)

# find runs of printable-or-nul bytes with length >= 200
runs = []
start = None
for i in range(N):
    if is_printable_or_nul(d[i]):
        if start is None:
            start = i
    else:
        if start is not None:
            ln = i - start
            if ln >= 200:
                runs.append((start, i, ln))
            start = None
if start is not None and N - start >= 200:
    runs.append((start, N, N - start))

print('printable runs (>=200):', len(runs))
# For each run, check if immediately following (aligned?) 512 bytes are increasing u16
for (s, e, ln) in sorted(runs, key=lambda x: x[1]-x[0])[:40]:
    for ap in (e, (e+1)&~1, (e+2)&~1):
        pass
    # check token_index right after run end (2-byte aligned)
    ti = (e + 1) & ~1
    if ti + 512 <= N:
        a = struct.unpack_from('<256H', d, ti)
        inc = all(a[i+1] > a[i] for i in range(255))
        if inc and a[0] <= 0x100:
            print('  run 0x%x-0x%x (len %d)  -> token_index at 0x%x last=%d ts=0x%x' % (s, e, ln, ti, a[255], ti - a[255] - 1))
print('--- top 40 longest runs ---')
for (s, e, ln) in sorted(runs, key=lambda x: -(x[1]-x[0]))[:40]:
    print('  0x%x - 0x%x  len %d' % (s, e, ln))
