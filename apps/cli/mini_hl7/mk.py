# Writes data/: the HL7 v2 feeds of a hospital interface engine for one
# morning at Riverside General (all people, numbers and codes invented),
# and jobs.txt, the list of jobs oracle.py and mini_hl7.kara run.
import os

R = "\r"


def msg(*segs):
    return R.join(segs) + R


ADT = msg(
    "MSH|^~\\&|PAS|RIVERSIDE|IE|RIVERSIDE|20261021083000||ADT^A01^ADT_A01|MSG00001|P|2.5.1",
    "EVN|A01|20261021083000",
    "PID|1||RG100234^^^RIVERSIDE^MR~9434765919^^^NHS^NH||Okafor^Adaeze^Ngozi^^Ms||19840312|F|||"
    "14 Mill Lane^Flat 2&Rear^Exeter^^EX1 1AA^GBR||01632 960142~07700 900461|||M",
    "PV1|1|I|WARD7^B12^1^RIVERSIDE||||C3456^Hale^Morgan^^^Dr|||MED||||7|||C3456^Hale^Morgan^^^Dr"
    "|IN|V9001|||||||||||||||||||||||||20261021082500",
    "NK1|1|Okafor^Chidi|SPO^Spouse|14 Mill Lane^^Exeter^^EX1 1AA|01632 960143",
    "AL1|1|DA|PEN^Penicillin \\T\\ derivatives^L|SV|Rash \\F\\ swelling~Wheeze",
)

LAB = msg(
    "MSH|^~\\&|LIMS|RIVERSIDE-LAB|IE|RIVERSIDE|20261021101500+0100||ORU^R01^ORU_R01|LAB7781|P|2.5.1",
    "PID|1||RG100234^^^RIVERSIDE^MR||Okafor^Adaeze",
    "ORC|RE|ORD5512|LAB7781",
    "OBR|1|ORD5512|LAB7781|CBC^Full blood count^L|||20261021091000",
    "OBX|1|NM|718-7^Haemoglobin^LN||118|g/L|120-150|L|||F",
    "OBX|2|NM|6690-2^WBC^LN||13.2|10*9/L|4.0-11.0|H|||F",
    "OBX|3|NM|777-3^Platelets^LN||250|10*9/L|150-400|N|||F",
    "NTE|1||Mild anaemia.\\.br\\Repeat in \\H\\2 weeks\\N\\.\\.sp2\\Reviewed by \\X44\\r Hale\\Zpg\\",
    "OBR|2|ORD5513|LAB7782|UE^Urea and electrolytes^L|||20261021091000",
    "OBX|4|NM|2951-2^Sodium^LN||139|mmol/L|133-146||||F",
    "OBX|5|NM|2823-3^Potassium^LN||5.9|mmol/L|3.5-5.3|HH|||F",
    "OBX|6|ST|COMM^Comment^L||Haemolysed sample \\E\\ retest~Second sample requested||||||F",
    "OBX|7|TX|COMM^Comment^L||See note:\\.in2\\indented \\X20AC\\5 fee||||||P",
    "NTE|2||Called to ward 7 at 10:12\\.sk3\\(read back)",
)

DISCHARGE = msg(
    "MSH|^~\\&|PAS|RIVERSIDE|IE|RIVERSIDE|20261021113000||ADT^A03^ADT_A03|MSG00002|P|2.5.1",
    "PID|1||RG100871^^^RIVERSIDE^MR||Brennan^Siobhan||19510627|F",
    "PV1|1|I|WARD3^A04^2^RIVERSIDE||||C2211^Osei^Kwame^^^Dr|||SUR||||||||IN|V8812"
    "|||||||||||||||||||||||||20261019140000|20261021112000",
)

UPDATE = msg(
    "MSH|^~\\&|PAS|RIVERSIDE|IE|RIVERSIDE|20261021114500||ADT^A08^ADT_A01|MSG00003|P|2.5.1",
    "PID|1||RG100234^^^RIVERSIDE^MR||Okafor^Adaeze^Ngozi^^Dr||19840312|F",
    "PV1|1|I|WARD7^B14^1^RIVERSIDE",
)

