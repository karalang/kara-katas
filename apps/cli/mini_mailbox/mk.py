# Writes data/: the mailboxes a mail client finds on disk -- an mbox
# inbox, an MMDF archive, an Emacs Rmail (Babyl) file, a Maildir tree with
# Maildir++ folders and an MH tree -- some raw messages to deliver, and
# data/jobs.tsv, what mini_mailbox does with them.
import os

os.makedirs("data", exist_ok=True)


def put(path, text):
    path = os.path.join("data", path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="ascii", newline="") as f:
        f.write(text)


def mail(frm, to, subject, date, mid, body, extra=(), ctype=None):
    h = [("From", frm), ("To", to), ("Subject", subject), ("Date", date),
         ("Message-ID", mid)]
    h.extend(extra)
    if ctype:
        h.append(("MIME-Version", "1.0"))
        h.append(("Content-Type", ctype))
    return "".join(f"{k}: {v}\n" for k, v in h) + "\n" + body


ANA = "Ana Lima <ana.lima@example.org>"
RAVI = '"Ravi K." <ravi@example.com>'
OPS = "ops@example.net"
MEI = "Mei Chen <mei@example.net>"
BOT = "CI Bot <ci@builds.example.net>"

DEPLOY = mail(ANA, OPS, "Deploy window moved to Thursday",
              "Mon, 19 Oct 2026 14:30:02 +0200", "<deploy-1@example.org>",
              "Hi all,\n\nThe deploy window moves to Thursday 09:00 UTC.\n\n"
              ">From now on, deploys need two approvals.\n\n-- Ana\n")
CAFE = mail(RAVI, OPS, "=?utf-8?q?Caf=C3=A9_budget_Q4?=",
            "Tue, 20 Oct 2026 08:05:44 +0530", "<cafe-q4@example.com>",
            "Budget for the team cafe is attached in the shared drive.\n",
            extra=[("Status", "RO"), ("X-Status", "A")])
REPORT = mail(BOT, OPS, "Nightly build #4412 failed",
              "Wed, 21 Oct 2026 02:10:00 GMT", "<build-4412@builds.example.net>",
              "This is a multi-part message in MIME format.\n"
              "--=_b4412\nContent-Type: text/plain; charset=us-ascii\n\n"
              "3 tests failed on linux-arm64.\n\n"
              "--=_b4412\nContent-Type: text/csv; name=\"failures.csv\"\n"
              "Content-Transfer-Encoding: base64\n"
              "Content-Disposition: attachment; filename=\"failures.csv\"\n\n"
              "dGVzdCxzZWNvbmRzCmh0dHBfa2VlcGFsaXZlLDEyLjQKdGxzX3Jlc3VtZSwwLjgK\n\n"
              "--=_b4412--\n",
              extra=[("Status", "O")],
              ctype='multipart/mixed; boundary="=_b4412"')
SHELL = mail(MEI, OPS, "How to rotate the logs",
             "Wed, 21 Oct 2026 11:47:19 -0700", "<logs-howto@example.net>",
             "Steps for the new log host:\n\n"
             "From the shell, run:\n\n    logrotate -f /etc/logrotate.conf\n\n"
             "and check /var/log/app.\n")
LUNCH = mail(RAVI, "mei@example.net", "Re: lunch?",
             "Thu, 22 Oct 2026 12:01:00 +0530", "<lunch-2@example.com>",
             "Sure, 1pm works.\n",
             extra=[("In-Reply-To", "<lunch-1@example.net>"),
                    ("Status", "R")])
INVOICE = mail("billing@vendor.example", OPS, "Invoice 2026-10 for ops",
               "Fri, 23 Oct 2026 07:00:00 +0000", "<inv-2026-10@vendor.example>",
               "Amount due: 1,250.00 EUR\nDue date: 2026-11-15\n")
OLD = mail(ANA, OPS, "Q2 retro notes",
           "Thu, 02 Jul 2026 16:00:00 +0200", "<retro-q2@example.org>",
           "Notes from the Q2 retro are in the wiki.\n",
           extra=[("Status", "RO")])
OLDER = mail(MEI, OPS, "On-call rota for June",
             "Mon, 1 Jun 2026 09:30:00 -0700", "<rota-june@example.net>",
             "Rota attached in the wiki, swap requests by Friday.\n")
