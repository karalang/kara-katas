"""Write data/: the job script (data/jobs.tsv, one Python statement a
line), the htpasswd, htdigest and CryptContext files the jobs read, and
data/files.txt listing them for gen_kara.py.

Reference hashes in the jobs are computed here with the vendored
passlib and fixed salts. Run from this directory: python3 -s -P -B mk.py
"""
import os
import shutil
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["PASSLIB_BUILTIN_BCRYPT"] = "enabled"
sys.path.insert(0, os.path.join(HERE, "vendor"))
warnings.simplefilter("ignore")

import passlib.hash as ph  # noqa: E402

for _name in ("bcrypt", "bcrypt_sha256"):
    getattr(ph, _name).set_backend("builtin")
ph.scrypt.set_backend("builtin")

D = os.path.join(HERE, "data")
FILES = {}
JOBS = []


def job(*lines):
    JOBS.extend(lines)


def section(title):
    JOBS.append("# " + title)


def mk(scheme, pw, **settings):
    """A reference hash, as `scheme.using(**settings).hash(pw)`."""
    return getattr(ph, scheme).using(**settings).hash(pw)


def q(s):
    return repr(s)


# ---------------------------------------------------------------- data files

MD5 = "$1$saltsalt$qjXMvbEw8oaL.CzflDtaK/"
APR = mk("apr_md5_crypt", "apache", salt="Xr4ilOzQ")
SHA256 = mk("sha256_crypt", "password", rounds=1000, salt="saltsalt")
SHA512 = mk("sha512_crypt", "password", rounds=1000, salt="saltsalt")
DES = mk("des_crypt", "password", salt="ab")
SHA1_LDAP = ph.ldap_sha1.hash("secret")
BCRYPT = mk("bcrypt", "password", rounds=4, salt="abcdefghijklmnopqrstuu")
BSHA = mk("bcrypt_sha256", "password", rounds=4, salt="abcdefghijklmnopqrstuu")

FILES["htpasswd"] = (
    "# web users\n"
    "alice:" + SHA1_LDAP + "\n"
    "bob:hunter2\n"
    "\n"
    "carol:" + mk("des_crypt", "letmein", salt="cr") + "\n"
    "dave:" + APR + "\n"
    "# retired\n"
    "erin:" + mk("ldap_salted_sha1", "s3cret", salt=b"NaCl") + "\n"
)
FILES["bad.htpasswd"] = "alice:x\nbob:y\ncarol\n"
FILES["dup.htpasswd"] = "alice:{SHA}abc=\nbob:pw\nalice:other\n"
FILES["legacy.htpasswd"] = (
    "admin:" + mk("des_crypt", "admin123", salt="ad") + "\n"
    "ops:" + ph.ldap_sha1.hash("opsops") + "\n"
    "guest:guest\n"
    "web:" + mk("ldap_salted_sha1", "webweb", salt=b"pepper") + "\n"
)
FILES["htdigest"] = (
    "alice:Restricted:" + ph.htdigest.hash("secret", "alice", "Restricted") + "\n"
    "bob:Restricted:" + ph.htdigest.hash("hunter2", "bob", "Restricted") + "\n"
    "alice:Admin:" + ph.htdigest.hash("root", "alice", "Admin") + "\n"
)
FILES["app.ini"] = (
    "[passlib]\n"
    "schemes = pbkdf2_sha256, ldap_salted_sha1, des_crypt\n"
    "deprecated = auto\n"
    "pbkdf2_sha256__default_rounds = 20\n"
    "pbkdf2_sha256__min_rounds = 10\n"
    "admin__pbkdf2_sha256__default_rounds = 40\n"
    "admin__pbkdf2_sha256__min_rounds = 30\n"
    "\n"
    "[other]\n"
    "schemes = md5_crypt\n"
)
FILES["migrate.ini"] = (
    "[passlib]\n"
    "schemes = pbkdf2_sha256, ldap_salted_sha1, ldap_sha1, des_crypt, plaintext\n"
    "deprecated = auto\n"
    "pbkdf2_sha256__default_rounds = 20\n"
)
FILES["bad.ini"] = "[passlib]\nschemes = md5_crypt\nbogus__x__y__z = 1\n"

# ---------------------------------------------------------------- jobs

section("hex digests")
job(
    "hex_md5.hash('password')",
    "hex_md5.verify('password', '5F4DCC3B5AA765D61D8327DEB882CF99')",
    "hex_md5.verify('Password', '5f4dcc3b5aa765d61d8327deb882cf99')",
    "hex_md5.identify('5f4dcc3b5aa765d61d8327deb882cf99')",
    "hex_md5.identify('5f4dcc3b')",
    "hex_md5.identify('')",
    "hex_md4.hash('password')",
    "hex_sha1.hash('p\\xe4ssw\\xf6rd')",
    "hex_sha256.hash(b'password')",
    "hex_sha512.hash('')",
    "hex_sha256.verify('x', 'zz')",
    "hex_sha256.verify('x', 'g' * 64)",
    "hex_sha1.verify('x', None)",
    "hex_md5.verify(None, '5f4dcc3b5aa765d61d8327deb882cf99')",
    "hex_md5.verify(3, '5f4dcc3b5aa765d61d8327deb882cf99')",
    "hex_md5.hash('x' * 4097)",
    "hex_md5.name",
    "hex_md5.setting_kwds",
    "hex_sha256.checksum_size",
    "htdigest.hash('secret', 'alice', 'Restricted')",
    "htdigest.verify('secret', %s, 'alice', 'Restricted')"
    % q(ph.htdigest.hash("secret", "alice", "Restricted")),
    "htdigest.verify('secret', 'ABC', 'alice', 'Restricted')",
    "htdigest.verify('secret', 'Z' * 32, 'alice', 'Restricted')",
    "htdigest.identify(%s)" % q(ph.htdigest.hash("x", "u", "r")),
    "htdigest.identify('nope')",
    "htdigest.hash('p\\xe4ss', 'j\\xf6rg', 'Zone', encoding='latin-1')",
    "htdigest.hash('\\u20ac', 'u', 'r', encoding='latin-1')",
    "htdigest.context_kwds",
)

