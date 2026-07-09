import struct
import shutil
from datetime import datetime

from core.stream import Stream
from core.constants import PT_BOOL, PT_I32, PT_U32, PT_FLT, PT_DBL, PT_I64, PT_U64, PT_I16, PT_U16, PT_BYTE, PT_SB, PT_SIZE, INT_TYPES, FLT_TYPES, BT_PRI, BT_SYS, BT_CLS, BT_PA, RT_MREF, RT_NULL, RT_CWMAT, RT_SCWMAT, RT_BOS, RT_ASP, RT_ASO, RT_ASS, RT_CWI, RT_MPT, RT_N256, RT_NM, RT_BAR
from core.parser import FullParser


def _to_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.lower() in ('true', '1', 'yes')
    return bool(int(v))


class Setter:
    def __init__(self, path):
        self.path = path
        with open(path, 'rb') as f:
            self.raw = bytearray(f.read())
        self._positions = {}

    def scan(self):
        s = Stream(self.raw)
        s.p += 17
        s.p += 1 + 4; s.rs()
        s.p += 1 + 4; s.rs()
        mc = s.ri()
        names = [s.rs() for _ in range(mc)]
        btypes = [s.rb() for _ in range(mc)]
        infos = []
        for bt in btypes:
            info = {'bt': bt}
            if bt == BT_PRI: info['pt'] = s.rb()
            elif bt == BT_SYS: info['sn'] = s.rs()
            elif bt == BT_CLS: info['cn'] = s.rs(); info['li'] = s.ri()
            elif bt == BT_PA: info['pt'] = s.rb()
            infos.append(info)
        s.p += 4

        for i, name in enumerate(names):
            info = infos[i]
            if info['bt'] == BT_PRI:
                self._positions[name] = (s.p, info['pt'])
                s.rp(info['pt'])
            else:
                self._skip_ref(s)
        return self._positions

    def _skip_ref(self, s, depth=0):
        if depth > 50: return
        rt = s.rb()
        if rt == RT_MREF: s.ri()
        elif rt == RT_NULL: pass
        elif rt == RT_CWMAT:
            s.ri(); s.rs(); mc = s.ri()
            for _ in range(mc): s.rs()
            btypes = [s.rb() for _ in range(mc)]
            for bt in btypes:
                if bt == BT_PRI: s.rb()
                elif bt == BT_SYS: s.rs()
                elif bt == BT_CLS: s.rs(); s.ri()
                elif bt == BT_PA: s.rb()
            s.p += 4
            for i in range(mc):
                if btypes[i] == BT_PRI: s.p += 4
                else: self._skip_ref(s, depth + 1)
        elif rt == RT_BOS: s.ri(); s.rs()
        elif rt == RT_ASP: s.ri(); alen = s.ri(); apt = s.rb(); s.p += alen * PT_SIZE.get(apt, 4)
        elif rt == RT_ASO: s.ri(); alen = s.ri(); s.p += alen * 4
        elif rt == RT_ASS: s.ri(); alen = s.ri(); [s.rs() for _ in range(alen)]
        elif rt == RT_CWI: s.ri(); s.ri()
        elif rt == RT_MPT: s.rb(); s.p += 4

    def modify(self, field, value):
        if field not in self._positions:
            print(f"警告: '{field}' 不存在或不是简单类型")
            return False
        pos, pt = self._positions[field]
        if pt in INT_TYPES:
            value = int(value)
        elif pt in FLT_TYPES:
            value = float(value)
        elif pt == PT_BOOL:
            value = _to_bool(value)
        ts = Stream(b'')
        ts.wp(pt, value)
        nb = bytes(ts.d)
        if len(nb) == PT_SIZE.get(pt, len(nb)):
            self.raw[pos:pos + len(nb)] = nb
        print(f"修改: {field} -> {value}")
        return True

    def set_path(self, path_str, value):
        parser = FullParser(self.raw)
        parser.parse()
        result = parser.find_field_offset(path_str)
        if result is None:
            print(f"路径不存在或不是简单类型: {path_str}")
            return False
        pos, pt, name = result
        if pt in INT_TYPES:
            value = int(value)
        elif pt in FLT_TYPES:
            value = float(value)
        elif pt == PT_BOOL:
            value = _to_bool(value)
        old_val = struct.unpack_from({PT_I32: '<i', PT_U32: '<I', PT_FLT: '<f', PT_DBL: '<d',
                                       PT_I64: '<q', PT_U64: '<Q', PT_I16: '<h', PT_U16: '<H',
                                       PT_BYTE: '<b', PT_SB: '<b', PT_BOOL: '<b'}.get(pt, '<i'),
                                      self.raw, pos)[0]
        ts = Stream(b'')
        ts.wp(pt, value)
        nb = bytes(ts.d)
        if len(nb) == PT_SIZE.get(pt, len(nb)):
            self.raw[pos:pos + len(nb)] = nb
        print(f"修改: {path_str} = {old_val} -> {value}")
        return True

    def save(self, output=None):
        if output is None:
            output = self.path
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        bak = f"{output}.{ts}.bak"
        shutil.copy2(output, bak)
        print(f"已备份: {bak}")
        with open(output, 'wb') as f:
            f.write(self.raw)
        print(f"已保存: {output}")