MARCH = mail(BOT, OPS, "Nightly build #3100 passed",
             "Sun, 15 Mar 2026 02:10:00 GMT", "<build-3100@builds.example.net>",
             "All 812 tests passed.\n")


def envelope(addr, date):
    return f"From {addr} {date}\n"


# The inbox: a blank line between messages, except before LUNCH. The log
# how-to was delivered by a mailer that did not quote its "From the shell"
# line, so that line starts a message of its own.
put("mail/inbox.mbox",
    envelope("ana.lima@example.org", "Mon Oct 19 12:30:02 2026") + DEPLOY + "\n"
    + envelope("ravi@example.com", "Tue Oct 20 02:35:44 2026") + CAFE + "\n"
    + envelope("ci@builds.example.net", "Wed Oct 21 02:10:00 2026") + REPORT + "\n"
    + envelope("mei@example.net", "Wed Oct 21 18:47:19 2026") + SHELL
    + envelope("ravi@example.com", "Thu Oct 22 06:31:00 2026") + LUNCH + "\n"
    + envelope("billing@vendor.example", "Fri Oct 23 07:00:00 2026") + INVOICE + "\n"
    + envelope("ana.lima@example.org", "Thu Jul  2 14:00:00 2026") + OLD)

# An MMDF archive. The second message was written by MMDF itself, with no
# From_ line; the last one has lost its closing marker.
M = "\x01\x01\x01\x01\n"
put("mail/archive.mmdf",
    M + envelope("mei@example.net", "Mon Jun  1 16:30:00 2026") + OLDER + "\n" + M
    + M + "Return-Path: <ci@builds.example.net>\n" + MARCH + "\n" + M
    + M + envelope("ana.lima@example.org", "Thu Jul  2 14:00:00 2026") + OLD)

# An Rmail file. Each message keeps its original header block, then the
# headers Rmail shows, then the body.
def babyl_msg(labels, orig, visible, body):
    return "\x0c\n" + labels + "\n" + orig + "\n*** EOOH ***\n" + visible + "\n" + body + "\n\x1f"


def split(m):
    i = m.index("\n\n")
    return m[:i + 1], m[i + 2:]


h1, b1 = split(DEPLOY)
h2, b2 = split(INVOICE)
h3, b3 = split(OLD)
put("mail/RMAIL",
    "BABYL OPTIONS:\nVersion: 5\nLabels:billing\n\x1f"
    + babyl_msg("1, unseen,,", h1,
                "Date: Mon, 19 Oct 2026 14:30:02 +0200\nFrom: " + ANA
                + "\nSubject: Deploy window moved to Thursday\n", b1)
    + babyl_msg("1,, billing,", h2, h2, b2)
    + babyl_msg("1, answered, deleted,,", h3, "", b3))

# A Maildir with flags in the file names, Maildir++ folders, a dot file
# and a half-delivered message in tmp/.
MD = "mail/Maildir/"
put(MD + "cur/1760870000.M100P200Q1.mx1:2,S", DEPLOY)
put(MD + "cur/1760870100.M101P200Q2.mx1:2,FRS", CAFE)
put(MD + "cur/1760870200.M102P200Q3.mx1:2,ST", OLD)
put(MD + "cur/.keep", "")
put(MD + "new/1760870300.M103P200Q4.mx1", REPORT)
put(MD + "new/1760870400.M104P200Q5.mx1:2,", INVOICE)
put(MD + "tmp/1760870500.M105P200Q6.mx1", "Subject: half\n\n")
put(MD + ".Lists/maildirfolder", "")
put(MD + ".Lists/cur/1760870600.M106P200Q7.mx1:2,S", OLDER)
put(MD + ".Lists/new/.keep", "")
put(MD + ".Lists/tmp/.keep", "")
put(MD + ".Lists.python/maildirfolder", "")
put(MD + ".Lists.python/cur/.keep", "")
put(MD + ".Lists.python/new/1760870700.M107P200Q8.mx1", MARCH)
put(MD + ".Lists.python/tmp/.keep", "")
put(MD + ".Archive/cur/.keep", "")
put(MD + ".Archive/new/.keep", "")
put(MD + ".Archive/tmp/.keep", "")
put(MD + ".Archive/.uidvalidity", "1760000000\n")
put(MD + ".Trash/cur/.keep", "")
put(MD + ".Trash/new/1760870800.M108P200Q9.mx1", LUNCH)
put(MD + ".Trash/tmp/.keep", "")
put(MD + ".Old/cur/.keep", "")
put(MD + ".Old/new/.keep", "")
put(MD + ".Old/tmp/.keep", "")
put(MD + ".Old/attic/.keep", "")
put(MD + "courierimapkeywords/.keep", "")

