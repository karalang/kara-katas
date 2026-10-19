#!/usr/bin/env python3
"""Writes data/: a fake root filesystem per distribution under data/roots,
and data/jobs.tsv.

A job is one line of tab-separated fields. In a field, a "⏎" stands for a
newline, a "⇥" for a tab and a "␣" for a space; "∅" is the empty string
and "-" an absent value.
"""
import os

# path under data/roots -> file content; None makes an empty directory.
FILES = {}


def put(root, path, text):
    FILES[root + "/" + path] = text


def os_release(root, text, where="etc"):
    put(root, where + "/os-release", text.lstrip("\n"))


os_release("ubuntu2204", """
PRETTY_NAME="Ubuntu 22.04.3 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
""")
put("ubuntu2204", "etc/lsb-release",
    "DISTRIB_ID=Ubuntu\nDISTRIB_RELEASE=22.04\nDISTRIB_CODENAME=jammy\nDISTRIB_DESCRIPTION=\"Ubuntu 22.04.3 LTS\"\n")
put("ubuntu2204", "etc/debian_version", "bookworm/sid\n")
put("ubuntu2204", "etc/hostname", "build-box\n")

os_release("ubuntu1404", """
NAME="Ubuntu"
VERSION="14.04.6 LTS, Trusty Tahr"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 14.04.6 LTS"
VERSION_ID="14.04"
HOME_URL="http://www.ubuntu.com/"
""")
put("ubuntu1404", "etc/debian_version", "jessie/sid\n")

os_release("debian12", """
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
""")
put("debian12", "etc/debian_version", "12.4\n")

os_release("debian_testing", """
PRETTY_NAME="Debian GNU/Linux trixie/sid"
NAME="Debian GNU/Linux"
VERSION_CODENAME=trixie
ID=debian
""")
put("debian_testing", "etc/debian_version", "trixie/sid\n")

os_release("fedora39", """
NAME="Fedora Linux"
VERSION="39 (Workstation Edition)"
ID=fedora
VERSION_ID=39
VERSION_CODENAME=""
PLATFORM_ID="platform:f39"
PRETTY_NAME="Fedora Linux 39 (Workstation Edition)"
ANSI_COLOR="0;38;2;60;110;180"
LOGO=fedora-logo-icon
CPE_NAME="cpe:/o:fedoraproject:fedora:39"
DEFAULT_HOSTNAME="fedora"
VARIANT="Workstation Edition"
VARIANT_ID=workstation
""")
put("fedora39", "etc/fedora-release", "Fedora release 39 (Thirty Nine)\n")
put("fedora39", "etc/redhat-release", "Fedora release 39 (Thirty Nine)\n")
put("fedora39", "etc/system-release", "Fedora release 39 (Thirty Nine)\n")

os_release("centos7", """
NAME="CentOS Linux"
VERSION="7 (Core)"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="7"
PRETTY_NAME="CentOS Linux 7 (Core)"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:centos:centos:7"
""")
put("centos7", "etc/centos-release", "CentOS Linux release 7.9.2009 (Core)\n")
put("centos7", "etc/redhat-release", "CentOS Linux release 7.9.2009 (Core)\n")
put("centos7", "etc/system-release", "CentOS Linux release 7.9.2009 (Core)\n")

put("centos5", "etc/redhat-release", "CentOS release 5.11 (Final)\n")

os_release("rhel9", """
NAME="Red Hat Enterprise Linux"
VERSION="9.3 (Plow)"
ID="rhel"
ID_LIKE="fedora"
VERSION_ID="9.3"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Red Hat Enterprise Linux 9.3 (Plow)"
""")
put("rhel9", "etc/redhat-release", "Red Hat Enterprise Linux release 9.3 (Plow)\n")

put("rhel6", "etc/redhat-release", "Red Hat Enterprise Linux Server release 6.5 (Santiago)\n")
put("rhel6", "etc/issue", "Red Hat Enterprise Linux Server release 6.5 (Santiago)\nKernel \\r on an \\m\n")

os_release("rocky9", """
NAME="Rocky Linux"
VERSION="9.3 (Blue Onyx)"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.3"
PRETTY_NAME="Rocky Linux 9.3 (Blue Onyx)"
ROCKY_SUPPORT_PRODUCT="Rocky-Linux-9"
""")
put("rocky9", "etc/rocky-release", "Rocky Linux release 9.3 (Blue Onyx)\n")
put("rocky9", "etc/redhat-release", "Rocky Linux release 9.3 (Blue Onyx)\n")

