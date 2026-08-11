import struct
d = open(r'D:\opporoot\boot\kernel','rb').read()
N = len(d)

# Loose scan: count windows of 256 u16 that are non-decreasing, last in sane range
stats = {}
samples = []
for p in range(0, N - 512, 1):
    a = struct.unpack_from('<256H', d, p)
    if a[0] > 0x100:
        continue
    inc = all(a[i+1] >= a[i] for i in range(255))
    if not inc:
        continue
    if not (200 <= a[255] <= 0x8000):
        continue
    key = 'a0<=0x10' if a[0] <= 0x10 else 'a0>0x10'
    stats[key] = stats.get(key, 0) + 1
    if len(samples) < 15:
        samples.append((p, a[0], a[255]))

print('non-decreasing u16[256] candidates with a[255] in range:', sum(stats.values()))
print(stats)
for s in samples:
    print('  0x%x a0=0x%x last=0x%x ts=0x%x' % (s[0], s[1], s[2], s[0]-s[2]-1))
