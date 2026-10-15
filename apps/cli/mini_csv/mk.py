# Writes the inputs of mini_csv into data/.
import os, shutil

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data/sniff")

def put(name, text):
    with open("data/" + name, "w", encoding="utf-8", newline="") as f:
        f.write(text)

# An Excel export: CRLF, quoted commas, doubled quotes, a CRLF inside a
# field, a blank line and non-ASCII names.
put("contacts.csv",
    "name,email,phone,notes\r\n"
    "\"Smith, Jane\",jane@example.org,555-0100,\"Prefers \"\"JD\"\"\"\r\n"
    "Bob Ng,bob@example.org,,\"Line one\r\nline two\"\r\n"
    "\"Ünal Çelik\",unal@example.org,+90 555 0101,\r\n"
    "\r\n"
    "Lee,lee@example.org,555-0102,trailing  \r\n")

put("inventory.tsv",
    "sku\tname\tqty\tlocation\n"
    "A-100\tWidget, large\t12\tAisle 3\n"
    "A-101\t\"Gadget\" (blue)\t0\t\n"
    "B-200\tSpanner\t7\tAisle 1\tovershoot\n")

put("prices_eu.csv",
    "sku;name;price;qty\n"
    "K-1;\"Kaffee; gemahlen\";12,50;3\n"
    "K-2;Tee;3,99;10\n"
    "K-3;\"Zucker \"\"fein\"\"\";1,25;\n")

put("survey.csv",
    "id, answer, score\n"
    "1, \"yes, mostly\", 4\n"
    "2, no, 2\n"
    "3,   \"spaced\"  , 5\n")

put("escaped.txt",
    "path|desc\n"
    "C:\\\\temp|has \\| pipe\n"
    "line\\\ncontinued|x\n"
    "\"quoted\"|kept\n")

put("numbers.csv",
    "\"label\",1,2.5,-3\n"
    "\"pi\",3.14159,,1e3\n"
    "\"empty\",\"\",0,\n")

put("nulls.csv",
    "\"a\",,1,\"\"\n"
    ",\"x\",,2.50\n")

put("after_quote.csv", "a,\"b\"c,d\n1,2,3\n")
put("eof_quote.csv", "a,\"unterminated\nfield")
put("cr_mid.csv", "a,b\rc,d\nnext,row\n")
put("long.csv", "short,this field is far too long for the limit\n")
put("ragged.csv",
    "id,name,city\n"
    "1,Ada,London\n"
    "2,Grace\n"
    "\n"
    "3,Linus,Helsinki,Finland,extra\n"
    "4,,\n")
put("headerless.csv", "x1,10\nx2,20,spare\nx3\n")
put("dupcols.csv", "k,v,k\n1,2,3\n")

put("read-jobs.txt",
    "contacts.csv\n"
    "inventory.tsv delimiter=tab\n"
    "prices_eu.csv delimiter=semicolon\n"
    "survey.csv\n"
    "survey.csv skipinitialspace=1\n"
    "escaped.txt delimiter=pipe quoting=none escapechar=backslash\n"
    "escaped.txt delimiter=pipe escapechar=backslash\n"
    "numbers.csv quoting=nonnumeric\n"
    "nulls.csv quoting=notnull\n"
    "nulls.csv quoting=strings\n"
    "contacts.csv quotechar=none\n"
    "survey.csv quotechar=squote skipinitialspace=1\n"
    "after_quote.csv\n"
    "after_quote.csv strict=1\n"
    "after_quote.csv doublequote=0\n"
    "eof_quote.csv\n"
    "eof_quote.csv strict=1\n"
    "cr_mid.csv source=text\n"
    "cr_mid.csv\n"
    "long.csv limit=16\n"
    "numbers.csv quoting=nonnumeric delimiter=semicolon\n"
    "nulls.csv quoting=nonnumeric\n")

put("write-jobs.txt",
    "\n"
    "quoting=all\n"
    "quoting=nonnumeric\n"
    "quoting=strings\n"
    "quoting=notnull\n"
    "quoting=none escapechar=backslash\n"
    "quoting=none\n"
    "doublequote=0 escapechar=backslash\n"
    "doublequote=0\n"
    "delimiter=semicolon lineterminator=lf\n"
    "delimiter=tab quotechar=squote\n"
    "delimiter=space skipinitialspace=1\n"
    "lineterminator=semicolon\n")

# Sniffer samples.
put("sniff/plain.txt", "city,population,area\nOslo,709037,454.0\nBergen,291940,465.3\nTromso,77544,2521.0\n")
put("sniff/quoted.txt", "'id';'title';'year'\n1;'Dune';1965\n2;'It''s here';2001\n3;'Solaris';1961\n")
put("sniff/spaced.txt", "name, \"role\", age\nAnn, \"dev, lead\", 41\nBo, \"ops\", 29\n")
put("sniff/tabs.txt", "date\tlevel\tmessage\n2026-10-01\tINFO\tstarted\n2026-10-01\tWARN\tdisk at 91%\n2026-10-02\tINFO\tstopped\n")
put("sniff/pipes.txt", "a|b|c\n1|2|3\n4|5|6\n7|8|9\n")
put("sniff/oneword.txt", "hello\nworld\nagain\n")
put("sniff/noheader.txt", "10,20,30\n40,50,60\n70,80,90\n")
put("sniff/colons.txt", "root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\nbin:x:2:2:bin:/bin:/usr/sbin/nologin\n")
put("sniff/dq.txt", "\"name\",\"quote\"\n\"Ann\",\"She said \"\"hi\"\"\"\n\"Bo\",\"none\"\n")
put("sniff/mixed.txt", "x;y,z\n1;2,3\n4;5,6\n")
put("sniff/onecol.txt", "\"alpha\"\n\"beta\"\n\"gamma\"\n")
put("sniff/lengths.txt", "code,label\nAB,first\nCD,second\nEF,third\n")
put("sniff/complex.txt", "re,im\n1+2j,3\n-4.5e1,inf\nnan,7j\n")

# The export the report is built from: a European shop system's orders.
put("orders.csv",
    "Bestellung;Datum;Land;Kunde;Betrag;Status\r\n"
    "1001;2026-10-01;DE;\"Müller GmbH\";1.234,50;bezahlt\r\n"
    "1002;2026-10-01;AT;\"Gruber; Söhne\";89,90;bezahlt\r\n"
    "1003;2026-10-02;DE;\"Schmidt \"\"Bau\"\"\";450,00;offen\r\n"
    "1004;2026-10-02;CH;Keller AG;2.100,00;bezahlt\r\n"
    "1005;2026-10-03;DE;Weber;12,05;storniert\r\n"
    "1006;2026-10-03;AT;\"Hofer\r\nFiliale 2\";310,40;bezahlt\r\n"
    "1007;2026-10-04;CH;Zürcher;-15,00;erstattet\r\n")
