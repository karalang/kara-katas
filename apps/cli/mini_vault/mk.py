#!/usr/bin/env python3
"""Writes data/: two files to encrypt and data/jobs.tsv, the jobs
mini_vault runs. Ciphertexts and tokens that the open jobs read are made
here with Python's cryptography library, some of them damaged on purpose."""
import base64
import hashlib
import hmac
import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.fernet import Fernet

os.makedirs("data", exist_ok=True)
for name in os.listdir("data"):
    os.remove("data/" + name)

ENV = """# production settings for the billing service
DATABASE_URL=postgres://billing:s3cr3t@db.internal:5432/billing
STRIPE_KEY=demo-stripe-key-0000-not-real
SESSION_SECRET=9f1c2a7e4b3d8f60a5e2c1b7d9f3a4e6
SMTP_PASSWORD=correct horse battery staple
FEATURE_FLAGS=new-checkout,dark-mode
"""
NOTES = "Rotate the Stripe key on 1 March.\nOn-call: Grace (week 9), Linus (week 10).\nÜbergabe: Schlüssel im Tresor.\n"
with open("data/app.env", "w") as f:
    f.write(ENV)
with open("data/notes.txt", "w") as f:
    f.write(NOTES)

J = []


def job(*f):
    J.append("\t".join(f))


def x(b):
    return "x:" + b.hex() if b else "-"


# SHA-256 and HMAC: the FIPS examples, the padding boundaries, RFC 4231.
for d in [b"", b"abc", b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
          b"a" * 55, b"a" * 56, b"a" * 63, b"a" * 64, b"a" * 65, bytes(range(256)) * 4]:
    job("sha256", x(d))
job("sha256", "f:app.env")
job("sha256", "t:The quick brown fox jumps over the lazy dog")
for key, data in [(b"\x0b" * 20, b"Hi There"), (b"Jefe", b"what do ya want for nothing?"),
                  (b"\xaa" * 20, b"\xdd" * 50), (bytes(range(1, 26)), b"\xcd" * 50),
                  (b"\xaa" * 131, b"Test Using Larger Than Block-Size Key - Hash Key First"),
                  (b"\xaa" * 131, b"This is a test using a larger than block-size key and a larger than block-size data. The key needs to be hashed before being used by the HMAC algorithm."),
                  (b"\x01" * 64, b"exactly one block of key"), (b"", b"")]:
    job("hmac", x(key), x(data))

# PBKDF2-HMAC-SHA256 and HKDF (RFC 5869).
for pw, salt, it, n in [(b"password", b"salt", 1, 32), (b"password", b"salt", 2, 32),
                        (b"password", b"salt", 64, 32),
                        (b"passwordPASSWORDpassword", b"saltSALTsaltSALTsaltSALTsaltSALTsalt", 25, 40),
                        (b"pass\x00word", b"sa\x00lt", 30, 16), (b"hunter2", b"", 3, 64),
                        (b"x" * 100, b"pepper", 10, 100)]:
    job("pbkdf2", x(pw), x(salt), str(it), str(n))
job("hkdf", x(b"\x0b" * 22), x(bytes(range(13))), x(bytes(range(0xf0, 0xfa))), "42")
job("hkdf", x(bytes(range(80))), x(bytes(range(0x60, 0xb0))), x(bytes(range(0xb0, 0x100))), "82")
job("hkdf", x(b"\x0b" * 22), "-", "-", "42")
job("hkdf", "t:session secret", "t:billing", "t:cookie-signing-key", "32")

# AES: FIPS-197 blocks, SP 800-38A CBC and CTR.
PT = bytes.fromhex("00112233445566778899aabbccddeeff")
for key in [bytes(range(16)), bytes(range(24)), bytes(range(32))]:
    job("aes-ecb", x(key), x(PT))
job("aes-ecb", x(bytes(10)), x(PT))
job("aes-ecb", x(bytes(16)), x(b"short"))
K128 = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
K256 = bytes.fromhex("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4")
SP = bytes.fromhex("6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e51"
                   "30c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c3710")
IV = bytes(range(16))
job("aes-cbc", x(K128), x(IV), x(SP))
job("aes-cbc", x(K256), x(IV), x(SP))
job("aes-cbc", x(K128), x(IV[:8]), x(SP))
CTR = bytes.fromhex("f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")
job("aes-ctr", x(K128), x(CTR), x(SP))
job("aes-ctr", x(K256), x(CTR), x(SP[:37]))
job("aes-ctr", x(K128), x(b"\xff" * 16), x(SP[:40]))

# AES-GCM: the GCM spec's test cases, nonces other than 96 bits, opening
# good and damaged messages.
GK = bytes.fromhex("feffe9928665731c6d6a8f9467308308")
GP = bytes.fromhex("d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a72"
                   "1c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b39")
