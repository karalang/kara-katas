# Writes data/: the DICOM files the jobs read, files.txt (the files
# gen_kara.py embeds) and jobs.txt (one job a line, words split on spaces).
# The files are built byte by byte here rather than with pydicom, so the
# malformed ones can be exactly as broken as they need to be.
# Run as: python3 -s -P -B mk.py
import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, 'data')
files = []
jobs = []

LONG_VRS = {'OB', 'OD', 'OF', 'OL', 'OV', 'OW', 'SQ', 'SV', 'UC', 'UN', 'UR',
            'UT', 'UV'}
UNDEF = 0xFFFFFFFF


def put(name, data):
    os.makedirs(D, exist_ok=True)
    with open(os.path.join(D, name), 'wb') as f:
        f.write(data)
    files.append(name)


def job(*words):
    for w in words:
        assert ' ' not in w and '\n' not in w, w
    jobs.append(' '.join(words))


class Enc:
    """One transfer syntax's element layout."""

    def __init__(self, implicit=False, little=True):
        self.implicit = implicit
        self.e = '<' if little else '>'

    def tag(self, tag):
        return struct.pack(self.e + 'HH', tag >> 16, tag & 0xFFFF)

    def elem(self, tag, vr, value, length=None):
        n = len(value) if length is None else length
        if self.implicit:
            return self.tag(tag) + struct.pack(self.e + 'L', n) + value
        head = self.tag(tag) + vr.encode('ascii')
        if vr in LONG_VRS or n == UNDEF:
            return head + b'\0\0' + struct.pack(self.e + 'L', n) + value
        return head + struct.pack(self.e + 'H', n) + value

    def us(self, tag, *vals):
        return self.elem(tag, 'US', struct.pack(self.e + '%dH' % len(vals), *vals))

    def ss(self, tag, *vals):
        return self.elem(tag, 'SS', struct.pack(self.e + '%dh' % len(vals), *vals))

    def ul(self, tag, *vals):
        return self.elem(tag, 'UL', struct.pack(self.e + '%dL' % len(vals), *vals))

    def sl(self, tag, *vals):
        return self.elem(tag, 'SL', struct.pack(self.e + '%dl' % len(vals), *vals))

    def fl(self, tag, *vals):
        return self.elem(tag, 'FL', struct.pack(self.e + '%df' % len(vals), *vals))

    def fd(self, tag, *vals):
        return self.elem(tag, 'FD', struct.pack(self.e + '%dd' % len(vals), *vals))

    def at(self, tag, *tags):
        return self.elem(tag, 'AT', b''.join(self.tag(t) for t in tags))

    def s(self, tag, vr, text, pad=b' ', enc='latin-1'):
        b = text.encode(enc) if isinstance(text, str) else text
        if len(b) % 2:
            b += pad
        return self.elem(tag, vr, b)

    def ui(self, tag, uid):
        return self.s(tag, 'UI', uid, pad=b'\0')

    def item(self, body, undefined=False):
        if undefined:
            return (self.tag(0xFFFEE000) + struct.pack(self.e + 'L', UNDEF) + body
                    + self.tag(0xFFFEE00D) + b'\0\0\0\0')
        return self.tag(0xFFFEE000) + struct.pack(self.e + 'L', len(body)) + body

    def sq(self, tag, items, undefined=False):
        body = b''.join(items)
        if undefined:
            return (self.elem(tag, 'SQ', body, UNDEF) + self.tag(0xFFFEE0DD)
                    + b'\0\0\0\0')
        return self.elem(tag, 'SQ', body)


LE = Enc()
IMP = Enc(implicit=True)
BE = Enc(little=False)

TS = {
    'implicit': '1.2.840.10008.1.2',
    'explicit': '1.2.840.10008.1.2.1',
    'deflated': '1.2.840.10008.1.2.1.99',
    'big': '1.2.840.10008.1.2.2',
    'jpeg': '1.2.840.10008.1.2.4.50',
}
CT = '1.2.840.10008.5.1.4.1.1.2'
MR = '1.2.840.10008.5.1.4.1.1.4'
US_IMG = '1.2.840.10008.5.1.4.1.1.6.1'
SR = '1.2.840.10008.5.1.4.1.1.88.11'
SC = '1.2.840.10008.5.1.4.1.1.7'
ROOT = '1.2.826.0.1.3680043.10.1138.'