# An MH tree. inbox has a gap at 4; imported was copied in by hand and one
# file is "007"; bad has a broken .mh_sequences.
put("mail/MH/inbox/1", DEPLOY)
put("mail/MH/inbox/2", CAFE)
put("mail/MH/inbox/3", SHELL)
put("mail/MH/inbox/5", LUNCH)
put("mail/MH/inbox/notes.txt", "remember to pack\n")
put("mail/MH/inbox/.mh_sequences", "unseen: 2-3 5\nflagged: 1\nreplied: 3 9\n")
put("mail/MH/drafts/.mh_sequences", "")
put("mail/MH/imported/1", OLDER)
put("mail/MH/imported/4", MARCH)
put("mail/MH/imported/007", OLD)
put("mail/MH/imported/.mh_sequences", "unseen: 4 7\n")
put("mail/MH/bad/1", INVOICE)
put("mail/MH/bad/.mh_sequences", "unseen: 1\nseen 1\n")
put("mail/MH/empty/.keep", "")
put("mail/MH/.mh_profile", "Path: Mail\n")

# Raw messages to deliver.
put("raw/alert.eml", envelope("alerts@monitor.example", "Sat Oct 24 03:12:09 2026")
    + mail("Monitor <alerts@monitor.example>", OPS, "Disk 91% on db-2",
           "Sat, 24 Oct 2026 03:12:09 +0000", "<alert-77@monitor.example>",
           "db-2:/var is 91% full.\nFrom here it grows 2% a day.\n"))
put("raw/standup.eml", mail(MEI, OPS, "Standup notes",
                            "Mon, 26 Oct 2026 10:15:00 -0700", "<standup-26@example.net>",
                            "Yesterday: log host.\nToday: alerts.\n"))
put("raw/nobody.eml", envelope("nobody", "Sun Oct 25 00:00:00 2026")
    + "Subject: no blank line\nX-Note: headers only")

K0 = "1760870000.M100P200Q1.mx1"
K1 = "1760870100.M101P200Q2.mx1"
K2 = "1760870200.M102P200Q3.mx1"
K3 = "1760870300.M103P200Q4.mx1"
K4 = "1760870400.M104P200Q5.mx1"
K5 = "1760870500.M105P200Q6.mx1"

