# Writes data/ for mini_cbor: CBOR files as real systems produce them,
# the test vectors from cbor2's own test suite, and the command lines
# the tool runs.
import base64
import hashlib
import os
import sys
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from fractions import Fraction
from ipaddress import ip_address, ip_network
from uuid import UUID

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cbor2  # noqa: E402
from cbor2 import CBORSimpleValue, CBORTag, undefined  # noqa: E402

DATA = os.path.join(HERE, "data")


def pattern(seed, n):
    out = bytearray()
    x = seed
    while len(out) < n:
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
        out.append((x >> 16) & 0xFF)
    return bytes(out)


def cose_key(seed):
    # an EC2 P-256 public key: kty, alg, crv, x, y
    return cbor2.dumps({1: 2, 3: -7, -1: 1, -2: pattern(seed, 32), -3: pattern(seed + 1, 32)})


def auth_data(rp_id, flags, count, cred_seed):
    out = hashlib.sha256(rp_id.encode()).digest()
    out += bytes([flags]) + count.to_bytes(4, "big")
    if flags & 0x40:
        cred_id = pattern(cred_seed, 32)
        out += bytes(16) + len(cred_id).to_bytes(2, "big") + cred_id
        out += cose_key(cred_seed + 7)
    return out


def files():
    out = {}
    # WebAuthn registration responses: the attestation object
    out["webauthn_none.cbor"] = cbor2.dumps(
        {"fmt": "none", "attStmt": {}, "authData": auth_data("login.example.com", 0x45, 0, 11)}
    )
    out["webauthn_packed.cbor"] = cbor2.dumps(
        {
            "fmt": "packed",
            "attStmt": {
                "alg": -7,
                "sig": b"\x30\x45\x02\x21\x00" + pattern(21, 32) + b"\x02\x20" + pattern(22, 32),
                "x5c": [b"\x30\x82\x01\x3a\x30\x81\xe1\xa0\x03\x02\x01\x02" + pattern(23, 40)],
            },
            "authData": auth_data("example.org", 0x45, 7, 31),
        }
    )
    # an authenticator assertion: authData without credential data
    out["webauthn_assertion_authdata.cbor"] = cbor2.dumps(auth_data("example.org", 0x05, 8, 0))
    # a COSE key on its own, and a key set
    out["cose_key.cbor"] = cose_key(41)
    out["cose_keyset.cbor"] = cbor2.dumps(
        [cbor2.loads(cose_key(51)), {1: 1, -1: 6, -2: pattern(52, 32), 2: b"11"}, {1: 4, -1: pattern(53, 16), 2: b"our-secret"}]
    )
    # a CWT (RFC 8392): tag 61 around a COSE_Sign1 (tag 18)
    claims = {
        1: "coap://as.example.com",
        2: "erikw",
        3: "coap://light.example.com",
        4: 1444064944,
        5: 1443944944,
        6: 1443944944,
        7: b"\x0b\x71",
    }
    sign1 = [cbor2.dumps({1: -7}), {4: b"AsymmetricECDSA256"}, cbor2.dumps(claims), pattern(61, 64)]
    out["cwt.cbor"] = cbor2.dumps(CBORTag(61, CBORTag(18, sign1)))
    # SenML (RFC 8428) with CBOR labels, as a sensor gateway sends it
    senml = [
        {-2: "urn:dev:ow:10e2073a01080063:", -3: 1276020076.001, -4: "A", -1: 120.1, 0: "voltage", 1: "V", 2: 0.0},
        {0: "current", 6: -5, 2: 1.2},
        {0: "current", 6: -4, 2: 1.3},
        {0: "current", 6: -3, 2: 1.4},
        {0: "current", 6: -2, 2: 1.5},
        {0: "door", 4: True},
        {0: "label", 3: "Living room"},
    ]
    out["senml.cbor"] = cbor2.dumps(senml, canonical=True)
    # a CBOR sequence (RFC 8742) of telemetry readings from a device log
    seq = b""
    for i in range(4):
        seq += cbor2.dumps({"seq": i, "t": 1760000000 + 60 * i, "temp": [21.5, 21.75, 22.0, 22.25][i], "ok": i != 2})
    seq += bytes.fromhex("bf63736571046174") + cbor2.dumps(1760000240) + bytes.fromhex("6474656d709ff93c00f94000ff626f6bf5ff")
    out["telemetry.cborseq"] = seq
    # values with semantic tags, as an IoT inventory service stores them
    inv = {
        "device": UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8"),
        "addr": ip_address("192.0.2.17"),
        "addr6": ip_address("2001:db8::1:0:0:1"),
        "mapped": ip_address("::ffff:198.51.100.7"),
        "mac": CBORTag(260, bytes.fromhex("0023dfa1b2c3")),
        "subnet": ip_network("192.0.2.0/24"),
        "subnet6": ip_network("2001:db8:1200::/40"),
        "seen": datetime(2026, 10, 3, 8, 15, 30, 250000, tzinfo=timezone(timedelta(hours=5, minutes=30))),
        "installed": date(2024, 2, 29),
        "price": Decimal("1299.95"),
        "ratio": Fraction(3, 8),
        "serial": 2**70 + 12345,
        "debt": -(2**65),
        "ports": {22, 80, 443},
        "nothing": None,
        "unset": undefined,
        "flag": CBORSimpleValue(99),
    }
    out["inventory.cbor"] = cbor2.dumps(inv, datetime_as_timestamp=False)
    out["inventory_timestamps.cbor"] = cbor2.dumps(
        {"seen": inv["seen"], "installed": inv["installed"], "boot": datetime(2026, 10, 1, 0, 0, tzinfo=timezone.utc)},
        datetime_as_timestamp=True,
    )
    # shared values and string references as a cache writes them
    tags = ["blue", "green", "blue", "green", "green"]
    shared = {"name": "pump-7", "tags": tags}
    out["shared.cbor"] = cbor2.dumps([shared, shared, {"name": "pump-8", "tags": tags}], value_sharing=True)
    out["stringref.cbor"] = cbor2.dumps(
        [{"name": "pump-7", "status": "running"}, {"name": "pump-8", "status": "running"}, {"name": "valve-2", "status": "stopped"}],
        string_referencing=True,
    )
    loop = []
    loop.append(loop)
    loop.append({"self": loop})
    out["cycle.cbor"] = cbor2.dumps(loop, value_sharing=True)
    # keys Python treats as equal, and keys that must be hashable
    out["keys.cbor"] = bytes.fromhex("a501616101fb3ff0000000000000616bf56163") + cbor2.dumps([1, 2]) + b"\x61t" + bytes.fromhex("a10102") + b"\x61f"
    # embedded CBOR (tag 24) and the self-describe tag, as the tool sees them
    out["embedded.cbor"] = cbor2.dumps(CBORTag(55799, {"payload": CBORTag(24, cbor2.dumps({"id": 7, "v": [1.5, None]})), "note": CBORTag(1000, "kept")}))
    # bigfloats and decimal fractions
    out["numbers.cbor"] = cbor2.dumps(
        [
            CBORTag(5, [-1, 3]),
            CBORTag(5, [-3, 7]),
            CBORTag(5, [4, 3]),
            CBORTag(5, [-40, 12345]),
            CBORTag(5, [100, 1]),
            CBORTag(4, [-2, 27315]),
            CBORTag(4, [3, -5]),
            CBORTag(4, [-30, 2**80]),
            CBORTag(30, [10, -4]),
            CBORTag(30, [-6, 9]),
            CBORTag(1, 1760000000.5),
            CBORTag(1, -1.25),
            CBORTag(100, -1),
            CBORTag(1004, "2026-W41-5"),
            CBORTag(1004, "20261009"),
            CBORTag(0, "2026-10-09T12:00:00.1234567-07:00"),
        ]
    )
    # broken files a decoder meets in practice
    good = out["webauthn_none.cbor"]
    out["broken/truncated.cbor"] = good[:100]
    out["broken/bad_utf8.cbor"] = bytes.fromhex("a1636b6579") + b"\x63\xe2\x28\xa1"
    out["broken/reserved.cbor"] = bytes.fromhex("82011c")
    out["broken/stringref_outside.cbor"] = bytes.fromhex("83d81900d81901d81902")
    out["broken/bad_uuid.cbor"] = cbor2.dumps(CBORTag(37, b"short"))
    out["broken/bad_bignum.cbor"] = cbor2.dumps(CBORTag(2, "123"))
    out["broken/leap_second.cbor"] = cbor2.dumps(CBORTag(0, "2026-10-09T23:59:60Z"))
    out["broken/empty_bignum.cbor"] = cbor2.dumps(CBORTag(2, b""))
    out["broken/bad_date.cbor"] = cbor2.dumps(CBORTag(1004, "2026-02-30"))
    out["broken/unhashable.cbor"] = bytes.fromhex("d81c81a1d81d0001")
    out["broken/empty.cbor"] = b""
    out["broken/simple24.cbor"] = bytes.fromhex("f818")
    return out


