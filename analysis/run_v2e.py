import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')

from vmlinux_to_elf.core.kallsyms import KallsymsFinder

data = open(r'D:\opporoot\boot\kernel','rb').read()
print('data size:', len(data))

kf = KallsymsFinder(data)
print('symbols parsed:', len(kf.symbols))
print('kernel_text_candidate:', hex(kf.kernel_text_candidate) if kf.kernel_text_candidate else None)

with open(r'D:\opporoot\analysis\kallsyms_v2e.txt','w',encoding='utf-8') as f:
    for s in kf.symbols:
        f.write('0x%016x %s\n' % (s.virtual_address, s.name))

print('written kallsyms_v2e.txt')