section("LDAP digests")
SSHA = mk("ldap_salted_sha1", "password", salt=b"NaCl")
job(
    "ldap_md5.hash('password')",
    "ldap_sha1.hash('password')",
    "ldap_sha1.verify('password', '{SHA}W6ph5Mm5Pz8GgiULbPgzG37mj9g=')",
    "ldap_sha1.verify('password', '{SHA}W6ph5Mm5Pz8GgiULbPgzG37mj9g')",
    "ldap_sha1.verify('password', '{SHA}W6ph5Mm5Pz8G!iULbPgzG37mj9g=')",
    "ldap_sha1.verify('password', '{SSHA}W6ph5Mm5Pz8GgiULbPgzG37mj9g=')",
    "ldap_md5.identify('{MD5}X03MO1qnZdYdgyfeuILPmQ==')",
    "ldap_md5.identify('{md5}X03MO1qnZdYdgyfeuILPmQ==')",
    "ldap_salted_md5.hash('password')",
    "ldap_salted_sha1.hash('password')",
    "ldap_salted_sha1.using(salt_size=8).hash('password')",
    "ldap_salted_sha256.hash('password')",
    "ldap_salted_sha512.using(salt=b'NaCl').hash('password')",
    "ldap_salted_sha1.verify('password', %s)" % q(SSHA),
    "ldap_salted_sha1.verify('Password', %s)" % q(SSHA),
    "ldap_salted_sha1.parsehash(%s)" % q(SSHA),
    "ldap_salted_sha1.parsehash(%s, sanitize=True)" % q(SSHA),
    "ldap_salted_sha1.parsehash(%s, checksum=False)" % q(SSHA),
    "ldap_salted_sha1.using(salt_size=2)",
    "H = ldap_salted_sha1.using(salt_size=20, relaxed=True)",
    "H.default_salt_size",
    "H.hash('password')",
    "ldap_salted_sha1.using(salt=b'ab')",
    "ldap_salted_sha1.using(salt='abcd')",
    "ldap_salted_sha1.using(salt=b'0123456789abcdefXYZ')",
    "ldap_salted_sha1.using(salt=b'0123456789abcdefXYZ', relaxed=True).hash('pw')",
    "ldap_salted_sha1.using(salt_size=8, default_salt_size=8)",
    "ldap_salted_sha1.verify('x', '{SSHA}abc')",
    "ldap_salted_sha1.verify('x', '{SSHA}' + 'A' * 33)",
    "ldap_salted_sha1.verify('x', '{SSHA}' + 'A' * 34)",
    "ldap_salted_md5.verify('x', '{SMD5}' + 'A' * 24)",
    "ldap_salted_md5.verify('x', '{SMD5}' + 'A' * 48)",
    "ldap_salted_sha1.min_salt_size",
    "ldap_salted_sha1.max_salt_size",
    "ldap_plaintext.hash('password')",
    "ldap_plaintext.identify('{SHA}abc')",
    "ldap_plaintext.identify('secret')",
    "ldap_plaintext.identify('')",
    "ldap_plaintext.verify('secret', 'secret')",
    "ldap_plaintext.verify('x', '{SHA}abc')",
    "ldap_hex_md5.hash('password')",
    "ldap_hex_sha1.hash('password')",
    "ldap_hex_md5.verify('password', '{MD5}5F4DCC3B5AA765D61D8327DEB882CF99')",
    "ldap_hex_md5.identify('{MD5}5f4dcc3b5aa765d61d8327deb882cf99')",
    "ldap_hex_md5.verify('password', '5f4dcc3b5aa765d61d8327deb882cf99')",
    "ldap_hex_md5.ident",
    "ldap_pbkdf2_sha256.ident",
)

section("DES crypt family")
BSDI = mk("bsdi_crypt", "password", rounds=101, salt="EZ.u")
BIG = mk("bigcrypt", "passwordpassword2", salt="Sa")
C16 = mk("crypt16", "passwordpassword", salt="aa")
job(
    "des_crypt.hash('password')",
    "des_crypt.using(salt='ab').hash('password')",
    "des_crypt.verify('password', %s)" % q(DES),
    "des_crypt.verify('passwordXYZ', %s)" % q(DES),
    "des_crypt.verify('passwor', %s)" % q(DES),
    "des_crypt.hash('')",
    "des_crypt.hash('\\xe9t\\xe9')",
    "des_crypt.using(truncate_error=True).hash('password1')",
    "des_crypt.using(truncate_error=True).hash('password')",
    "des_crypt.using(truncate_error='yes')",
    "des_crypt.using(salt='a')",
    "des_crypt.using(salt='a$')",
    "des_crypt.using(salt_size=3)",
    "des_crypt.using(salt_size=3, relaxed=True).default_salt_size",
    "des_crypt.identify(%s)" % q(DES),
    "des_crypt.identify('ab')",
    "des_crypt.identify('ab$')",
    "des_crypt.identify(b'abJnggxhB/yWI')",
    "des_crypt.verify('x', 'ab')",
    "des_crypt.verify('x', 'abJnggxhB/yW')",
    "des_crypt.verify('x', 'a')",
    "des_crypt.verify('x', 'a$Jnggxh!/yWI')",
    "des_crypt.hash('pass\\x00word')",
    "des_crypt.parsehash(%s)" % q(DES),
    "des_crypt.truncate_size",
    "des_crypt.truncate_error",
    "bsdi_crypt.using(rounds=101).hash('password')",
    "H = bsdi_crypt.using(rounds=100)",
    "H.default_rounds",
    "H.hash('password')",
    "bsdi_crypt.verify('password', %s)" % q(BSDI),
    "bsdi_crypt.verify('passwor', %s)" % q(BSDI),
    "bsdi_crypt.parsehash(%s)" % q(BSDI),
    "bsdi_crypt.needs_update(%s)" % q(BSDI),
    "bsdi_crypt.needs_update('_1/..EZ.uwKgJjMpXmeg')",
    "bsdi_crypt.using(min_rounds=200).needs_update(%s)" % q(BSDI),
    "bsdi_crypt.identify('_/...EZ.u')",
    "bsdi_crypt.verify('x', '_/...EZ.uwKgJjMp')",
    "bsdi_crypt.verify('x', '_....EZ.uwKgJjMpXmeg')",
    "bsdi_crypt.using(rounds=0)",
    "bsdi_crypt.using(rounds=20000000)",
    "bigcrypt.hash('passwordpassword2')",
    "bigcrypt.verify('passwordpassword2', %s)" % q(BIG),
    "bigcrypt.verify('passwordpassword', %s)" % q(BIG),
    "bigcrypt.verify('x', 'Sa' + 'A' * 12)",
    "bigcrypt.parsehash(%s)" % q(BIG),
    "crypt16.hash('passwordpassword')",
    "crypt16.verify('passwordpassword', %s)" % q(C16),
    "crypt16.verify('passwordpasswordXX', %s)" % q(C16),
    "crypt16.using(truncate_error=True).hash('x' * 17)",
    "ldap_des_crypt.hash('password')",
    "ldap_des_crypt.verify('password', '{CRYPT}' + %s)" % q(DES),
    "ldap_des_crypt.identify('{CRYPT}' + %s)" % q(DES),
    "ldap_des_crypt.identify(%s)" % q(DES),
    "ldap_des_crypt.verify('password', %s)" % q(DES),
    "des_crypt.genconfig()",
    "des_crypt.genhash('password', 'ab')",
    "des_crypt.genhash('password', None)",
)

