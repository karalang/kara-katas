# The inputs of mini_shadow: two system roots (one healthy, one with
# broken account files), an htpasswd file, and the commands run against
# them. Run as a script, it writes them into data/; mini_shadow.py,
# real.py and gen_kara.py import FILES.
import os

FILES = {}

# Directories and empty programs each root needs, as `pwck` looks for
# home directories and shells.
FILES["sys/layout.txt"] = """d root
d home/alice
d home/bob
d home/carol
d home/dave
d home/erin
d home/frank
d home/gina
d home/henry
d home/judy
d home/kim
d home/liam
d usr/sbin
f bin/bash
f bin/sh
f usr/sbin/nologin
"""

FILES["sys/etc/passwd"] = """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
alice:x:1000:1000:Alice Liddell,,,:/home/alice:/bin/bash
bob:x:1001:1001:Bob Builder:/home/bob:/bin/bash
carol:x:1002:1002::/home/carol:/bin/sh
dave:x:1003:1003::/home/dave:/bin/bash
erin:x:1004:1004::/home/erin:/bin/bash
frank:x:1005:1005::/home/frank:/bin/bash
gina:x:1006:1006::/home/gina:/bin/bash
henry:x:1007:1007::/home/henry:/bin/sh
ivan:x:1008:1008:batch jobs:/home/ivan:/usr/sbin/nologin
judy:x:1009:1009::/home/judy:/bin/bash
kim:x:1010:1010::/home/kim:/bin/zsh
liam:$1$Mn3vC8$WSq/FlpGHh0pPei.eEdY0/:1011:1011::/home/liam:/bin/sh
"""

FILES["sys/etc/shadow"] = """root:$6$rounds=1000$Rr0tS4lt$svsnhawktjKHBncB4Cf30ODH.vnalpMr7qoNw4FguG3B06mmLJ7tLmPVj0rfVAzm1KHbOuOJJjY/8jofw9V4C.:20400:0:99999:7:::
daemon:*:20400:0:99999:7:::
alice:$6$rounds=1000$Wq3vB7xk$DqbVzyjGkh2tPAmRTUMflyIlGFZJzuTKgmx4hewa.HwDZl6NEE02.QKvEY/yZVt8H/lTM2Ejk5gVJb71z7GLN.:20706:0:90:7:14::
bob:$5$rounds=1000$Nf8sKe2p$TDzeg2Al9So/ul20/v0XlKrGi82uJzgTD45p4wR9R02:20656:1:90:7:::
carol:$1$Hx9bQ2$Yda4efbbBnCJrfotRyDEQ0:0:0:99999:7:::
dave:$6$rounds=1200$Dt5mZ0aQ$xZvL6GNEQyojIrwN.92XE11TIseS0aiiZhiekPaZwppEHeP98zOGMlZczLBmEEfD49Gc6fobsGZjUYr.YGe4U/:20641:0:90:7:30::
erin:$5$rounds=1000$Jz1cR4yT$P5Pv6oSZ/Y8ZMOfc1wM1eu3VcDDzMrcQqG9xGzyL622:20541:0:90:7:14::
frank:$1$Pk7wL2nV$J8YBgG2oyU/fh3mWWI4oz1:20700:0:99999:7::20730:
gina:!$6$rounds=1000$Gt4hY6uE$txKVgub/AaINMjRPpmepO.uFh2HiCcuwst7AaKLH9oZruJTT7I4NMnluUty/hduPkTYkL6hrEN4K1VupcE4zk/:20600:0:99999:7:::
henry::20650:0:99999:7:::
ivan:*:20500:0:99999:7:::
judy:$y$j9T$F5Jx5fExrKuPp53xLKQ..1$X3DX6M94c7o.9agCG9G317fhZg9SqC.5i5rd.RhAtQ7:20720:0:99999:7:::
"""

FILES["sys/etc/group"] = """root:x:0:
daemon:x:1:
sudo:x:27:alice
alice:x:1000:
bob:x:1001:
carol:x:1002:
dave:x:1003:
erin:x:1004:
frank:x:1005:
gina:x:1006:
henry:x:1007:
ivan:x:1008:
judy:x:1009:
kim:x:1010:
liam:x:1011:
"""

FILES["broken/layout.txt"] = """d root
d home/ok
d srv
f bin/bash
f bin/sh
"""

FILES["broken/etc/passwd"] = """root:x:0:0:root:/root:/bin/bash
ok:x:1000:1000::/home/ok:/bin/bash
truncated:x:1001:1001
ok:x:1002:1000::/home/ok:/bin/bash
badid:x:12a:1003::/srv:/bin/sh
nogroup:x:1004:4444::/srv:/bin/sh
nohome:x:1005:1000::/home/nohome:/bin/sh
noshell:x:1006:1000::/srv:/bin/fish
noshadow:x:1007:1000::/srv:/bin/sh

future:x:1008:1000::/srv:/bin/sh
"""