def meta(sop_class, sop_inst, ts, group_length=True, extra=b''):
    body = (LE.elem(0x00020001, 'OB', b'\x00\x01')
            + LE.ui(0x00020002, sop_class)
            + LE.ui(0x00020003, sop_inst)
            + (LE.ui(0x00020010, ts) if ts else b'')
            + LE.ui(0x00020012, ROOT + '0.1')
            + LE.s(0x00020013, 'SH', 'KARA_DCM_1')
            + extra)
    if group_length:
        body = LE.ul(0x00020000, len(body)) + body
    return body


def dicom(meta_bytes, dataset, preamble=True):
    out = b''
    if preamble:
        out += b'\0' * 128 + b'DICM'
    return out + meta_bytes + dataset


def pixels(w, h, seed, bits=16):
    vals = [(seed * 37 + i * 11 + (i // w) * 5) % (4096 if bits == 16 else 256)
            for i in range(w * h)]
    if bits == 16:
        return vals
    return bytes(vals)


def patient(e, name, pid, birth='19700101', sex='O', enc='latin-1'):
    return (e.s(0x00100010, 'PN', name, enc=enc) + e.s(0x00100020, 'LO', pid)
            + e.s(0x00100030, 'DA', birth) + e.s(0x00100040, 'CS', sex))


# --- 1. explicit little endian CT with most VRs --------------------------
def ct_explicit():
    e = LE
    inst = ROOT + '1.1.1'
    ref_item = e.item(e.ui(0x00081150, CT) + e.ui(0x00081155, ROOT + '1.1.0'))
    ref_item2 = e.item(e.ui(0x00081150, CT) + e.ui(0x00081155, ROOT + '1.1.2'))
    code_item = e.item(e.s(0x00080100, 'SH', 'T-A0100') + e.s(0x00080102, 'SH', 'SRT')
                       + e.s(0x00080104, 'LO', 'Brain'))
    px = pixels(4, 4, 3)
    ds = (e.s(0x00080005, 'CS', 'ISO_IR 100')
          + e.s(0x00080008, 'CS', 'ORIGINAL\\PRIMARY\\AXIAL')
          + e.s(0x00080016, 'UI', CT, pad=b'\0')
          + e.ui(0x00080018, inst)
          + e.s(0x00080020, 'DA', '20240311')
          + e.s(0x00080030, 'TM', '101500.25')
          + e.s(0x00080050, 'SH', 'ACC0042')
          + e.s(0x00080060, 'CS', 'CT')
          + e.s(0x00080070, 'LO', 'Acme Imaging')
          + e.s(0x00080080, 'LO', "St. Mary's Clinic")
          + e.s(0x00080090, 'PN', 'House^Gregory^^Dr.')
          + e.sq(0x00081140, [ref_item, ref_item2])
          + e.sq(0x00082218, [code_item])
          + e.s(0x0008103E, 'LO', 'HEAD W/O CONTRAST')
          + e.s(0x00081030, 'LO', 'Head "routine"')
          + e.s(0x00090010, 'LO', 'GEMS_IDEN_01')
          + e.s(0x00091001, 'LO', 'full')
          + e.s(0x00091002, 'SH', 'CT01')
          + e.us(0x0009101A, 77)
          + patient(e, 'Doe^Jane^Q^^', 'PAT-0001', '19800214', 'F')
          + e.s(0x00101010, 'AS', '044Y')
          + e.s(0x00101020, 'DS', '1.65')
          + e.s(0x00101030, 'DS', '61.5')
          + e.s(0x00104000, 'LT', 'Patient was cooperative and still for the scan.')
          + e.s(0x00180050, 'DS', '2.50')
          + e.s(0x00180060, 'DS', '120')
          + e.s(0x00181020, 'LO', 'v1.2\\build7')
          + e.s(0x00181150, 'IS', ' 750 ')
          + e.s(0x00181151, 'IS', '200')
          + e.s(0x00181152, 'IS', '9')
          + e.s(0x00185100, 'CS', 'HFS')
          + e.ui(0x0020000D, ROOT + '1')
          + e.ui(0x0020000E, ROOT + '1.1')
          + e.s(0x00200010, 'SH', 'STUDY1')
          + e.s(0x00200011, 'IS', '1')
          + e.s(0x00200013, 'IS', '1')
          + e.s(0x00200032, 'DS', '-125.0\\-125.0\\45.5')
          + e.s(0x00200037, 'DS', '1\\0\\0\\0\\1\\0')
          + e.ui(0x00200052, ROOT + '1.9')
          + e.s(0x00201041, 'DS', '45.5')
          + e.s(0x00204000, 'LT', 'short note')
          + e.us(0x00280002, 1)
          + e.s(0x00280004, 'CS', 'MONOCHROME2')
          + e.us(0x00280010, 4)
          + e.us(0x00280011, 4)
          + e.s(0x00280030, 'DS', '0.488281\\0.488281')
          + e.us(0x00280100, 16)
          + e.us(0x00280101, 12)
          + e.us(0x00280102, 11)
          + e.us(0x00280103, 0)
          + e.us(0x00280106, 3)
          + e.us(0x00280107, 4000)
          + e.s(0x00281050, 'DS', '40\\400')
          + e.s(0x00281051, 'DS', '80\\2000')
          + e.s(0x00281052, 'DS', '-1024')
          + e.s(0x00281053, 'DS', '1')
          + e.s(0x00290010, 'LO', 'SIEMENS CSA HEADER')
          + e.s(0x00291008, 'CS', 'IMAGE NUM 4')
          + e.elem(0x00291010, 'OB', bytes(range(40)))
          + e.fl(0x00189306, 0.3)
          + e.fd(0x00189307, 1.0 / 3.0, 2.5)
          + e.at(0x00209165, 0x00200032, 0x00201041)
          + e.sl(0x00189330, -3)
          + e.ss(0x00189329, -12, 7)
          + e.ul(0x00189328, 3000000000)
          + e.elem(0x00189345, 'UN', struct.pack('<d', 12.5))
          + e.elem(0x7FE00010, 'OW', struct.pack('<16H', *px)))
    put('ct_explicit.dcm', dicom(meta(CT, inst, TS['explicit']), ds))


# --- 2. implicit little endian MR with nested undefined-length SQ --------
def mr_implicit():
    e = IMP
    inst = ROOT + '2.1.1'
    inner = e.item(e.s(0x00080100, 'SH', '113619') + e.s(0x00080102, 'SH', 'DCM')
                   + e.s(0x00080104, 'LO', 'Image Processing'), undefined=True)
    outer = e.item(e.s(0x00401001, 'SH', 'RP-11') + e.sq(0x00400260, [inner], undefined=True)
                   + e.s(0x00400253, 'SH', 'PPS-7'), undefined=True)
    outer2 = e.item(b'', undefined=True)
    ds = (e.s(0x00080008, 'CS', 'DERIVED\\SECONDARY')
          + e.ui(0x00080016, MR)
          + e.ui(0x00080018, inst)
          + e.s(0x00080020, 'DA', '20240312')
          + e.s(0x00080060, 'CS', 'MR')
          + e.s(0x00080080, 'LO', 'Northside Imaging')
          + e.s(0x00090010, 'LO', 'GEMS_IDEN_01')
          + e.s(0x00091004, 'SH', 'SIGNA')
          + e.s(0x00091017, 'LT', 'Sagittal T1 weighted series, motion corrected')
          + e.sl(0x00091027, 1234567)
          + e.s(0x00091030, 'SH', 'svc9')
          + e.s(0x00091099, 'LO', 'unknown element in a known block')
          + e.us(0x00111001, 5)
          + patient(e, 'Smith^John', 'PAT-0002', '19621103', 'M')
          + e.s(0x00180020, 'CS', 'SE')
          + e.s(0x00180080, 'DS', '500')
          + e.s(0x00180081, 'DS', '15.00')
          + e.s(0x00180087, 'DS', '1.5')
          + e.s(0x00181030, 'LO', 'T1_SAG')
          + e.ui(0x0020000D, ROOT + '2')
          + e.ui(0x0020000E, ROOT + '2.1')
          + e.s(0x00200011, 'IS', '3')
          + e.s(0x00200013, 'IS', '12')
          + e.sq(0x00400275, [outer, outer2], undefined=True)
          + e.us(0x00280002, 1)
          + e.s(0x00280004, 'CS', 'MONOCHROME2')
          + e.us(0x00280010, 2)
          + e.us(0x00280011, 4)
          + e.us(0x00280100, 16)
          + e.us(0x00280101, 16)
          + e.us(0x00280102, 15)
          + e.us(0x00280103, 1)
          + e.ss(0x00280106, -20)
          + e.ss(0x00280107, 900)
          + e.elem(0x7FE00010, 'OW', struct.pack('<8H', *pixels(4, 2, 9))))
    put('mr_implicit.dcm', dicom(meta(MR, inst, TS['implicit']), ds))


# --- 3. explicit big endian ultrasound -------------------------------------
def us_big():
    e = BE
    inst = ROOT + '3.1.1'
    region = e.item(e.us(0x00186012, 1) + e.us(0x00186014, 2) + e.ul(0x00186018, 0)
                    + e.ul(0x0018601A, 0) + e.fd(0x0018602C, 0.0125)
                    + e.fd(0x0018602E, 0.0125))
    ds = (e.s(0x00080005, 'CS', 'ISO_IR 192')
          + e.ui(0x00080016, US_IMG)
          + e.ui(0x00080018, inst)
          + e.s(0x00080020, 'DA', '20240313')
          + e.s(0x00080060, 'CS', 'US')
          + e.s(0x00080080, 'LO', 'Κέντρο Υγείας', enc='utf-8')
          + patient(e, 'Παπαδόπουλος^Νίκος=Παπαδόπουλος^Νίκος', 'PAT-0003', '19900505',
                    'M', enc='utf-8')
          + e.sq(0x00186011, [region])
          + e.ui(0x0020000D, ROOT + '3')
          + e.ui(0x0020000E, ROOT + '3.1')
          + e.s(0x00200011, 'IS', '1')
          + e.s(0x00200013, 'IS', '1')
          + e.us(0x00280002, 3)
          + e.s(0x00280004, 'CS', 'RGB')
          + e.us(0x00280006, 0)
          + e.us(0x00280010, 2)
          + e.us(0x00280011, 2)
          + e.us(0x00280100, 8)
          + e.us(0x00280101, 8)
          + e.us(0x00280102, 7)
          + e.us(0x00280103, 0)
          + e.elem(0x7FE00010, 'OB', bytes([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])))
    put('us_big.dcm', dicom(meta(US_IMG, inst, TS['big']), ds))


# --- 4. deflated explicit little endian SR ----------------------------------
def sr_deflated():
    e = LE
    inst = ROOT + '4.1.1'
    concept = e.item(e.s(0x00080100, 'SH', '121071') + e.s(0x00080102, 'SH', 'DCM')
                     + e.s(0x00080104, 'LO', 'Finding'))
    content = e.item(e.s(0x0040A010, 'CS', 'CONTAINS') + e.s(0x0040A040, 'CS', 'TEXT')
                     + e.sq(0x0040A043, [concept])
                     + e.s(0x0040A160, 'UT', 'No acute intracranial abnormality.'))
    ds = (e.ui(0x00080016, SR)
          + e.ui(0x00080018, inst)
          + e.s(0x00080020, 'DA', '20240311')
          + e.s(0x00080060, 'CS', 'SR')
          + patient(e, 'Doe^Jane^Q', 'PAT-0001', '19800214', 'F')
          + e.ui(0x0020000D, ROOT + '1')
          + e.ui(0x0020000E, ROOT + '1.5')
          + e.s(0x00200011, 'IS', '5')
          + e.s(0x00200013, 'IS', '1')
          + e.s(0x0040A040, 'CS', 'CONTAINER')
          + e.s(0x0040A050, 'CS', 'SEPARATE')
          + e.s(0x0040A491, 'CS', 'COMPLETE')
          + e.s(0x0040A493, 'CS', 'UNVERIFIED')
          + e.sq(0x0040A730, [content]))
    c = zlib.compressobj(9, zlib.DEFLATED, -15)
    z = c.compress(ds) + c.flush()
    if len(z) % 2:
        z += b'\0'
    put('sr_deflated.dcm', dicom(meta(SR, inst, TS['deflated']), z))


# --- 5. a series of small secondary-capture files for the index job ---------
def series():
    names = []
    plan = [
        ('7', '1', 'Brown^Alice', 'PAT-0007', '20240301', 'CHEST', 'OT', '2', 'Lateral', 3),
        ('7', '1', 'Brown^Alice', 'PAT-0007', '20240301', 'CHEST', 'OT', '1', 'Frontal', 1),
        ('7', '1', 'Brown^Alice', 'PAT-0007', '20240301', 'CHEST', 'OT', '1', 'Frontal', 2),
        ('7', '1', 'Brown^Alice', 'PAT-0007', '20240301', 'CHEST', 'OT', '2', 'Lateral', 1),
        ('5', '2', 'Green^Bob', 'PAT-0005', '20231225', 'KNEE', 'OT', '10', 'Knee AP', 1),
        ('7', '1', 'Brown^Alice', 'PAT-0007', '20240301', 'CHEST', 'OT', '1', 'Frontal', 10),
    ]
    for k, (study, _, name, pid, date, desc, mod, ser, sdesc, num) in enumerate(plan):
        e = IMP if k % 2 else LE
        inst = ROOT + '%s.%s.%d' % (study, ser, num)
        ds = (e.ui(0x00080016, SC) + e.ui(0x00080018, inst)
              + e.s(0x00080020, 'DA', date) + e.s(0x00080060, 'CS', mod)
              + e.s(0x00081030, 'LO', desc) + e.s(0x0008103E, 'LO', sdesc)
              + patient(e, name, pid)
              + e.ui(0x0020000D, ROOT + study) + e.ui(0x0020000E, ROOT + study + '.' + ser)
              + e.s(0x00200011, 'IS', ser) + e.s(0x00200013, 'IS', str(num)))
        fn = 'sc_%d.dcm' % k
        put(fn, dicom(meta(SC, inst, TS['implicit' if k % 2 else 'explicit']), ds))
        names.append(fn)
    return names


# --- 6. odd and broken files --------------------------------------------------
def odd():
    e = LE
    # no preamble, no meta: a bare implicit dataset (needs force)
    bare = (IMP.ui(0x00080016, SC) + IMP.ui(0x00080018, ROOT + '6.1')
            + IMP.s(0x00080060, 'CS', 'OT') + patient(IMP, 'Bare^Dataset', 'PAT-0006')
            + IMP.s(0x00200013, 'IS', '4'))
    put('bare_implicit.dcm', bare)
    # meta without a transfer syntax; the body is explicit big endian
    body = (BE.ui(0x00080016, SC) + BE.ui(0x00080018, ROOT + '6.2')
            + BE.s(0x00080060, 'CS', 'OT') + BE.us(0x00280010, 300)
            + patient(BE, 'Nots^Ynt', 'PAT-0008'))
    put('no_ts.dcm', dicom(meta(SC, ROOT + '6.2', None), body))
    # meta says implicit, body is explicit
    body = (e.ui(0x00080016, SC) + e.ui(0x00080018, ROOT + '6.3')
            + e.s(0x00080060, 'CS', 'OT') + e.us(0x00280010, 64)
            + patient(e, 'Mis^Match', 'PAT-0009'))
    put('ts_mismatch.dcm', dicom(meta(SC, ROOT + '6.3', TS['implicit']), body))
    # JPEG baseline: encapsulated pixel data of undefined length
    frag = b'\xff\xd8\xff\xe0' + b'\x00\x10JFIF\x00' + b'\x01' * 7 + b'\xff\xd9'
    encaps = (e.tag(0xFFFEE000) + b'\0\0\0\0' + e.tag(0xFFFEE000)
              + struct.pack('<L', len(frag)) + frag)
    body = (e.ui(0x00080016, SC) + e.ui(0x00080018, ROOT + '6.4')
            + e.s(0x00080060, 'CS', 'OT') + patient(e, 'Jay^Peg', 'PAT-0010')
            + e.us(0x00280010, 8) + e.us(0x00280011, 8) + e.us(0x00280100, 8)
            + e.elem(0x7FE00010, 'OB', encaps, UNDEF) + e.tag(0xFFFEE0DD) + b'\0\0\0\0')
    put('jpeg_encaps.dcm', dicom(meta(SC, ROOT + '6.4', TS['jpeg']), body))
    # odd values: wrong-length US
    body = (e.ui(0x00080016, SC) + e.ui(0x00080018, ROOT + '6.5')
            + e.elem(0x00280010, 'US', b'\x01\x02\x03\x00') + e.elem(0x00280011, 'US', b'\x05\x00\x07'))
    put('bad_us.dcm', dicom(meta(SC, ROOT + '6.5', TS['explicit']), body))
    # the same wrong length, one level down in a defined-length sequence
    bad_item = e.item(e.elem(0x00186012, 'US', b'\x01\x00\x02'))
    body = (e.ui(0x00080016, SC) + e.sq(0x00186011, [bad_item]))
    put('bad_nested.dcm', dicom(meta(SC, ROOT + '6.6', TS['explicit']), body))
    # number strings that do not parse, and other text corners
    body = (e.s(0x00080005, 'CS', 'ISO IR 100')
            + e.ui(0x00080016, SC) + e.ui(0x00080018, ROOT + '6.7')
            + e.s(0x00080080, 'LO', 'Caf\xe9 \xab M\xfcller \xbb')
            + e.s(0x00081030, 'LO', 'both \'single\' and "double"')
            + e.s(0x0008103E, 'LO', '  lead and trail  ')
            + e.s(0x00100010, 'PN', 'M\xfcller^J\xfcrgen=^=')
            + e.s(0x00101000, 'LO', 'ALIAS1\\ALIAS2\\\\ALIAS4')
            + e.s(0x00101020, 'DS', '1.7x')
            + e.s(0x00101030, 'DS', ' 70 \\ 71.5 ')
            + e.s(0x00181150, 'IS', 'abc')
            + e.s(0x00181151, 'IS', '2.5')
            + e.s(0x00181152, 'IS', '+08')
            + e.s(0x00181153, 'IS', '3.0')
            + e.s(0x00204000, 'LT', 'line one\r\nline two\ttabbed \\ kept')
            + e.s(0x00321060, 'LO', 'tab\there')
            + e.s(0x00400254, 'LO', 'ctl\x01\x7f')
            + e.elem(0x00400280, 'ST', b'nul\x00pad\x00')
            + e.s(0x00080054, 'AE', ' PACS1 \\STORE2')
            + e.s(0x00081190, 'UR', 'http://example.invalid/wado?x=1 ')
            + e.ui(0x00081155, ' ' + ROOT + '6.0'))
    put('text_corners.dcm', dicom(meta(SC, ROOT + '6.7', TS['explicit']), body))
    # empty values of every kind, and long ones
    body = (e.ui(0x00080016, SC) + e.ui(0x00080018, ROOT + '6.8')
            + e.elem(0x00080020, 'DA', b'') + e.elem(0x00080050, 'SH', b'')
            + e.elem(0x00080090, 'PN', b'') + e.elem(0x00081110, 'SQ', b'')
            + e.elem(0x00081155, 'UI', b'') + e.elem(0x00100030, 'DA', b'  ')
            + e.elem(0x00101020, 'DS', b'') + e.elem(0x00181150, 'IS', b'')
            + e.elem(0x00209165, 'AT', b'') + e.elem(0x00280010, 'US', b'')
            + e.elem(0x00280030, 'DS', b'0.5\\0.5\\0.5\\0.5\\0.5\\0.5\\0.5\\0.5\\0.5\\0.5'
                     b'\\0.5\\0.5\\0.5\\0.5\\0.5\\0.5\\0.5\\0.5')
            + e.s(0x00204000, 'LT', 'exactly sixteen!')
            + e.s(0x00321066, 'UT', 'seventeen chars..')
            + e.us(0x00181310, *range(17))
            + e.us(0x00280012, *range(16))
            + e.elem(0x00291010, 'OB', b'')
            + e.elem(0x00500004, 'CS', b'\x00\x00')
            + e.elem(0x7FE00010, 'OB', bytes(range(16))))
    put('empty_long.dcm', dicom(meta(SC, ROOT + '6.8', TS['explicit']), body))
    # undefined-length sequence that never ends
    item = e.tag(0xFFFEE000) + struct.pack('<L', UNDEF) + e.s(0x00080100, 'SH', 'X1')
    body = (e.ui(0x00080016, SC) + e.s(0x00080060, 'CS', 'OT')
            + e.elem(0x00081115, 'SQ', item, UNDEF))
    put('open_sq.dcm', dicom(meta(SC, ROOT + '6.9', TS['explicit']), body))
    # undefined-length OB with no delimiter: the reader keeps what came before
    body = (e.ui(0x00080016, SC) + e.s(0x00080060, 'CS', 'OT')
            + e.s(0x00100010, 'PN', 'Kept^Before')
            + e.elem(0x00420011, 'OB', b'%PDF-1.4 no end', UNDEF))
    put('open_ob.dcm', dicom(meta(SC, ROOT + '6.10', TS['explicit']), body))
    # a value cut off by the end of the file
    body = (e.ui(0x00080016, SC) + e.s(0x00080060, 'CS', 'OT')
            + e.elem(0x00081030, 'LO', b'Cut off he', 20))
    put('cut_value.dcm', dicom(meta(SC, ROOT + '6.11', TS['explicit']), body))
    # a defined-length sequence whose item header is cut short
    body = (e.ui(0x00080016, SC) + e.elem(0x00081140, 'SQ', b'\xfe\xff\x00\xe0\x10\x00'))
    put('cut_item.dcm', dicom(meta(SC, ROOT + '6.12', TS['explicit']), body))
    # explicit VR UN elements: one with a dictionary VR, one private
    body = (e.ui(0x00080016, SC) + e.elem(0x00080060, 'UN', b'OT')
            + e.elem(0x00280010, 'UN', b'\x00\x02')
            + e.s(0x00290010, 'LO', 'SIEMENS CSA HEADER')
            + e.elem(0x00291008, 'UN', b'MR ')
            + e.elem(0x00291009, 'UN', b'20100114')
            + e.elem(0x00331010, 'UN', b'\x01\x02')
            + e.s(0x00331011, 'LO', 'orphan private'))
    put('un_vr.dcm', dicom(meta(SC, ROOT + '6.13', TS['explicit']), body))
    # an unknown VR outside AA..ZZ switches the reader to implicit
    body = (e.ui(0x00080016, SC) + e.s(0x00080060, 'CS', 'OT')
            + IMP.s(0x00100010, 'PN', 'Switched^Midway')
            + IMP.s(0x00100020, 'LO', 'PAT-0011'))
    put('vr_switch.dcm', dicom(meta(SC, ROOT + '6.14', TS['explicit']), body))
    # group length elements and a duplicate tag
    body = (e.ul(0x00080000, 999) + e.ui(0x00080016, SC) + e.s(0x00080060, 'CS', 'XA')
            + e.s(0x00080060, 'CS', 'CR') + e.ul(0x00100000, 4)
            + patient(e, 'Group^Length', 'PAT-0012'))
    put('group_len.dcm', dicom(meta(SC, ROOT + '6.15', TS['explicit']), body))
    put('notes.txt', b'This is not a DICOM file at all, just some text.\n' * 4)
    put('tiny.dcm', b'\0' * 64)


def main():
    ct_explicit()
    mr_implicit()
    us_big()
    sr_deflated()
    sc = series()
    odd()
    for f in ['ct_explicit.dcm', 'mr_implicit.dcm', 'us_big.dcm', 'sr_deflated.dcm',
              'sc_0.dcm', 'sc_1.dcm', 'no_ts.dcm', 'ts_mismatch.dcm', 'jpeg_encaps.dcm',
              'bad_us.dcm', 'bad_nested.dcm', 'text_corners.dcm', 'empty_long.dcm',
              'open_sq.dcm', 'open_ob.dcm', 'cut_value.dcm', 'cut_item.dcm', 'un_vr.dcm',
              'vr_switch.dcm', 'group_len.dcm', 'notes.txt', 'tiny.dcm']:
        job('show', f)
    job('show', 'bare_implicit.dcm')
    job('show', 'bare_implicit.dcm', 'force')
    job('show', 'notes.txt', 'force')
    for kw in ['PatientName', 'PixelSpacing', 'ImagePositionPatient', 'InstanceNumber',
               'ExposureTime', 'SliceThickness', 'ImageType', 'Rows', 'WindowCenter',
               'FrameOfReferenceUID', 'SOPClassUID', 'PixelData', 'PatientWeight',
               'StudyComments', 'SmallestImagePixelValue']:
        job('get', 'ct_explicit.dcm', kw)
    for kw in ['PatientWeight', 'ExposureTime', 'XRayTubeCurrent', 'Exposure',
               'ExposureInuAs', 'OtherPatientIDs', 'RetrieveAETitle', 'InstitutionName',
               'SeriesDescription', 'RetrieveURL', 'ReferencedSOPInstanceUID',
               'StudyDescription']:
        job('get', 'text_corners.dcm', kw)
    for kw in ['SmallestImagePixelValue', 'PixelData', 'PatientName']:
        job('get', 'mr_implicit.dcm', kw)
    for kw in ['PatientWeight', 'AcquisitionDate', 'Rows', 'PixelSpacing', 'ReferencedSOPInstanceUID']:
        job('get', 'empty_long.dcm', kw)
    for f in ['ct_explicit.dcm', 'us_big.dcm', 'text_corners.dcm', 'empty_long.dcm',
              'sc_4.dcm']:
        job('pn', f)
    for f in ['ct_explicit.dcm', 'mr_implicit.dcm', 'us_big.dcm', 'jpeg_encaps.dcm',
              'text_corners.dcm', 'bare_implicit.dcm', 'group_len.dcm', 'un_vr.dcm']:
        job('resave', f, 'out/re_' + f)
    for f in ['ct_explicit.dcm', 'mr_implicit.dcm', 'us_big.dcm', 'text_corners.dcm']:
        job('anon', f, 'out/anon_' + f)
    job('show', 'out/anon_mr_implicit.dcm')
    job('show', 'out/anon_text_corners.dcm')
    for f, ts in [('ct_explicit.dcm', 'big'), ('ct_explicit.dcm', 'implicit'),
                  ('mr_implicit.dcm', 'explicit'), ('mr_implicit.dcm', 'big'),
                  ('us_big.dcm', 'explicit'), ('us_big.dcm', 'implicit'),
                  ('sr_deflated.dcm', 'explicit'), ('jpeg_encaps.dcm', 'explicit'),
                  ('sc_1.dcm', 'jpeg'), ('group_len.dcm', 'implicit')]:
        job('convert', f, ts, 'out/%s_%s' % (ts, f))
    job('show', 'out/big_mr_implicit.dcm')
    job('show', 'out/explicit_us_big.dcm')
    job('show', 'out/explicit_sr_deflated.dcm')
    job('index', *(sc + ['ct_explicit.dcm', 'mr_implicit.dcm', 'sr_deflated.dcm',
                         'us_big.dcm']))
    job('index', 'sc_2.dcm', 'notes.txt', 'sc_5.dcm')
    with open(os.path.join(D, 'jobs.txt'), 'w') as f:
        f.write('\n'.join(jobs) + '\n')
    with open(os.path.join(D, 'files.txt'), 'w') as f:
        f.write('\n'.join(files) + '\n')


main()
