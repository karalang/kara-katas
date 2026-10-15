# Builds data/: a small PKI made with Python's cryptography 50 (an RSA
# root, an intermediate, server and client leaves, an EC leaf) and broken
# certificates, for mini_x509 to read and verify.
import datetime as dt, ipaddress, os, shutil
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID, AuthorityInformationAccessOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec

if os.path.isdir("data"):
    shutil.rmtree("data")
os.makedirs("data")
UTC = dt.timezone.utc


def name(**kw):
    order = [("C", NameOID.COUNTRY_NAME), ("ST", NameOID.STATE_OR_PROVINCE_NAME), ("L", NameOID.LOCALITY_NAME),
             ("O", NameOID.ORGANIZATION_NAME), ("OU", NameOID.ORGANIZATIONAL_UNIT_NAME), ("CN", NameOID.COMMON_NAME),
             ("emailAddress", NameOID.EMAIL_ADDRESS)]
    return x509.Name([x509.NameAttribute(oid, kw[k]) for k, oid in order if k in kw])


def key(bits=2048):
    return rsa.generate_private_key(public_exponent=65537, key_size=bits)


def build(subject, issuer, pub, signer, serial, nb, na, exts, algo=hashes.SHA256()):
    b = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(pub)
    b = b.serial_number(serial).not_valid_before(nb).not_valid_after(na)
    for e, crit in exts:
        b = b.add_extension(e, critical=crit)
    return b.sign(signer, algo)


def pem(c):
    return c.public_bytes(serialization.Encoding.PEM)


def ski(pub):
    return x509.SubjectKeyIdentifier.from_public_key(pub)


def aki(pub):
    return x509.AuthorityKeyIdentifier.from_issuer_public_key(pub)


