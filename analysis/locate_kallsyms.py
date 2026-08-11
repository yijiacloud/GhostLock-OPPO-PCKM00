import struct, sys

IMG = r'D:\opporoot\boot\kernel'
d = open(IMG, 'rb').read()
N = len(d)
print('Image size: 0x%x (%d)' % (N, N))

def is_printable_token(seg):
    for b in seg:
        if b == 0:
            return False
        if not (0x20 <= b <= 0x7e):
            return False
    return True

# ---- Step 1: locate kallsyms_token_index (256 u16, increasing, at 2-byte aligned) ----
candidates = []
for p in range(0, N - 512, 2):
    a = struct.unpack_from('<256H', d, p)
    if a[0] > 0x10:
        continue
    inc = all(a[i+1] > a[i] for i in range(255))
    if not inc:
        continue
    if not (250 <= a[255] < 0x4000):
        continue
    # token table start = p - (a[255] + 1)
    ts = p - a[255] - 1
    if ts < 0:
        continue
    # validate 256 tokens are printable or empty
    ok = True
    for i in range(256):
        s = ts + a[i]
        e = p if i == 255 else ts + a[i+1]
        tok = d[s:e]
        if tok and not is_printable_token(tok):
            ok = False
            break
        # ensure no stray NUL inside token
        if b'\x00' in tok:
            ok = False
            break
    if ok:
        candidates.append((p, a[255]))

print('token_index candidates:', len(candidates))
for p, last in candidates[:10]:
    print('  0x%x last=%d token_table_start=0x%x' % (p, last, p - last - 1))