section("MD5 crypt")
job(
    "md5_crypt.hash('password')",
    "md5_crypt.verify('password', %s)" % q(MD5),
    "apr_md5_crypt.verify('apache', %s)" % q(APR),
    "md5_crypt.using(salt='toolongsalt')",
    "H = md5_crypt.using(salt='toolongsalt', relaxed=True)",
    "md5_crypt.verify('x', '$1$abc')",
    "md5_crypt.verify('x', '$1$abc$def$ghi')",
    "md5_crypt.verify('x', '$2$abc$def')",
    "md5_crypt.verify('x', '$1$abc$def')",
    "md5_crypt.verify('x', '$1$a!c$qjXMvbEw8oaL.CzflDtaK/')",
    "md5_crypt.verify('x', '$1$abc$qjXMvbEw8oaL.CzflDt!K/')",
    "md5_crypt.hash('a\\x00b')",
    "md5_crypt.parsehash(%s)" % q(MD5),
    "md5_crypt.parsehash(%s, checksum=False)" % q(MD5),
    "md5_crypt.parsehash(%s, sanitize=True)" % q(MD5),
    "md5_crypt.parsehash('$1$$qjXMvbEw8oaL.CzflDtaK/')",
    "md5_crypt.identify(%s)" % q(MD5),
    "md5_crypt.identify(%s)" % q(APR),
    "apr_md5_crypt.identify(%s)" % q(APR),
    "md5_crypt.genconfig()",
    "md5_crypt.genconfig(salt='abc')",
    "md5_crypt.ident",
    "apr_md5_crypt.ident",
    "md5_crypt.default_salt_size",
    "md5_crypt.setting_kwds",
    "md5_crypt.needs_update(%s)" % q(MD5),
    "ldap_md5_crypt.ident",
    "ldap_md5_crypt.identify('{CRYPT}' + %s)" % q(MD5),
    "ldap_md5_crypt.verify('x', '{CRYPT}$5$abc')",
)

section("SHA crypt")
job(
    "sha256_crypt.using(rounds=1000).hash('password')",
    "sha512_crypt.verify('password', %s)" % q(SHA512),
    "sha256_crypt.verify('x', '$5$rounds=01000$saltsalt$' + 'a' * 43)",
    "sha256_crypt.verify('x', '$5$rounds=999$saltsalt$' + 'a' * 43)",
    "sha256_crypt.verify('x', '$5$rounds=999$saltsalt')",
    "sha256_crypt.verify('x', '$5$rounds=1000$saltsalt$abc$def')",
    "sha256_crypt.verify('x', '$5$rounds=10x0$saltsalt$')",
    "sha256_crypt.verify('x', '$5$saltsaltsaltsaltsalt$' + 'a' * 43)",
    "sha256_crypt.parsehash(%s)" % q(SHA256),
    "sha256_crypt.parsehash('$5$saltsalt$' + 'a' * 43)",
    "sha256_crypt.parsehash('$5$rounds=5000$saltsalt$' + 'a' * 43)",
    "sha512_crypt.parsehash(%s, sanitize=True)" % q(SHA512),
    "sha256_crypt.identify(%s)" % q(SHA256),
    "sha256_crypt.identify(%s)" % q(SHA512),
    "sha256_crypt.needs_update(%s)" % q(SHA256),
    "sha256_crypt.using(min_rounds=2000).needs_update(%s)" % q(SHA256),
    "sha256_crypt.using(max_rounds=999999).needs_update(%s)" % q(SHA256),
    "sha256_crypt.using(rounds=999)",
    "H = sha256_crypt.using(rounds=999, relaxed=True)",
    "H.default_rounds",
    "H.min_desired_rounds",
    "sha256_crypt.using(min_desired_rounds=2000, default_rounds=1500)",
    "sha256_crypt.using(max_rounds=1000, min_rounds=2000)",
    "sha256_crypt.using(max_rounds=1000).max_desired_rounds",
    "sha256_crypt.using(max_rounds=500000).default_rounds",
    "sha256_crypt.using(min_rounds='1500').min_desired_rounds",
    "sha256_crypt.using(min_rounds=1500, min_desired_rounds=1500)",
    "sha256_crypt.using(default_rounds=2000000000)",
    "H = sha256_crypt.using(rounds=1000, vary_rounds=0.1)",
    "H.vary_rounds",
    "sha256_crypt.using(vary_rounds=-1)",
    "sha256_crypt.using(vary_rounds=1.5)",
    "sha256_crypt.using(vary_rounds='10%').vary_rounds",
    "sha256_crypt.default_rounds",
    "sha512_crypt.default_rounds",
    "sha256_crypt.min_rounds",
    "sha256_crypt.max_rounds",
    "sha256_crypt.rounds_cost",
    "sha256_crypt.setting_kwds",
    "sha256_crypt.checksum_size",
    "sha512_crypt.checksum_size",
    "ldap_sha512_crypt.identify('{CRYPT}' + %s)" % q(SHA512),
    "sha1_crypt.using(rounds=40).hash('password')",
    "sha1_crypt.using(rounds=40, salt='saltsalt').hash('password')",
    "sha1_crypt.verify('password', %s)" % q(mk("sha1_crypt", "password", rounds=40, salt="saltsalt")),
    "sha1_crypt.using(rounds=10, salt_size=4).hash('pw')",
    "sha1_crypt.using(salt_size=70)",
    "sha1_crypt.using(salt_size=70, relaxed=True).default_salt_size",
    "sha1_crypt.parsehash('$sha1$40$saltsalt$' + 'a' * 28)",
    "sha1_crypt.verify('x', '$sha1$$saltsalt$' + 'a' * 28)",
    "sha1_crypt.verify('x', '$sha1$040$saltsalt$' + 'a' * 28)",
    "sha1_crypt.verify('x', '$sha1$40$saltsalt')",
    "sha1_crypt.verify('x', '$sha1$0$saltsalt$' + 'a' * 28)",
    "sha1_crypt.default_rounds",
)

