import struct
from core.constants import PT_BOOL, PT_BYTE, PT_I32, PT_U32, PT_I64, PT_FLT, PT_DBL, PT_STR, PT_I16, PT_U16, PT_SIZE


class Stream:
    def __init__(self, data):
        self.d = memoryview(data)
        self.p = 0

    def rb(self): b = self.d[self.p]; self.p += 1; return b
    def ri(self): v = struct.unpack_from('<i', self.d, self.p)[0]; self.p += 4; return v
    def ru(self): v = struct.unpack_from('<I', self.d, self.p)[0]; self.p += 4; return v
    def rl(self): v = struct.unpack_from('<q', self.d, self.p)[0]; self.p += 8; return v
    def rf(self): v = struct.unpack_from('<f', self.d, self.p)[0]; self.p += 4; return v
    def rd(self): v = struct.unpack_from('<d', self.d, self.p)[0]; self.p += 8; return v
    def r7(self):
        r = 0; s = 0
        while True:
            b = self.rb(); r |= (b & 0x7F) << s; s += 7
            if (b & 0x80) == 0: break
        return r
    def rs(self):
        l = self.r7(); s = bytes(self.d[self.p:self.p+l]).decode('utf-8','replace')
        self.p += l; return s
    def rp(self, pt):
        if pt == PT_BOOL: return self.rb() != 0
        if pt == PT_BYTE: return self.rb()
        if pt == PT_I32: return self.ri()
        if pt == PT_U32: return self.ru()
        if pt == PT_I64: return self.rl()
        if pt == PT_FLT: return self.rf()
        if pt == PT_DBL: return self.rd()
        if pt == PT_STR: return self.rs()
        if pt == PT_I16: v = struct.unpack_from('<h', self.d, self.p)[0]; self.p += 2; return v
        if pt == PT_U16: v = struct.unpack_from('<H', self.d, self.p)[0]; self.p += 2; return v
        self.p += PT_SIZE.get(pt, 4); return None

    def wb(self, b): self.d = bytearray(self.d); self.d.append(b & 0xFF); self.p += 1; return self.d
    def wi(self, v): self.d = bytearray(self.d); self.d.extend(struct.pack('<i',v)); self.p += 4; return self.d
    def wf(self, v): self.d = bytearray(self.d); self.d.extend(struct.pack('<f',v)); self.p += 4; return self.d
    def wp(self, pt, v):
        if pt == PT_BOOL: return self.wb(1 if v else 0)
        if pt == PT_I32: return self.wi(v)
        if pt == PT_U32: return self.wi(v)
        if pt == PT_FLT: return self.wf(v)
        if pt == PT_DBL: self.d = bytearray(self.d); self.d.extend(struct.pack('<d',v)); self.p += 8; return self.d
        raise ValueError(f"Cannot write pt={pt}")
