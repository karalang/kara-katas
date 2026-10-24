# Writes data/: the bank's key files, the license records and the secrets,
# plus jobs.txt and files.txt. Run as: python3 -s -P -B mk.py
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'vendor'))
sys.path.insert(0, HERE)
import rng  # noqa: E402

stream = rng.Stream(2024)
os.urandom = stream.read
import rsa  # noqa: E402

D = 'data'
files = []


def put(name, data):
    os.makedirs(os.path.dirname(os.path.join(D, name)), exist_ok=True)
    if isinstance(data, str):
        data = data.encode('utf-8')
    with open(os.path.join(D, name), 'wb') as f:
        f.write(data)
    files.append(name)


def der_len(n):
    if n < 128:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    return bytes([0x80 | len(b)]) + b


def tlv(tag, body):
    return bytes([tag]) + der_len(len(body)) + body


def der_int(v):
    return tlv(0x02, v.to_bytes(v.bit_length() // 8 + 1, 'big'))


def der_oid(dotted):
    parts = [int(x) for x in dotted.split('.')]
    body = bytes([parts[0] * 40 + parts[1]])
    for p in parts[2:]:
        chunk = [p & 0x7F]
        p >>= 7
        while p:
            chunk.insert(0, 0x80 | (p & 0x7F))
            p >>= 7
        body += bytes(chunk)
    return tlv(0x06, body)


def pem(der, marker, headers=(), eol='\n'):
    b64 = base64.standard_b64encode(der).decode()
    lines = ['-----BEGIN %s-----' % marker] + list(headers)
    lines += [b64[i:i + 64] for i in range(0, len(b64), 64)]
    lines.append('-----END %s-----' % marker)
    return eol.join(lines) + eol


pub, priv = rsa.newkeys(1024)
put('keys/bank.pem', priv.save_pkcs1('PEM'))
put('keys/bank_pub.pem', pub.save_pkcs1('PEM'))
pkcs1 = pub.save_pkcs1('DER')
spki = tlv(0x30, tlv(0x30, der_oid('1.2.840.113549.1.1.1') + b'\x05\x00') + tlv(0x03, b'\x00' + pkcs1))
put('keys/bank_ssl.pem', pem(spki, 'PUBLIC KEY'))
not_rsa = tlv(0x30, tlv(0x30, der_oid('1.2.840.10045.2.1') + b'\x05\x00') + tlv(0x03, b'\x00' + pkcs1))
put('keys/ec_ssl.pem', pem(not_rsa, 'PUBLIC KEY'))
put('keys/commented.pem', 'Key for the billing service\r\n\r\n' + pem(
    pkcs1, 'RSA PUBLIC KEY', headers=['Comment: issued 2024-03-01', ''], eol='\r\n'))
put('keys/no_end.pem', pem(pkcs1, 'RSA PUBLIC KEY').replace('-----END RSA PUBLIC KEY-----\n', ''))
v1 = tlv(0x30, b''.join(der_int(x) for x in (
    1, priv.n, priv.e, priv.d, priv.p, priv.q, priv.exp1, priv.exp2, priv.coef)))
put('keys/v1.pem', pem(v1, 'RSA PRIVATE KEY'))

put('licenses.txt', '''acme-corp|inventory-pro|seats=25|expires=2025-12-31
globex|inventory-pro|seats=5|expires=2024-06-30
initech|reports|seats=100|expires=2026-01-15
umbrella|inventory-lite|seats=1|expires=2024-12-01
''')
put('tampered.txt', '''acme-corp|inventory-pro|seats=25|expires=2025-12-31
globex|inventory-pro|seats=50|expires=2024-06-30
initech|reports|seats=100|expires=2027-01-15
umbrella|inventory-lite|seats=1|expires=2024-12-01
hooli|reports|seats=10|expires=2025-01-01
''')
put('secrets.txt', '''db=s3cret
api=k-17
pin=4321
a much longer secret than fits
''')

jobs = [
    'seed 7',
    'newkeys alice 256',
    'newkeys bob 512',
    'newkeys tiny 16',
    'newkeys bad 15',
    'show alice',
    'show tiny',
    'pem alice',
    'der alice',
    'load bank keys/bank.pem',
    'loadpub bankpub keys/bank_pub.pem',
    'loadssl bankssl keys/bank_ssl.pem',
    'loadssl ec keys/ec_ssl.pem',
    'loadpub billing keys/commented.pem',
    'load wrong keys/bank_pub.pem',
    'loadpub cut keys/no_end.pem',
    'load old keys/v1.pem',
    'same bank bankpub',
    'same bankpub bankssl',
    'same bankpub billing',
    'same alice bob',
    'resave bank keys/bank.pem',
    'resave bankpub keys/bank_pub.pem',
    'encrypt alice hello world',
    'decrypt alice',
    'decrypt alice',
    'decrypt bob',
    'encrypt alice twenty-two bytes long!',
    'encrypt alice twenty-one bytes long',
    'decrypt alice',
    'encrypt bankpub meet at the usual place',
    'decrypt bank',
    'sign bank SHA-256 transfer 100 to account 42',
    'verify bankpub transfer 100 to account 42',
    'verify bankpub transfer 900 to account 42',
    'verify alice transfer 100 to account 42',
    'sign bank MD5 hello',
    'verify bankssl hello',
    'sign bank SHA-1 hello',
    'verify bankssl hello',
    'sign bank SHA-224 hello',
    'verify bankssl hello',
    'sign bank SHA-384 hello',
    'verify bankssl hello',
    'sign bank SHA-512 hello',
    'verify bankssl hello',
    'sign bob SHA-256 hello',
    'verify bob hello',
    'sign bob SHA-512 hello',
    'sign bank BLAKE hello',
    'mgf1 00 20 SHA-1',
    'mgf1 0001020304 47 SHA-256',
    'mgf1 abcdef 3 MD5',
    'mgf1 abcdef 0 SHA-512',
    'mgf1 abcdef 10 SHA-3',
    'inverse 3 11',
    'inverse 65537 3120',
    'inverse 6 9',
    'crt 2,3,2 3,5,7',
    'prime 1 2 9 15 17 561 7919 1000003 2147483647 4294967297',
    '!licenses licenses.txt tampered.txt bank bankssl',
    '!vault secrets.txt alice bob',
]
with open(D + '/jobs.txt', 'w') as f:
    f.write('\n'.join(jobs) + '\n')
with open(D + '/files.txt', 'w') as f:
    f.write('\n'.join(files) + '\n')
print(len(files), 'files,', len(jobs), 'jobs')