section("bcrypt")
BAD_PAD = "$2b$04$abcdefghijklmnopqrstuv" + BCRYPT[29:]
job(
    "bcrypt.using(rounds=4).hash('password')",
    "bcrypt.verify('password', %s)" % q(BCRYPT),
    "bcrypt.using(rounds=4, ident='2y').hash('password')",
    "bcrypt.using(rounds=3)",
    "bcrypt.using(rounds=32)",
    "bcrypt.using(ident='2x')",
    "bcrypt.using(ident='$2x$').default_ident",
    "bcrypt.using(ident='2q')",
    "bcrypt.using(ident='2a', default_ident='2b')",
    "bcrypt.using(default_ident='2').default_ident",
    "bcrypt.verify('x', '$2x$04$abcdefghijklmnopqrstuu' + 'a' * 31)",
    "bcrypt.verify('x', '$2b$4$abcdefghijklmnopqrstuu' + 'a' * 31)",
    "bcrypt.verify('x', '$2z$04$abcdefghijklmnopqrstuu')",
    "bcrypt.verify('x', '$2b$04$abcdefghijklmnopqrstuu')",
    "bcrypt.verify('x', '$2b$04$abcdefghijklmnopqrstu')",
    "bcrypt.verify('x', '$2b$04$abc$defghijklmnopqrstuu')",
    "bcrypt.verify('x', '$2b$40$abcdefghijklmnopqrstuu' + 'a' * 31)",
    "bcrypt.parsehash(%s)" % q(BCRYPT),
    "bcrypt.parsehash(%s)" % q(BAD_PAD),
    "bcrypt.parsehash(%s)" % q(BCRYPT[:-1] + "b"),
    "bcrypt.normhash(%s)" % q(BAD_PAD),
    "bcrypt.normhash(%s)" % q(BCRYPT),
    "bcrypt.normhash('$1$abc')",
    "bcrypt.identify(%s)" % q(BCRYPT),
    "bcrypt.identify('$2y$04$x')",
    "bcrypt.identify('$2c$04$x')",
    "bcrypt.needs_update(%s)" % q(BCRYPT),
    "bcrypt.needs_update('$2a$04$abcdefghijklmnopqrstuv' + 'a' * 30 + 'e')",
    "bcrypt.needs_update('$2a$04$abcdefghijklmnopqrstuu' + 'a' * 30 + 'e')",
    "bcrypt.using(rounds=5).needs_update(%s)" % q(BCRYPT),
    "bcrypt.using(truncate_error=True).hash('x' * 73)",
    "bcrypt.hash('a\\x00b')",
    "bcrypt.ident_values",
    "bcrypt.default_rounds",
    "bcrypt.rounds_cost",
    "bcrypt.truncate_size",
    "bcrypt.checksum_size",
    "bcrypt.setting_kwds",
    "bcrypt.using(rounds=4, vary_rounds=0.5).vary_rounds",
    "bcrypt_sha256.using(rounds=4).hash('password')",
    "bcrypt_sha256.verify('password', %s)" % q(BSHA),
    "bcrypt_sha256.using(ident='2a')",
    "bcrypt_sha256.using(version=1, ident='2a').default_ident",
    "bcrypt_sha256.using(version=3)",
    "bcrypt_sha256.parsehash(%s)" % q(BSHA),
    "bcrypt_sha256.parsehash('$bcrypt-sha256$2a,4$abcdefghijklmnopqrstuu$' + 'a' * 31)",
    "bcrypt_sha256.parsehash('$bcrypt-sha256$v=1,t=2b,r=4$abcdefghijklmnopqrstuu$' + 'a' * 31)",
    "bcrypt_sha256.parsehash('$bcrypt-sha256$v=2,t=2b,r=04$abcdefghijklmnopqrstuu$' + 'a' * 31)",
    "bcrypt_sha256.parsehash('$bcrypt-sha256$v=2,t=2a,r=4$abcdefghijklmnopqrstuu$' + 'a' * 31)",
    "bcrypt_sha256.needs_update('$bcrypt-sha256$2a,4$abcdefghijklmnopqrstuu$' + 'a' * 31)",
    "bcrypt_sha256.needs_update(%s)" % q(BSHA),
    "bcrypt_sha256.identify('$bcrypt-sha256$x')",
    "bcrypt_sha256.identify(%s)" % q(BCRYPT),
    "bcrypt_sha256.setting_kwds",
    "bcrypt_sha256.truncate_size",
    "bcrypt_sha256.version",
)

section("scrypt")
SCRYPT = mk("scrypt", "password", rounds=4, block_size=1, salt=b"saltsalt")
job(
    "scrypt.using(rounds=4, block_size=1).hash('password')",
    "scrypt.using(rounds=3, block_size=2, parallelism=2).hash('password')",
    "scrypt.using(rounds=3, block_size=1, salt_size=6, ident='$7$').hash('password')",
    "scrypt.verify('password', %s)" % q(SCRYPT),
    "scrypt.verify('passwort', %s)" % q(SCRYPT),
    "scrypt.parsehash(%s)" % q(SCRYPT),
    "scrypt.verify('x', '$scrypt$ln=4,r=1$c2FsdA$c2FsdA')",
    "scrypt.verify('x', '$scrypt$ln=4,r=1,p=1')",
    "scrypt.verify('x', '$scrypt$ln=4,r=1,p=1$c2FsdA')",
    "scrypt.verify('x', '$scrypt$ln=4,r=0,p=1$c2FsdA$c2FsdA')",
    "scrypt.verify('x', '$scrypt$ln=4,r=1,p=1$c2FsdA$c2FsdA')",
    "scrypt.verify('x', '$7$abc')",
    "scrypt.verify('x', '$7$abc$def$ghi')",
    "scrypt.using(rounds=40)",
    "scrypt.using(block_size=0)",
    "scrypt.using(block_size='2').block_size",
    "scrypt.using(parallelism=0)",
    "scrypt.needs_update(%s)" % q(SCRYPT),
    "scrypt.using(block_size=1).needs_update(%s)" % q(SCRYPT),
    "scrypt.using(block_size=1, parallelism=2).needs_update(%s)" % q(SCRYPT),
    "scrypt.identify('$7$abc')",
    "scrypt.ident_values",
    "scrypt.default_rounds",
    "scrypt.block_size",
    "scrypt.setting_kwds",
)