SIU = msg(
    "MSH|^~\\&|THEATRE|RIVERSIDE|IE|RIVERSIDE|20261021115000||SIU^S12^SIU_S12|THR0042|P|2.5.1",
    "SCH|1|THR0042||||ROUTINE",
)

NOPID = msg(
    "MSH|^~\\&|PAS|RIVERSIDE|IE|RIVERSIDE|20261021115500||ADT^A01^ADT_A01|MSG00004|P|2.5.1",
    "EVN|A01|20261021115500",
    "PV1|1|E|ED^R3",
)

QRY = msg(
    "MSH|^~\\&|OLDSYS|ANNEX|IE|RIVERSIDE|20261021120000||QRY|Q0001|P|2.3",
    "QRD|20261021120000|R|I|Q0001",
)

ZOE = msg(
    "MSH|^~\\&|PAS|RIVERSIDE|IE|RIVERSIDE|20261021121000||ADT^A01^ADT_A01|MSG00005|P|2.5.1",
    "PID|1||RG101502^^^RIVERSIDE^MR||Lefèvre^Zoë||19990101|F",
    "PV1|1|I|WARD7^B03^1^RIVERSIDE||||C3456^Hale^Morgan^^^Dr|||MED||||||||IN|V9015"
    "|||||||||||||||||||||||||20261021120500",
)

CUSTOM = msg(
    "MSH*:@!$*PAS*ANNEX*IE*RIVERSIDE*20261021090000-0330**ADT:A08*CUS0001*P*2.4",
    "PID*1**AX5521:::ANNEX:MR@NH778:::NHS**Ng:Wei Ling**19770804*F***Unit 4$Block C:Dock Rd:Cardiff",
    "OBX*1*ST*NOTE**Pay 5!F!10 !T! 20!S!x!R!y!E!z",
)

SHORT = msg(
    "MSH|^~|LEGACY|ANNEX|IE|RIVERSIDE|2026102109||ADT^A04|LEG001|P|2.1",
    "PID|1||L77^^^ANNEX||Price^Owen&Jr~Price^O",
)

DUPE = msg(
    "MSH|^^\\&|DUPE|ANNEX|IE|RIVERSIDE|20261021||ADT^A04|DUP01|P|2.3",
    "PID|1||D1",
)

EDGE = {
    "e_pid_first.hl7": "PID|1||X1\rMSH|^~\\&|A",
    "e_bare.hl7": "MSH",
    "e_one_sep.hl7": "MSH|",
    "e_no_end.hl7": "MSH|^~\\&",
    "e_empty_seg.hl7": "MSH|^~\\&|A|B\r\rPID|1|X2\r",
    "e_ws.hl7": "\n  MSH|^~\\&|A|B\rPID|1|X3^Y\r\n\n",
    "e_empty.hl7": "",
    "e_lower.hl7": "msh|^~\\&|A|B\r",
    "e_negative.hl7": "MSH|^~\\&|A|B|C|D|2026||ADT^A01|N1|P|2.5\rPID|1||N1~N2^x&y|z\r",
}

BHS = "BHS|^~\\&|LIMS|RIVERSIDE-LAB|IE|RIVERSIDE|20261021120000||||BATCH01"
B1 = msg(
    "MSH|^~\\&|LIMS|RIVERSIDE-LAB|IE|RIVERSIDE|20261021115900||ORU^R01|LAB7790|P|2.5.1",
    "PID|1||RG100871^^^RIVERSIDE^MR||Brennan^Siobhan",
    "OBX|1|NM|2160-0^Creatinine^LN||88|umol/L|45-84|H|||F",
)
B2 = msg(
    "MSH|^~\\&|LIMS|RIVERSIDE-LAB|IE|RIVERSIDE|20261021115930||ORU^R01|LAB7791|P|2.5.1",
    "PID|1||RG101502^^^RIVERSIDE^MR||Lefevre^Zoe",
    "OBX|1|NM|2345-7^Glucose^LN||6.1|mmol/L|3.0-7.8|N|||F",
)
B3 = msg(
    "MSH|^~\\&|RAD|RIVERSIDE|IE|RIVERSIDE|20261021123000||ORU^R01|RAD0301|P|2.5.1",
    "PID|1||RG100234^^^RIVERSIDE^MR||Okafor^Adaeze",
    "OBX|1|TX|CXR^Chest X-ray^L||No consolidation.\\.br\\Heart size normal.||||||F",
)