def vectors():
    # hex payloads from cbor2 5.6.5's tests (tests/test_*.py), in order,
    # without the regular-expression and MIME tags (35 and 36)
    with open(os.path.join(HERE, "vectors.txt"), encoding="utf-8") as f:
        return [l for l in f.read().split("\n") if l]


def jobs():
    return [
        "tool webauthn_none.cbor",
        "tool -p webauthn_packed.cbor",
        "tool cose_key.cbor cose_keyset.cbor",
        "tool -k cose_key.cbor",
        "tool cwt.cbor",
        "tool -i 61,18 cwt.cbor",
        "tool -p senml.cbor",
        "tool -k senml.cbor",
        "tool -s telemetry.cborseq",
        "tool telemetry.cborseq",
        "tool -p -k inventory_timestamps.cbor",
        "tool embedded.cbor",
        "tool -i 55799 -p embedded.cbor",
        "tool shared.cbor",
        "tool stringref.cbor",
        "tool cycle.cbor",
        "tool keys.cbor",
        "tool -k keys.cbor",
        "tool -d examples.cbor.b64",
        "tool -d -k -p examples.cbor.b64",
        "tool broken/truncated.cbor",
        "tool -s broken/truncated.cbor",
        "tool broken/bad_utf8.cbor",
        "tool broken/empty.cbor",
        "tool -s broken/empty.cbor",
    ]


def main():
    for rel, body in files().items():
        path = os.path.join(DATA, "files", rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(body)
    with open(os.path.join(HERE, "examples.cbor.b64"), "rb") as f:
        b64 = f.read()
    with open(os.path.join(DATA, "files", "examples.cbor.b64"), "wb") as f:
        f.write(b64)
    names = sorted(files()) + ["examples.cbor.b64"]
    with open(os.path.join(DATA, "files.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(n for n in names if not n.endswith(".b64")) + "\n")
    with open(os.path.join(DATA, "vectors.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(vectors()) + "\n")
    with open(os.path.join(DATA, "jobs.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(jobs()) + "\n")


if __name__ == "__main__":
    main()