section("PBKDF2")
P256 = mk("pbkdf2_sha256", "password", rounds=20, salt=b"saltsalt")
job(
    "pbkdf2_sha256.using(rounds=20).hash('password')",
    "pbkdf2_sha1.using(rounds=20, salt_size=8).hash('password')",
    "pbkdf2_sha512.using(rounds=5, salt=b'saltsalt').hash('password')",
    "pbkdf2_sha256.verify('password', %s)" % q(P256),
    "pbkdf2_sha256.verify('Password', %s)" % q(P256),
    "pbkdf2_sha256.parsehash(%s)" % q(P256),
    "pbkdf2_sha256.parsehash(%s, sanitize=True)" % q(P256),
    "pbkdf2_sha256.using(rounds=0)",
    "pbkdf2_sha256.using(rounds=0, relaxed=True).default_rounds",
    "pbkdf2_sha256.using(rounds=5000000000)",
    "pbkdf2_sha256.verify('x', '$pbkdf2-sha256$20$c2FsdHNhbHQ$')",
    "pbkdf2_sha256.verify('x', '$pbkdf2-sha256$20$c2FsdHNhbHQ$abc')",
    "pbkdf2_sha256.verify('x', '$pbkdf2-sha256$20$c2FsdHNhbHQ$a')",
    "pbkdf2_sha256.verify('x', '$pbkdf2-sha256$$c2FsdHNhbHQ$abc')",
    "pbkdf2_sha256.verify('x', '$pbkdf2-sha256$20$c2Fs!HNhbHQ$abc')",
    "pbkdf2_sha256.verify('x', '$pbkdf2-sha256$20$c2FsdHNhbHQ')",
    "pbkdf2_sha256.verify('x', '$pbkdf2$20$c2FsdHNhbHQ$abc')",
    "pbkdf2_sha256.default_rounds",
    "pbkdf2_sha1.default_rounds",
    "pbkdf2_sha512.default_rounds",
    "pbkdf2_sha1.ident",
    "pbkdf2_sha256.using(salt_size=0).hash('pw', rounds=3)",
    "pbkdf2_sha256.hash('pw', rounds=3, salt=b'')",
    "pbkdf2_sha256.using(salt_size=1025)",
    "cta_pbkdf2_sha1.using(rounds=20).hash('password')",
    "cta_pbkdf2_sha1.verify('password', %s)" % q(mk("cta_pbkdf2_sha1", "password", rounds=26, salt=b"\xfb\xff\xfe")),
    "cta_pbkdf2_sha1.parsehash(%s)" % q(mk("cta_pbkdf2_sha1", "password", rounds=26, salt=b"\xfb\xff\xfe")),
    "dlitz_pbkdf2_sha1.using(rounds=20).hash('password')",
    "dlitz_pbkdf2_sha1.verify('password', %s)" % q(mk("dlitz_pbkdf2_sha1", "password", rounds=20, salt="JQQ1pQ.1")),
    "dlitz_pbkdf2_sha1.parsehash('$p5k2$$JQQ1pQ.1$abc')",
    "dlitz_pbkdf2_sha1.parsehash('$p5k2$1f$JQQ1pQ.1$abc')",
    "grub_pbkdf2_sha512.using(rounds=5, salt_size=16).hash('password')",
    "grub_pbkdf2_sha512.verify('password', %s)" % q(mk("grub_pbkdf2_sha512", "password", rounds=5, salt=b"0123456789abcdef")),
    "grub_pbkdf2_sha512.verify('x', 'grub.pbkdf2.sha512.5.XYZ.ABC')",
    "atlassian_pbkdf2_sha1.parsehash('{PKCS5S2}' + 'QUJDREVGR0hJSktMTU5PUA' + 'A' * 42 + '==')",
    "atlassian_pbkdf2_sha1.verify('x', '{PKCS5S2}QUJD')",
    "atlassian_pbkdf2_sha1.identify('{PKCS5S2}QUJD')",
    "ldap_pbkdf2_sha256.using(rounds=20).hash('password')",
    "ldap_pbkdf2_sha256.verify('password', %s)" % q("{PBKDF2-SHA256}" + P256[15:]),
    "ldap_pbkdf2_sha256.identify(%s)" % q(P256),
    "django_pbkdf2_sha256.using(rounds=20).hash('password')",
    "django_pbkdf2_sha1.using(rounds=20, salt='NaCl').hash('password')",
    "django_pbkdf2_sha256.verify('password', %s)" % q(mk("django_pbkdf2_sha256", "password", rounds=20, salt="seasalt")),
    "django_pbkdf2_sha256.parsehash(%s)" % q(mk("django_pbkdf2_sha256", "password", rounds=20, salt="seasalt")),
    "django_pbkdf2_sha256.using(salt='')",
    "django_pbkdf2_sha256.using(salt='a$b')",
)

