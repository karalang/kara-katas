# The Python mirror of mini_readelf: the same readelf port, checksec
# table and link check, written over plain bytes. Its readelf half is
# checked against GNU readelf 2.42 (real.py); the rest is the oracle.
import os, sys

D = "data"
out = []
def w(s):
    out.append(s)

def u(b, i, n):
    return int.from_bytes(b[i:i + n], "little")

def hexs(v):
    return "%x" % v

SHT = {0: "NULL", 1: "PROGBITS", 2: "SYMTAB", 3: "STRTAB", 4: "RELA", 5: "HASH", 6: "DYNAMIC", 7: "NOTE",
       8: "NOBITS", 9: "REL", 10: "SHLIB", 11: "DYNSYM", 14: "INIT_ARRAY", 15: "FINI_ARRAY",
       16: "PREINIT_ARRAY", 17: "GROUP", 18: "SYMTAB SECTION INDICIES", 0x6ffffff6: "GNU_HASH",
       0x6ffffffd: "VERDEF", 0x6ffffffe: "VERNEED", 0x6fffffff: "VERSYM", 0x70000001: "X86_64_UNWIND"}
PT = {0: "NULL", 1: "LOAD", 2: "DYNAMIC", 3: "INTERP", 4: "NOTE", 5: "SHLIB", 6: "PHDR", 7: "TLS",
      0x6474e550: "GNU_EH_FRAME", 0x6474e551: "GNU_STACK", 0x6474e552: "GNU_RELRO", 0x6474e553: "GNU_PROPERTY",
      0x6474e554: "GNU_SFRAME"}
DT = {0: "NULL", 1: "NEEDED", 2: "PLTRELSZ", 3: "PLTGOT", 4: "HASH", 5: "STRTAB", 6: "SYMTAB", 7: "RELA",
      8: "RELASZ", 9: "RELAENT", 10: "STRSZ", 11: "SYMENT", 12: "INIT", 13: "FINI", 14: "SONAME", 15: "RPATH",
      16: "SYMBOLIC", 17: "REL", 18: "RELSZ", 19: "RELENT", 20: "PLTREL", 21: "DEBUG", 22: "TEXTREL",
      23: "JMPREL", 24: "BIND_NOW", 25: "INIT_ARRAY", 26: "FINI_ARRAY", 27: "INIT_ARRAYSZ", 28: "FINI_ARRAYSZ",
      29: "RUNPATH", 30: "FLAGS", 32: "PREINIT_ARRAY", 33: "PREINIT_ARRAYSZ", 0x6ffffef5: "GNU_HASH",
      0x6ffffff0: "VERSYM", 0x6ffffff9: "RELACOUNT", 0x6ffffffa: "RELCOUNT", 0x6ffffffb: "FLAGS_1",
      0x6ffffffc: "VERDEF", 0x6ffffffd: "VERDEFNUM", 0x6ffffffe: "VERNEED", 0x6fffffff: "VERNEEDNUM"}
RT = {0: "NONE", 1: "64", 2: "PC32", 3: "GOT32", 4: "PLT32", 5: "COPY", 6: "GLOB_DAT", 7: "JUMP_SLOT",
      8: "RELATIVE", 9: "GOTPCREL", 10: "32", 11: "32S", 12: "16", 13: "PC16", 14: "8", 15: "PC8",
      16: "DTPMOD64", 17: "DTPOFF64", 18: "TPOFF64", 19: "TLSGD", 20: "TLSLD", 21: "DTPOFF32",
      22: "GOTTPOFF", 23: "TPOFF32", 24: "PC64", 25: "GOTOFF64", 26: "GOTPC32", 37: "IRELATIVE",
      41: "GOTPCRELX", 42: "REX_GOTPCRELX"}
STT = {0: "NOTYPE", 1: "OBJECT", 2: "FUNC", 3: "SECTION", 4: "FILE", 5: "COMMON", 6: "TLS", 10: "IFUNC"}
STB = {0: "LOCAL", 1: "GLOBAL", 2: "WEAK", 10: "UNIQUE"}
STV = ["DEFAULT", "INTERNAL", "HIDDEN", "PROTECTED"]
DF = [(1, "ORIGIN"), (2, "SYMBOLIC"), (4, "TEXTREL"), (8, "BIND_NOW"), (0x10, "STATIC_TLS")]
DF1 = ["NOW", "GLOBAL", "GROUP", "NODELETE", "LOADFLTR", "INITFIRST", "NOOPEN", "ORIGIN", "DIRECT",
       "TRANS", "INTERPOSE", "NODEFLIB", "NODUMP", "CONFALT", "ENDFILTEE", "DISPRELDNE", "DISPRELPND",
       "NODIRECT", "IGNMULDEF", "NOKSYMS", "NOHDR", "EDITED", "NORELOC", "SYMINTPOSE", "GLOBAUDIT",
       "SINGLETON", "STUB", "PIE", "KMOD", "WEAKFILTER", "NOCOMMON"]
SHF = [(1, "W"), (2, "A"), (4, "X"), (0x10, "M"), (0x20, "S"), (0x40, "I"), (0x80, "L"), (0x100, "O"),
       (0x200, "G"), (0x400, "T"), (0x800, "C"), (0x10000000, "l"), (0x80000000, "E")]

def sel(tab, v, unknown):
    return tab[v] if v in tab else unknown


