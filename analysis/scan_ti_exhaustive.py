import struct
d = open(r'D:\opporoot\boot\kernel','rb').read()

# scan aligned-4 positions in .rodata-ish region
lo, hi = 0x0f00000, 0x1e00000
results = []
for p in range(lo, hi - 512, 4):
    a = struct.unpack_from('<256H', d, p)
    if a[0] > 0x200:
        continue
    inc = True
    for i in range(255):
        if a[i+1] <= a[i]:
            inc = False
            break
    if not inc:
        continue
    # classify: arithmetic (counter) vs token-like
    diffs = [a[i+1]-a[i] for i in range(255)]
    dset = set(diffs)
    avg = sum(diffs)/len(diffs)
    results.append((p, a[255], a[0], avg, len(dset)))

print('total increasing u16[256] (aligned4) in region:', len(results))
for r in results:
    print('  idx=0x%x a255=%d a0=%d avgdiff=%.1f ndiff=%d' % r)
