"""Write data/jobs.txt: the jobs mini_pydes and oracle.py both play.

A job is a title line and steps. Values are written as
  h:<hex>        bytes
  b:<text>       bytes from ASCII text, ~XX for byte XX
  s:<text>       a str, ~XX for the code point XX (so ~e9 is U+00E9)
  r:<n>:<hex>    bytes: the hex pattern repeated to n bytes
  n              None
  @              the result of the last enc or dec
Run: python3 -s -P -B mk.py"""
import os
import random

R = random.Random(20261024)
out = []


def job(title):
    out.append("job " + title)


def step(*parts):
    out.append(" ".join(parts))


def esc(text):
    s = ""
    for c in text:
        if c == " " or c == "~" or ord(c) < 33 or ord(c) > 126:
            s += "~%02x" % ord(c)
        else:
            s += c
    return s


def b(text):
    return "b:" + esc(text)


def h(data):
    return "h:" + data.hex()


def rand_bytes(n):
    return bytes(R.randrange(256) for _ in range(n))


WORDS = ("settlement batch terminal merchant acquirer issuer approved declined reversal "
         "refund amount currency track card holder expiry service code cryptogram").split()


def sentence(n):
    words = []
    while len(" ".join(words)) < n:
        words.append(R.choice(WORDS))
    return " ".join(words)[:n]


# ---------------------------------------------------------------- known answers

job("FIPS 81 and the classic DES vectors")
step("new k des key=h:0123456789abcdef")
step("enc k " + b("Now is the time for all "))
step("dec k @")
step("new c des key=h:0123456789abcdef mode=CBC iv=h:1234567890abcdef")
step("enc c " + b("Now is the time for all "))
step("dec c @")
step("new v des key=h:133457799bbcdff1")
step("enc v h:0123456789abcdef")
step("dec v @")

job("NIST SP 800-17 variable plaintext, key 0101010101010101")
step("new k des key=h:0101010101010101")
for i in range(0, 64, 4):
    step("enc k " + h((1 << (63 - i)).to_bytes(8, "big")))

job("NIST SP 800-17 variable key, plaintext zero")
for i in range(0, 56, 7):
    raw = bytearray(b"\x01" * 8)
    byte = i // 7
    raw[byte] = 0x80 >> (i % 7)
    step("new k des key=" + h(bytes(raw)))
    step("enc k h:0000000000000000")

job("The pyDes docstring example")
step("new k des key=s:DESCRYPT mode=CBC iv=b:~00~00~00~00~00~00~00~00 pad=n padmode=2")
step("enc k " + b("Please encrypt my data"))
step("dec k @")
step("dec k @ padmode=2")

job("Triple DES, three keys and two")
step("new t3 3des key=h:0123456789abcdef23456789abcdef01456789abcdef0123")
step("enc t3 " + b("The quick brown fox jump"))
step("dec t3 @")
step("new t2 3des key=h:0123456789abcdeffedcba9876543210")
step("enc t2 h:0123456789abcdef0123456789abcdef")
step("dec t2 @")
step("new same 3des key=h:0123456789abcdef0123456789abcdef")
step("enc same h:4e6f772069732074")
step("new single des key=h:0123456789abcdef")
step("enc single h:4e6f772069732074")

job("Triple DES CBC, with an IV and with the key's first half")
step("new a 3des key=h:0123456789abcdeffedcba9876543210 mode=CBC iv=h:0011223344556677 padmode=2")
step("enc a " + b("card 4111111111111111 exp 2612"))
step("dec a @")
step("get a iv")
step("new b 3des key=b:K1K1K1K1K2K2K2K2K3K3K3K3 mode=CBC padmode=2")
step("get b iv")
step("enc b " + b("approved 000123"))
step("dec b @")
step("new c 3des key=s:K1K1K1K1K2K2K2K2K3K3K3K3 mode=CBC padmode=2")
step("get c iv")
step("get c key")
step("enc c " + b("approved 000123"))

# ---------------------------------------------------------------- padding

job("PAD_NORMAL with a pad character")
step("new k des key=b:8bytekey pad=b:*")
step("enc k " + b("ABCDE"))
step("dec k @")
step("enc k " + b("ABCDE") + " pad=b:#")
step("dec k @ pad=b:#")
step("dec k @ pad=b:*")
step("enc k " + b("12345678"))
step("dec k @")

job("PAD_NORMAL strips real data that ends in the pad character")
step("new k des key=b:8bytekey pad=b:0")
step("enc k " + b("total 1000"))
step("dec k @")
step("enc k " + b("pad0pad00000"))
step("dec k @")
step("enc k " + b("x0000000"))
step("dec k @")
step("dec k @ pad=b:x0")