FILES["broken/etc/shadow"] = """root:*:20400:0:99999:7:::
ok:*:20400:0:99999:7:::
nogroup:*:20400:0:99999:7:::
nohome:*:20400:0:99999:7:::
noshell:*:20400:0:99999:7:::
orphan:*:20400:0:99999:7:::
future:*:22000:0:99999:7:::
badid:*:20400:0:99999:7:::
torn:*:20400
"""

FILES["broken/etc/group"] = """root:x:0:
ok:x:1000:
"""

FILES["htpasswd"] = """# web users
alice:$apr1$Qw8eRt2y$WLyBSzyA4kwtMrJzO7vuF.
bob:{SHA}5en6G6MezRroT3XKqkdPOmY/BfQ=
carol:$1$Hx9bQ2$Yda4efbbBnCJrfotRyDEQ0
dave:$6$rounds=1000$Wq3vB7xk$DqbVzyjGkh2tPAmRTUMflyIlGFZJzuTKgmx4hewa.HwDZl6NEE02.QKvEY/yZVt8H/lTM2Ejk5gVJb71z7GLN.
erin:$2y$05$ReB5QpX1rhd7cAHP0KX4vO0mOnlQhB/tdTyR8D8PY0ezM8B0yWk6m
frank:plaintext
"""

FILES["jobs.txt"] = r"""# Account files: today is 2026-10-15, day 20741.
pwck -r -R data/sys
pwck -r -q -R data/sys
pwck -r -R data/broken
pwck -r -q -R data/broken
# Aging.
chage -R data/sys -l alice
chage -R data/sys -l bob
chage -R data/sys -l carol
chage -R data/sys -l -i dave
chage -R data/sys -l frank
chage -R data/sys -l henry
chage -R data/sys -l zed
chage -R data/sys -l kim
passwd -R data/sys -S alice
passwd -R data/sys -S kim
passwd -R data/sys -S liam
passwd -R data/sys -S zed
passwd -R data/sys -S -a
# Logging in.
login data/sys root rootpw
login data/sys alice wonderland
login data/sys carol wrongpass
login data/sys bob builder42
login data/sys carol pa55word
login data/sys dave hunter2
login data/sys erin letmein
login data/sys frank s3cret
login data/sys gina opensesame
login data/sys henry anything
login data/sys ivan x
login data/sys daemon x
login data/sys judy secret
login data/sys kim x
login data/sys liam tiger
login data/sys zed x
# Hashes.
openssl passwd -1 -salt Hx9bQ2 pa55word
openssl passwd -apr1 -salt Qw8eRt2y apache
openssl passwd -1 -salt abcdefghijk long
openssl passwd -5 -salt '' empty
crypt builder42 '$5$rounds=1000$Nf8sKe2p$'
crypt 'Hello world!' '$5$rounds=1000$saltstringsaltstring'
crypt pw '$6$rounds=10$tiny'
crypt pw '$1$abc'
crypt pw '$9$what'
# htpasswd files.
htpasswd -vb data/htpasswd alice apache
htpasswd -vb data/htpasswd alice wrong
htpasswd -vb data/htpasswd bob secret
htpasswd -vb data/htpasswd carol pa55word
htpasswd -vb data/htpasswd dave wonderland
htpasswd -vb data/htpasswd erin x
htpasswd -vb data/htpasswd frank plaintext
htpasswd -vb data/htpasswd zed x
# Changing aging and locks.
chage -R data/sys -d 2026-10-01 -M 60 -W 10 alice
chage -R data/sys -l alice
chage -R data/sys -E 2026-12-31 -I 5 bob
chage -R data/sys -l bob
chage -R data/sys -E -1 frank
login data/sys frank s3cret
chage -R data/sys -d 0 alice
login data/sys alice wonderland
chage -R data/sys -d 2026-02-30 -m 3 dave
chage -R data/sys -l dave
chage -R data/sys -M x alice
chage -R data/sys -d garbage alice
chage -R data/sys -m 5 zed
passwd -R data/sys -l bob
passwd -R data/sys -S bob
login data/sys bob builder42
passwd -R data/sys -u bob
passwd -R data/sys -u ivan
passwd -R data/sys -d carol
passwd -R data/sys -S carol
login data/sys carol whatever
passwd -R data/sys -e erin
passwd -R data/sys -S erin
passwd -R data/sys -n 2 -x 45 -w 3 -i 9 root
passwd -R data/sys -S root
passwd -R data/sys -x many root
passwd -R data/sys -l zed
cat data/sys/etc/shadow
"""


def write_all():
    for name, text in FILES.items():
        path = os.path.join("data", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(text)


if __name__ == "__main__":
    write_all()
