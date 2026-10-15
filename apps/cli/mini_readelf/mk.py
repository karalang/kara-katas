# Builds data/: four ELF files compiled here with gcc 13.3 and binutils
# 2.42 (a relocatable object, a PIE that links a versioned shared
# library, the library, and an old-style non-PIE executable), a stripped
# copy, four damaged files, a shell script and the job list.
import os, shutil, struct, subprocess
W = "w"
shutil.rmtree(W, ignore_errors=True)
shutil.rmtree("data", ignore_errors=True)
os.makedirs(W)
os.makedirs("data/src")
SRC = {
"app.c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
extern const char *greet(const char *who);
extern char *greet_dup(const char *who);
extern int greet_score(int x);
static int counter = 3;
int shared_total;
const char banner[] = "app 1.4";
int add(int a, int b) { return a + b + counter; }
int main(int argc, char **argv) {
    char buf[32];
    strncpy(buf, argc > 1 ? argv[1] : "world", sizeof buf - 1);
    buf[31] = 0;
    char *d = greet_dup(buf);
    printf("%s: %s %s %d\n", banner, greet(buf), d, add(argc, greet_score(2)));
    free(d);
    shared_total += argc;
    return 0;
}
''',
"greet.c": r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static char last[64];
int greet_count = 0;
__thread int greet_depth;
const char *greet_old(const char *who) { snprintf(last, sizeof last, "hi %s", who); greet_count++; return last; }
const char *greet_new(const char *who) { snprintf(last, sizeof last, "hello, %s!", who); greet_count++; return last; }
char *greet_dup(const char *who) { greet_depth++; char *p = malloc(strlen(who) + 8); strcpy(p, "dear "); strcat(p, who); return p; }
static int helper(int x) { return x * 3; }
int greet_score(int x) { return helper(x) + greet_count; }
__asm__(".symver greet_old,greet@GREET_1.0");
__asm__(".symver greet_new,greet@@GREET_2.0");
''',
"greet.map": '''GREET_1.0 { global: greet; greet_count; local: *; };
GREET_2.0 { global: greet; greet_dup; greet_score; greet_depth; } GREET_1.0;
''',
"hello.c": r'''#include <stdio.h>
#include <string.h>
static int counter = 3;
int shared_total;
extern int helper(int);
int add(int a, int b) { return a + b + counter; }
int main(int argc, char **argv) {
    char buf[32];
    strncpy(buf, argc > 1 ? argv[1] : "world", sizeof buf - 1);
    buf[31] = 0;
    printf("hello %s %d\n", buf, add(argc, 2));
    return 0;
}
''',
}
for n, t in SRC.items():
    open(f"{W}/{n}", "w").write(t)
    open(f"data/src/{n}", "w").write(t)
def sh(cmd):
    subprocess.run(cmd, shell=True, check=True, cwd=W)
sh("gcc -O1 -fPIC -shared -Wl,--version-script=greet.map -Wl,-soname,libgreet.so.2 greet.c -o libgreet.so.2")
sh("gcc -O1 -fstack-protector-strong -c app.c -o app.o")
sh("gcc -O1 -fstack-protector-strong -z now app.c -L. -l:libgreet.so.2 -Wl,-rpath,'$ORIGIN' -o app")
sh("cp app app-stripped && strip --strip-all app-stripped")
sh("gcc -O1 -fno-pie -no-pie -fno-stack-protector -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=0 -z execstack -z norelro "
   "-Wl,--hash-style=sysv -Wl,-rpath,/opt/legacy/lib -Wl,--disable-new-dtags hello.c -o legacy")
for n in ["app.o", "app", "app-stripped", "libgreet.so.2", "legacy"]:
    shutil.copy(f"{W}/{n}", f"data/{n}")
app = open(f"{W}/app", "rb").read()
obj = bytearray(open(f"{W}/app.o", "rb").read())
open("data/app.trunc", "wb").write(app[:5000])      # cut inside .text
open("data/app.head", "wb").write(app[:40])         # cut inside the header
d = bytearray(obj); struct.pack_into("<Q", d, 0x28, 0x100000)
open("data/badshoff.o", "wb").write(d)              # section headers past the end
e = bytearray(obj); struct.pack_into("<H", e, 0x3e, 99)
open("data/badstrndx.o", "wb").write(e)             # no section-name table
# app.v3: app as if it had been linked against a newer libgreet that
# defines GREET_3.0. Its version need is renamed in .dynstr, with the
# vna_hash the linker would have written.
def elf_hash(name):
    h = 0
    for c in name:
        h = ((h << 4) + c) & 0xffffffff
        g = h & 0xf0000000
        if g:
            h ^= g >> 24
        h &= ~g & 0xffffffff
    return h
v3 = bytearray(app)
at = v3.index(b"\0GREET_2.0\0", 0x510) + 1
assert at < 0x615
v3[at:at + 9] = b"GREET_3.0"
assert struct.unpack_from("<I", v3, 0x690)[0] == elf_hash(b"GREET_2.0")
struct.pack_into("<I", v3, 0x690, elf_hash(b"GREET_3.0"))
open("data/app.v3", "wb").write(v3)
open("data/build.sh", "w").write("#!/bin/sh\n# not an ELF file: the script that made the others\nexec make -C src all\n")
JOBS = """\
# Each line is one readelf command, run from data/.
readelf -W -h -l -S -d -r -s -n -V app.o
readelf -W -h -l -S -d -r -s -n -V app
readelf -W -h -l -S -d -r -s -n -V libgreet.so.2
readelf -W -h -l -S -d -r -s -n -V legacy
readelf -W -h -S -s -n app-stripped
readelf -W -l app-stripped
readelf -W -d app-stripped legacy
readelf -p .comment -x .rodata app
readelf -p .rodata -x .comment app.o
readelf -x .interp -p .dynstr legacy
readelf -p .dynstr -x .gnu.version libgreet.so.2
readelf -x .nosuch -p .comment app
readelf -h build.sh
readelf -h app.head
readelf -h missing.so
readelf -W -h -S -l -d app.trunc
readelf -W -s app.trunc
readelf -W -S -s badshoff.o
readelf -W -V app.v3
readelf -W -I libgreet.so.2 legacy app
readelf -W -h -S -s -r badstrndx.o
# The rest are this tool's own commands, checked against its Python mirror.
checksec app app-stripped legacy libgreet.so.2 app.o app.v3 build.sh app.head missing.so
ldcheck app
ldcheck app.v3
ldcheck legacy
ldcheck libgreet.so.2
lookup libgreet.so.2 greet greet@GREET_1.0 greet@GREET_2.0 greet_dup greet_count greet_depth greet_score greet_old malloc nosuch _init greet_open GREET_1.0
lookup legacy printf strncpy main __gmon_start__
lookup app greet _IO_stdin_used __cxa_finalize
"""
open("data/jobs.txt", "w").write(JOBS)
