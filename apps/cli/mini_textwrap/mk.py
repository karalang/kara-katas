#!/usr/bin/env python3
"""Writes data/: four text files and data/jobs.tsv.

A job is one line of tab-separated fields. In a field, "⏎" stands for a
newline, "⇥" for a tab, "¤" for a no-break space, "␍" for a carriage
return, "␋" for a vertical tab and "␌" for a form feed. A field that
starts with "@" names a file in data/.
"""
import os

os.makedirs("data", exist_ok=True)

FILES = {
    "commit.txt": (
        "Fix the off-by-one in the ring buffer's wrap-around logic -- the "
        "reader could observe a half-written slot when the writer lapped it. "
        "This affects every multi-producer queue built on top of it, e.g. the "
        "log shipper and the metrics pipeline.  See "
        "https://example.org/issues/4711-ring-buffer-wraparound-race for the "
        "full write-up.\n\nReviewed-by: A. N. Other <another@example.org>\n"
    ),
    "docstring.txt": (
        "    Parse a configuration file.\n"
        "\n"
        "    The file is read line by line; each line is either a comment,\n"
        "    a section header or a key-value pair.\n"
        "      \n"
        "        Nested examples keep their extra indent.\n"
        "    \tA tab after the margin stays.\n"
        "\n"
        "    Returns a dict of dicts.\n"
    ),
    "mixed.txt": (
        "  two spaces\n"
        "\tone tab\n"
        "  \ttwo spaces then a tab\n"
        "\n"
        "  back to two\n"
    ),
    "tabs.txt": (
        "name\tsize\tmodified\n"
        "a.txt\t12\t2026-10-18\n"
        "longer-name.json\t4096\t2026-01-02\n"
        "x\t1\t\tdouble tab\n"
    ),
    "notes.md": (
        "Kāra's ownership model has three tiers: owned values, borrowed "
        "references and reference-counted shared values. Most code never "
        "needs the third.\n"
        "\n"
        "A long identifier like "
        "configuration_loader_with_environment_overrides_and_defaults "
        "does not fit on one line, nor does "
        "https://docs.example.org/very/long/path/to/a/page.html at all.\n"
        "\n"
        "Distances are written 10 km and 2 h; the no-break space "
        "keeps each pair together. Café, naïve and façade are words too.\n"
        "\n"
        "Short.\n"
    ),
}
for name, text in FILES.items():
    with open(os.path.join("data", name), "w") as f:
        f.write(text)

JOBS = r"""
wrap	30	-	The quick brown fox jumps over the lazy dog.
wrap	10	-	The quick brown fox jumps over the lazy dog.
wrap	1	-	abc def
wrap	3	-	abcdefgh ij
wrap	0	-	anything
wrap	-5	-	anything
wrap	20	-	
wrap	20	-	   
wrap	20	dw=0	   
wrap	20	-	  leading and trailing spaces  
wrap	20	dw=0	  leading and trailing spaces  
wrap	12	-	well-known self-contained state-of-the-art
wrap	12	boh=0	well-known self-contained state-of-the-art
wrap	8	-	well-known self-contained state-of-the-art
wrap	15	-	this is--an em-dash test--with words
wrap	15	-	a ---- b --c d-- e
wrap	10	-	x-y-z a-b-c-d-e-f-g-h-i-j
wrap	6	-	co-op re-enter -flag --opt pre--
wrap	10	-	12-34 ab-12 12-ab a1-b2
wrap	20	-	hyphen-at-the-very-end-
wrap	10	-	aaaaaaaaaaaaaaaaaaaaaaaaa
wrap	10	blw=0	aaaaaaaaaaaaaaaaaaaaaaaaa bb
wrap	10	-	aaaa-bbbb-cccc-dddd-eeee
wrap	10	boh=0	aaaa-bbbb-cccc-dddd-eeee
wrap	10	-	----------abc
wrap	7	-	--------ab-cd
wrap	20	-	one⇥two⇥⇥three
wrap	20	ts=4	one⇥two⇥⇥three
wrap	20	tabs=0	one⇥two⇥⇥three
wrap	20	tabs=0,rw=0	one⇥two⇥⇥three
wrap	20	rw=0	line one⏎line two
wrap	20	-	line one⏎line two⏎⏎line four
wrap	20	-	cr␍and␋vt␌ff
wrap	20	rw=0,tabs=0	cr␍and␋vt␌ff
wrap	25	fse=1	This is a sentence. And another! Is it? Yes.
wrap	25	fse=1	Mr. Smith met Dr. Jones. "Quoted." Ok.'
wrap	25	fse=1	end with a.  Already two. Word.⇥tab
wrap	25	fse=1,rw=0	end. next
wrap	24	ii=* ,si=  	The first line gets a bullet and the rest are indented to match it.
wrap	24	ii=>>> ,si=... 	print the value of a very long expression here
wrap	10	ii=0123456789	abc def
wrap	10	ii=012345678901	abc def
wrap	15	ml=2	one two three four five six seven eight nine
wrap	15	ml=1	one two three four five six seven eight nine
wrap	15	ml=1	one two three
wrap	15	ml=2,ph= ...	one two three four five six seven eight nine
wrap	15	ml=2,ph=…	one two three four five six seven eight nine
wrap	10	ml=1,ph= [...]	verylongwordthatbreaks here
wrap	5	ml=1	abcdefghij
wrap	6	ml=2,ph=[...]	ab cd ef gh ij
wrap	10	ml=2,ph=  [more]	alpha beta gamma delta epsilon
wrap	10	ml=1,ph=xxxxxxxxxxx	a
wrap	10	ml=2,si=    ,ph=......	a b c
wrap	12	ml=3	short   lines   with   gaps   between   them   all
wrap	12	ml=3,dw=0	short   lines   with   gaps   between   them   all
wrap	18	-	10¤km and 2¤h are pairs; ¤ alone
wrap	16	-	Café naïve façade Ünïcode-wörds über-schön
wrap	40	-	@commit.txt
wrap	72	fse=1	@commit.txt
wrap	50	ii=- ,si=  ,boh=0	@notes.md
wrap	33	ml=4	@notes.md
fill	30	-	The quick brown fox jumps over the lazy dog.
fill	16	ii=# ,si=# 	a comment that wraps over several lines
fill	20	-	
shorten	12	-	Hello  world!
shorten	11	-	Hello  world!
shorten	30	-	   lots   of   space	and⇥tabs⏎and newlines   
shorten	15	ph=…	The quick brown fox jumps over the lazy dog.
shorten	15	ph= (more)	The quick brown fox jumps over the lazy dog.
shorten	6	-	Hello world
shorten	5	-	Hello world
shorten	4	ph=..	abcdefgh
shorten	60	-	@commit.txt
shorten	10	blw=0	supercalifragilistic word
dedent	@docstring.txt
dedent	@mixed.txt
dedent	@notes.md
dedent	    a⏎      b⏎    c
dedent	  a⏎⇥b
dedent	⏎   ⏎   x⏎   y⏎ 
dedent	   only⏎   
dedent	
dedent	  ␍⏎  x
indent	> 	-	@docstring.txt
indent	> 	all	@mixed.txt
indent	  	-	one⏎⏎   ⏎two
indent	# 	all	one⏎⏎   ⏎two
indent	* 	-	cr␍line␍⏎crlf␍⏎ff␌end
indent	| 	-	
indent	| 	all	no newline at end
fmt	50	@notes.md
fmt	30	@commit.txt
fmt	20	@tabs.txt
"""
with open("data/jobs.tsv", "w") as f:
    f.write(JOBS.lstrip("\n"))