job("PAD_NORMAL with no pad character")
step("new k des key=b:8bytekey")
step("enc k " + b("short"))
step("enc k " + b("short") + " pad=b:~20")
step("dec k @")
step("dec k @ pad=b:~20")

job("A pad of more than one byte")
step("new k des key=b:8bytekey")
step("enc k " + b("abc") + " pad=b:xy")
step("new p des key=b:8bytekey pad=b:.")
step("enc p " + b("abc") + " pad=b:xy")
step("dec p @ pad=b:xy")
step("enc p " + b("abcdefg") + " pad=b:xy")
step("dec p @")

job("PAD_PKCS5")
step("new k des key=b:pkcs5key padmode=2")
for n in (0, 1, 7, 8, 9, 15, 16):
    step("enc k r:%d:41" % n)
    step("dec k @")
step("enc k " + b("tail") + " pad=b:*")
step("dec k h:0000000000000000 pad=b:*")

job("PAD_PKCS5 decryption under the wrong key")
step("new k des key=b:rightkey padmode=2")
step("new w des key=b:wrongkey padmode=2")
step("enc k " + b("a message of thirty-one bytes!!"))
step("dec w @")
step("enc k " + b("abc"))
step("dec w @")
step("enc k " + b("abcdefghijklmnopqrstuvwxyz"))
step("dec w @")

job("Padding mode per call")
step("new k des key=b:callmode")
step("enc k " + b("hello") + " padmode=2")
step("dec k @")
step("dec k @ padmode=2")
step("dec k @ padmode=1 pad=b:~03")
step("enc k " + b("hello") + " padmode=1 pad=b:!")
step("dec k @ padmode=1")

# ---------------------------------------------------------------- empty data

job("Empty data")
step("new d des key=b:emptykey")
step("enc d b:")
step("dec d b:")
step("dec d @")
step("new e des key=b:emptykey padmode=2")
step("enc e b:")
step("dec e @")
step("new t 3des key=h:0123456789abcdeffedcba9876543210")
step("enc t b:")
step("dec t b:")
step("new tc 3des key=h:0123456789abcdeffedcba9876543210 mode=CBC")
step("enc tc b:")
step("dec tc b:")
step("new dc des key=b:emptykey mode=CBC")
step("enc dc b:")

# ---------------------------------------------------------------- errors

job("Key and IV checks")
step("new a des key=b:7bytes!")
step("new a des key=b:9bytes!!!")
step("new a des key=b:")
step("new a 3des key=b:8bytekey")
step("new a 3des key=b:17bytekey17bytek!")
step("new a 3des key=r:32:00")
step("new a des key=b:8bytekey mode=CBC iv=b:short")
step("new a des key=b:8bytekey mode=CBC iv=b:")
step("new a des key=b:8bytekey pad=b:* padmode=2")
step("new a 3des key=r:16:01 pad=b:* padmode=2")
step("new a 3des key=r:16:01 mode=CBC iv=b:9bytes!!!")
step("new a des key=b:8bytekey mode=ECB iv=b:12345678")
step("get a mode")
step("get a iv")

job("CBC without an IV")
step("new k des key=b:8bytekey mode=CBC")
step("enc k b:12345678")
step("enc k b:1234567")
step("set k iv b:12345678")
step("enc k b:12345678")
step("dec k @")

job("Lengths that are not a multiple of 8")
step("new k des key=b:8bytekey")
step("dec k b:1234567")
step("dec k b:123456789")
step("enc k b:123456789")
step("new t 3des key=r:24:5a mode=CBC")
step("dec t b:123456789")
step("new e 3des key=r:24:5a")
step("dec e b:12345")

job("Unicode arguments")
step("new k des key=s:asciikey")
step("get k key")
step("enc k s:plain~20text")
step("dec k @")
step("enc k s:caf~e9")
step("new u des key=s:k~e9y~e9~e9~e9~e9~e9")
step("new u des key=s:k~e9y")
step("new p des key=b:8bytekey pad=s:~e9")
step("new q des key=b:8bytekey pad=s:*")
step("enc q b:abc")
step("dec q @")
step("enc q b:abc pad=s:~2b")
step("dec q @ pad=s:+")

# ---------------------------------------------------------------- setters

