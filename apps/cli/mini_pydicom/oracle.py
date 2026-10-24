# Runs data/jobs.txt against the vendored pydicom 3.0.1 and prints what
# mini_pydicom.kara must print. numpy is blocked so pydicom takes its
# pure-Python paths, and warnings are silenced: pydicom's default reading
# mode only warns, which never changes stdout.
# Run as: python3 -I -B oracle.py > expected.out
import os
import sys
import warnings
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.modules['numpy'] = None
sys.path.insert(0, os.path.join(HERE, 'vendor'))
warnings.simplefilter('ignore')
import logging  # noqa: E402
logging.disable(logging.CRITICAL)
import pydicom  # noqa: E402
from pydicom import dcmread, dcmwrite  # noqa: E402
from pydicom.uid import UID  # noqa: E402

TS = {
    'implicit': '1.2.840.10008.1.2',
    'explicit': '1.2.840.10008.1.2.1',
    'big': '1.2.840.10008.1.2.2',
    'jpeg': '1.2.840.10008.1.2.4.50',
}


def err(e):
    return '%s: %s' % (type(e).__name__, str(e).split('\n')[0])


def written(path):
    with open(path, 'rb') as f:
        data = f.read()
    return data, '%d bytes, crc32 %08x' % (len(data), zlib.crc32(data))


def show(words):
    try:
        ds = dcmread(words[1], force=len(words) > 2)
        text = str(ds)
    except Exception as e:
        print('error: ' + err(e))
        return
    print(text)


def get(words):
    ds = dcmread(words[1])
    v = ds.get(words[2])
    print('%s: %s' % (words[2], 'missing' if v is None else str(v)))


def pn(words):
    ds = dcmread(words[1])
    v = ds.get('PatientName')
    if v is None:
        print('no PatientName')
        return
    print('name %r: family %r given %r middle %r prefix %r suffix %r' % (
        str(v), v.family_name, v.given_name, v.middle_name, v.name_prefix,
        v.name_suffix))
    print('  ideographic %r phonetic %r' % (v.ideographic, v.phonetic))


def resave(words):
    ds = dcmread(words[1], force=True)
    try:
        dcmwrite(words[2], ds)
    except Exception as e:
        print('resave %s: error: %s' % (words[1], err(e)))
        return
    data, info = written(words[2])
    with open(words[1], 'rb') as f:
        same = f.read() == data
    print('resave %s: %s, %s' % (words[1], info, 'identical' if same else 'differs'))


def anon(words):
    ds = dcmread(words[1])

    def person_names(dataset, elem):
        if elem.VR == 'PN':
            elem.value = 'Anonymous'

    ds.walk(person_names)
    for kw in ['PatientBirthDate', 'OtherPatientIDs']:
        if kw in ds:
            delattr(ds, kw)
    ds.PatientID = 'ANON'
    ds.remove_private_tags()
    try:
        dcmwrite(words[2], ds)
    except Exception as e:
        print('anon %s: error: %s' % (words[1], err(e)))
        return
    print('anon %s: %s' % (words[1], written(words[2])[1]))


def convert(words):
    ds = dcmread(words[1])
    ds.file_meta.TransferSyntaxUID = UID(TS[words[2]])
    try:
        dcmwrite(words[3], ds)
    except Exception as e:
        print('convert %s to %s: error: %s' % (words[1], words[2], err(e)))
        return
    print('convert %s to %s: %s' % (words[1], words[2], written(words[3])[1]))


def index(words):
    studies = {}
    skipped = []
    for path in words[1:]:
        try:
            ds = dcmread(path)
        except Exception as e:
            skipped.append((path, type(e).__name__))
            continue
        st = studies.setdefault(str(ds.StudyInstanceUID), {
            'date': str(ds.get('StudyDate', '')),
            'desc': str(ds.get('StudyDescription', '')),
            'patient': str(ds.get('PatientName', '')),
            'id': str(ds.get('PatientID', '')),
            'series': {}})
        se = st['series'].setdefault(str(ds.SeriesInstanceUID), {
            'num': int(ds.get('SeriesNumber', 0)),
            'mod': str(ds.get('Modality', '')),
            'desc': str(ds.get('SeriesDescription', '')),
            'inst': []})
        se['inst'].append((int(ds.get('InstanceNumber', 0)), path))
    for uid in sorted(studies):
        st = studies[uid]
        print('Study %s %s %r, patient %s (%s)' % (uid, st['date'], st['desc'],
                                                  st['patient'], st['id']))
        series = sorted(st['series'].items(), key=lambda kv: (kv[1]['num'], kv[0]))
        for suid, se in series:
            print('  Series %d %s %r: %d instance(s)' % (se['num'], se['mod'], se['desc'],
                                                        len(se['inst'])))
            for num, path in sorted(se['inst']):
                print('    #%d %s' % (num, path))
    for path, why in skipped:
        print('  skipped %s: %s' % (path, why))


JOBS = {'show': show, 'get': get, 'pn': pn, 'resave': resave, 'anon': anon,
        'convert': convert, 'index': index}


def main():
    os.chdir(os.path.join(HERE, 'data'))
    os.makedirs('out', exist_ok=True)
    with open('jobs.txt') as f:
        jobs = [ln for ln in f.read().split('\n') if ln]
    for line in jobs:
        print('> ' + line)
        words = line.split(' ')
        try:
            JOBS[words[0]](words)
        except Exception as e:
            print('error: ' + err(e))


main()