section("Windows, MySQL, PostgreSQL, PHP")
LM = ph.lmhash.hash("password")
job(
    "nthash.hash('password')",
    "nthash.verify('password', '8846F7EAEE8FB117AD06BDD830B7586C')",
    "nthash.hash('p\\xe4ss\\u20ac')",
    "nthash.raw('password')",
    "lmhash.hash('password')",
    "lmhash.verify('PASSWORD', %s)" % q(LM),
    "lmhash.verify('passwor', %s)" % q(LM),
    "lmhash.hash('passwordpassword')",
    "lmhash.using(truncate_error=True).hash('x' * 15)",
    "lmhash.raw('Password')",
    "lmhash.raw(b'abc')",
    "lmhash.hash('')",
    "bsd_nthash.hash('password')",
    "bsd_nthash.verify('password', '$3$$8846f7eaee8fb117ad06bdd830b7586c')",
    "bsd_nthash.identify('$3$$8846f7eaee8fb117ad06bdd830b7586c')",
    "bsd_nthash.verify('password', '8846f7eaee8fb117ad06bdd830b7586c')",
    "msdcc.hash('password', user='Administrator')",
    "msdcc.verify('password', %s, user='administrator')" % q(ph.msdcc.hash("password", user="Administrator")),
    "msdcc.verify('password', %s, user='admin')" % q(ph.msdcc.hash("password", user="Administrator")),
    "msdcc.hash('password')",
    "mysql323.hash('password')",
    "mysql323.hash('pass word\\t')",
    "mysql323.verify('password', '5D2E19393CC5EF67')",
    "mysql41.hash('password')",
    "mysql41.verify('password', '*2470c0c06dee42fd1618bb99005adca2ec9d1e19')",
    "mysql41.verify('password', '2470c0c06dee42fd1618bb99005adca2ec9d1e19')",
    "mysql41.identify('*2470C0C06DEE42FD1618BB99005ADCA2EC9D1E19')",
    "postgres_md5.hash('password', user='admin')",
    "postgres_md5.verify('password', %s, user='admin')" % q(ph.postgres_md5.hash("password", user="admin")),
    "postgres_md5.verify('password', %s, user='root')" % q(ph.postgres_md5.hash("password", user="admin")),
    "postgres_md5.hash('password')",
    "postgres_md5.context_kwds",
    "phpass.using(rounds=7).hash('password')",
    "phpass.using(rounds=7, ident='H').hash('password')",
    "phpass.verify('password', %s)" % q(mk("phpass", "password", rounds=8, salt="saltsalt")),
    "phpass.parsehash(%s)" % q(mk("phpass", "password", rounds=8, salt="saltsalt")),
    "phpass.verify('x', '$P$')",
    "phpass.verify('x', '$P$9saltsalt')",
    "phpass.verify('x', '$P$!saltsalt')",
    "phpass.verify('x', '$P$5saltsalt')",
    "phpass.verify('x', '$Q$9saltsalt')",
    "phpass.using(rounds=6)",
    "phpass.default_ident",
    "phpass.ident_values",
)

section("Cisco, Django and the disabled hashes")
job(
    "cisco_type7.hash('cisco')",
    "cisco_type7.using(salt=5).hash('cisco')",
    "cisco_type7.decode('0822455D0A16')",
    "cisco_type7.decode('0822455D0A16', None)",
    "cisco_type7.verify('cisco', '0822455D0A16')",
    "cisco_type7.verify('cisco', '0822455d0a16')",
    "cisco_type7.using(salt=60)",
    "cisco_type7.using(salt=60, relaxed=True).hash('x')",
    "cisco_type7.using(salt='5')",
    "cisco_type7.verify('x', 'zz1234')",
    "cisco_type7.verify('x', '7')",
    "cisco_type7.verify('x', '99ABCD')",
    "cisco_type7.verify('x', '05GH')",
    "cisco_pix.hash('cisco')",
    "cisco_pix.hash('cisco', user='admin')",
    "cisco_asa.hash('a long password here', user='user')",
    "cisco_asa.hash('a password of exactly 28 ch', user='u')",
    "cisco_pix.hash('a' * 17)",
    "cisco_pix.verify('a' * 17, %s)" % q(ph.cisco_pix.hash("a" * 16)),
    "cisco_pix.verify('a' * 16, %s)" % q(ph.cisco_pix.hash("a" * 16)),
    "cisco_pix.truncate_size",
    "cisco_asa.truncate_size",
    "django_salted_sha1.hash('password')",
    "django_salted_md5.using(salt='abc').hash('password')",
    "django_salted_sha1.verify('password', %s)" % q(mk("django_salted_sha1", "password", salt="NaCl")),
    "django_salted_sha1.parsehash(%s)" % q(mk("django_salted_sha1", "password", salt="NaCl")),
    "django_salted_sha1.verify('x', 'sha1$NaCl$ABC')",
    "django_salted_sha1.verify('x', 'sha1$Na-Cl$' + 'a' * 40)",
    "django_salted_md5.default_salt_size",
    "django_disabled.hash('x')",
    "django_disabled.verify('x', '!abc')",
    "django_disabled.verify('x', 'abc')",
    "django_disabled.identify('!')",
    "plaintext.hash('password')",
    "plaintext.hash(b'caf\\xc3\\xa9')",
    "plaintext.verify('password', 'password')",
    "plaintext.verify('password', b'password')",
    "plaintext.identify('$1$abc')",
    "plaintext.hash('caf\\xe9', encoding='latin-1')",
    "plaintext.verify('caf\\xe9', b'caf\\xe9', encoding='latin-1')",
    "plaintext.verify('x', 3)",
    "unix_disabled.hash('x')",
    "unix_disabled.using(marker='*').hash('x')",
    "unix_disabled.using(marker='x')",
    "unix_disabled.verify('x', '!')",
    "unix_disabled.verify('x', '*abc')",
    "unix_disabled.verify('x', '')",
    "unix_disabled.verify('x', 'abc')",
    "unix_disabled.identify('')",
    "unix_disabled.disable('$1$abc$def')",
    "unix_disabled.disable('!$1$abc$def')",
    "unix_disabled.disable()",
    "unix_disabled.enable('!$1$abc$def')",
    "unix_disabled.enable('*x')",
    "unix_disabled.enable('!')",
    "unix_disabled.enable('$1$abc')",
    "unix_disabled.is_disabled",
    "md5_crypt.is_disabled",
    "unix_disabled.hash('x', marker='*')",
)

