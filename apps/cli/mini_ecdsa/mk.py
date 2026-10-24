# Writes data/: the token issuer's keys in several PEM shapes, a few broken
# or unusual key files, the ledger's accounts and entries, the token claims
# and the presented tokens, plus jobs.txt and files.txt.
# Run as: python3 -s -P -B mk.py
import base64
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'vendor'))
sys.path.insert(0, HERE)
import rng  # noqa: E402

os.urandom = rng.Stream(2025).read
import ecdsa  # noqa: E402
from ecdsa import der  # noqa: E402
from ecdsa.util import sigencode_string  # noqa: E402

D = 'data'
files = []


def put(name, data):
    os.makedirs(os.path.dirname(os.path.join(D, name)) or D, exist_ok=True)
    if isinstance(data, str):
        data = data.encode('utf-8')
    with open(os.path.join(D, name), 'wb') as f:
        f.write(data)
    files.append(name)


def spki(alg, params, point):
    return der.encode_sequence(
        der.encode_sequence(der.encode_oid(*alg), params),
        der.encode_bitstring(point, 0))


# The token issuer's key, in every shape the library writes.
issuer = ecdsa.SigningKey.generate(ecdsa.NIST256p, hashfunc=hashlib.sha256)
ivk = issuer.get_verifying_key()
put('keys/issuer.pem', issuer.to_pem())
put('keys/issuer_pkcs8.pem', issuer.to_pem(format='pkcs8'))
put('keys/issuer_pub.pem', ivk.to_pem())
put('keys/issuer_explicit.pem', ivk.to_pem(point_encoding='compressed',
                                            curve_parameters_encoding='explicit'))
k1 = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
put('keys/k1.pem', k1.to_pem(point_encoding='compressed'))

pt = ivk.to_string('uncompressed')
ec_oid = (1, 2, 840, 10045, 2, 1)
put('keys/unknown_curve.pem', der.topem(
    spki(ec_oid, der.encode_oid(1, 3, 132, 0, 99), pt), 'PUBLIC KEY'))
put('keys/rsa_oid.pem', der.topem(
    spki((1, 2, 840, 113549, 1, 1, 1), der.encode_oid(*ecdsa.NIST256p.oid), pt), 'PUBLIC KEY'))
put('keys/raw_point.pem', der.topem(
    spki(ec_oid, der.encode_oid(*ecdsa.NIST256p.oid), ivk.to_string('raw')), 'PUBLIC KEY'))
put('keys/trailing.pem', der.topem(ivk.to_der() + b'\x00', 'PUBLIC KEY'))
# Explicit parameters with b changed: a curve the library does not know.
c = ecdsa.NIST256p.curve
p = c.p()
params = der.encode_sequence(
    der.encode_integer(1),
    der.encode_sequence(der.encode_oid(1, 2, 840, 10045, 1, 1), der.encode_integer(p)),
    der.encode_sequence(der.encode_octet_string((c.a() % p).to_bytes(32, 'big')),
                        der.encode_octet_string((c.b() + 1).to_bytes(32, 'big'))),
    der.encode_octet_string(ecdsa.NIST256p.generator.to_bytes('uncompressed')),
    der.encode_integer(ecdsa.NIST256p.order),
    der.encode_integer(1))
put('keys/odd_curve.pem', der.topem(spki(ec_oid, params, pt), 'PUBLIC KEY'))

# The ledger: accounts on secp256k1 with opening balances, and entries
# signed by whoever claims to send the money (or by someone else).
names = ['alice', 'bob', 'carol', 'dave', 'mallory']
order = ecdsa.SECP256k1.order
acct = {}
for name in names:
    secexp = int(hashlib.sha256(('ledger-' + name).encode()).hexdigest(), 16) % order
    acct[name] = ecdsa.SigningKey.from_secret_exponent(secexp, ecdsa.SECP256k1, hashlib.sha256)
opening = {'alice': 100, 'bob': 40, 'carol': 0, 'dave': 15}
put('accounts.txt', ''.join('%s %d %s\n' % (n, opening[n], acct[n].get_verifying_key().to_string('compressed').hex())
                            for n in names if n in opening))


def entry(frm, to, amount, signer=None, alter=None):
    msg = '%s|%s|%d' % (frm, to, amount)
    sig = acct[signer or frm].sign_deterministic(msg.encode())
    if alter:
        msg = '%s|%s|%d' % alter
    return '%s|%s\n' % (msg, sig.hex())


put('ledger.txt', ''.join([
    entry('alice', 'bob', 25),
    entry('bob', 'carol', 30),
    entry('dave', 'alice', 5, alter=('dave', 'alice', 50)),
    entry('alice', 'mallory', 60, signer='mallory'),
    entry('carol', 'alice', 99),
    entry('bob', 'dave', 12, signer='alice'),
    'alice|carol|5|' + acct['alice'].sign_deterministic(b'alice|carol|5').hex()[:-2] + '\n',
    'dave|bob|1|' + '07' * 64 + '\n',
]))

# Tokens: claims the issuer signs, then what customers present back.
claims = [
    '{"sub":"alice","role":"admin","exp":1767225600}',
    '{"sub":"bob","role":"viewer","exp":1735689600}',
    '{"sub":"carol","role":"editor","exp":1767225600}',
]
put('claims.txt', '\n'.join(claims) + '\n')


def b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b'=').decode()


HEADER = '{"alg":"ES256","typ":"JWT"}'