os_release("alpine319", """
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.19.0
PRETTY_NAME="Alpine Linux v3.19"
HOME_URL="https://alpinelinux.org/"
""")
put("alpine319", "etc/alpine-release", "3.19.0\n")

os_release("arch", """
NAME="Arch Linux"
PRETTY_NAME="Arch Linux"
ID=arch
BUILD_ID=rolling
ANSI_COLOR="38;2;23;147;209"
LOGO=archlinux-logo
""")
put("arch", "etc/arch-release", "")

os_release("leap155", """
NAME="openSUSE Leap"
VERSION="15.5"
ID="opensuse-leap"
ID_LIKE="suse opensuse"
VERSION_ID="15.5"
PRETTY_NAME="openSUSE Leap 15.5"
CPE_NAME="cpe:/o:opensuse:leap:15.5"
""", where="usr/lib")
put("leap155", "etc/SUSE-brand", "openSUSE\nVERSION = 15.5\n")

put("sles12", "etc/SuSE-release", "SUSE Linux Enterprise Server 12 (x86_64)\nVERSION = 12\nPATCHLEVEL = 5\n")

os_release("amzn2", """
NAME="Amazon Linux"
VERSION="2"
ID="amzn"
ID_LIKE="centos rhel fedora"
VERSION_ID="2"
PRETTY_NAME="Amazon Linux 2"
CPE_NAME="cpe:2.3:o:amazon:amazon_linux:2"
""")
put("amzn2", "etc/system-release", "Amazon Linux release 2 (Karoo)\n")
put("amzn2", "etc/image-id", "image_name=\"amzn2-ami-kernel-5.10-hvm\"\n")

os_release("mint21", """
NAME="Linux Mint"
VERSION="21.2 (Victoria)"
ID=linuxmint
ID_LIKE="ubuntu debian"
PRETTY_NAME="Linux Mint 21.2"
VERSION_ID="21.2"
VERSION_CODENAME=victoria
UBUNTU_CODENAME=jammy
""")
put("mint21", "etc/debian_version", "bookworm/sid\n")
put("mint21", "etc/upstream-release/lsb-release", "DISTRIB_ID=Ubuntu\nDISTRIB_RELEASE=22.04\n")

os_release("raspbian11", """
PRETTY_NAME="Raspbian GNU/Linux 11 (bullseye)"
NAME="Raspbian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=raspbian
ID_LIKE=debian
""")
put("raspbian11", "etc/debian_version", "11.8\n")

os_release("gentoo", """
NAME=Gentoo
ID=gentoo
PRETTY_NAME="Gentoo Linux"
ANSI_COLOR="1;32"
""")
put("gentoo", "etc/gentoo-release", "Gentoo Base System release 2.14\n")

os_release("slackware15", """
NAME=Slackware
VERSION="15.0"
ID=slackware
VERSION_ID=15.0
PRETTY_NAME="Slackware 15.0 x86_64"
""")
put("slackware15", "etc/slackware-version", "Slackware 15.0\n")

put("cloudlinux6", "etc/redhat-release", "CloudLinux Server release 6.10 (Vladislav Volkov)\n")

os_release("oracle8", """
NAME="Oracle Linux Server"
VERSION="8.9"
ID="ol"
ID_LIKE="fedora"
VARIANT="Server"
VERSION_ID="8.9"
PRETTY_NAME="Oracle Linux Server 8.9"
""")
put("oracle8", "etc/oracle-release", "Oracle Linux Server release 8.9\n")
put("oracle8", "etc/redhat-release", "Red Hat Enterprise Linux release 8.9 (Ootpa)\n")

put("mageia9", "etc/mageia-release", "Mageia release 9 (Official) for x86_64\n")

os_release("nixos", """
BUG_REPORT_URL="https://github.com/NixOS/nixpkgs/issues"
BUILD_ID="23.11.20240115.b8dd8be"
ID=nixos
NAME=NixOS
PRETTY_NAME="NixOS 23.11 (Tapir)"
VERSION="23.11 (Tapir)"
VERSION_CODENAME=tapir
VERSION_ID="23.11"
""", where="usr/lib")
put("nixos", "etc/static/", None)

# Both files: etc wins over usr/lib.
os_release("both", """
ID=etcwins
NAME="From etc"
VERSION_ID=1.2
""")
os_release("both", """
ID=libloses
NAME="From usr/lib"
VERSION_ID=9.9.9
""", where="usr/lib")