GA = bytes.fromhex("feedfacedeadbeeffeedfacedeadbeefabaddad2")
GN = bytes.fromhex("cafebabefacedbaddecaf888")
job("gcm-seal", x(bytes(16)), x(bytes(12)), "-", "-")
job("gcm-seal", x(bytes(16)), x(bytes(12)), "-", x(bytes(16)))
job("gcm-seal", x(GK), x(GN), "-", x(GP + bytes.fromhex("b16aedf5aa0de657ba637b391aafd255")))
job("gcm-seal", x(GK), x(GN), x(GA), x(GP))
job("gcm-seal", x(GK), x(GN[:8]), x(GA), x(GP))
job("gcm-seal", x(GK), x(bytes.fromhex("9313225df88406e555909c5aff5269aa6a7a9538534f7da1e4c303d2a318a728"
                                       "c3c0c95156809539fcf0e2429a6b525416aedbf5a0de6a57a637b39b")), x(GA), x(GP))
job("gcm-seal", x(GK + GK), x(GN), x(GA), x(GP))
job("gcm-seal", x(GK[:12] * 2), x(GN), "t:header", "t:twenty-four byte key")
job("gcm-seal", x(GK), x(GN), "t:only authenticated", "-")
job("gcm-seal", x(bytes(16)), x(bytes(7)), "-", "t:x")
job("gcm-seal", x(bytes(20)), x(bytes(12)), "-", "t:x")
key = bytes(range(100, 132))
nonce = bytes(range(12))
ct = AESGCM(key).encrypt(nonce, ENV.encode(), b"app.env")
job("gcm-open", x(key), x(nonce), "t:app.env", x(ct))
job("gcm-open", x(key), x(nonce), "t:app.env2", x(ct))
bad = bytearray(ct)
bad[5] ^= 0x20
job("gcm-open", x(key), x(nonce), "t:app.env", x(bytes(bad)))
bad = bytearray(ct)
bad[-1] ^= 1
job("gcm-open", x(key), x(nonce), "t:app.env", x(bytes(bad)))
job("gcm-open", x(key), x(nonce), "t:app.env", x(ct[:10]))
job("gcm-open", x(key), x(bytes(range(1, 13))), "t:app.env", x(ct))
long_nonce = bytes(range(60))
ct = AESGCM(key[:16]).encrypt(long_nonce, NOTES.encode(), None)
job("gcm-open", x(key[:16]), x(long_nonce), "-", x(ct))

# ChaCha20-Poly1305: RFC 8439's example, the empty message, damage.
CK = bytes(range(0x80, 0xa0))
CN = bytes.fromhex("070000004041424344454647")
CA = bytes.fromhex("50515253c0c1c2c3c4c5c6c7")
CP = b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it."
job("chacha-seal", x(CK), x(CN), x(CA), x(CP))
job("chacha-seal", x(bytes(32)), x(bytes(12)), "-", "-")
job("chacha-seal", x(bytes(32)), x(bytes(12)), "-", x(bytes(64)))
job("chacha-seal", x(CK), x(CN), "t:notes.txt", "f:notes.txt")
job("chacha-seal", x(bytes(16)), x(CN), "-", "t:x")
job("chacha-seal", x(CK), x(CN[:8]), "-", "t:x")
ct = ChaCha20Poly1305(CK).encrypt(CN, CP, CA)
job("chacha-open", x(CK), x(CN), x(CA), x(ct))
bad = bytearray(ct)
bad[0] ^= 0x80
job("chacha-open", x(CK), x(CN), x(CA), x(bytes(bad)))
job("chacha-open", x(CK), x(CN), "-", x(ct))
ct = ChaCha20Poly1305(CK).encrypt(CN, b"\xff\xfe binary \x00", None)
job("chacha-open", x(CK), x(CN), "-", x(ct))

