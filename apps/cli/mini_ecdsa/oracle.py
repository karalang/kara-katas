# Runs data/jobs.txt on the vendored ecdsa and prints the results.
# Run as: python3 -I -B oracle.py > expected.out
import base64
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'vendor'))
sys.path.insert(0, HERE)
import rng  # noqa: E402
import ecdsa  # noqa: E402
from ecdsa import curves, util  # noqa: E402
from ecdsa.ecdh import ECDH  # noqa: E402

D = os.path.join(HERE, 'data')
ALL_ENCODINGS = ['uncompressed', 'compressed', 'hybrid', 'raw']
SIGENCODE = {'string': util.sigencode_string, 'der': util.sigencode_der,
             'canon': util.sigencode_der_canonize}
SIGDECODE = {'string': util.sigdecode_string, 'der': util.sigdecode_der}
HEADER = '{"alg":"ES256","typ":"JWT"}'


def read(path):
    with open(os.path.join(D, path), 'rb') as f:
        return f.read()


def hashfunc(name):
    return getattr(hashlib, name)


def lines(blob):
    for line in blob.decode().split('\n'):
        if line:
            print('  ' + line)


def main():
    keys = {}
    for job in read('jobs.txt').decode().split('\n'):
        if not job:
            continue
        print('> ' + job)
        w = job.split(' ')
        try:
            run(w, keys)
        except Exception as e:
            print('  %s: %s' % (type(e).__name__, e))


state = {'sig': b''}


def run(w, keys):
    cmd = w[0]
    if cmd == 'seed':
        os.urandom = rng.Stream(int(w[1])).read
    elif cmd == 'curves':
        for name in w[1:]:
            c = curves.curve_by_name(name)
            print('  %s (%s): baselen %d, public key %d bytes, signature %d bytes, oid %s' % (
                c.name, c.openssl_name, c.baselen, c.verifying_key_length,
                c.signature_length, '.'.join(str(x) for x in c.oid)))
    elif cmd == 'curve':
        c = curves.curve_by_name(w[1])
        print('  %s, order %d bits' % (c.name, c.order.bit_length()))
    elif cmd == 'genkey':
        sk = ecdsa.SigningKey.generate(curves.curve_by_name(w[2]), hashfunc=hashfunc(w[3]))
        keys[w[1]] = sk
        print('  secret %s' % sk.to_string().hex())
    elif cmd == 'secret':
        sk = ecdsa.SigningKey.from_secret_exponent(int(w[3], 16), curves.curve_by_name(w[2]),
                                                   hashlib.sha256)
        keys[w[1]] = sk
        print('  public %s' % sk.get_verifying_key().to_string('compressed').hex())
    elif cmd == 'show':
        k = keys[w[1]]
        vk = k.get_verifying_key() if isinstance(k, ecdsa.SigningKey) else k
        print('  ' + repr(vk))
    elif cmd == 'encodings':
        vk = keys[w[1]].get_verifying_key()
        for enc in ('raw', 'uncompressed', 'compressed', 'hybrid'):
            print('  %s %s' % (enc, vk.to_string(enc).hex()))
    elif cmd == 'pem':
        sk = keys[w[1]]
        lines(sk.to_pem(point_encoding=w[3], format=w[2], curve_parameters_encoding=w[4]))
        lines(sk.get_verifying_key().to_pem(point_encoding=w[3], curve_parameters_encoding=w[4]))
    elif cmd == 'der':
        sk = keys[w[1]]
        print('  private ' + sk.to_der().hex())
        print('  public  ' + sk.get_verifying_key().to_der().hex())
    elif cmd == 'load':
        sk = ecdsa.SigningKey.from_pem(read(w[2]))
        keys[w[1]] = sk
        print('  %s key, secret %s' % (sk.curve.name, sk.to_string().hex()))
    elif cmd == 'loadpub':
        vk = ecdsa.VerifyingKey.from_pem(read(w[2]))
        keys[w[1]] = vk
        print('  %s key %s' % (vk.curve.name, vk.to_string('compressed').hex()))
    elif cmd == 'same':
        a, b = (keys[x] for x in w[1:3])
        a = a.get_verifying_key() if isinstance(a, ecdsa.SigningKey) else a
        b = b.get_verifying_key() if isinstance(b, ecdsa.SigningKey) else b
        print('  ' + str(a == b))
    elif cmd in ('sign', 'signk', 'signrand', 'digest'):
        sk = keys[w[1]]
        if cmd == 'signk':
            k, w = int(w[2]), w[:2] + w[3:]
        h = hashfunc(w[2])
        msg = ' '.join(w[4:]).encode()
        if cmd == 'sign':
            s = sk.sign_deterministic(msg, hashfunc=h, sigencode=SIGENCODE[w[3]])
        elif cmd == 'signk':
            s = sk.sign(msg, hashfunc=h, sigencode=SIGENCODE[w[3]], k=k)
        elif cmd == 'signrand':
            s = sk.sign(msg, hashfunc=h, sigencode=SIGENCODE[w[3]])
        else:
            s = sk.sign_digest(h(msg).digest(), sigencode=SIGENCODE[w[3]])
        state['sig'] = s
        print('  %d bytes %s' % (len(s), s.hex()))
    elif cmd == 'verify':
        k = keys[w[1]]
        vk = k.get_verifying_key() if isinstance(k, ecdsa.SigningKey) else k
        msg = ' '.join(w[4:]).encode()
        print('  ' + str(vk.verify(state['sig'], msg, hashfunc(w[2]), sigdecode=SIGDECODE[w[3]])))
    elif cmd == 'badsig':
        vk = keys[w[1]].get_verifying_key()
        print('  ' + str(vk.verify(bytes.fromhex(w[2]), b'hello', sigdecode=util.sigdecode_der)))
    elif cmd == 'recover':
        k = keys[w[1]]
        vks = ecdsa.VerifyingKey.from_public_key_recovery(
            state['sig'], ' '.join(w[3:]).encode(), k.curve, hashfunc(w[2]))
        for vk in vks:
            mark = ' (the signer)' if vk == k.get_verifying_key() else ''
            print('  %s%s' % (vk.to_string('compressed').hex(), mark))
    elif cmd == 'point':
        encs = ALL_ENCODINGS if w[2] == '-' else w[2].split(',')
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(w[3]), curves.curve_by_name(w[1]),
                                            valid_encodings=encs)
        print('  ' + vk.to_string('uncompressed').hex())
    elif cmd == 'ecdh':
        a, b = keys[w[1]], keys[w[2]]
        vb = b.get_verifying_key() if isinstance(b, ecdsa.SigningKey) else b
        e = ECDH(private_key=a)
        e.load_received_public_key(vb)
        print('  ' + e.generate_sharedsecret_bytes().hex())
    elif cmd == '!tokens':
        tokens(keys[w[1]], read(w[2]).decode(), read(w[3]).decode(), keys[w[4]])
    elif cmd == '!ledger':
        ledger(read(w[1]).decode(), read(w[2]).decode())