def lf(text, end):
    return text.replace(R, end)


BATCH = BHS + R + B1 + B2 + "BTS|2" + R
FILES = {
    "adt.hl7": ADT,
    "lab.hl7": LAB,
    "discharge.hl7": DISCHARGE,
    "custom.hl7": CUSTOM,
    "short.hl7": SHORT,
    "dupe.hl7": DUPE,
    "batch.hl7": BATCH,
    "batch_crlf.hl7": lf(BATCH, "\r\n"),
    "batch_lf.hl7": lf(BATCH, "\n"),
    "batch_nobhs.hl7": B1 + B2,
    "batch_nobts.hl7": BHS + R + B1 + B2,
    "batch_twobhs.hl7": BHS + R + B1 + BHS + R + B2,
    "batch_orphan.hl7": BHS + R + "PID|1||X9" + R + B1 + "BTS|1" + R,
    "batch_btsbts.hl7": BHS + R + B1 + "BTS|1" + R + "BTS|9" + R,
    "file.hl7": "FHS|^~\\&|IE|RIVERSIDE|ARCHIVE|RIVERSIDE|20261021130000||||FILE01" + R
    + BATCH
    + "BHS|^~\\&|RAD|RIVERSIDE|IE|RIVERSIDE|20261021123500||||BATCH02" + R + B3 + "BTS|1" + R
    + ADT
    + "FTS|2" + R,
    "file_nofts.hl7": "FHS|^~\\&|IE|RIVERSIDE" + R + B1 + B3,
    "file_twofhs.hl7": "FHS|^~\\&|IE" + R + "FHS|^~\\&|IE" + R + B1,
    "file_bhs_open.hl7": "FHS|^~\\&|IE" + R + BHS + R + B1 + BHS + R + B2,
    "file_orphan.hl7": "FHS|^~\\&|IE" + R + BHS + R + "OBX|1|X" + R + B1 + "BTS|1" + R,
    "file_free_orphan.hl7": "FHS|^~\\&|IE" + R + "OBX|1|X" + R + B1,
}
FILES.update(EDGE)

SB, EB, CR, FF = "\x0b", "\x1c", "\r", "\x0c"


def frame(m):
    return SB + m + EB + CR


INBOUND = [ADT, LAB, DISCHARGE, UPDATE, SIU, NOPID, QRY, ZOE]
BIN = {
    "inbound.mllp": "".join(frame(m) for m in INBOUND).encode("utf-8"),
    "ff.mllp": (FF.join(SB + m for m in [ADT, DISCHARGE, UPDATE]) + FF).encode(),
    "broken.mllp": (frame(DISCHARGE) + SB + UPDATE[:60]).encode(),
    "badblock.mllp": (frame(SIU) + UPDATE + EB + CR + frame(QRY) + "\x0bMSH|^~\\&|X\xff").encode("latin-1"),
    "mixed.mllp": (frame(SIU) + SB + "MSH|^~\\&|A|B\rPID|1||\xc3A" + EB + CR).encode("latin-1")
    + frame(ZOE).encode("utf-8")
    + (SB + "MSH|^~\\&|A|B\rPID|1||\xff" + EB + CR).encode("latin-1")
    + (SB + "NOT HL7" + EB + CR + "trailing").encode(),
    "loose.txt": ("# export from LIMS, 21 Oct\r\n" + lf(B1, "\r\n") + "\r\n" + lf(B2, "\n")
                  + "  \x1c\r\n" + lf(B3, "\r\n")).encode(),
    "loose_clean.txt": (lf(SIU, "\n") + lf(QRY, "\n")).encode(),
}

