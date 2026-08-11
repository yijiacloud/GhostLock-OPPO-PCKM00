import struct
d = open(r'D:\opporoot\boot\kernel','rb').read()
N = len(d)

TOKEN_INDEX = 0x1a76900
a = struct.unpack_from('<256H', d, TOKEN_INDEX)
token_table = TOKEN_INDEX - a[255] - 1
print('token_table=0x%x  token_index=0x%x  a255=%d' % (token_table, TOKEN_INDEX, a[255]))

# build token dictionary
tokens = []
for i in range(256):
    s = token_table + a[i]
    e = TOKEN_INDEX - 1 if i == 255 else token_table + a[i+1]
    tokens.append(d[s:e])
tokmap = {i: tokens[i] for i in range(256)}

def expand_name(data, pos):
    """decode symbol name from kallsyms_names at 'pos'; returns (name, nextpos)"""
    ln = data[pos]
    pos += 1
    out = bytearray()
    for k in range(ln):
        t = data[pos]
        pos += 1
        out += tokmap[t]
    return bytes(out), pos

# markers: examine the u64 array candidate at 0x1a76000
M = 0x1a76000
vals = []
i = 0
while M + i*8 < token_table and i < 2000:
    v = struct.unpack_from('<Q', d, M + i*8)[0]
    if (v >> 32) != 0:
        break
    vals.append(v & 0xffffffff)
    i += 1
print('u64 array len:', len(vals), 'first:', vals[:5], 'last:', vals[-5:])
print('increasing:', all(vals[j+1] > vals[j] for j in range(len(vals)-1)))

# names_end = markers start = M (4-aligned). names_total_len = vals[-1]
nt = vals[-1]
names_start = M - nt
print('names_start = 0x%x (len %d)' % (names_start, nt))
print('num_syms candidate before names_start:', struct.unpack_from('<I', d, names_start-4)[0])

# verify names: parse num_syms symbols, check offsets at multiples of 256 match vals
nsyms = struct.unpack_from('<I', d, names_start-4)[0]
p = names_start
ok = True
marks = []
for s in range(nsyms):
    if p >= M:
        ok = False; print('overflow at symbol', s); break
    ln = d[p]
    if ln >= 0x80:
        ok = False; print('bad len', ln, 'at', hex(p)); break
    p += 1 + ln
    if (s+1) % 256 == 0:
        marks.append(p - names_start)
print('parsed %d symbols, names_end=0x%x, markers_match=%s' % (nsyms, p, (marks == list(vals))))
if marks != list(vals):
    print('  marks[:5]=%s' % marks[:5])
    print('  vals[:5]=%s' % list(vals[:5]))
    print('  len mismatch: marks=%d vals=%d' % (len(marks), len(vals)))
