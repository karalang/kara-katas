# Runs data/jobs.txt on the vendored rsa and prints the results.
# Run as: python3 -I -B oracle.py > expected.out
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'vendor'))
sys.path.insert(0, HERE)
import rng  # noqa: E402
import rsa  # noqa: E402
import rsa.common  # noqa: E402
import rsa.prime  # noqa: E402
from rsa.pkcs1_v2 import mgf1  # noqa: E402

D = os.path.join(HERE, 'data')


def read(path):
    with open(os.path.join(D, path), 'rb') as f:
        return f.read()


def fail(e):
    print('  %s: %s' % (type(e).__name__, e))


def pub_of(k):
    return rsa.PublicKey(k.n, k.e)


def main():
    keys = {}
    last = b''
    sig = b''
    for job in read('jobs.txt').decode().split('\n'):
        if not job:
            continue
        print('> ' + job)
        w = job.split(' ')
        rest = ' '.join(w[3:]).encode()
        try:
            if w[0] == 'seed':
                os.urandom = rng.Stream(int(w[1])).read
            elif w[0] == 'newkeys':
                pub, priv = rsa.newkeys(int(w[2]))
                keys[w[1]] = priv
                print('  n has %d bits, p %d, q %d, e=%d' % (
                    rsa.common.bit_size(priv.n), rsa.common.bit_size(priv.p),
                    rsa.common.bit_size(priv.q), priv.e))
            elif w[0] == 'show':
                print('  ' + repr(pub_of(keys[w[1]])))
                print('  ' + repr(keys[w[1]]))
            elif w[0] == 'pem':
                k = keys[w[1]]
                for blob in (k.save_pkcs1(), pub_of(k).save_pkcs1()):
                    for line in blob.decode().split('\n'):
                        if line:
                            print('  ' + line)
            elif w[0] == 'der':
                k = keys[w[1]]
                print('  private ' + k.save_pkcs1('DER').hex())
                print('  public  ' + pub_of(k).save_pkcs1('DER').hex())
            elif w[0] in ('load', 'loadpub', 'loadssl'):
                data = read(w[2])
                if w[0] == 'load':
                    k = rsa.PrivateKey.load_pkcs1(data)
                elif w[0] == 'loadpub':
                    k = rsa.PublicKey.load_pkcs1(data)
                else:
                    k = rsa.PublicKey.load_pkcs1_openssl_pem(data)
                keys[w[1]] = k
                print('  %s, n has %d bits, e=%d' % (
                    type(k).__name__, rsa.common.bit_size(k.n), k.e))
            elif w[0] == 'same':
                print('  ' + str(pub_of(keys[w[1]]) == pub_of(keys[w[2]])))
            elif w[0] == 'resave':
                same = keys[w[1]].save_pkcs1() == read(w[2])
                print('  ' + ('identical' if same else 'differs'))
            elif w[0] == 'encrypt':
                rest = ' '.join(w[2:]).encode()
                last = rsa.encrypt(rest, keys[w[1]])
                print('  %d bytes %s' % (len(last), last.hex()))
            elif w[0] == 'decrypt':
                print('  ' + repr(rsa.decrypt(last, keys[w[1]])))
            elif w[0] == 'sign':
                sig = rsa.sign(rest, keys[w[1]], w[2])
                print('  %d bytes %s' % (len(sig), sig.hex()))
            elif w[0] == 'verify':
                rest = ' '.join(w[2:]).encode()
                print('  ' + rsa.verify(rest, sig, keys[w[1]]))
            elif w[0] == 'mgf1':
                print('  ' + mgf1(bytes.fromhex(w[1]), int(w[2]), w[3]).hex())
            elif w[0] == 'inverse':
                print('  %d' % rsa.common.inverse(int(w[1]), int(w[2])))
            elif w[0] == 'crt':
                a = [int(x) for x in w[1].split(',')]
                m = [int(x) for x in w[2].split(',')]
                print('  %d' % rsa.common.crt(a, m))
            elif w[0] == 'prime':
                print('  ' + ' '.join('%s:%s' % (x, rsa.prime.is_prime(int(x))) for x in w[1:]))
            elif w[0] == '!licenses':
                licenses(read(w[1]).decode(), read(w[2]).decode(), keys[w[3]], keys[w[4]])
            elif w[0] == '!vault':
                vault(read(w[1]).decode(), [(name, keys[name]) for name in w[2:]])
        except Exception as e:
            fail(e)


def licenses(issued, presented, signer, checker):
    sigs = []
    for line in issued.split('\n'):
        if not line:
            continue
        s = rsa.sign(line.encode(), signer, 'SHA-256')
        sigs.append(s)
        print('  issued %s' % line)
        print('    %s' % base64.b64encode(s).decode())
    for i, line in enumerate(presented.split('\n')):
        if not line:
            continue
        if i >= len(sigs):
            print('  %s: no signature' % line)
            continue
        try:
            how = rsa.verify(line.encode(), sigs[i], checker)
            print('  %s: valid (%s)' % (line, how))
        except rsa.VerificationError as e:
            print('  %s: REJECTED (%s)' % (line, e))


def vault(text, people):
    for line in text.split('\n'):
        if not line:
            continue
        print('  secret %r' % line)
        for name, k in people:
            try:
                box = rsa.encrypt(line.encode(), k)
            except OverflowError as e:
                print('    for %s: OverflowError: %s' % (name, e))
                continue
            print('    for %s: %d bytes, starts %s' % (name, len(box), box[:6].hex()))
            for other, k2 in people:
                try:
                    got = rsa.decrypt(box, k2)
                    print('      %s opens it: %r' % (other, got))
                except rsa.DecryptionError as e:
                    print('      %s cannot: %s' % (other, e))


main()