job("Setters and getters")
step("new k des key=b:firstkey mode=CBC iv=b:initvect padmode=2")
step("get k key")
step("get k mode")
step("get k iv")
step("get k pad")
step("get k padmode")
step("enc k " + b("rotate me"))
step("set k key b:secondky")
step("get k key")
step("enc k " + b("rotate me"))
step("set k iv b:othervec")
step("enc k " + b("rotate me"))
step("set k iv b:bad")
step("set k iv n")
step("set k mode ECB")
step("enc k " + b("rotate me"))
step("set k padmode 1")
step("enc k " + b("rotate me"))
step("set k pad b:_")
step("enc k " + b("rotate me"))
step("dec k @")
step("set k pad n")
step("get k pad")
step("set k pad s:~e9")

job("Triple DES setters")
step("new t 3des key=h:0123456789abcdeffedcba9876543210")
step("enc t " + b("ECB first"))
step("set t mode CBC")
step("enc t " + b("ECB first"))
step("set t iv b:12345678")
step("enc t " + b("ECB first") + " pad=b:~00")
step("dec t @ pad=b:~00")
step("set t key h:89abcdef01234567fedcba9876543210")
step("get t iv")
step("enc t " + b("ECB first") + " pad=b:~00")
step("set t padmode 2")
step("enc t " + b("ECB first"))
step("dec t @")
step("set t pad b:*")
step("set t padmode 1")
step("set t pad b:*")
step("enc t " + b("ECB first"))
step("dec t @")
step("set t key b:short")
step("set t iv b:1234")

# ---------------------------------------------------------------- payment tools

job("Key check values")
for key in ("0123456789abcdeffedcba9876543210", "0123456789abcdef0123456789abcdef",
            "c8a7f2e1d0b3a4958677c8f9e0d1b2a3", "0123456789abcdeffedcba987654321089abcdef01234567",
            "1111111111111111", "0000000000000000"):
    step("kcv h:" + key)
step("kcv b:shortkey!")

PANS = ["4111111111111111", "5500005555555559", "340000000000009", "6011000990139424",
        "4012888888881881", "3530111333300000", "4000056655665556", "5105105105105100"]
PINS = ["1234", "0000", "987654", "4321", "123456789012", "55", "7777", "135790"]

job("ISO 9564 format 0 PIN blocks under a zone PIN key")
for pan, pin in zip(PANS, PINS):
    step("pin h:0123456789abcdeffedcba9876543210 " + pan + " " + pin)

job("PIN translation from one zone key to another")
for pan, pin in zip(PANS[:4], PINS[:4]):
    step("translate h:0123456789abcdeffedcba9876543210 h:c8a7f2e1d0b3a4958677c8f9e0d1b2a3 " + pan + " " + pin)

job("ANSI X9.19 retail MAC")
MAC_KEY = "0123456789abcdeffedcba9876543210"
for text in ("4E6F77206973207468652074696D6520666F7220616C6C20",
             "", "00", "0102030405060708", "0102030405060708090a"):
    step("mac h:" + MAC_KEY + " h:" + text)
for n in (12, 40, 77):
    step("mac h:" + MAC_KEY + " " + b(sentence(n)))
step("mac h:0123456789abcdef " + b("single length"))

# ---------------------------------------------------------------- bulk

job("A settlement file, Triple DES CBC with PKCS5")
lines = []
for i in range(24):
    lines.append("%04d,%s,%d.%02d" % (i + 1, R.choice(PANS)[-4:], R.randrange(1, 5000), R.randrange(100)))
text = "\n".join(lines) + "\n"
step("new f 3des key=h:0123456789abcdef23456789abcdef01456789abcdef0123 mode=CBC iv=h:a1b2c3d4e5f60718 padmode=2")
step("sum f " + b(text))
step("dec f @")

job("Round trips")
modes = [("des key=b:roundkey", ""), ("des key=b:roundkey mode=CBC iv=b:rounviv!", ""),
         ("3des key=b:roundkeyroundkey mode=CBC", ""), ("3des key=b:roundkeyroundkeyroundkey", "")]
for i, (spec, _) in enumerate(modes):
    step("new m%d %s padmode=2" % (i, spec))
for _ in range(16):
    i = R.randrange(4)
    step("roundtrip m%d %s" % (i, h(rand_bytes(R.randrange(0, 30)))))

job("A long record under single DES, ECB")
step("new k des key=b:longrecs pad=b:~20")
step("sum k " + b(sentence(300)))
step("dec k @")

os.makedirs("data", exist_ok=True)
with open("data/jobs.txt", "w") as f:
    f.write("\n".join(out) + "\n")
print(len(out), "lines")