DTM = [
    "2026", "202610", "20261021", "2026102108", "202610210830", "20261021083000",
    "20261021083005.1234", "20261021083005.0000005", "20261021083000+0100",
    "20261021083000-0330", "20261021083000-0030", "20261021083000+0000",
    "20261021+0530", "2026102108+05", "20261021083059.9999999", "202",
    "", "abc", "2026023012", "20261321", "00001021", "2026102124", "202610210860",
    "20261021083060", "2026102114.5", "202610211430.5", "202.5", "20261021083000+2500",
    "19840312", "20261021083000.5+0100", "2026-10-21",
]

ESCAPES = [
    "plain text", "a|b^c~d&e\\f", "line1\rline2", "tab\there", "café", "price €5",
    "new\nline", "", "\\F\\\\S\\", "x\\.br\\y\\.sp3\\z\\.in1\\w", "\\H\\bold\\N\\ text",
    "hex \\X41424344\\ \\X 9\\ \\X41G\\ \\XABC\\", "\\Zcustom\\ \\Cxx\\ \\Myyy\\ \\\\",
    "\\.spX\\", "\\.ce\\\\.fi\\\\.nf\\\\.ti2\\\\.sk\\", "no end \\F",
]

JOBS = """\
tree adt.hl7
tree lab.hl7
tree discharge.hl7
tree custom.hl7
tree short.hl7
tree dupe.hl7
tree e_pid_first.hl7
tree e_bare.hl7
tree e_one_sep.hl7
tree e_no_end.hl7
tree e_empty_seg.hl7
tree e_ws.hl7
tree e_empty.hl7
tree e_lower.hl7
tree e_negative.hl7
tree batch.hl7
tree batch_crlf.hl7
tree batch_lf.hl7
tree batch_nobhs.hl7
tree batch_nobts.hl7
tree batch_twobhs.hl7
tree batch_orphan.hl7
tree batch_btsbts.hl7
tree file.hl7
tree file_nofts.hl7
tree file_twofhs.hl7
tree file_bhs_open.hl7
tree file_orphan.hl7
tree file_free_orphan.hl7
batchof adt.hl7
fileof batch_nobhs.hl7
get adt.hl7 PID PID.3 PID.F3.R2 PID.3.2 PID.3.2.1 PID.3.2.4 PID.3.1.5 PID.5 PID.5.1.2 PID.F11.R1.C2.S2 PID.11.1.2.1 PID.11.1.2.3 PID.11.1.9 PID.11.1.9.2 PID.13.2 PID.13.3 PID.99 PID.99.1.1 PID.99.2 PID.3.1.2.2 PID.5.1.1.2 PID.5.3 MSH.1 MSH.2 MSH.9.1.2 MSH.9 MSH.F1.R1.C2 AL1.3.1.2 AL1.5 AL1.5.2 PV1.3.1.2 ZZZ ZZZ.1 PID2.3 PID0.3 PID.0 PID.-1 PID.-1.1 PI PID..2 PID.Fx PIDX.3 PID.F3.R0.C0
get lab.hl7 OBX OBX2.5 OBX5.8 OBX6.5 OBX6.5.2 OBX7.5 NTE.3 NTE2.3 OBR2.4.1.2 OBX8.5 OBX-1.5 OBX0.3.1.2 NTE NTE.3.1.1 NTE.3.1.2
get custom.hl7 MSH.1 MSH.2 PID.3.2 PID.3.2.1 PID.5.1.2 PID.11.1.1.2 OBX.5 MSH.9.1.2
get short.hl7 PID.3 PID.5.1.2 PID.5.1.2.2 PID.5.2
get e_empty_seg.hl7 MSH.3 PID
get e_negative.hl7 PID.-1 PID.3.-1 PID.3.2.-1 PID.3.2.2.-1 PID.-2.1 PID.-9
accessor PID PID.3 PID.F3.R2.C1.S1 OBX2.5.1 MSH.1.1 PID.r1 PID.3.c2 X ZZ9.1 PID.F3.R2.C1.S1.Q7 PID.3.R
set adt.hl7 PID.5.1.2=Ada PID.F13.R3=01632 960199 PID.30=Y PID.3.2.4=NHS-E PV1.3.1.2=B14 PID.11.1.2.3=Side PID.11.1.2.1=Flat 3
set adt.hl7 ZZZ.1=x PID=nope PID.5.1=Okafor-Smith PID.5.1.1.1=Okafor PID.3.1.9.2=deep MSH.3=PAS2 PID.0=QQQ EVN.1.1.1.1=a
set adt.hl7 PID.8.1.1=M PID.8.1.2=X PID.8.1.1.2=Y PID.13.1.1.3=Z AL1.5.2.1.4=W
set short.hl7 PID.5.1.2.3=III PID.5.2.1=Pryce PID.3.1.4.1=ANNEX2
set e_negative.hl7 PID.-1=last PID.-1.1.1=w PID.-9=bad PID.3.-1.1=n PID.3.1.-1=c
assign adt.hl7 PID 1 13 - - - home
assign adt.hl7 PID 1 13 2 - - mobile
assign adt.hl7 PID 1 7 1 1 1 19840313
assign adt.hl7 PV1 1 3 1 2 1 B15
assign adt.hl7 PID 2 3 - - - x
assign adt.hl7 NK1 1 - - - - x
assign adt.hl7 PID 1 40 1 2 3 deep
idx adt.hl7 0 1 -1 2:4 9 -9
escape adt.hl7 -
escape adt.hl7 H=<b>,N=</b>,Zcustom=[c],.sp=_,F=(bar),Cxx=?
escape custom.hl7 -
escape dupe.hl7 -
escapeout adt.hl7 -
escapeout adt.hl7 |=PIPE,é=e,<CR>=BR
escapeout custom.hl7 -
escapeout dupe.hl7 -
dtm
ack adt.hl7 AA ACK00001 - -
ack lab.hl7 AE - IE-ACK RIVERSIDE-IE
ack custom.hl7 CA C1 - -
ack short.hl7 AR - - -
ack e_pid_first.hl7 AA - - -
ack e_negative.hl7 AA x - -
ack e_empty_seg.hl7 AA x - -
mcid 3
split file.hl7
split batch_lf.hl7
split e_pid_first.hl7
split e_empty.hl7
is adt.hl7 lab.hl7 batch.hl7 batch_nobhs.hl7 file.hl7 e_ws.hl7 e_empty.hl7 e_lower.hl7 file_nofts.hl7 custom.hl7
stream inbound.mllp 4096
stream inbound.mllp 64
stream ff.mllp 4096
stream ff.mllp 100
stream broken.mllp 4096
stream badblock.mllp 4096
loose loose.txt
loose loose_clean.txt
loose inbound.mllp
blocks inbound.mllp 65536 -
blocks inbound.mllp 65536 utf-8
blocks inbound.mllp 300 utf-8
blocks badblock.mllp 65536 -
blocks mixed.mllp 65536 -
blocks mixed.mllp 65536 utf-8
blocks mixed.mllp 65536 utf-8,replace
blocks ff.mllp 65536 -
blocks broken.mllp 40 -
route inbound.mllp
reencode adt.hl7 *:@!$
reencode custom.hl7 |^~\\&
reencode lab.hl7 #^~\\&
audit file.hl7
"""


def main():
    os.makedirs("data/out", exist_ok=True)
    for name, text in FILES.items():
        with open(os.path.join("data", name), "w", newline="") as f:
            f.write(text)
    for name, data in BIN.items():
        with open(os.path.join("data", name), "wb") as f:
            f.write(data)
    with open("data/dtm.txt", "w") as f:
        f.write("".join(v + "\n" for v in DTM))
    with open("data/escapes.txt", "w", newline="") as f:
        # one value per line, with \r, \n and \t written as \\r, \\n, \\t
        for v in ESCAPES:
            f.write(v.replace("\r", "<CR>").replace("\n", "<LF>").replace("\t", "<TAB>") + "\n")
    with open("data/jobs.txt", "w") as f:
        f.write(JOBS)


main()