T0 = dt.datetime(2026, 1, 1, tzinfo=UTC)
root_k = key(4096)
root_n = name(C="US", O="Kara Test PKI", CN="Kara Root CA R1")
root = build(root_n, root_n, root_k.public_key(), root_k, 0x01, T0, dt.datetime(2046, 1, 1, tzinfo=UTC), [
    (x509.BasicConstraints(ca=True, path_length=None), True),
    (x509.KeyUsage(False, False, False, False, False, True, True, False, False), True),
    (ski(root_k.public_key()), False),
])
int_k = key()
int_n = name(C="US", O="Kara Test PKI", OU="Issuing", CN="Kara Issuing CA 2026")
inter = build(int_n, root_n, int_k.public_key(), root_k, 0x1000, T0, dt.datetime(2031, 1, 1, tzinfo=UTC), [
    (x509.BasicConstraints(ca=True, path_length=0), True),
    (x509.KeyUsage(True, False, False, False, False, True, True, False, False), True),
    (ski(int_k.public_key()), False),
    (aki(root_k.public_key()), False),
    (x509.CRLDistributionPoints([x509.DistributionPoint([x509.UniformResourceIdentifier("http://crl.kara.test/root.crl")], None, None, None)]), False),
])
srv_k = key()
srv = build(name(C="US", ST="California", L="San Francisco", O="Kara Shop", CN="shop.kara.test"), int_n,
            srv_k.public_key(), int_k, 0x0A1B2C3D4E5F60718293, dt.datetime(2026, 9, 1, 12, 0, tzinfo=UTC),
            dt.datetime(2026, 12, 1, 12, 0, tzinfo=UTC), [
    (x509.SubjectAlternativeName([x509.DNSName("shop.kara.test"), x509.DNSName("*.shop.kara.test"),
                                  x509.DNSName("kara.test"), x509.IPAddress(ipaddress.ip_address("192.0.2.10")),
                                  x509.IPAddress(ipaddress.ip_address("2001:db8::10"))]), False),
    (x509.BasicConstraints(ca=False, path_length=None), True),
    (x509.KeyUsage(True, False, True, False, False, False, False, False, False), True),
    (x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH, ExtendedKeyUsageOID.CLIENT_AUTH]), False),
    (ski(srv_k.public_key()), False),
    (aki(int_k.public_key()), False),
    (x509.AuthorityInformationAccess([
        x509.AccessDescription(AuthorityInformationAccessOID.OCSP, x509.UniformResourceIdentifier("http://ocsp.kara.test")),
        x509.AccessDescription(AuthorityInformationAccessOID.CA_ISSUERS, x509.UniformResourceIdentifier("http://pki.kara.test/issuing.crt"))]), False),
    (x509.CertificatePolicies([x509.PolicyInformation(x509.ObjectIdentifier("2.23.140.1.2.2"), None)]), False),
])
cli_k = key()
cli = build(name(O="Kara Shop", OU="Ops", CN="deploy-bot", emailAddress="bot@kara.test"), int_n,
            cli_k.public_key(), int_k, 0x7F, dt.datetime(2026, 2, 1, tzinfo=UTC), dt.datetime(2027, 2, 1, tzinfo=UTC), [
    (x509.SubjectAlternativeName([x509.RFC822Name("bot@kara.test"), x509.UniformResourceIdentifier("spiffe://kara.test/deploy")]), False),
    (x509.KeyUsage(True, False, False, False, False, False, False, False, False), True),
    (x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CLIENT_AUTH]), False),
    (aki(int_k.public_key()), False),
])
ec_k = ec.generate_private_key(ec.SECP256R1())
ecc = build(name(C="US", O="Kara Shop", CN="api.kara.test"), int_n, ec_k.public_key(), int_k, 0x0123456789,
            dt.datetime(2026, 9, 15, tzinfo=UTC), dt.datetime(2026, 12, 14, tzinfo=UTC), [
    (x509.SubjectAlternativeName([x509.DNSName("api.kara.test")]), False),
    (x509.KeyUsage(True, False, False, False, False, False, False, False, False), True),
    (x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), False),
    (aki(int_k.public_key()), False),
])
old_k = key()
old = build(name(C="US", O="Kara Shop", CN="old.kara.test"), int_n, old_k.public_key(), int_k, 0x42,
            dt.datetime(2026, 1, 1, tzinfo=UTC), dt.datetime(2026, 4, 1, tzinfo=UTC), [
    (x509.SubjectAlternativeName([x509.DNSName("old.kara.test")]), False),
    (aki(int_k.public_key()), False),
])
# a leaf that tries to act as a CA for another leaf
rogue_k = key()
rogue = build(name(O="Evil", CN="rogue.kara.test"), srv.subject, rogue_k.public_key(), srv_k, 0x666,
              dt.datetime(2026, 9, 2, tzinfo=UTC), dt.datetime(2026, 11, 1, tzinfo=UTC), [
    (x509.SubjectAlternativeName([x509.DNSName("rogue.kara.test")]), False),
])
# self-signed, with no extensions
ss_k = key(2048)
ss_n = name(CN="localhost")
ss = build(ss_n, ss_n, ss_k.public_key(), ss_k, 0x3039, dt.datetime(2025, 6, 1, tzinfo=UTC),
           dt.datetime(2035, 6, 1, tzinfo=UTC), [])
for n, c in [("root.pem", root), ("issuing.pem", inter), ("shop.pem", srv), ("client.pem", cli), ("api-ec.pem", ecc),
             ("old.pem", old), ("rogue.pem", rogue), ("localhost.pem", ss)]:
    open("data/" + n, "wb").write(pem(c))
open("data/shop.der", "wb").write(srv.public_bytes(serialization.Encoding.DER))
open("data/chain.pem", "wb").write(pem(srv) + pem(inter))
# one flipped bit in the signed part of shop's certificate
der = bytearray(srv.public_bytes(serialization.Encoding.DER))
at = der.index(b"San Francisco")
der[at] ^= 0x20
import base64
b = base64.encodebytes(bytes(der)).decode().replace("\n", "")
open("data/tampered.pem", "w").write("-----BEGIN CERTIFICATE-----\n" + "\n".join(b[i:i + 64] for i in range(0, len(b), 64)) + "\n-----END CERTIFICATE-----\n")
open("data/garbage.pem", "w").write("-----BEGIN CERTIFICATE-----\nnot base64 at all!!\n-----END CERTIFICATE-----\n")
open("data/notes.txt", "w").write("no certificate here\n")
shutil.copy("jobs.txt", "data/jobs.txt") if os.path.exists("jobs.txt") else None