def token(payload, key=issuer, header=HEADER):
    head = b64u(header.encode()) + '.' + b64u(payload.encode())
    sig = key.sign_deterministic(head.encode(), hashfunc=hashlib.sha256, sigencode=sigencode_string)
    return head + '.' + b64u(sig)


other = ecdsa.SigningKey.generate(ecdsa.NIST256p, hashfunc=hashlib.sha256)
good = [token(cl) for cl in claims]
h, pl, sg = good[1].split('.')
forged = h + '.' + b64u(claims[1].replace('viewer', 'admin').encode()) + '.' + sg
put('tokens.txt', '\n'.join([
    good[0],
    forged,
    good[2],
    token(claims[0].replace('alice', 'eve'), key=other),
    good[1][:-3],
    b64u(b'{"alg":"none","typ":"JWT"}') + '.' + b64u(claims[0].encode()) + '.',
    'not-a-token',
    good[1],
]) + '\n')

jobs = [
    'seed 11',
    'curves NIST192p NIST224p NIST256p NIST384p NIST521p SECP256k1 BRAINPOOLP256r1 BRAINPOOLP320t1',
    'curve prime256v1',
    'curve secp256k1',
    'curve P-256',
    'genkey a NIST256p sha256',
    'genkey b NIST256p sha256',
    'genkey c SECP256k1 sha256',
    'genkey d NIST192p sha1',
    'genkey e NIST521p sha512',
    'genkey f NIST224p sha224',
    'genkey g BRAINPOOLP256r1 sha256',
    'genkey h NIST384p sha384',
    'secret one NIST256p 1',
    'secret zero NIST256p 0',
    'secret rfc NIST256p C9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721',
    'secret tiny SECP256k1 3',
    'show a',
    'show d',
    'show one',
    'encodings one',
    'encodings tiny',
    'pem a ssleay uncompressed named_curve',
    'pem d pkcs8 compressed named_curve',
    'pem d ssleay hybrid explicit',
    'der d',
    'load issuer keys/issuer.pem',
    'load issuer8 keys/issuer_pkcs8.pem',
    'loadpub ipub keys/issuer_pub.pem',
    'loadpub iexp keys/issuer_explicit.pem',
    'load k1 keys/k1.pem',
    'load bad keys/issuer_pub.pem',
    'loadpub unknown keys/unknown_curve.pem',
    'loadpub rsa keys/rsa_oid.pem',
    'loadpub raw keys/raw_point.pem',
    'loadpub trail keys/trailing.pem',
    'loadpub odd keys/odd_curve.pem',
    'same issuer issuer8',
    'same ipub iexp',
    'same ipub a',
    'show iexp',
    'sign rfc sha256 string sample',
    'sign rfc sha256 string test',
    'sign rfc sha1 string sample',
    'sign rfc sha512 string sample',
    'sign rfc sha224 der sample',
    'verify rfc sha224 der sample',
    'verify rfc sha224 der Sample',
    'sign a sha256 der transfer 100 to account 42',
    'verify a sha256 der transfer 100 to account 42',
    'verify b sha256 der transfer 100 to account 42',
    'verify a sha256 string transfer 100 to account 42',
    'sign c sha256 canon pay bob 5',
    'verify c sha256 der pay bob 5',
    'signk a 12345 sha256 string hello',
    'signk a 0 sha256 string hello',
    'signrand a sha256 string hello',
    'signrand a sha256 string hello',
    'verify a sha256 string hello',
    'sign e sha512 string a long curve',
    'verify e sha512 string a long curve',
    'sign h sha384 der short',
    'verify h sha384 der short',
    'sign g sha256 string brainpool',
    'verify g sha256 string brainpool',
    'digest a sha256 string short digest',
    'digest f sha512 string long digest',
    'digest d sha512 string long digest',
    'badsig a 3045022100ff',
    'badsig a 3006020101020101ff',
    'badsig a 3006020181020101',
    'badsig a 300702020001020101',
    'badsig a 3006020100020101',
    'sign tiny sha256 string recover me',
    'recover tiny sha256 recover me',
    'sign c sha256 string recover me',
    'recover c sha256 recover me',
    'point NIST256p - 036b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296',
    'point NIST256p - 026b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296',
    'point NIST256p - 056b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296',
    'point NIST256p - 020000000000000000000000000000000000000000000000000000000000000005',
    'point NIST256p - 020000000000000000000000000000000000000000000000000000000000000001',
    'point NIST224p - 0300000000000000000000000000000000000000000000000000000003',
    'point NIST224p - 02b70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21',
    'point NIST192p - 07188da80eb03090f67cbf20eb43a18800f4ff0afd82ff101207192b95ffc8da78631011ed6b24cdd573f977a11e794811',
    'point NIST192p - 06188da80eb03090f67cbf20eb43a18800f4ff0afd82ff101207192b95ffc8da78631011ed6b24cdd573f977a11e794811',
    'point SECP256k1 - 0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b9',
    'point SECP256k1 - 0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8',
    'point SECP256k1 compressed,raw 0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b9',
    'point SECP256k1 compressed 79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798',
    'ecdh a b',
    'ecdh b a',
    'ecdh a c',
    'ecdh c k1',
    '!tokens issuer claims.txt tokens.txt ipub',
    '!ledger accounts.txt ledger.txt',
]
with open(D + '/jobs.txt', 'w') as f:
    f.write('\n'.join(jobs) + '\n')
with open(D + '/files.txt', 'w') as f:
    f.write('\n'.join(files) + '\n')
print(len(files), 'files,', len(jobs), 'jobs')