section("CryptContext")
job(
    "C = CryptContext(schemes=['sha256_crypt', 'md5_crypt', 'des_crypt'], deprecated=['des_crypt'], sha256_crypt__default_rounds=1000)",
    "C.schemes()",
    "C.default_scheme()",
    "C.to_string()",
    "C.to_dict()",
    "C.identify(%s)" % q(MD5),
    "C.identify('nonsense')",
    "C.identify('nonsense', required=True)",
    "C.identify(%s, resolve=True)" % q(SHA256),
    "C.identify(None)",
    "C.verify('password', %s)" % q(DES),
    "C.verify('wrong', %s)" % q(DES),
    "C.verify('password', '$9$abc')",
    "C.needs_update(%s)" % q(DES),
    "C.needs_update(%s)" % q(MD5),
    "C.needs_update(%s)" % q(SHA256),
    "C.verify_and_update('password', %s)" % q(DES),
    "C.verify_and_update('wrong', %s)" % q(DES),
    "C.hash('password', scheme='des_crypt')",
    "C.hash('password', scheme='bcrypt')",
    "C.handler('md5_crypt')",
    "C.handler('bcrypt')",
    "C.handler().default_rounds",
    "C.handler('md5_crypt').deprecated",
    "C.handler('des_crypt').deprecated",
    "C.handler('des_crypt', unconfigured=True)",
    "C2 = C.copy(default='md5_crypt')",
    "C2.default_scheme()",
    "C.default_scheme()",
    "C.update(deprecated=['md5_crypt', 'des_crypt'])",
    "C.to_string()",
    "C.needs_update(%s)" % q(MD5),
    "C.update(sha256_crypt__min_rounds=2000, sha256_crypt__default_rounds=2000)",
    "C.needs_update(%s)" % q(SHA256),
    "C.handler().default_rounds",
    "C.update({'default': 'md5_crypt'})",
    "C.update('[passlib]\\nschemes = des_crypt\\n')",
    "C.schemes()",
    "C.update({}, x=1)",
    "CryptContext(schemes=['md5_crypt', 'md5_crypt'])",
    "CryptContext(schemes=['nosuch'])",
    "CryptContext(schemes=['md5_crypt'], default='des_crypt')",
    "CryptContext(schemes=['md5_crypt'], default=md5_crypt).default_scheme()",
    "CryptContext(schemes=['md5_crypt'], default=1)",
    "CryptContext(schemes=['md5_crypt'], deprecated=['md5_crypt'])",
    "CryptContext(schemes=['md5_crypt', 'des_crypt'], default='des_crypt', deprecated=['des_crypt'])",
    "CryptContext(schemes=['md5_crypt'], foo=1)",
    "CryptContext(schemes=['md5_crypt'], md5_crypt__salt='abc')",
    "CryptContext(schemes=['md5_crypt'], md5_crypt__rounds=5)",
    "CryptContext(schemes=['md5_crypt'], md5_crypt__salt_size=4).handler().default_salt_size",
    "CryptContext(schemes=['md5_crypt'], md5_crypt__salt_size=40)",
    "CryptContext(schemes=['sha256_crypt'], all__vary_rounds=0.1).to_string()",
    "CryptContext(schemes=['sha256_crypt'], vary_rounds='5%').to_dict()",
    "CryptContext(schemes=['sha256_crypt'], all__default_rounds=1000).handler().default_rounds",
    "CryptContext(schemes=['md5_crypt'], deprecated=['auto', 'md5_crypt'])",
    "CryptContext(schemes=['md5_crypt'], deprecated=['des_crypt'])",
    "CryptContext(schemes=['md5_crypt'], deprecated='md5_crypt, des_crypt')",
    "CryptContext(schemes='md5_crypt, des_crypt').schemes()",
    "CryptContext(schemes=[md5_crypt, 'des_crypt', ldap_md5_crypt]).schemes()",
    "CryptContext(schemes=['md5_crypt'], admin__schemes=['des_crypt'])",
    "CryptContext(schemes=['md5_crypt'], a__b__c__d=1)",
    "CryptContext(schemes=['md5_crypt'], __md5_crypt__x=1)",
    "CryptContext(schemes=['md5_crypt'], min_verify_time=0.5).to_dict()",
    "CryptContext(schemes=['md5_crypt'], harden_verify=True).to_dict()",
    "CryptContext().schemes()",
    "CryptContext().hash('x')",
    "CryptContext().identify('x')",
    "CryptContext().handler()",
    "CryptContext(schemes=['ldap_salted_sha1']).verify('pw', None)",
    "CryptContext(schemes=['ldap_salted_sha1']).verify_and_update('pw', None)",
    "D = CryptContext(schemes=['sha256_crypt', 'unix_disabled'])",
    "D.disable(%s)" % q(SHA256),
    "D.disable()",
    "D.enable('!' + %s)" % q(SHA256),
    "D.enable(%s)" % q(SHA256),
    "D.is_enabled('!' + %s)" % q(SHA256),
    "D.is_enabled(%s)" % q(SHA256),
    "D.is_enabled('nonsense')",
    "D.verify('x', '!')",
    "CryptContext(schemes=['md5_crypt']).disable()",
)

section("categories and config files")
job(
    "A = CryptContext.from_path('data/app.ini')",
    "A.to_string()",
    "A.schemes()",
    "A.default_scheme()",
    "A.default_scheme('admin')",
    "A.handler(category='admin').default_rounds",
    "A.handler(category='admin').min_desired_rounds",
    "A.handler(category='staff').default_rounds",
    "A.hash('password')",
    "A.hash('password', category='admin')",
    "A.needs_update(%s)" % q(P256),
    "A.needs_update(%s, category='admin')" % q(P256),
    "A.needs_update(%s)" % q(SSHA),
    "A.verify_and_update('password', %s)" % q(SSHA),
    "A.verify_and_update('password', %s, category='admin')" % q(P256),
    "A.verify_and_update('password', %s)" % q(P256),
    "A.to_dict()",
    "A.to_string(section='app')",
    "CryptContext.from_string(read_text('data/app.ini'), section='other').schemes()",
    "CryptContext.from_string('[passlib]\\nschemes = md5_crypt\\n').schemes()",
    "CryptContext.from_string('[other]\\nx = 1\\n')",
    "CryptContext.from_string('schemes = md5_crypt')",
    "CryptContext.from_string(3)",
    "CryptContext.from_path('data/bad.ini')",
    "CryptContext.from_path('data/missing.ini')",
    "CryptContext.from_string('[passlib]\\nschemes = md5_crypt\\ndefault = md5_crypt\\nmd5_crypt__salt_size = 6\\n').to_string()",
    "CryptContext.from_string('[passlib]\\nSchemes = des_crypt\\nDES_CRYPT__Truncate_Error = true\\n').to_dict()",
    "B = CryptContext(schemes=['pbkdf2_sha256', 'des_crypt'], default='pbkdf2_sha256', pbkdf2_sha256__default_rounds=20, staff__context__default='des_crypt', staff__des_crypt__truncate_error=True, staff__context__deprecated=['pbkdf2_sha256'])",
    "B.to_string()",
    "B.default_scheme('staff')",
    "B.hash('password', category='staff')",
    "B.hash('password1', category='staff')",
    "B.needs_update(%s, category='staff')" % q(P256),
    "B.needs_update(%s)" % q(P256),
    "B.handler('pbkdf2_sha256', 'staff').deprecated",
    "B.handler('pbkdf2_sha256').deprecated",
    "B.identify(%s, category='staff')" % q(DES),
    "CryptContext(schemes=['md5_crypt'], staff__context__default='des_crypt')",
    "CryptContext(schemes=['md5_crypt', 'des_crypt'], staff__context__deprecated=['md5_crypt', 'des_crypt'])",
    "CryptContext(schemes=['md5_crypt', 'des_crypt'], staff__context__default='des_crypt', staff__context__deprecated=['des_crypt'])",
)