put("empty", "", None)
put("noetc", "usr/lib/", None)

os_release("broken", """
NAME="Broken Linux
ID=broken
""")

# A hand-written os-release that leans on the shell syntax.
os_release("quirky", """
# comment line
NAME='Quirky "Q" Linux'   # trailing comment
ID="Quirky Linux"
Version="2.4.1, Hatchling Edition"
VERSION_CODENAME=café
PRETTY_NAME="Quirky\\ Linux \\"2.4\\"" extra-token another
MULTI="first
second"
ESCAPED=a\\ b\\$c
EMPTY=
=novalue
noequals
KEY=one=two
ID_LIKE="suse    debian"
""")

# Several release files: the empty one and the directory are passed over.
put("multi", "etc/aaa-release", "\n")
put("multi", "etc/bbb-release/", None)
put("multi", "etc/centos-release", "CentOS Stream release 9\n")
put("multi", "etc/redhat-release", "CentOS Stream release 9\n")
put("multi", "etc/zzz-release", "Zed Linux 1.0\n")
put("multi", "etc/foo-version.bak", "Foo 2\n")
put("multi", "etc/lsb-release", "DISTRIB_ID=Nope\n")
put("multi", "etc/oem-release", "Some OEM 7\n")

# Only names that the pattern refuses, and an ignored one.
put("nomatch", "etc/release", "Plain Release 3.0\n")
put("nomatch", "etc/my.distro-release", "Dotted 4.0\n")
put("nomatch", "etc/system-release", "System 5.0\n")
put("nomatch", "etc/Weird_version", "  Weird OS  release  8.1.2  (Wobbly)  \n")

put("misc", "etc/custom-info", "Custom Distro 3.1 (Lazy)\n")
put("misc", "etc/empty-release", "")
put("misc", "etc/os-release-alt", "ID=altid\nNAME=Alt\nVERSION_ID=\"5.6.7\"\nVERSION=\"5.6.7 (Seven)\"\n")