# Fernet: the spec's token, opening fresh, expired, early and damaged
# tokens, keys that are not keys, and a key rotation with MultiFernet.
FK = "cw_0x689RpI-jtRR7oE8h_eQsKImvJapLeSbXpwF4e4="
FK2 = base64.urlsafe_b64encode(bytes(range(32))).decode()
job("fernet-seal", FK, "499162800", x(bytes(range(16))), "t:hello")
job("fernet-seal", FK2, "1700000000", x(bytes(range(16, 32))), "f:app.env")
job("fernet-seal", FK2, "1700000000", x(bytes(16)), "-")
job("fernet-seal", FK2, "1700000000", x(bytes(16)), x(b"sixteen bytes!!!"))
job("fernet-seal", "not-a-key", "0", x(bytes(16)), "t:x")
job("fernet-seal", base64.urlsafe_b64encode(bytes(31)).decode(), "0", x(bytes(16)), "t:x")
f2 = Fernet(FK2.encode())
tok = f2._encrypt_from_parts(NOTES.encode(), 1700000000, bytes(range(32, 48))).decode()
job("fernet-open", FK2, tok, "60", "1700000030")
job("fernet-open", FK2, tok, "60", "1700000060")
job("fernet-open", FK2, tok, "60", "1700000061")
job("fernet-open", FK2, tok, "3600", "1699999941")
job("fernet-open", FK2, tok, "3600", "1699999939")
job("fernet-open", FK, tok, "60", "1700000000")
job("fernet-open", FK2, tok.rstrip("="), "60", "1700000000")
job("fernet-open", FK2, tok[:20] + "!!" + tok[20:], "60", "1700000000")
job("fernet-open", FK2, tok[:-6] + "AAAA==", "60", "1700000000")
raw = bytearray(base64.urlsafe_b64decode(tok))
raw[0] = 0x81
job("fernet-open", FK2, base64.urlsafe_b64encode(bytes(raw)).decode(), "60", "1700000000")
job("fernet-open", FK2, base64.urlsafe_b64encode(b"\x80\x00\x00").decode(), "60", "0")
job("fernet-open", FK2, "", "60", "0")
job("fernet-open", FK2, "gAAAAA=", "60", "0")
# A token whose MAC is right but whose padding is not.
sk, ek = bytes(range(16)), bytes(range(16, 32))
e = Cipher(algorithms.AES(ek), modes.CBC(bytes(16))).encryptor()
body = b"\x80" + (1700000000).to_bytes(8, "big") + bytes(16) + e.update(b"bad padding!!!\x05\x03") + e.finalize()
mac = hmac.new(sk, body, hashlib.sha256).digest()
job("fernet-open", FK2, base64.urlsafe_b64encode(body + mac).decode(), "60", "1700000000")
FK3 = base64.urlsafe_b64encode(hashlib.sha256(b"next key").digest()).decode()
job("fernet-multi", FK3 + "," + FK2, tok, "60", "1700000000")
job("fernet-multi", FK3, tok, "60", "1700000000")

# The vault: a passphrase-protected store of secrets, kept in a file
# between jobs.
P = "t:correct horse battery staple"
job("vault-init", "team.vault", P, x(b"vault salt 0001"), "16", x(bytes(range(12))))
job("vault-list", "team.vault")
job("vault-put", "team.vault", P, "stripe", "t:demo-stripe-key-0000-not-real", x(bytes(range(1, 13))))
job("vault-put", "team.vault", P, "db", "t:postgres://billing:s3cr3t@db.internal:5432/billing", x(bytes(range(2, 14))))
job("vault-put", "team.vault", P, "env", "f:app.env", x(bytes(range(3, 15))))
job("vault-put", "team.vault", "t:Correct horse battery staple", "smtp", "t:x", x(bytes(12)))
job("vault-list", "team.vault")
job("vault-get", "team.vault", P, "db")
job("vault-get", "team.vault", P, "env")
job("vault-get", "team.vault", P, "missing")
job("vault-get", "team.vault", "t:wrong", "db")
job("vault-put", "team.vault", P, "db", "t:postgres://billing:n3w-s3cr3t@db2.internal/billing", x(bytes(range(4, 16))))
job("vault-put", "team.vault", P, "notes", "f:notes.txt", x(bytes(range(5, 17))))
job("vault-put", "team.vault", P, "hsm-pin", x(bytes([0, 1, 2, 250, 255])), x(bytes(range(6, 18))))
job("vault-get", "team.vault", P, "db")
job("vault-get", "team.vault", P, "notes")
job("vault-get", "team.vault", P, "hsm-pin")
job("vault-cat", "team.vault")
job("vault-flip", "team.vault", "stripe", "3")
job("vault-get", "team.vault", P, "stripe")
job("vault-rekey", "team.vault", P, "t:new passphrase", x(b"salt 0002"), "12", "t:seed")
job("vault-flip", "team.vault", "stripe", "3")
job("vault-rekey", "team.vault", P, "t:new passphrase", x(b"salt 0002"), "12", "t:seed")
job("vault-del", "team.vault", "t:new passphrase", "stripe")
job("vault-get", "team.vault", P, "db")
job("vault-rekey", "team.vault", P, "t:new passphrase", x(b"salt 0002"), "12", "t:seed")
job("vault-del", "team.vault", "t:new passphrase", "stripe")
job("vault-rekey", "team.vault", "t:new passphrase", "t:third", x(b"salt 0003"), "10", "t:seed 3")
job("vault-list", "team.vault")
job("vault-get", "team.vault", "t:third", "hsm-pin")
job("vault-cat", "team.vault")
job("vault-list", "missing.vault")
with open("data/jobs.tsv", "w") as f:
    f.write("\n".join(J) + "\n")