section("Apache htpasswd")
job(
    "F = HtpasswdFile('data/htpasswd')",
    "F.users()",
    "F.check_password('alice', 'secret')",
    "F.check_password('alice', 'wrong')",
    "F.check_password('bob', 'hunter2')",
    "F.check_password('carol', 'letmein')",
    "F.check_password('dave', 'apache')",
    "F.check_password('erin', 's3cret')",
    "F.check_password('nobody', 'x')",
    "F.get_hash('alice')",
    "F.get_hash('nobody')",
    "F.context.schemes()",
    "F.context.default_scheme()",
    "F.set_hash('frank', %s)" % q(SHA1_LDAP),
    "F.set_hash('alice', 'plain')",
    "F.delete('bob')",
    "F.delete('bob')",
    "F.users()",
    "F.to_string().decode()",
    "F.save('data/out/htpasswd')",
    "read_text('data/out/htpasswd')",
    "F.set_password('bad:user', 'x')",
    "F.set_password('tab\\tuser', 'x')",
    "F.set_password('u' * 256, 'x')",
    "F.set_password(5, 'x')",
    "F.path",
    "G = HtpasswdFile('data/out/new.htpasswd', new=True, default_scheme='portable')",
    "G.context.default_scheme()",
    "G.users()",
    "G.path",
    "G = HtpasswdFile(new=True, default_scheme='plaintext')",
    "G.set_password('zed', 'pw')",
    "G.set_password('zed', 'pw2')",
    "G.set_password('amy', 'pw3')",
    "G.to_string()",
    "G.save()",
    "G.load()",
    "G.context.default_scheme()",
    "HtpasswdFile(new=True, default_scheme='portable_apache_22').context.default_scheme()",
    "HtpasswdFile(new=True, default_scheme='ldap_salted_sha1')",
    "HtpasswdFile('data/missing')",
    "HtpasswdFile('data/bad.htpasswd')",
    "HtpasswdFile('data/dup.htpasswd').users()",
    "HtpasswdFile('data/dup.htpasswd').get_hash('alice')",
    "HtpasswdFile.from_string('alice:{SHA}abc\\n\\n# end\\n').to_string()",
    "HtpasswdFile.from_string(b'alice:{SHA}abc\\n').users()",
    "HtpasswdFile.from_string('x:y\\n', path='p')",
    "HtpasswdFile(encoding='utf-16')",
    "E = HtpasswdFile(new=True, context=CryptContext(schemes=['ldap_salted_sha1', 'ldap_sha1', 'plaintext']))",
    "E.set_password('ana', 'pw')",
    "E.set_password('ana', 'pw2')",
    "E.check_password('ana', 'pw2')",
    "E.check_password('ana', 'pw')",
    "E.to_string().decode()",
    "U = HtpasswdFile('data/out/legacy.htpasswd', new=True, autosave=True, context=CryptContext.from_path('data/migrate.ini'))",
    "U.load('data/legacy.htpasswd')",
    "U.users()",
    "U.check_password('admin', 'admin123')",
    "U.check_password('ops', 'opsops')",
    "U.check_password('guest', 'guest')",
    "U.check_password('web', 'wrong')",
    "U.check_password('web', 'webweb')",
    "read_text('data/out/legacy.htpasswd')",
    "U.check_password('admin', 'admin123')",
    "U.delete('guest')",
    "read_text('data/out/legacy.htpasswd')",
    "HtpasswdFile('data/out/legacy.htpasswd').users()",
)

section("Apache htdigest")
job(
    "W = HtdigestFile('data/htdigest')",
    "sorted(W.realms())",
    "W.users('Restricted')",
    "W.users('Admin')",
    "W.users('Nowhere')",
    "W.users()",
    "W.check_password('alice', 'Restricted', 'secret')",
    "W.check_password('alice', 'Admin', 'secret')",
    "W.check_password('alice', 'Admin', 'root')",
    "W.check_password('zed', 'Admin', 'root')",
    "W.check_password('alice', 'secret')",
    "W.get_hash('bob', 'Restricted')",
    "W.set_password('erin', 'Admin', 'pw')",
    "W.set_password('erin', 'Admin', 'pw2')",
    "W.get_hash('erin', 'Admin')",
    "W.set_hash('frank', 'Admin', 'ABC')",
    "W.delete('bob', 'Restricted')",
    "W.delete('bob', 'Restricted')",
    "W.to_string().decode()",
    "W.delete_realm('Admin')",
    "W.to_string().decode()",
    "W.set_password('a:b', 'Admin', 'x')",
    "V = HtdigestFile('data/htdigest', default_realm='Restricted')",
    "V.check_password('alice', 'secret')",
    "V.users()",
    "V.set_password('gil', 'pw')",
    "V.get_hash('gil')",
    "V.save('data/out/htdigest')",
    "read_text('data/out/htdigest')",
    "HtdigestFile.from_string('alice:Restricted\\n')",
    "HtdigestFile.from_string('a:r:' + 'f' * 32 + '\\n').users('r')",
)

section("reference values")
job(
    "md5_crypt.name",
    "sha512_crypt.name",
    "C.schemes(resolve=True)",
    "A.schemes(resolve=True, category='admin')",
)


def main():
    if os.path.isdir(D):
        shutil.rmtree(D)
    os.makedirs(os.path.join(D, "out"))
    for name, text in FILES.items():
        with open(os.path.join(D, name), "w", encoding="utf-8") as f:
            f.write(text)
    with open(os.path.join(D, "jobs.tsv"), "w", encoding="utf-8") as f:
        for line in JOBS:
            assert "\n" not in line and "\t" not in line, line
            f.write(line + "\n")
    with open(os.path.join(D, "files.txt"), "w", encoding="utf-8") as f:
        for name in FILES:
            f.write(name + "\n")
    print("%d jobs, %d files" % (len(JOBS), len(FILES)))


main()