JOBS = r"""
# Every root, through the class the way `distro` builds it from a root.
root	ubuntu2204
root	ubuntu1404
root	debian12
root	debian_testing
root	fedora39
root	centos7
root	centos5
root	rhel9
root	rhel6
root	rocky9
root	alpine319
root	arch
root	leap155
root	sles12
root	amzn2
root	mint21
root	raspbian11
root	gentoo
root	slackware15
root	cloudlinux6
root	oracle8
root	mageia9
root	nixos
root	both
root	empty
root	noetc
root	nosuchroot
root	broken
root	quirky
root	multi
root	nomatch
root	misc
# Data source files named explicitly.
files	misc	data/roots/misc/etc/os-release-alt	-
files	misc	-	data/roots/misc/etc/custom-info
files	misc	-	data/roots/misc/etc/empty-release
files	misc	-	data/roots/misc/etc/missing-release
files	empty	data/roots/fedora39/etc/os-release	data/roots/rhel6/etc/redhat-release
files	debian12	data/roots/nowhere/os-release	-
files	nomatch	-	data/roots/nomatch/etc/Weird_version
# lsb_release -a, uname -rs and oslevel output, fed in.
inject	empty	No LSB modules are available.⏎Distributor ID:⇥Ubuntu⏎Description:⇥Ubuntu 20.04.6 LTS⏎Release:⇥20.04⏎Codename:⇥focal⏎	-	-
inject	empty	Distributor ID:⇥RedHatEnterpriseServer⏎Description:⇥Red Hat Enterprise Linux Server release 7.9 (Maipo)⏎Release:⇥7.9⏎Codename:⇥Maipo⏎	-	-
inject	empty	Distributor ID:⇥EnterpriseEnterpriseServer⏎Description:⇥Enterprise Linux Enterprise Linux Server release 5.11 (Carthage)⏎Release:⇥5.11⏎Codename:⇥Carthage⏎	-	-
inject	empty	LSB Version:⇥:core-4.1-amd64:core-4.1-noarch⏎Distributor ID:⇥Linux Mint⏎Description:⇥Linux Mint 21.2 Victoria⏎Release:⇥21.2⏎Codename:⇥victoria⏎	-	-
inject	empty	-	FreeBSD 13.2-RELEASE⏎	-
inject	empty	-	Linux 6.1.0-13-amd64⏎	-
inject	empty	-	Darwin 23.1.0⏎	-
inject	empty	-	   ⏎	-
inject	empty	-	MidnightBSD⏎	-
inject	empty	-	AIX 2⏎	7200-05-06-2320⏎
inject	empty	-	AIX 1⏎	-
inject	rhel6	Distributor ID:⇥RedHatEnterpriseServer⏎Description:⇥Red Hat Enterprise Linux Server release 6.5 (Santiago)⏎Release:⇥6.5⏎Codename:⇥Santiago⏎	Linux 2.6.32-431.el6.x86_64⏎	-
inject	debian12	Distributor ID:⇥Debian⏎Description:⇥Debian GNU/Linux 12 (bookworm)⏎Release:⇥12⏎Codename:⇥bookworm⏎	-	-
inject	arch	Distributor ID:⇥Arch⏎Description:⇥Arch Linux⏎Release:⇥rolling⏎Codename:⇥n/a⏎	-	-
inject	cloudlinux6	-	OpenBSD 7.4⏎	-
# The constructor's guard.
ctor	data/roots/debian12	T	-	-
ctor	data/roots/debian12	-	T	-
ctor	data/roots/debian12	-	-	T
ctor	data/roots/debian12	F	F	F
ctor	data/roots/debian12	-	-	-
# Release-file lines.
release	CentOS Linux release 7.9.2009 (Core)
release	Red Hat Enterprise Linux Server release 6.5 (Santiago)
release	Fedora release 39 (Thirty Nine)
release	Ubuntu 22.04.3 LTS
release	Gentoo Base System release 2.14
release	SUSE Linux Enterprise Server 12 (x86_64)
release	Mageia release 9 (Official) for x86_64
release	3.19.0
release	Slackware 15.0
release	Slackware 14.2 LTS
release	Debian GNU/Linux trixie/sid
release	Linux Mint 21.2 Victoria
release	CloudLinux release 7.9 (Boris Yegorov)
release	   Padded release  1.2-beta3␣␣␣
release	Rolling
release	1.0
release	release 2
release	Name (Code) Name 4.4 (Codename) tail
release	v1.2.3+git20240101
release	OS 10.0-rc1 (pre (alpha))
release	a)b(c 5
release	∅
release	␣␣␣
# os-release text.
osrel	ID=x⏎VERSION="1.0 (Alpha One)"⏎
osrel	ID=x⏎VERSION="1.0, Beta"⏎VERSION_CODENAME=gamma⏎
osrel	ID=x⏎VERSION="1.0 (Alpha One)"⏎UBUNTU_CODENAME=delta⏎
osrel	ID=x⏎VERSION="12 (1984)"⏎
osrel	ID=x⏎VERSION="7 (Core), extra"⏎
osrel	ID=x⏎VERSION="7(Core)"⏎
osrel	VERSION=",   spaced out"⏎
osrel	VERSION=",9"⏎
osrel	a=1 b=2 c="3 4"⏎d='5'"6"⏎
osrel	X="unterminated⏎
osrel	X=trailing\
osrel	# just a comment⏎
osrel	∅
osrel	Q="a\"b" R='a\b' S=a\\b T="a\$b\`c"⏎
osrel	ÄÖ=Ü ID=Mixed_Case⏎
# lsb_release -a text.
lsb	Distributor ID:⇥Ubuntu⏎Description:⇥Ubuntu 22.04.3 LTS⏎Release:⇥22.04⏎Codename:⇥jammy⏎
lsb	No colon here⏎Key: value: with: colons⏎ Spaced Key :  padded  ⏎:empty key⏎
lsb	∅
# uname -rs text.
uname	Linux 5.15.0-91-generic
uname	FreeBSD 14.0-RELEASE-p3⏎ignored second line
uname	SunOS 5.11
uname	  NetBSD   9.3␣␣
uname	HP-UX B.11.31
uname	∅
# The command line.
cli	--root-dir	data/roots/ubuntu2204
cli	-r	data/roots/centos5
cli	--json	--root-dir	data/roots/fedora39
cli	-j	-r	data/roots/quirky
cli	-r	data/roots/empty	-j
cli	--root-dir=data/roots/sles12
cli	-jr	data/roots/mint21
"""

if __name__ == "__main__":
    for path, text in FILES.items():
        p = os.path.join("data/roots", path)
        if text is None:
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
    with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
        fh.write(JOBS.lstrip("\n"))