JOBS = f"""
job	mbox: read the inbox
copy	mail/inbox.mbox	work/1/inbox.mbox
open	in	mbox	work/1/inbox.mbox
len	in
keys	in
summary	in
get	in	0
get	in	2
get	in	3
get	in	4
get	in	5
bytes	in	1
bytes	in	1	from
string	in	2
string	in	4	from
bytes	in	7
get	in	9
has	in	7
has	in	12
digest	in

job	mbox: mark read and rewrite
copy	mail/inbox.mbox	work/2/inbox.mbox
open	in	mbox	work/2/inbox.mbox
flag	in	0	add	R
flag	in	0	add	O
flag	in	1	remove	A
flag	in	6	set	RFAx
flag	in	2	remove	O
flag	in	5	remove	Z
remove	in	4
remove	in	4
discard	in	4
flush	in
keys	in
file	work/2/inbox.mbox
close	in
open	again	mbox	work/2/inbox.mbox
summary	again

job	mbox: deliver raw messages
copy	mail/inbox.mbox	work/3/inbox.mbox
open	in	mbox	work/3/inbox.mbox
add	in	raw/alert.eml
add	in	raw/nobody.eml
replace	in	3	raw/alert.eml
keys	in
bytes	in	8	from
bytes	in	9	from
close	in
open	again	mbox	work/3/inbox.mbox
keys	again
summary	again
get	again	3
get	again	9

job	mmdf: read the archive
copy	mail/archive.mmdf	work/4/archive.mmdf
open	ar	mmdf	work/4/archive.mmdf
len	ar
summary	ar
get	ar	1
bytes	ar	1	from
get	ar	2
string	ar	0	from

job	mmdf: archive old mail from the inbox
copy	mail/inbox.mbox	work/5/inbox.mbox
copy	mail/archive.mmdf	work/5/archive.mmdf
open	in	mbox	work/5/inbox.mbox
open	ar	mmdf	work/5/archive.mmdf
archive	in	ar	2026-10-21	mmdf
flush	in
flush	ar
keys	in
keys	ar
file	work/5/archive.mmdf
summary	in

job	babyl: read the Rmail file
copy	mail/RMAIL	work/6/RMAIL
open	rm	babyl	work/6/RMAIL
len	rm
labels	rm
summary	rm
get	rm	0
bytes	rm	0
string	rm	1
get	rm	2

job	babyl: a labelled file cannot be rewritten
copy	mail/RMAIL	work/7/RMAIL
open	rm	babyl	work/7/RMAIL
label	rm	1	add	urgent
remove	rm	2
flush	rm
keys	rm
file	work/7/RMAIL

job	babyl: a new Rmail file
copy	mail/inbox.mbox	work/8/inbox.mbox
open	in	mbox	work/8/inbox.mbox
open	nb	babyl	work/8/new.babyl
move	in	0	nb	babyl
move	in	1	nb	babyl
move	in	6	nb	babyl
file	work/8/new.babyl
label	nb	2	add	billing
label	nb	2	add	unseen
label	nb	0	remove	unseen
remove	nb	1
flush	nb
file	work/8/new.babyl
labels	nb
close	nb
open	again	babyl	work/8/new.babyl
labels	again
summary	again
string	again	2

job	mh: read the inbox
copy	mail/MH	work/9/MH
open	mh	mh	work/9/MH/inbox
keys	mh
len	mh
seqs	mh
summary	mh
get	mh	3
bytes	mh	2
get	mh	4
has	mh	5
has	mh	4
open	root	mh	work/9/MH
folders	root
keys	root

job	mh: sequences and pack
copy	mail/MH	work/10/MH
open	mh	mh	work/10/MH/inbox
seq	mh	1	add	unseen
seq	mh	2	remove	unseen
seq	mh	5	add	urgent
seqs	mh
file	work/10/MH/inbox/.mh_sequences
setseqs	mh	unseen=1,2,3,5;flagged=3;empty=;replied=5,3,2
file	work/10/MH/inbox/.mh_sequences
pack	mh
keys	mh
seqs	mh
file	work/10/MH/inbox/.mh_sequences
add	mh	raw/standup.eml
remove	mh	2
remove	mh	2
discard	mh	2
keys	mh
tree	work/10/MH/inbox

job	mh: odd folders
copy	mail/MH	work/11/MH
open	root	mh	work/11/MH
folder	root	imported	imp
keys	imp
get	imp	7
seqs	imp
pack	imp
tree	work/11/MH/imported
folder	root	bad	b
keys	b
seqs	b
get	b	1
bytes	b	1
folder	root	nope	x
rmfolder	root	empty
rmfolder	root	drafts
addfolder	root	lists	l
add	l	raw/standup.eml
seqs	l
folders	root
tree	work/11/MH

job	maildir: read
copy	mail/Maildir	work/12/Maildir
open	md	maildir	work/12/Maildir
len	md
keys	md
summary	md
get	md	{K1}
info	md	{K1}
info	md	{K3}
info	md	{K4}
get	md	nope
has	md	{K5}
has	md	{K0}
folders	md
folder	md	Lists	l
keys	l
folder	md	Lists.python	lp
summary	lp
folder	md	Nope	x

job	maildir: flags and folders
copy	mail/Maildir	work/13/Maildir
open	md	maildir	work/13/Maildir
add_flag	md	{K0}	FR
remove_flag	md	{K1}	FRS
set_flags	md	{K2}	ZSaS
remove_flag	md	{K3}	S
add_flag	md	{K3}	S
setinfo	md	{K4}
info	md	{K4}
flag	md	{K1}	add	T
flag	md	{K3}	remove	S
remove	md	{K2}
remove	md	{K2}
discard	md	{K2}
tree	work/13/Maildir
summary	md
rmfolder	md	Trash
rmfolder	md	Old
rmfolder	md	Archive
addfolder	md	Projects	p
folders	md
add	p	raw/standup.eml
len	p
unread	p
tree	work/13/Maildir/.Archive

job	convert between formats
copy	mail	work/14
open	in	mbox	work/14/inbox.mbox
open	mh	mh	work/14/MH/inbox
open	md	maildir	work/14/Maildir
open	rm	babyl	work/14/RMAIL
convert	in	1	maildir
convert	in	0	mh
convert	in	1	babyl
convert	in	2	maildir
convert	in	3	mmdf
convert	in	0	plain
convert	mh	3	mbox	redate
convert	mh	1	maildir
convert	mh	2	babyl
convert	md	{K1}	mbox	redate
convert	md	{K2}	mh
convert	md	{K3}	babyl
convert	rm	0	maildir
convert	rm	2	mbox	redate
convert	rm	1	babyl
convert	rm	0	mh

job	move the inbox into MH
copy	mail	work/15
open	in	mbox	work/15/inbox.mbox
open	dst	mh	work/15/MH/inbox
move	in	0	dst	mh
move	in	1	dst	mh
seqs	dst
file	work/15/MH/inbox/.mh_sequences
move	dst	3	in	mbox	redate
move	dst	6	in	mbox	redate
flush	in
keys	in
bytes	in	9	from

job	unread across mailboxes
copy	mail	work/16
open	in	mbox	work/16/inbox.mbox
open	ar	mmdf	work/16/archive.mmdf
open	rm	babyl	work/16/RMAIL
open	mh	mh	work/16/MH/inbox
open	md	maildir	work/16/Maildir
open	l	maildir	work/16/Maildir/.Lists
unread	in	ar	rm	mh	md	l

job	search
copy	mail	work/17
open	in	mbox	work/17/inbox.mbox
open	ar	mmdf	work/17/archive.mmdf
open	mh	mh	work/17/MH/inbox
open	md	maildir	work/17/Maildir
open	rm	babyl	work/17/RMAIL
search	in	mh	md	rm	deploy
search	in	ar	md	build
search	mh	rm	in	wiki
search	in	logrotate

job	digest
copy	mail	work/18
open	in	mbox	work/18/inbox.mbox
open	ar	mmdf	work/18/archive.mmdf
open	mh	mh	work/18/MH/inbox
digest	in
digest	ar
digest	mh

job	dedupe the MH inbox against the Maildir
copy	mail	work/19
open	md	maildir	work/19/Maildir
open	mh	mh	work/19/MH/inbox
dedupe	md	mh
pack	mh
keys	mh
seqs	mh
summary	mh

job	missing and new mailboxes
copy	raw/alert.eml	work/20/alert.eml
open	x	mbox	work/20/none.mbox	nocreate
open	y	mh	work/20/none-mh	nocreate
open	z	maildir	work/20/none-md	nocreate
open	n	mbox	work/20/new.mbox
len	n
add	n	work/20/alert.eml
remove	n	3
keys	n
open	nm	mh	work/20/newmh
add	nm	raw/standup.eml
add	nm	raw/alert.eml
seqs	nm
keys	nm
open	nd	maildir	work/20/newmd
add	nd	raw/standup.eml
len	nd
unread	nd	n	nm
open	m2	mmdf	work/20/new.mmdf
add	m2	raw/nobody.eml
file	work/20/new.mmdf
tree	work/20/newmh

job	dates
date	Mon, 19 Oct 2026 14:30:02 +0200
date	Tue, 20 Oct 2026 08:05:44 +0530
date	Wed, 21 Oct 2026 02:10:00 GMT
date	Thu, 22 Oct 2026 12:01:00 EDT
date	19 Oct 2026 14:30 -0000
date	Monday, 19-Oct-26 14:30:02 PST
date	Oct 19 2026 14:30:02
date	1 Jan 70 00:00:00 +0000
date	31 Dec 2026 23:59:60 +0000
date	2026-10-19
date	
date	Sat, 24 Oct 2026 03:12:09 +0000 (UTC)
date	Mon, 19 Oct 2026 14.30.02 +0100
date	Fri, 30 Feb 2026 10:00:00 +0000
date	Mon, 19 Oct 2026 25:61:61 +0000
date	Mon, 19 Oct 2026 14:30:02 +05:30
date	Mon,19 Oct 2026 14:30:02 -0130
date	19 October 2026 14:30:02 +0100
date	19 Oct 2026 14:30:02 z
date	Thu, 01 Jan 1970 00:00:00 +0100
"""

put("jobs.tsv", JOBS.lstrip("\n"))