class Elf:
    def __init__(self, name, b):
        self.name, self.b = name, b
        self.err = []
        self.shnum = u(b, 0x3c, 2)
        self.shoff = u(b, 0x28, 8)
        self.phoff = u(b, 0x20, 8)
        self.phnum = u(b, 0x38, 2)
        self.shstrndx = u(b, 0x3e, 2)
        self.secs = None
        if self.shnum > 0:
            size = self.shnum * u(b, 0x3a, 2)
            if self.shoff + size > len(b):
                self.err.append(f"readelf: Error: Reading {size} bytes extends past end of file for section headers")
            else:
                self.secs = []
                for k in range(self.shnum):
                    p = self.shoff + 64 * k
                    self.secs.append(dict(name=u(b, p, 4), type=u(b, p + 4, 4), flags=u(b, p + 8, 8),
                                          addr=u(b, p + 16, 8), off=u(b, p + 24, 8), size=u(b, p + 32, 8),
                                          link=u(b, p + 40, 4), info=u(b, p + 44, 4), align=u(b, p + 48, 8),
                                          es=u(b, p + 56, 8)))
        self.has_strings = self.secs is not None and self.shstrndx < self.shnum
        self.phdrs = []
        for k in range(self.phnum):
            p = self.phoff + 56 * k
            self.phdrs.append(dict(type=u(b, p, 4), flags=u(b, p + 4, 4), off=u(b, p + 8, 8), va=u(b, p + 16, 8),
                                   pa=u(b, p + 24, 8), fs=u(b, p + 32, 8), ms=u(b, p + 40, 8), al=u(b, p + 48, 8)))
        self.dyn_tried = False
        self.dyn = None

    def cstr(self, at):
        b = self.b
        e = at
        while e < len(b) and b[e] != 0:
            e += 1
        return b[at:e].decode("latin-1")

    def sec_name(self, s):
        if not self.has_strings:
            return "<no-strings>"
        st = self.secs[self.shstrndx]
        if s["name"] >= st["size"]:
            return "<corrupt>"
        return self.cstr(st["off"] + s["name"])

    def find(self, name):
        if self.secs is None:
            return None
        for k, s in enumerate(self.secs):
            if self.has_strings and self.sec_name(s) == name:
                return k
        return None

    # The dynamic entries, up to and including DT_NULL, read through
    # PT_DYNAMIC as readelf does; an error the first time it fails.
    def dynamic(self):
        if not self.dyn_tried:
            self.dyn_tried = True
            for p in self.phdrs:
                if p["type"] == 2:
                    if p["off"] + p["fs"] > len(self.b):
                        self.err.append("readelf: Error: the dynamic segment offset + size exceeds the size of the file")
                        break
                    ents = []
                    for k in range(p["fs"] // 16):
                        t, v = u(self.b, p["off"] + 16 * k, 8), u(self.b, p["off"] + 16 * k + 8, 8)
                        ents.append((t, v))
                        if t == 0:
                            break
                    self.dyn = (p["off"], ents)
                    break
        return self.dyn

    def is_pie(self):
        d = self.dynamic()
        if d is None:
            return False
        for t, v in d[1]:
            if t == 0x6ffffffb:
                return (v & 0x08000000) != 0
        return False

    def ftype(self):
        t = u(self.b, 0x10, 2)
        if t == 1:
            return "REL (Relocatable file)"
        if t == 2:
            return "EXEC (Executable file)"
        if t == 3:
            return "DYN (Position-Independent Executable file)" if self.is_pie() else "DYN (Shared object file)"
        if t == 4:
            return "CORE (Core file)"
        return f"<unknown>: {t:x}"


# ------------------------------------------------------------ -h

def file_header(e):
    b = e.b
    w("ELF Header:\n")
    w("  Magic:   " + "".join("%2.2x " % c for c in b[:16]) + "\n")
    def row(label, val):
        w("  " + (label + ":").ljust(35) + val + "\n")
    row("Class", {1: "ELF32", 2: "ELF64", 0: "none"}.get(b[4], f"<unknown: {b[4]:x}>"))
    row("Data", {1: "2's complement, little endian", 2: "2's complement, big endian", 0: "none"}.get(b[5], f"<unknown: {b[5]:x}>"))
    row("Version", f"{b[6]} (current)" if b[6] == 1 else f"{b[6]} <unknown>")
    row("OS/ABI", {0: "UNIX - System V", 3: "UNIX - GNU"}.get(b[7], f"<unknown: {b[7]:x}>"))
    row("ABI Version", f"{b[8]}")
    row("Type", e.ftype())
    row("Machine", "Advanced Micro Devices X86-64" if u(b, 0x12, 2) == 62 else f"<unknown>: 0x{u(b, 0x12, 2):x}")
    row("Version", f"0x{u(b, 0x14, 4):x}")
    row("Entry point address", f"0x{u(b, 0x18, 8):x}")
    row("Start of program headers", f"{e.phoff} (bytes into file)")
    row("Start of section headers", f"{e.shoff} (bytes into file)")
    row("Flags", f"0x{u(b, 0x30, 4):x}")
    row("Size of this header", f"{u(b, 0x34, 2)} (bytes)")
    row("Size of program headers", f"{u(b, 0x36, 2)} (bytes)")
    row("Number of program headers", f"{e.phnum}")
    row("Size of section headers", f"{u(b, 0x3a, 2)} (bytes)")
    row("Number of section headers", f"{e.shnum}")
    row("Section header string table index", f"{e.shstrndx}" + (" <corrupt: out of range>" if e.shstrndx >= e.shnum else ""))


# ------------------------------------------------------------ -S

def flags_str(f):
    return "".join(c for bit, c in SHF if f & bit)

def section_headers(e, do_header):
    if e.shnum == 0:
        w("\nThere are no sections in this file.\n")
        return
    if not do_header:
        w(f"There are {e.shnum} section headers, starting at offset 0x{e.shoff:x}:\n")
    if e.secs is None:
        return
    w("\nSection Headers:\n" if e.shnum > 1 else "\nSection Header:\n")
    w("  [Nr] Name              Type            Address          Off    Size   ES Flg Lk Inf Al\n")
    for k, s in enumerate(e.secs):
        w("  [%2d] %-17s %-15s %016x %6.6x %6.6x %2.2x %3s %2d %3d %2d\n" % (
            k, e.sec_name(s), sel(SHT, s["type"], "%08x: <unknown>" % s["type"]), s["addr"], s["off"],
            s["size"], s["es"], flags_str(s["flags"]), s["link"], s["info"], s["align"]))
    w("Key to Flags:\n")
    w("  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),\n")
    w("  L (link order), O (extra OS processing required), G (group), T (TLS),\n")
    w("  C (compressed), x (unknown), o (OS specific), E (exclude),\n")
    w("  D (mbind), l (large), p (processor specific)\n")


# ------------------------------------------------------------ -l

def le_last(x, n):
    # x <= n - 1 in unsigned arithmetic
    return n == 0 or x <= n - 1

def in_segment(s, p):
    tls = s["flags"] & 0x400 != 0
    alloc = s["flags"] & 2 != 0
    nobits = s["type"] == 8
    pt = p["type"]
    tbss_special = tls and nobits and pt != 7
    size = 0 if tbss_special else s["size"]
    if not ((tls and pt in (7, 0x6474e552, 1)) or (not tls and pt != 7 and pt != 6)):
        return False
    if not alloc and pt in (1, 2, 0x6474e550, 0x6474e551, 0x6474e552, 0x6474e554):
        return False
    if not nobits:
        if not (s["off"] >= p["off"] and le_last(s["off"] - p["off"], p["fs"])
                and s["off"] - p["off"] + size <= p["fs"]):
            return False
    if alloc:
        if not (s["addr"] >= p["va"] and le_last(s["addr"] - p["va"], p["ms"])
                and s["addr"] - p["va"] + size <= p["ms"]):
            return False
    if pt in (2, 4) and s["size"] == 0 and p["ms"] != 0:
        ok_off = nobits or (s["off"] > p["off"] and s["off"] - p["off"] < p["fs"])
        ok_addr = not alloc or (s["addr"] > p["va"] and s["addr"] - p["va"] < p["ms"])
        if not (ok_off and ok_addr):
            return False
    return True

def program_headers(e, do_header):
    if e.phnum == 0:
        w("\nThere are no program headers in this file.\n")
        return
    if not do_header:
        w(f"\nElf file type is {e.ftype()}\n")
        w(f"Entry point 0x{u(e.b, 0x18, 8):x}\n")
        w(f"There are {e.phnum} program headers, starting at offset {e.phoff}\n")
    w("\nProgram Headers:\n" if e.phnum > 1 else "\nProgram Header:\n")
    w("  Type           Offset   VirtAddr           PhysAddr           FileSiz  MemSiz   Flg Align\n")
    for p in e.phdrs:
        fl = ("R" if p["flags"] & 4 else " ") + ("W" if p["flags"] & 2 else " ") + ("E" if p["flags"] & 1 else " ")
        al = "0x%x" % p["al"] if p["al"] else "0"
        w("  %-14.14s 0x%6.6x 0x%16.16x 0x%16.16x 0x%6.6x 0x%6.6x %s %s\n" % (
            sel(PT, p["type"], "LOPROC+%#x" % p["type"]), p["off"], p["va"], p["pa"], p["fs"], p["ms"], fl, al))
        if p["type"] == 3:
            w("      [Requesting program interpreter: %s]\n" % e.cstr(p["off"]))
    if e.secs is None or e.shnum == 0:
        return
    w("\n Section to Segment mapping:\n  Segment Sections...\n")
    for k, p in enumerate(e.phdrs):
        w("   %2.2d     " % k)
        for j in range(1, e.shnum):
            s = e.secs[j]
            tbss_special = s["flags"] & 0x400 and s["type"] == 8 and p["type"] != 7
            if not tbss_special and in_segment(s, p):
                w(e.sec_name(s) + " ")
        w("\n")


# ------------------------------------------------------------ -d

def dyn_value(e, strtab, t, v):
    name = DT.get(t)
    if t in (1, 14, 15, 29):
        label = {1: "Shared library", 14: "Library soname", 15: "Library rpath", 29: "Library runpath"}[t]
        return f"{label}: [{e.cstr(strtab + v)}]" if strtab is not None else f"0x{v:x}"
    if t == 30:
        return " ".join(n for bit, n in DF if v & bit)
    if t == 0x6ffffffb:
        return "Flags:" + "".join(" " + DF1[k] for k in range(len(DF1)) if v >> k & 1)
    if t == 20:
        return DT.get(v, f"0x{v:x}")
    if t in (2, 8, 9, 10, 11, 18, 19, 27, 28, 33):
        return f"{v} (bytes)"
    if t in (0x6ffffffd, 0x6fffffff, 0x6ffffff9, 0x6ffffffa):
        return f"{v}"
    return f"0x{v:x}"

def vaddr_to_off(e, a):
    for p in e.phdrs:
        if p["type"] == 1 and p["va"] <= a < p["va"] + p["fs"]:
            return a - p["va"] + p["off"]
    return None

def dyn_strtab(e, ents):
    for t, v in ents:
        if t == 5:
            return vaddr_to_off(e, v)
    return None

def dynamic_section(e):
    d = e.dynamic()
    if d is None:
        w("\nThere is no dynamic section in this file.\n")
        return
    off, ents = d
    n = len(ents)
    w(f"\nDynamic section at offset 0x{off:x} contains {n} " + ("entry" if n == 1 else "entries") + ":\n")
    w("  Tag        Type                         Name/Value\n")
    st = dyn_strtab(e, ents)
    for t, v in ents:
        name = DT.get(t, f"<unknown>: {t:x}")
        w(" 0x%016x (%s)%*s%s\n" % (t, name, 19 - len(name), " ", dyn_value(e, st, t, v)))


# ------------------------------------------------------------ symbols and versions

class Syms:
    def __init__(self, e, k):
        s = e.secs[k]
        self.k = k
        self.sec = s
        self.n = s["size"] // 24 if s["es"] else 0
        self.str_off = e.secs[s["link"]]["off"] if s["link"] < e.shnum else 0
        self.rows = []
        for i in range(self.n):
            p = s["off"] + 24 * i
            self.rows.append(dict(name=u(e.b, p, 4), info=e.b[p + 4], other=e.b[p + 5], shndx=u(e.b, p + 6, 2),
                                  value=u(e.b, p + 8, 8), size=u(e.b, p + 16, 8)))

def sym_name(e, t, r):
    if r["info"] & 15 == 3 and r["name"] == 0:
        if r["shndx"] < e.shnum and e.secs is not None:
            return e.sec_name(e.secs[r["shndx"]])
        return ""
    return e.cstr(t.str_off + r["name"])

class Versions:
    def __init__(self, e):
        self.versym = None
        self.need = {}   # index -> name
        self.defs = {}   # index -> name
        if e.secs is None:
            return
        for k, s in enumerate(e.secs):
            st = e.secs[s["link"]]["off"] if s["link"] < e.shnum else 0
            if s["type"] == 0x6fffffff:
                self.versym = [u(e.b, s["off"] + 2 * i, 2) for i in range(s["size"] // 2)]
            elif s["type"] == 0x6ffffffe:
                p = s["off"]
                for _ in range(s["info"]):
                    cnt, aux, nxt = u(e.b, p + 2, 2), u(e.b, p + 8, 4), u(e.b, p + 12, 4)
                    a = p + aux
                    for _ in range(cnt):
                        self.need[u(e.b, a + 6, 2)] = e.cstr(st + u(e.b, a + 8, 4))
                        a += u(e.b, a + 12, 4)
                    p += nxt
            elif s["type"] == 0x6ffffffd:
                p = s["off"]
                for _ in range(s["info"]):
                    ndx, aux, nxt = u(e.b, p + 4, 2), u(e.b, p + 12, 4), u(e.b, p + 16, 4)
                    self.defs[ndx] = e.cstr(st + u(e.b, p + aux, 4))
                    p += nxt

# The version a dynamic symbol shows: (name, kind), kind 'u' for a
# needed version, 'h' for a hidden definition, 'd' for the default one.
def sym_version(v, i, r, name):
    if v.versym is None or i >= len(v.versym):
        return None
    data = v.versym[i]
    idx = data & 0x7fff
    if idx < 2:
        return None
    if r["shndx"] == 0:
        if idx in v.need:
            return (v.need[idx], "u", idx)
        return None
    if idx in v.defs:
        if v.defs[idx] == name:
            return None
        return (v.defs[idx], "h" if data & 0x8000 else "d", idx)
    return None

def ndx_str(e, n):
    if n == 0:
        return "UND"
    if n == 0xfff1:
        return "ABS"
    if n == 0xfff2:
        return "COM"
    if not e.has_strings and n < e.shnum:
        return "<no-strings>"
    return "%3d" % n

def symbols(e):
    if e.secs is None:
        # readelf falls back on the dynamic segment's symbol table
        e.dynamic()
        return
    v = Versions(e)
    for k, s in enumerate(e.secs):
        if s["type"] not in (2, 11):
            continue
        t = Syms(e, k)
        name = e.sec_name(s)
        w(f"\nSymbol table '{name}' contains {t.n} " + ("entry" if t.n == 1 else "entries") + ":\n")
        w("   Num:    Value          Size Type    Bind   Vis      Ndx Name\n")
        for i, r in enumerate(t.rows):
            nm = sym_name(e, t, r)
            if s["type"] == 11:
                ver = sym_version(v, i, r, nm)
                if ver:
                    nm += (f"@{ver[0]} ({ver[2]})" if ver[1] == "u" else ("@" if ver[1] == "h" else "@@") + ver[0])
            w("%6d: %016x %5d %-7s %-6s %-7s %4s %s\n" % (
                i, r["value"], r["size"], sel(STT, r["info"] & 15, f"<unknown>: {r['info'] & 15}"),
                sel(STB, r["info"] >> 4, f"<unknown>: {r['info'] >> 4}"), STV[r["other"] & 3],
                ndx_str(e, r["shndx"]), nm))


# ------------------------------------------------------------ -r

def relocs(e):
    if e.secs is None:
        w("\nThere are no relocations in this file.\n")
        return
    v = Versions(e)
    any_ = False
    for k, s in enumerate(e.secs):
        if s["type"] != 4:
            continue
        any_ = True
        n = s["size"] // 24
        label = f"'{e.sec_name(s)}'" if e.has_strings else f"{s['name']}"
        w(f"\nRelocation section {label} at offset 0x{s['off']:x} contains {n} " + ("entry" if n == 1 else "entries") + ":\n")
        w("    Offset             Info             Type               Symbol's Value  Symbol's Name + Addend\n")
        t = Syms(e, s["link"]) if s["link"] < e.shnum and s["link"] != 0 else None
        for i in range(n):
            p = s["off"] + 24 * i
            off, info, add = u(e.b, p, 8), u(e.b, p + 8, 8), u(e.b, p + 16, 8)
            if add >= 1 << 63:
                add -= 1 << 64
            sym, typ = info >> 32, info & 0xffffffff
            line = "%16.16x  %16.16x %-22s" % (off, info, "R_X86_64_" + RT.get(typ, "unknown"))
            if sym == 0:
                line += " " * 20 + ("%x" % add if add >= 0 else "-%x" % -add)
            else:
                r = t.rows[sym]
                nm = sym_name(e, t, r)
                if e.secs[s["link"]]["type"] == 11:
                    ver = sym_version(v, sym, r, nm)
                    if ver:
                        nm += ("@" if ver[1] in "uh" else "@@") + ver[0]
                line += " %016x %s %s %x" % (r["value"], nm, "-" if add < 0 else "+", abs(add))
            w(line + "\n")
    if not any_:
        w("\nThere are no relocations in this file.\n")


# ------------------------------------------------------------ -V

def c_hash06(x):
    return "000000" if x == 0 else "0x%04x" % x

def ver_sections(e):
    if e.secs is None:
        return
    found = False
    syms = None
    for k, s in enumerate(e.secs):
        if s["type"] == 11:
            syms = Syms(e, k)
    v = Versions(e)
    for k, s in enumerate(e.secs):
        if s["type"] not in (0x6ffffffd, 0x6ffffffe, 0x6fffffff):
            continue
        found = True
        link = e.secs[s["link"]]
        st = link["off"]
        head = " Addr: 0x%016x  Offset: 0x%08x  Link: %d (%s)\n" % (s["addr"], s["off"], s["link"], e.sec_name(link))
        if s["type"] == 0x6fffffff:
            n = s["size"] // 2
            w(f"\nVersion symbols section '{e.sec_name(s)}' contains {n} " + ("entry" if n == 1 else "entries") + ":\n")
            w(head)
            for c in range(0, n, 4):
                w("  %03x:" % c)
                for j in range(4):
                    if c + j >= n:
                        break
                    data = v.versym[c + j]
                    if data == 0:
                        w("   0 (*local*)    ")
                    elif data == 1:
                        w("   1 (*global*)   ")
                    else:
                        cell = "%4x%c" % (data & 0x7fff, "h" if data & 0x8000 else " ")
                        r = syms.rows[c + j]
                        idx = data & 0x7fff
                        name = None
                        if r["shndx"] == 0 or (r["shndx"] < e.shnum and e.secs[r["shndx"]]["type"] == 8):
                            check_def = r["shndx"] != 0
                            check_need = r["shndx"] == 0
                        else:
                            check_def = check_need = True
                        if check_need and idx in v.need and data != 0x8001:
                            name = v.need[idx]
                        elif check_def and idx in v.defs:
                            name = v.defs[idx]
                        if name is not None:
                            cell += "(%s%-*s" % (name, 12 - len(name), ")")
                        if len(cell) < 18:
                            cell += " " * (18 - len(cell))
                        w(cell)
                w("\n")
        elif s["type"] == 0x6ffffffd:
            w(f"\nVersion definition section '{e.sec_name(s)}' contains {s['info']} " + ("entry" if s["info"] == 1 else "entries") + ":\n")
            w(head)
            p = s["off"]
            for _ in range(s["info"]):
                rev, fl, ndx, cnt = u(e.b, p, 2), u(e.b, p + 2, 2), u(e.b, p + 4, 2), u(e.b, p + 6, 2)
                aux, nxt = u(e.b, p + 12, 4), u(e.b, p + 16, 4)
                fls = "none" if fl == 0 else " | ".join(n for bit, n in [(1, "BASE"), (2, "WEAK")] if fl & bit)
                a = p + aux
                w("  %s: Rev: %d  Flags: %s  Index: %d  Cnt: %d  Name: %s\n" % (
                    c_hash06(p - s["off"]), rev, fls, ndx, cnt, e.cstr(st + u(e.b, a, 4))))
                for j in range(1, cnt):
                    a += u(e.b, a + 4, 4)
                    w("  %s: Parent %d: %s\n" % (c_hash06(a - s["off"]), j, e.cstr(st + u(e.b, a, 4))))
                p += nxt
        else:
            w(f"\nVersion needs section '{e.sec_name(s)}' contains {s['info']} " + ("entry" if s["info"] == 1 else "entries") + ":\n")
            w(head)
            p = s["off"]
            for _ in range(s["info"]):
                ver, cnt, fname, aux, nxt = u(e.b, p, 2), u(e.b, p + 2, 2), u(e.b, p + 4, 4), u(e.b, p + 8, 4), u(e.b, p + 12, 4)
                w("  %s: Version: %d  File: %s  Cnt: %d\n" % (c_hash06(p - s["off"]), ver, e.cstr(st + fname), cnt))
                a = p + aux
                for _ in range(cnt):
                    fl, other, nm, anext = u(e.b, a + 4, 2), u(e.b, a + 6, 2), u(e.b, a + 8, 4), u(e.b, a + 12, 4)
                    fls = "none" if fl == 0 else "WEAK" if fl == 2 else "%x" % fl
                    w("  %s:   Name: %s  Flags: %s  Version: %d\n" % (c_hash06(a - s["off"]), e.cstr(st + nm), fls, other))
                    a += anext
                p += nxt
    if not found:
        w("\nNo version information found in this file.\n")


# ------------------------------------------------------------ -n

def property_text(e, p, n):
    parts = []
    end = p + n
    while p + 8 <= end:
        t, sz = u(e.b, p, 4), u(e.b, p + 4, 4)
        val = u(e.b, p + 8, 4)
        if t == 0xc0000002:
            names = [nm for bit, nm in [(1, "IBT"), (2, "SHSTK"), (4, "LAM_U48"), (8, "LAM_U57")] if val & bit]
            parts.append("x86 feature: " + ", ".join(names))
        elif t == 0xc0008002:
            names = [nm for bit, nm in [(1, "x86-64-baseline"), (2, "x86-64-v2"), (4, "x86-64-v3"), (8, "x86-64-v4")] if val & bit]
            parts.append("x86 ISA needed: " + ", ".join(names))
        else:
            parts.append(f"<unknown type 0x{t:x}>")
        p += 8 + ((sz + 7) & ~7)
    return ", ".join(parts)

def notes(e):
    if e.secs is None:
        return
    for k, s in enumerate(e.secs):
        if s["type"] != 7:
            continue
        w(f"\nDisplaying notes found in: {e.sec_name(s)}\n")
        w("  Owner                Data size \tDescription\n")
        p, end = s["off"], s["off"] + s["size"]
        while p + 12 <= end:
            nsz, dsz, typ = u(e.b, p, 4), u(e.b, p + 4, 4), u(e.b, p + 8, 4)
            owner = e.cstr(p + 12)
            desc = p + 12 + ((nsz + 3) & ~3)
            line = "  %-20s 0x%08x\t" % (owner, dsz)
            if typ == 5:
                line += "NT_GNU_PROPERTY_TYPE_0\t      Properties: " + property_text(e, desc, dsz)
            elif typ == 3:
                line += "NT_GNU_BUILD_ID (unique build ID bitstring)\t    Build ID: " + e.b[desc:desc + dsz].hex()
            elif typ == 1:
                os_ = {0: "Linux", 1: "Hurd", 2: "Solaris", 3: "FreeBSD"}.get(u(e.b, desc, 4), "Unknown")
                line += "NT_GNU_ABI_TAG (ABI version tag)\t    OS: %s, ABI: %d.%d.%d" % (
                    os_, u(e.b, desc + 4, 4), u(e.b, desc + 8, 4), u(e.b, desc + 12, 4))
            else:
                line += "Unknown note type: (0x%08x)" % typ
            w(line + "\n")
            align = 8 if s["align"] == 8 else 4
            p = desc + ((dsz + align - 1) & ~(align - 1))


# ------------------------------------------------------------ -x and -p

def hex_dump(e, s, name):
    w(f"\nHex dump of section '{name}':\n")
    addr, data, n = s["addr"], s["off"], s["size"]
    while n > 0:
        m = min(16, n)
        line = "  0x%8.8x " % addr
        for j in range(16):
            line += "%2.2x" % e.b[data + j] if j < m else "  "
            if j & 3 == 3:
                line += " "
        for j in range(m):
            c = e.b[data + j]
            line += chr(c) if 32 <= c < 0x7f else "."
        w(line + "\n")
        data += m
        addr += m
        n -= m
    w("\n")

def str_dump(e, s, name):
    w(f"\nString dump of section '{name}':\n")
    b = e.b
    start, end = s["off"], s["off"] + s["size"]
    p = start
    shown = False
    while p < end:
        while p < end and not (32 <= b[p] < 0x7f):
            p += 1
        if p < end:
            line = "  [%6x]  " % (p - start)
            while p < end:
                c = b[p]
                p += 1
                if c == 0:
                    break
                if 32 <= c < 0x7f:
                    line += chr(c)
                elif c == 10:
                    line += "\\n"
                else:
                    line += "\\%03o" % c
            w(line + "\n")
            shown = True
    if not shown:
        w("  No strings found in this section.")
    w("\n")


# ------------------------------------------------------------ -I

def pct(num, den):
    # printf("%5.1f", num * 100.0 / den), rounding half to even
    q, r = divmod(num * 1000, den)
    if 2 * r > den or (2 * r == den and q % 2 == 1):
        q += 1
    return "%5s" % ("%d.%d" % (q // 10, q % 10))

def hist_rows(lengths):
    n = len(lengths)
    top = max(lengths) if lengths else 0
    counts = [0] * (top + 1)
    for L in lengths:
        counts[L] += 1
    total = sum(lengths)
    w(" Length  Number     % of total  Coverage\n")
    w("      0  %-10d (%s%%)\n" % (counts[0], pct(counts[0], n)))
    cov = 0
    for i in range(1, top + 1):
        cov += counts[i] * i
        w("%7d  %-10d (%s%%)    %s%%\n" % (i, counts[i], pct(counts[i], n), pct(cov, total)))

def dyn_tag(e, tag):
    d = e.dynamic()
    if d is None:
        return None
    for t, v in d[1]:
        if t == tag:
            return v
    return None

def sysv_lengths(e, off):
    nb, nc = u(e.b, off, 4), u(e.b, off + 4, 4)
    buckets = [u(e.b, off + 8 + 4 * i, 4) for i in range(nb)]
    chains = [u(e.b, off + 8 + 4 * nb + 4 * i, 4) for i in range(nc)]
    out_ = []
    for b0 in buckets:
        L, k = 0, b0
        while k != 0:
            L += 1
            k = chains[k]
        out_.append(L)
    return out_

class GnuHash:
    def __init__(self, e, off):
        b = e.b
        self.nb, self.symoff, self.bloom_n, self.shift = (u(b, off + 4 * i, 4) for i in range(4))
        self.bloom = [u(b, off + 16 + 8 * i, 8) for i in range(self.bloom_n)]
        p = off + 16 + 8 * self.bloom_n
        self.buckets = [u(b, p + 4 * i, 4) for i in range(self.nb)]
        self.chain_at = p + 4 * self.nb
        self.b = b

    def chain(self, sym):
        return u(self.b, self.chain_at + 4 * (sym - self.symoff), 4)

    def lengths(self):
        out_ = []
        for b0 in self.buckets:
            L = 0
            if b0 != 0:
                k = b0
                while True:
                    L += 1
                    if self.chain(k) & 1:
                        break
                    k += 1
            out_.append(L)
        return out_

def histogram(e):
    h = dyn_tag(e, 4)
    if h is not None:
        lens = sysv_lengths(e, vaddr_to_off(e, h))
        if lens:
            w(f"\nHistogram for bucket list length (total of {len(lens)} buckets):\n")
            hist_rows(lens)
    g = dyn_tag(e, 0x6ffffef5)
    if g is not None:
        lens = GnuHash(e, vaddr_to_off(e, g)).lengths()
        if lens:
            w(f"\nHistogram for `.gnu.hash' bucket list length (total of {len(lens)} buckets):\n")
            hist_rows(lens)


# ------------------------------------------------------------ checksec

def elf_hash(name):
    h = 0
    for c in name.encode("latin-1"):
        h = ((h << 4) + c) & 0xffffffff
        g = h & 0xf0000000
        if g:
            h ^= g >> 24
        h &= ~g & 0xffffffff
    return h

def gnu_hash(name):
    h = 5381
    for c in name.encode("latin-1"):
        h = (h * 33 + c) & 0xffffffff
    return h

def open_elf(f):
    path = f"{D}/{f}"
    if not os.path.exists(path):
        return None, "no such file"
    b = open(path, "rb").read()
    if len(b) < 64:
        return None, "too short for an ELF header"
    if b[:4] != b"\x7fELF":
        return None, "not an ELF file"
    e = Elf(f, b)
    return e, None

def sym_tables(e):
    out_ = []
    if e.secs is not None:
        for k, s in enumerate(e.secs):
            if s["type"] in (2, 11):
                out_.append((s["type"], Syms(e, k)))
    return out_

def all_sym_names(e):
    names = []
    for _, t in sym_tables(e):
        for r in t.rows:
            names.append(sym_name(e, t, r))
    return names

def cet(e):
    k = None
    if e.secs is not None:
        for j, s in enumerate(e.secs):
            if s["type"] == 7 and e.sec_name(s) == ".note.gnu.property":
                k = j
    if k is None:
        return "-"
    s = e.secs[k]
    p = s["off"]
    nsz, dsz = u(e.b, p, 4), u(e.b, p + 4, 4)
    q = p + 12 + ((nsz + 3) & ~3)
    end = q + dsz
    while q + 8 <= end:
        t, sz = u(e.b, q, 4), u(e.b, q + 4, 4)
        if t == 0xc0000002:
            v = u(e.b, q + 8, 4)
            names = [nm for bit, nm in [(1, "IBT"), (2, "SHSTK")] if v & bit]
            return ", ".join(names) if names else "-"
        q += 8 + ((sz + 7) & ~7)
    return "-"

def checksec(files):
    rows = [["File", "RELRO", "Stack canary", "NX", "PIE", "RPATH", "RUNPATH", "Symbols", "FORTIFY", "CET"]]
    bad = []
    for f in files:
        e, why = open_elf(f)
        if e is None:
            bad.append(f"{f}: {why}")
            continue
        etype = u(e.b, 0x10, 2)
        names = all_sym_names(e)
        has = lambda t: any(p["type"] == t for p in e.phdrs)
        if etype == 1:
            relro, nx, pie = "N/A", "N/A", "REL"
        else:
            now = (dyn_tag(e, 30) or 0) & 8 or (dyn_tag(e, 0x6ffffffb) or 0) & 1 or dyn_tag(e, 24) is not None
            relro = ("Full RELRO" if now else "Partial RELRO") if has(0x6474e552) else "No RELRO"
            stack = [p for p in e.phdrs if p["type"] == 0x6474e551]
            nx = "NX enabled" if stack and not stack[0]["flags"] & 1 else "NX disabled"
            if etype == 2:
                pie = "No PIE"
            elif (dyn_tag(e, 0x6ffffffb) or 0) & 0x08000000 or dyn_tag(e, 21) is not None:
                pie = "PIE enabled"
            else:
                pie = "DSO"
        canary = "Canary found" if "__stack_chk_fail" in [n.split("@")[0] for n in names] else "No canary found"
        rpath = "RPATH" if dyn_tag(e, 15) is not None else "No RPATH"
        runpath = "RUNPATH" if dyn_tag(e, 29) is not None else "No RUNPATH"
        nsym = None
        for t, tab in sym_tables(e):
            if t == 2:
                nsym = tab.n
        symbols_ = f"{nsym} Symbols" if nsym is not None else "No Symbols"
        chk = sorted(set(n.split("@")[0] for n in names if n.startswith("__") and n.split("@")[0].endswith("_chk")
                         and n.split("@")[0] != "__stack_chk"))
        fort = f"Yes ({len(chk)})" if chk else "No"
        rows.append([f, relro, canary, nx, pie, rpath, runpath, symbols_, fort, cet(e)])
    widths = [max(len(r[c]) for r in rows) for c in range(len(rows[0]))]
    for r in rows:
        w("  ".join(r[c].ljust(widths[c]) for c in range(len(r))).rstrip() + "\n")
    for line in bad:
        w(line + "\n")
    # the fortified functions themselves
    for f in files:
        e, why = open_elf(f)
        if e is None:
            continue
        names = all_sym_names(e)
        chk = sorted(set(n.split("@")[0] for n in names if n.startswith("__") and n.split("@")[0].endswith("_chk")))
        chk = [c for c in chk if c != "__stack_chk"]
        if chk:
            w(f"{f} fortifies: " + ", ".join(c[2:-4] for c in chk) + "\n")


# ------------------------------------------------------------ the loader's view

class Dso:
    def __init__(self, e):
        self.e = e
        self.dsym = None
        for t, tab in sym_tables(e):
            if t == 11:
                self.dsym = tab
        self.v = Versions(e)

    def name(self, i):
        return sym_name(self.e, self.dsym, self.dsym.rows[i])

def verneeds(e):
    # [(file, [(name, hash, flags, other)])]
    out_ = []
    if e.secs is None:
        return out_
    for s in e.secs:
        if s["type"] != 0x6ffffffe:
            continue
        st = e.secs[s["link"]]["off"]
        p = s["off"]
        for _ in range(s["info"]):
            cnt, fname, aux, nxt = u(e.b, p + 2, 2), u(e.b, p + 4, 4), u(e.b, p + 8, 4), u(e.b, p + 12, 4)
            a = p + aux
            vs = []
            for _ in range(cnt):
                vs.append((e.cstr(st + u(e.b, a + 8, 4)), u(e.b, a, 4), u(e.b, a + 4, 2), u(e.b, a + 6, 2)))
                a += u(e.b, a + 12, 4)
            out_.append((e.cstr(st + fname), vs))
            p += nxt
    return out_

def verdefs(e):
    # [(index, flags, name, hash)]
    out_ = []
    if e.secs is None:
        return out_
    for s in e.secs:
        if s["type"] != 0x6ffffffd:
            continue
        st = e.secs[s["link"]]["off"]
        p = s["off"]
        for _ in range(s["info"]):
            fl, ndx, hsh, aux, nxt = u(e.b, p + 2, 2), u(e.b, p + 4, 2), u(e.b, p + 8, 4), u(e.b, p + 12, 4), u(e.b, p + 16, 4)
            out_.append((ndx, fl, e.cstr(st + u(e.b, p + aux, 4)), hsh))
            p += nxt
    return out_

# Look a name up as ld.so does: through .gnu.hash (or .hash), keeping
# only definitions, and matching the version when one is asked for.
# Returns (symbol index or None, a line saying how).
def lookup(d, name, version):
    e = d.e
    g = dyn_tag(e, 0x6ffffef5)
    if g is not None:
        gh = GnuHash(e, vaddr_to_off(e, g))
        h = gnu_hash(name)
        word = gh.bloom[(h // 64) % gh.bloom_n]
        mask = (1 << (h % 64)) | (1 << ((h >> gh.shift) % 64))
        how = f"gnu hash 0x{h:08x}"
        if word & mask != mask:
            return None, how + ", the bloom filter rules it out"
        b0 = gh.buckets[h % gh.nb]
        if b0 == 0:
            return None, how + f", bucket {h % gh.nb} is empty"
        k, tried = b0, 0
        while True:
            h2 = gh.chain(k)
            if (h | 1) == (h2 | 1):
                tried += 1
                if match(d, k, name, version):
                    return k, how + f", bucket {h % gh.nb}, symbol {k} after {tried} name compare" + ("" if tried == 1 else "s")
            if h2 & 1:
                return None, how + f", bucket {h % gh.nb}, end of chain after {tried} name compare" + ("" if tried == 1 else "s")
            k += 1
    hs = dyn_tag(e, 4)
    off = vaddr_to_off(e, hs)
    nb = u(e.b, off, 4)
    h = elf_hash(name)
    k = u(e.b, off + 8 + 4 * (h % nb), 4)
    how = f"sysv hash 0x{h:08x}"
    tried = 0
    while k != 0:
        if d.name(k) == name:
            tried += 1
            if match(d, k, name, version):
                return k, how + f", bucket {h % nb}, symbol {k}"
        k = u(e.b, off + 8 + 4 * nb + 4 * k, 4)
    return None, how + f", bucket {h % nb}, not defined" + (" (only an undefined reference)" if tried else "")

def match(d, k, name, version):
    r = d.dsym.rows[k]
    if d.name(k) != name or r["shndx"] == 0:
        return False
    if r["info"] >> 4 == 0:
        return False
    if d.v.versym is None:
        return True
    data = d.v.versym[k]
    idx = data & 0x7fff
    vname = d.v.defs.get(idx)
    if version is None:
        return data & 0x8000 == 0
    return vname == version

def describe(d, k):
    r = d.dsym.rows[k]
    nm = d.name(k)
    ver = sym_version(d.v, k, r, nm)
    if ver:
        nm += ("@" if ver[1] == "h" else "@@") + ver[0]
    return "%s = 0x%x %s %s, %d bytes" % (nm, r["value"], STT.get(r["info"] & 15, "?"), STB.get(r["info"] >> 4, "?"), r["size"])

def do_lookup(f, names):
    e, why = open_elf(f)
    if e is None:
        w(f"{f}: {why}\n")
        return
    d = Dso(e)
    g = dyn_tag(e, 0x6ffffef5)
    if g is not None:
        gh = GnuHash(e, vaddr_to_off(e, g))
        w(f"{f}: .gnu.hash with {gh.nb} buckets, symbols from {gh.symoff}, {gh.bloom_n} bloom word" + ("" if gh.bloom_n == 1 else "s") + f", shift {gh.shift}\n")
    else:
        off = vaddr_to_off(e, dyn_tag(e, 4))
        w(f"{f}: .hash with {u(e.b, off, 4)} buckets and {u(e.b, off + 4, 4)} symbols\n")
    for q in names:
        name, _, version = q.partition("@")
        k, how = lookup(d, name, version or None)
        w(f"  {q}: {how}\n")
        if k is not None:
            w(f"    -> {describe(d, k)}\n")

def search_dirs(e):
    rp, run = dyn_tag(e, 15), dyn_tag(e, 29)
    st = dyn_strtab(e, e.dynamic()[1])
    if run is not None:
        return "runpath", e.cstr(st + run).split(":")
    if rp is not None:
        return "rpath", e.cstr(st + rp).split(":")
    return None, []

SYSTEM = {"libc.so.6", "ld-linux-x86-64.so.2", "libm.so.6"}

def ldcheck(f):
    e, why = open_elf(f)
    if e is None:
        w(f"{f}: {why}\n")
        return
    d = e.dynamic()
    if d is None:
        w(f"{f}: not dynamically linked\n")
        return
    st = dyn_strtab(e, d[1])
    needed = [e.cstr(st + v) for t, v in d[1] if t == 1]
    kind, dirs = search_dirs(e)
    interp = [p for p in e.phdrs if p["type"] == 3]
    line = f"{f}: needs " + ", ".join(needed)
    if interp:
        line += "; interpreter " + e.cstr(interp[0]["off"])
    if kind:
        line += f"; {kind} " + ":".join(dirs)
    w(line + "\n")
    found = {}
    for lib in needed:
        hit = None
        for dir_ in dirs:
            if dir_ == "$ORIGIN" and os.path.exists(f"{D}/{lib}"):
                hit = dir_
                break
        if hit is not None:
            le, _ = open_elf(lib)
            ld = le.dynamic()
            son = [le.cstr(dyn_strtab(le, ld[1]) + v) for t, v in ld[1] if t == 14]
            w(f"  {lib}: data/{lib} through {hit}" + (f", soname {son[0]}" if son else "") + "\n")
            found[lib] = Dso(le)
        elif lib in SYSTEM:
            w(f"  {lib}: a system library, not checked\n")
        else:
            outside = [x for x in dirs if x != "$ORIGIN"]
            w(f"  {lib}: not found" + (f" ({' and '.join(outside)} is outside data/)" if outside else "") + "\n")
    # version needs: the loader checks these before any symbol
    refused = []
    for lib, vs in verneeds(e):
        for vname, hsh, fl, other in vs:
            ok = "ok" if hsh == elf_hash(vname) else f"WRONG, expected 0x{elf_hash(vname):08x}"
            if lib in found:
                defs = verdefs(found[lib].e)
                hit = [x for x in defs if x[2] == vname]
                if hit:
                    w(f"  version {vname} (hash 0x{hsh:08x}, {ok}) is version {hit[0][0]} of {lib}\n")
                else:
                    have = ", ".join(x[2] for x in defs if not x[1] & 1)
                    w(f"  version {vname} (hash 0x{hsh:08x}, {ok}) is not defined by {lib}, which defines {have}\n")
                    refused.append(f"{lib}: version `{vname}' not found (required by ./{f})")
            else:
                w(f"  version {vname} (hash 0x{hsh:08x}, {ok}) from {lib}\n")
    if refused:
        for r in refused:
            w(f"  ld.so: ./{f}: {r}\n")
        w("  result: the loader refuses to start it\n")
        return
    # the undefined dynamic symbols
    me = Dso(e)
    if me.dsym is None:
        return
    bound = system = weak = 0
    missing = []
    for i in range(1, me.dsym.n):
        r = me.dsym.rows[i]
        if r["shndx"] != 0:
            continue
        nm = me.name(i)
        ver = sym_version(me.v, i, r, nm)
        lib = None
        if ver:
            for l, vs in verneeds(e):
                if any(x[3] == ver[2] for x in vs):
                    lib = l
        shown = nm + (f"@{ver[0]}" if ver else "")
        targets = [lib] if lib else [l for l in needed]
        hit = None
        for l in targets:
            if l in found:
                k, how = lookup(found[l], nm, ver[0] if ver else None)
                if k is not None:
                    hit = (l, k, how)
                    break
        if hit:
            w(f"  {shown} -> {hit[0]}: {describe(found[hit[0]], hit[1])}\n")
            bound += 1
        elif lib in SYSTEM or (lib is None and all(l in SYSTEM or l not in found for l in needed) and r["info"] >> 4 != 2):
            system += 1
        elif r["info"] >> 4 == 2:
            weak += 1
        else:
            missing.append(shown)
    for m in missing:
        w(f"  {m}: undefined symbol\n")
    w(f"  result: {bound} bound in data/, {system} left to system libraries, {weak} weak and unresolved")
    w(f", {len(missing)} missing\n" if missing else "\n")
    defs = verdefs(e)
    for ndx, fl, vname, hsh in defs:
        ok = "ok" if hsh == elf_hash(vname) else f"WRONG, expected 0x{elf_hash(vname):08x}"
        w(f"  defines version {ndx} {vname}" + (" (base)" if fl & 1 else "") + f", hash 0x{hsh:08x} {ok}\n")


# ------------------------------------------------------------ a job

def readelf(args):
    opts = set()
    dumps = []
    files = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-x", "-p"):
            dumps.append((a, args[i + 1]))
            i += 2
            continue
        if a.startswith("-"):
            opts.add(a)
        else:
            files.append(a)
        i += 1
    status = 0
    for f in files:
        if len(files) > 1:
            w(f"\nFile: {f}\n")
        path = f"{D}/{f}"
        if not os.path.exists(path):
            w(f"readelf: Error: '{f}': No such file\n")
            status = 1
            continue
        b = open(path, "rb").read()
        need = 64 if len(b) > 4 and b[4] == 2 else 52
        if len(b) < 16 or len(b) < need:
            w(f"readelf: Error: {f}: Failed to read file header\n")
            status = 1
            continue
        if b[:4] != b"\x7fELF":
            w("readelf: Error: Not an ELF file - it has the wrong magic bytes at the start\n")
            status = 1
            continue
        e = Elf(f, b)
        do_header = "-h" in opts
        if do_header:
            file_header(e)
        if "-S" in opts:
            section_headers(e, do_header)
        if "-l" in opts:
            program_headers(e, do_header)
        if "-d" in opts:
            dynamic_section(e)
        if "-r" in opts:
            relocs(e)
        if "-s" in opts:
            symbols(e)
        if "-V" in opts:
            ver_sections(e)
        if dumps and e.secs is not None:
            done = set()
            for k, s in enumerate(e.secs):
                nm = e.sec_name(s)
                for kind, want in dumps:
                    if want == nm and want not in done:
                        done.add(want)
                        (hex_dump if kind == "-x" else str_dump)(e, s, nm)
            for kind, want in dumps:
                if want not in done:
                    e.err.append(f"readelf: Warning: Section '{want}' was not dumped because it does not exist")
        if "-I" in opts:
            histogram(e)
        if "-n" in opts:
            notes(e)
        for line in e.err:
            w(line + "\n")
    return status


def main():
    for line in open(f"{D}/jobs.txt"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        w(f"$ {line}\n")
        words = line.split()
        st = 0
        if words[0] == "readelf":
            st = readelf(words[1:])
        elif words[0] == "checksec":
            checksec(words[1:])
        elif words[0] == "ldcheck":
            for f in words[1:]:
                ldcheck(f)
        elif words[0] == "lookup":
            do_lookup(words[1], words[2:])
        if st:
            w(f"[exit status {st}]\n")
        w("\n")

main()
sys.stdout.write("".join(out))