def b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b'=').decode()


def unb64u(s):
    return base64.urlsafe_b64decode(s + '=' * (-len(s) % 4))


def tokens(issuer, claims, presented, vk):
    for cl in claims.split('\n'):
        if not cl:
            continue
        head = b64u(HEADER.encode()) + '.' + b64u(cl.encode())
        s = issuer.sign_deterministic(head.encode(), hashfunc=hashlib.sha256,
                                      sigencode=util.sigencode_string)
        print('  issued %s' % cl)
        print('    %s.%s' % (head, b64u(s)))
    for tok in presented.split('\n'):
        if not tok:
            continue
        parts = tok.split('.')
        if len(parts) != 3:
            print('  %s: malformed' % tok)
            continue
        header = unb64u(parts[0]).decode()
        if header != HEADER:
            print('  unsupported header %s' % header)
            continue
        payload = unb64u(parts[1]).decode()
        try:
            vk.verify(unb64u(parts[2]), (parts[0] + '.' + parts[1]).encode(), hashlib.sha256,
                      sigdecode=util.sigdecode_string)
            print('  valid %s' % payload)
        except ecdsa.BadSignatureError as e:
            print('  REJECTED %s: %s' % (payload, e))


def ledger(accounts, entries):
    names = []
    balance = {}
    keys = {}
    for line in accounts.split('\n'):
        if not line:
            continue
        name, amount, pub = line.split(' ')
        names.append(name)
        balance[name] = int(amount)
        keys[name] = ecdsa.VerifyingKey.from_string(bytes.fromhex(pub), ecdsa.SECP256k1,
                                                    hashlib.sha256)
    for line in entries.split('\n'):
        if not line:
            continue
        frm, to, amount, sighex = line.split('|')
        msg = '%s|%s|%s' % (frm, to, amount)
        try:
            cands = ecdsa.VerifyingKey.from_public_key_recovery(
                bytes.fromhex(sighex), msg.encode(), ecdsa.SECP256k1, hashlib.sha256)
        except Exception as e:
            print('  %s: %s: %s' % (msg, type(e).__name__, e))
            continue
        signer = None
        for n in names:
            if keys[n] in cands:
                signer = n
        if signer is None:
            print('  %s: unknown signer' % msg)
        elif signer != frm:
            print('  %s: forged, signed by %s' % (msg, signer))
        elif to not in balance:
            print('  %s: no account %s' % (msg, to))
        elif balance[frm] < int(amount):
            print('  %s: insufficient funds (%d)' % (msg, balance[frm]))
        else:
            balance[frm] -= int(amount)
            balance[to] += int(amount)
            print('  %s: ok' % msg)
    print('  balances: ' + ', '.join('%s %d' % (n, balance[n]) for n in names))


main()
