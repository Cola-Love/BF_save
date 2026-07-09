import struct
import sys
from collections import OrderedDict

from core.stream import Stream
from core.constants import *


class Ref:
    __slots__ = ('id',)
    def __init__(self, rid): self.id = rid
    def __repr__(self): return f'<Ref:{self.id}>'
    def __eq__(self, o): return isinstance(o, Ref) and self.id == o.id
    def __hash__(self): return hash(self.id)


class FullParser:
    def __init__(self, data):
        self.s = Stream(data)
        self.classes = {}
        self.objects = {}
        self.strings = {}
        self.libs = []
        self.root = None
        self.root_id = None
        self._record_offsets = {}
        self._raw = bytes(data)

    def parse(self):
        self._header()
        self._records()
        return self._resolve_refs(self.root)

    def _header(self):
        self.s.rb(); self.s.ri(); self.s.ri(); self.s.ri(); self.s.ri()

    def _records(self):
        while self.s.p < len(self._raw):
            rec_off = self.s.p
            rt = self.s.rb()
            if rt == RT_LIB: self._lib()
            elif rt == RT_CWMAT: self._cwmat(is_root=(self.root is None), rec_off=rec_off)
            elif rt == RT_SCWMAT: self._scwmat(rec_off=rec_off)
            elif rt == RT_CWI: self._cwi(rec_off=rec_off)
            elif rt == RT_BOS: self._bos(rec_off=rec_off)
            elif rt == RT_BAR: self._bar(rec_off=rec_off)
            elif rt == RT_ASP: self._asp(rec_off=rec_off)
            elif rt == RT_ASO: self._aso(rec_off=rec_off)
            elif rt == RT_ASS: self._ass(rec_off=rec_off)
            elif rt == RT_MPT: self._mpt()
            elif rt == RT_MREF: self.s.ri()
            elif rt == RT_NULL: pass
            elif rt == RT_NM: self.s.ri()
            elif rt == RT_N256: self.s.rb()
            elif rt == RT_END: break
            else:
                sys.stderr.write(f"WARN: Unknown rt=0x{rt:02x} at {self.s.p-1}\n")
                break

    def _lib(self):
        self.s.ri(); self.libs.append(self.s.rs())

    def _read_class_def(self):
        cid = self.s.ri()
        name = self.s.rs()
        mc = self.s.ri()
        names = [self.s.rs() for _ in range(mc)]
        btypes = [self.s.rb() for _ in range(mc)]
        infos = []
        for bt in btypes:
            info = {'bt': bt}
            if bt == BT_PRI: info['pt'] = self.s.rb()
            elif bt == BT_SYS: info['sn'] = self.s.rs()
            elif bt == BT_CLS: info['cn'] = self.s.rs(); info['li'] = self.s.ri()
            elif bt == BT_PA: info['pt'] = self.s.rb()
            infos.append(info)
        lid = self.s.ri()
        self.classes[cid] = {'name': name, 'names': names, 'infos': infos}
        return cid, name, names, infos

    def _read_member_values(self, names, infos, depth=0):
        if depth > 50:
            return {'_error': 'MaxDepth'}
        vals = OrderedDict()
        for name, info in zip(names, infos):
            if info['bt'] == BT_PRI:
                vals[name] = self.s.rp(info['pt'])
            else:
                vals[name] = self._read_ref_value(depth + 1)
        return vals

    def _read_ref_value(self, depth=0):
        rec_off = self.s.p - 1
        rt = self.s.rb()
        if rt == RT_MREF:
            return Ref(self.s.ri())
        elif rt == RT_NULL:
            return None
        elif rt == RT_CWMAT:
            cid, name, names, infos = self._read_class_def()
            self._record_offsets[cid] = rec_off
            vals = self._read_member_values(names, infos, depth)
            vals['_type'] = name
            self.objects[cid] = vals
            return vals
        elif rt == RT_BOS:
            oid = self.s.ri(); s = self.s.rs()
            self._record_offsets[oid] = rec_off
            self.strings[oid] = s; self.objects[oid] = s
            return s
        elif rt == RT_BAR:
            oid = self.s.ri(); ba_type = self.s.rb(); rank = self.s.ri()
            self._record_offsets[oid] = rec_off
            lengths = [self.s.ri() for _ in range(rank)]
            total = 1
            for l in lengths: total *= l
            if ba_type in (0, 2, 3, 5):
                bt = self.s.rb()
                self._skip_additional_info(bt)
            if ba_type in (0, 3):
                refs = [self._read_ref_value(depth + 1) for _ in range(total)]
            else:
                refs = [self.s.ri() for _ in range(total)]
            self.objects[oid] = refs
            return refs
        elif rt == RT_SCWMAT:
            oid = self.s.ri()
            self._record_offsets[oid] = rec_off
            class_name = self.s.rs()
            mc = self.s.ri()
            names = [self.s.rs() for _ in range(mc)]
            btypes = [self.s.rb() for _ in range(mc)]
            infos = [self._read_additional_info(bt) for bt in btypes]
            self.classes[oid] = {'name': class_name, 'names': names, 'infos': infos}
            vals = OrderedDict()
            for i, name in enumerate(names):
                info = infos[i]
                if info['bt'] == BT_PRI:
                    vals[name] = self.s.rp(info.get('pt', 8))
                else:
                    vals[name] = self._read_ref_value(depth + 1)
            vals['_type'] = class_name
            self.objects[oid] = vals
            return vals
        elif rt == RT_ASP:
            oid = self.s.ri(); alen = self.s.ri(); apt = self.s.rb()
            self._record_offsets[oid] = rec_off
            arr = [self.s.rp(apt) for _ in range(alen)]
            self.objects[oid] = arr
            return arr
        elif rt == RT_ASO:
            oid = self.s.ri(); alen = self.s.ri()
            self._record_offsets[oid] = rec_off
            refs = [self.s.ri() for _ in range(alen)]
            self.objects[oid] = refs
            return refs
        elif rt == RT_ASS:
            oid = self.s.ri(); alen = self.s.ri()
            self._record_offsets[oid] = rec_off
            arr = [self.s.rs() for _ in range(alen)]
            self.objects[oid] = arr
            return arr
        elif rt == RT_CWI:
            oid = self.s.ri(); mid = self.s.ri()
            self._record_offsets[oid] = rec_off
            cd = self.classes.get(mid)
            if cd:
                vals = self._read_member_values(cd['names'], cd['infos'], depth)
                vals['_type'] = cd['name']
                self.objects[oid] = vals
                return vals
            return f'<UnknownCWI:{oid}>'
        elif rt == RT_MPT:
            return self.s.rp(self.s.rb())
        else:
            return f'<UnknownRT:0x{rt:02x}>'

    def _cwmat(self, is_root=False, rec_off=None):
        cid, name, names, infos = self._read_class_def()
        if rec_off is not None:
            self._record_offsets[cid] = rec_off
        vals = self._read_member_values(names, infos)
        vals['_type'] = name
        self.objects[cid] = vals
        if is_root:
            self.root = vals
            self.root_id = cid

    def _cwi(self, rec_off=None):
        oid = self.s.ri(); mid = self.s.ri()
        if rec_off is not None:
            self._record_offsets[oid] = rec_off
        cd = self.classes.get(mid)
        if cd:
            vals = self._read_member_values(cd['names'], cd['infos'])
            vals['_type'] = cd['name']
            self.objects[oid] = vals

    def _bos(self, rec_off=None):
        oid = self.s.ri(); s = self.s.rs()
        if rec_off is not None:
            self._record_offsets[oid] = rec_off
        self.strings[oid] = s; self.objects[oid] = s

    def _bar(self, rec_off=None):
        oid = self.s.ri()
        if rec_off is not None:
            self._record_offsets[oid] = rec_off
        ba_type = self.s.rb()
        rank = self.s.ri()
        lengths = [self.s.ri() for _ in range(rank)]
        total = 1
        for l in lengths: total *= l
        if ba_type in (0, 2, 3, 5):
            bt = self.s.rb()
            self._skip_additional_info(bt)
        if ba_type in (0, 3):
            refs = []
            while len(refs) < total:
                rt = self.s.rb()
                if rt == RT_N256:
                    refs.extend([None] * self.s.rb())
                elif rt == RT_NM:
                    self.s.ri()
                    refs.append(None)
                elif rt == RT_NULL:
                    refs.append(None)
                elif rt == RT_MREF:
                    refs.append(Ref(self.s.ri()))
                else:
                    self.s.p -= 1
                    refs.append(self._read_ref_value())
            self.objects[oid] = refs
        else:
            self.objects[oid] = [self.s.ri() for _ in range(total)]

    def _read_additional_info(self, bt):
        info = {'bt': bt}
        if bt == BT_PRI: info['pt'] = self.s.rb()
        elif bt == BT_SYS: info['sn'] = self.s.rs()
        elif bt == BT_CLS: info['cn'] = self.s.rs(); info['li'] = self.s.ri()
        elif bt == BT_PA: info['pt'] = self.s.rb()
        return info

    def _skip_additional_info(self, bt):
        self._read_additional_info(bt)

    def _scwmat(self, rec_off=None):
        cid = self.s.ri()
        if rec_off is not None:
            self._record_offsets[cid] = rec_off
        class_name = self.s.rs()
        mc = self.s.ri()
        names = [self.s.rs() for _ in range(mc)]
        btypes = [self.s.rb() for _ in range(mc)]
        infos = [self._read_additional_info(bt) for bt in btypes]
        self.classes[cid] = {'name': class_name, 'names': names, 'infos': infos}
        vals = OrderedDict()
        for i, name in enumerate(names):
            info = infos[i]
            if info['bt'] == BT_PRI:
                vals[name] = self.s.rp(info.get('pt', 8))
            else:
                vals[name] = self._read_ref_value()
        vals['_type'] = class_name
        self.objects[cid] = vals

    def _asp(self, rec_off=None):
        oid = self.s.ri(); alen = self.s.ri(); apt = self.s.rb()
        if rec_off is not None:
            self._record_offsets[oid] = rec_off
        self.objects[oid] = [self.s.rp(apt) for _ in range(alen)]

    def _aso(self, rec_off=None):
        oid = self.s.ri(); alen = self.s.ri()
        if rec_off is not None:
            self._record_offsets[oid] = rec_off
        self.objects[oid] = [self.s.ri() for _ in range(alen)]

    def _ass(self, rec_off=None):
        oid = self.s.ri(); alen = self.s.ri()
        if rec_off is not None:
            self._record_offsets[oid] = rec_off
        self.objects[oid] = [self.s.rs() for _ in range(alen)]

    def _mpt(self):
        self.s.rb(); self.s.rp(0)

    def _resolve_refs(self, obj, depth=0, max_depth=30, path=None):
        if path is None:
            path = set()
        if depth > max_depth:
            return '<MaxDepth>'
        if obj is None or isinstance(obj, bool):
            return obj
        if isinstance(obj, Ref):
            rid = obj.id
            if rid in path:
                return f'<Cycle:{rid}>'
            path.add(rid)
            if rid in self.objects:
                result = self._resolve_refs(self.objects[rid], depth + 1, max_depth, path)
                path.discard(rid)
                return result
            if rid in self.strings:
                return self.strings[rid]
            return f'<Unresolved:{rid}>'
        if isinstance(obj, (int, float)):
            return obj
        if isinstance(obj, str):
            return obj
        if isinstance(obj, list):
            return [self._resolve_refs(x, depth + 1, max_depth, path) for x in obj]
        if isinstance(obj, (dict, OrderedDict)):
            result = OrderedDict()
            for k, v in obj.items():
                result[k] = self._resolve_refs(v, depth + 1, max_depth, path)
            return result
        return obj

    def find_field_offset(self, path_str):
        segments = [s.strip() for s in path_str.split('>')]
        if not segments:
            return None

        root_id = self.root_id
        offset = self._record_offsets.get(root_id)
        if offset is None:
            return None

        for i, seg in enumerate(segments):
            is_last = (i == len(segments) - 1)
            result = self._walk_binary_step(offset, seg, is_last)
            if result is None:
                return None
            if is_last:
                return result
            offset = result

        return None

    def _walk_binary_step(self, offset, seg, is_last):
        s = Stream(self._raw)
        s.p = offset
        rt = s.rb()

        if rt in (RT_CWMAT, RT_SCWMAT, RT_CWI):
            return self._walk_member_step(s, rt, seg, is_last)
        elif rt == RT_BAR:
            return self._walk_bar_step(s, seg, is_last)
        elif rt == RT_ASP:
            return self._walk_asp_step(s, seg, is_last)
        elif rt == RT_ASO:
            return self._walk_aso_step(s, seg, is_last)
        elif rt == RT_ASS:
            return self._walk_ass_step(s, seg, is_last)
        return None

    def _walk_member_step(self, s, rt, seg, is_last):
        names, infos, btypes = self._parse_record_values(s, rt)
        if names is None:
            return None

        if seg.isdigit() and names == ['_items', '_size', '_version']:
            if btypes[0] == BT_PRI:
                return None
            rt2 = s.rb()
            if rt2 == RT_MREF:
                ref_id = s.ri()
                bar_off = self._record_offsets.get(ref_id)
                if bar_off is not None:
                    return self._walk_binary_step(bar_off, seg, is_last)
            return None

        for i, name in enumerate(names):
            if name == seg:
                if btypes[i] == BT_PRI:
                    if is_last:
                        return (s.p, infos[i].get('pt', 8), name)
                    return None
                else:
                    rt2 = s.rb()
                    if rt2 == RT_MREF:
                        ref_id = s.ri()
                        return self._record_offsets.get(ref_id)
                    elif rt2 in (RT_CWMAT, RT_SCWMAT, RT_CWI, RT_BAR, RT_ASP, RT_ASO, RT_ASS):
                        s.p -= 1
                        if is_last:
                            return self._find_value_in_inline(s, rt2)
                        return s.p
                    elif rt2 == RT_BOS:
                        s.ri(); s.rs()
                        return None
                    elif rt2 == RT_NULL:
                        return None
                    return None
            else:
                if btypes[i] == BT_PRI:
                    s.p += PT_SIZE.get(infos[i].get('pt', 8), 4)
                else:
                    self._skip_one_ref(s)
        return None

    def _walk_bar_step(self, s, seg, is_last):
        idx = int(seg)
        s.ri()
        ba_type = s.rb()
        rank = s.ri()
        lengths = [s.ri() for _ in range(rank)]
        total = 1
        for l in lengths: total *= l
        if ba_type in (0, 2, 3, 5):
            bt = s.rb()
            self._skip_additional_info_stream(s, bt)
        if ba_type in (0, 3):
            for j in range(idx):
                self._skip_one_ref(s)
            rt_elem = s.rb()
            if is_last:
                if rt_elem in (RT_CWMAT, RT_SCWMAT):
                    s.p -= 1
                    return self._find_value_in_inline(s, rt_elem)
                return None
            if rt_elem == RT_MREF:
                return self._record_offsets.get(s.ri())
            elif rt_elem in (RT_CWMAT, RT_SCWMAT, RT_CWI):
                return s.p - 1
            elif rt_elem == RT_NULL:
                return None
            return None
        else:
            s.p += idx * 4
            return self._record_offsets.get(s.ri())

    def _walk_asp_step(self, s, seg, is_last):
        idx = int(seg)
        s.ri(); alen = s.ri(); apt = s.rb()
        if is_last:
            return (s.p + idx * PT_SIZE.get(apt, 4), apt, seg)
        return None

    def _walk_aso_step(self, s, seg, is_last):
        idx = int(seg)
        s.ri(); alen = s.ri()
        s.p += idx * 4
        ref_id = s.ri()
        if is_last:
            return None
        return self._record_offsets.get(ref_id)

    def _walk_ass_step(self, s, seg, is_last):
        idx = int(seg)
        s.ri(); alen = s.ri()
        for _ in range(idx):
            s.rs()
        return None

    def _find_value_in_inline(self, s, rt):
        s.rb()
        names, infos, btypes = self._parse_record_values(s, rt)
        if names is None:
            return None
        for i, name in enumerate(names):
            if name == 'value__' and btypes[i] == BT_PRI:
                return (s.p, infos[i].get('pt', 8), 'value__')
            if btypes[i] == BT_PRI:
                s.p += PT_SIZE.get(infos[i].get('pt', 8), 4)
            else:
                self._skip_one_ref(s)
        return None

    def _parse_record_values(self, s, rt):
        if rt == RT_CWMAT:
            s.ri(); s.rs(); mc = s.ri()
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
            s.ri()
            return names, infos, btypes
        elif rt == RT_SCWMAT:
            s.ri(); s.rs(); mc = s.ri()
            names = [s.rs() for _ in range(mc)]
            btypes = [s.rb() for _ in range(mc)]
            infos = [self._read_additional_info_stream(s, bt) for bt in btypes]
            return names, infos, btypes
        elif rt == RT_CWI:
            s.ri(); mid = s.ri()
            cd = self.classes.get(mid)
            if cd is None:
                return None, None, None
            return cd['names'], cd['infos'], [info['bt'] for info in cd['infos']]
        return None, None, None

    def _read_additional_info_stream(self, s, bt):
        info = {'bt': bt}
        if bt == BT_PRI: info['pt'] = s.rb()
        elif bt == BT_SYS: info['sn'] = s.rs()
        elif bt == BT_CLS: info['cn'] = s.rs(); info['li'] = s.ri()
        elif bt == BT_PA: info['pt'] = s.rb()
        return info

    def _skip_additional_info_stream(self, s, bt):
        self._read_additional_info_stream(s, bt)

    def _skip_one_ref(self, s, depth=0):
        if depth > 50: return
        rt = s.rb()
        if rt == RT_MREF: s.ri()
        elif rt == RT_NULL: pass
        elif rt == RT_CWMAT:
            s.ri(); s.rs(); mc = s.ri()
            for _ in range(mc): s.rs()
            btypes = [s.rb() for _ in range(mc)]
            pts = []
            for bt in btypes:
                if bt == BT_PRI: pts.append(s.rb())
                elif bt == BT_PA: pts.append(s.rb())
                elif bt == BT_SYS: s.rs(); pts.append(None)
                elif bt == BT_CLS: s.rs(); s.ri(); pts.append(None)
                else: pts.append(None)
            s.ri()
            for i in range(mc):
                if btypes[i] in (BT_PRI, BT_PA):
                    s.p += PT_SIZE.get(pts[i], 4)
                else:
                    self._skip_one_ref(s, depth + 1)
        elif rt == RT_SCWMAT:
            s.ri(); s.rs(); mc = s.ri()
            for _ in range(mc): s.rs()
            btypes = [s.rb() for _ in range(mc)]
            pts = []
            for bt in btypes:
                if bt == BT_PRI: pts.append(s.rb())
                elif bt == BT_PA: pts.append(s.rb())
                elif bt == BT_SYS: s.rs(); pts.append(None)
                elif bt == BT_CLS: s.rs(); s.ri(); pts.append(None)
                else: pts.append(None)
            for i in range(mc):
                if btypes[i] in (BT_PRI, BT_PA):
                    s.p += PT_SIZE.get(pts[i], 4)
                else:
                    self._skip_one_ref(s, depth + 1)
        elif rt == RT_BOS: s.ri(); s.rs()
        elif rt == RT_ASP: s.ri(); alen = s.ri(); apt = s.rb(); s.p += alen * PT_SIZE.get(apt, 4)
        elif rt == RT_ASO: s.ri(); alen = s.ri(); s.p += alen * 4
        elif rt == RT_ASS: s.ri(); alen = s.ri(); [s.rs() for _ in range(alen)]
        elif rt == RT_CWI:
            s.ri(); mid = s.ri()
            cd = self.classes.get(mid)
            if cd:
                for i, bt in enumerate([info['bt'] for info in cd['infos']]):
                    if bt == BT_PRI:
                        s.p += PT_SIZE.get(cd['infos'][i].get('pt', 8), 4)
                    elif bt == BT_PA:
                        s.p += PT_SIZE.get(cd['infos'][i].get('pt', 8), 4)
                    else:
                        self._skip_one_ref(s, depth + 1)
        elif rt == RT_MPT: s.rb(); s.p += 4
        elif rt == RT_BAR:
            s.ri(); ba_type = s.rb(); rank = s.ri()
            lengths = [s.ri() for _ in range(rank)]
            total = 1
            for l in lengths: total *= l
            if ba_type in (0, 2, 3, 5):
                bt = s.rb()
                self._skip_additional_info_stream(s, bt)
            if ba_type in (0, 3):
                for _ in range(total):
                    self._skip_one_ref(s, depth + 1)
            else:
                s.p += total * 4
        elif rt == RT_N256: s.rb()
        elif rt == RT_NM: s.ri()
