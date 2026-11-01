"""Writes data/ for mini_pycparser: the job list and the C sources the jobs
parse. The sources are what pycparser is fed in practice: preprocessor
output, with `# <line> "<file>"` markers in place of the #include lines and
no comments.

Run from this directory: python3 -s -P -B mk.py"""
import os

os.makedirs("data", exist_ok=True)


def write(name, text):
    with open(os.path.join("data", name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


# A ring buffer for a UART driver, after `cpp`: the header's typedefs come
# first under its own line marker, then the source.
write("ring.i", """\
# 1 "ring.c"
# 1 "ring.h" 1
typedef unsigned char uint8_t;
typedef unsigned int uint32_t;
typedef unsigned long size_t;

typedef struct ring {
    uint8_t *buf;
    size_t cap;
    volatile size_t head;
    volatile size_t tail;
    unsigned overflowed : 1;
    unsigned : 7;
} ring_t;

int ring_init(ring_t *r, uint8_t *storage, size_t cap);
size_t ring_put(ring_t *r, const uint8_t *src, size_t n);
size_t ring_get(ring_t *r, uint8_t *dst, size_t n);
# 2 "ring.c" 2

static inline size_t ring_used(const ring_t *r)
{
    return (r->head - r->tail) & (r->cap - 1);
}

static inline size_t ring_free(const ring_t *r)
{
    return r->cap - 1 - ring_used(r);
}

int ring_init(ring_t *r, uint8_t *storage, size_t cap)
{
    if (cap == 0 || (cap & (cap - 1)) != 0)
        return -1;
    r->buf = storage;
    r->cap = cap;
    r->head = r->tail = 0;
    r->overflowed = 0;
    return 0;
}

size_t ring_put(ring_t *r, const uint8_t *src, size_t n)
{
    size_t i, room = ring_free(r);
    if (n > room) {
        r->overflowed = 1;
        n = room;
    }
    for (i = 0; i < n; i++) {
        r->buf[r->head] = src[i];
        r->head = (r->head + 1) & (r->cap - 1);
    }
    return n;
}

size_t ring_get(ring_t *r, uint8_t *dst, size_t n)
{
    size_t got = 0;
    while (got < n && r->tail != r->head) {
        *dst++ = r->buf[r->tail];
        r->tail = (r->tail + 1) & (r->cap - 1);
        ++got;
    }
    return got;
}
""")

# An open-addressing hash map with function pointers for the hash and the
# comparison, a union in the slot, an enum of states and a switch.
write("hashmap.i", """\
# 1 "hashmap.c"
typedef unsigned long size_t;
typedef unsigned long long u64;

enum slot_state { SLOT_EMPTY, SLOT_FULL = 1, SLOT_DEAD = 2, };

typedef u64 (*hash_fn)(const void *key, size_t len);
typedef int (*eq_fn)(const void *a, const void *b, size_t len);

struct slot {
    enum slot_state state;
    u64 hash;
    union {
        long i;
        double d;
        void *p;
    } value;
    const char *key;
};

struct map {
    struct slot *slots;
    size_t mask, len;
    hash_fn hash;
    eq_fn eq;
};

static u64 fnv1a(const void *key, size_t len)
{
    const unsigned char *p = key;
    u64 h = 14695981039346656037ULL;
    while (len--) {
        h ^= *p++;
        h *= 1099511628211ULL;
    }
    return h;
}

static struct slot *probe(struct map *m, const char *key, size_t len, u64 h)
{
    size_t i = h & m->mask, step = 1;
    for (;;) {
        struct slot *s = &m->slots[i];
        switch (s->state) {
        case SLOT_EMPTY:
            return s;
        case SLOT_DEAD:
            break;
        case SLOT_FULL:
            if (s->hash == h && m->eq(s->key, key, len))
                return s;
            break;
        default:
            return 0;
        }
        i = (i + step++) & m->mask;
    }
}

int map_put_int(struct map *m, const char *key, size_t len, long v)
{
    u64 h = m->hash ? m->hash(key, len) : fnv1a(key, len);
    struct slot *s = probe(m, key, len, h);
    if (!s)
        return -1;
    s->state = SLOT_FULL;
    s->hash = h;
    s->key = key;
    s->value.i = v;
    m->len += s->state == SLOT_FULL;
    return 0;
}

static const struct map empty_map = { .slots = 0, .mask = 0, .len = 0, .hash = fnv1a, .eq = 0 };
static struct slot sentinel[1] = { [0] = { .state = SLOT_DEAD, .value.d = -1.5e3 } };
""")

# A JSON tokenizer: a state machine with fall-through cases, goto, labels,
# character constants with escapes and adjacent string literals.
write("jsontok.i", """\
# 1 "jsontok.c"
typedef enum {
    TOK_LBRACE = '{', TOK_RBRACE = '}', TOK_LBRACKET = '[', TOK_RBRACKET = ']',
    TOK_COLON = ':', TOK_COMMA = ',', TOK_STRING = 256, TOK_NUMBER, TOK_TRUE,
    TOK_FALSE, TOK_NULL, TOK_EOF, TOK_ERROR = -1
} tok_kind;

typedef struct {
    const char *src;
    int pos, line;
    char err[64];
} lexer;

extern int snprintf(char *buf, unsigned long n, const char *fmt, ...);

static int is_digit(int c) { return c >= '0' && c <= '9'; }

static tok_kind fail(lexer *lx, const char *what)
{
    snprintf(lx->err, sizeof lx->err, "line %d: " "unexpected %s" "\\n", lx->line, what);
    return TOK_ERROR;
}

tok_kind next_token(lexer *lx)
{
    int c;
again:
    c = lx->src[lx->pos++];
    switch (c) {
    case '\\n':
        lx->line++;
    case ' ': case '\\t': case '\\r':
        goto again;
    case '{': case '}': case '[': case ']': case ':': case ',':
        return (tok_kind)c;
    case '"':
        while ((c = lx->src[lx->pos++]) != '"') {
            if (c == '\\\\')
                lx->pos++;
            else if (c == '\\0')
                return fail(lx, "end of input in string");
        }
        return TOK_STRING;
    case '-':
    case '0': case '1': case '2': case '3': case '4':
    case '5': case '6': case '7': case '8': case '9':
        while (is_digit(lx->src[lx->pos]) || lx->src[lx->pos] == '.'
               || lx->src[lx->pos] == 'e' || lx->src[lx->pos] == 'E')
            lx->pos++;
        return TOK_NUMBER;
    case 't':
        lx->pos += 3;
        return TOK_TRUE;
    case '\\0':
        lx->pos--;
        return TOK_EOF;
    default:
        return fail(lx, "character");
    }
}
""")

# Declarations that need lookahead to read: function pointers, arrays of
# them, typedef names reused as variables, K&R definitions, qualifiers in
# array brackets, C11 keywords and the old implicit int.
write("decls.i", """\
# 1 "decls.c"
typedef int T;
typedef char *string;
typedef void (*sighandler_t)(int);

int (*signal_fn(int sig, sighandler_t h))(int);
sighandler_t handlers[32];
char *(*(*cbs)[4])(const char *, ...);
int (*matrix)[3][4];
const char *const *volatile names;
unsigned long long counts[] = { 1, 2u, 3UL, 4llu, 0x10, 017, 0b101 };
double weights[2][2] = { { 0.5, .25 }, { 1e-3, 6.02e23f } };
long double ld = 1.0L;
_Bool ready;
_Complex double z;
static _Thread_local int tls_counter;
_Alignas(16) char aligned_buf[64];
_Atomic int atomic_flag;
_Static_assert(sizeof(T) == 4, "T is an int");

void sum(n, xs)
    int n;
    int *xs;
{
    int T = n;
    while (T--)
        xs[0] += xs[T];
}

f(x) { return x * 2; }

int g(int (T));
int h(int (y));
void copy(char *restrict dst, const char *restrict src, unsigned long n);
void fill(int n, int a[static 10], int b[const n], int c[*]);
inline int square(int v) { return v * v; }
_Noreturn void die(const char *msg);

struct packet {
    unsigned version : 4, ihl : 4;
    union {
        struct { short src, dst; };
        int both;
    };
    char payload[];
};

int use(void)
{
    struct packet *p = (struct packet *)0;
    int n = sizeof(struct packet) + sizeof p->payload[0];
    int off = offsetof(struct packet, payload);
    string s = "a" "b" "c";
    n = (n > 0 ? n : -n), n++;
    n <<= 2; n >>= 1; n |= 1; n &= ~0; n ^= 3; n %= 7;
    retry: n = *(&n) + !n;
    return ((int (*)(int))square)(n) + (int){ 7 } + (struct packet){ .version = 4 };
}
""")

# A GCC-style preprocessed file: line markers with flags, an OpenMP pragma
# inside a function and pragmas at file scope.
write("omp.i", """\
# 1 "omp.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "omp.c"
# 1 "/usr/include/omp.h" 1 3 4
extern int omp_get_thread_num(void);
extern int omp_get_num_threads(void);
# 2 "omp.c" 2
#pragma once
#pragma pack(push, 4)

struct work { int id; float load; };

#pragma pack(pop)

void run(struct work *w, int n)
{
    int i;
    #pragma omp parallel for schedule(static)
    for (i = 0; i < n; i++)
        w[i].load *= 0.5f;
    #pragma omp barrier
    if (omp_get_thread_num() == 0)
        #pragma omp critical
        w[0].id = omp_get_num_threads();
}
# 40 "omp.c"
int after_marker;
""")

# An embedded state machine with a dispatch table, nested ternaries, a
# do-while and every precedence level, to exercise the generator's
# parenthesisation.
write("fsm.i", """\
# 1 "fsm.c"
typedef enum { IDLE, RUN, STOP, N_STATES } state_t;
typedef state_t (*handler)(int ev, void *ctx);

static state_t on_idle(int ev, void *ctx);
static state_t on_run(int ev, void *ctx);
static state_t on_stop(int ev, void *ctx);

static const handler table[N_STATES] = { [IDLE] = on_idle, [RUN] = on_run, [STOP] = on_stop };

static state_t on_idle(int ev, void *ctx) { return ev == 1 ? RUN : ev == 2 ? STOP : IDLE; }
static state_t on_run(int ev, void *ctx) { (void)ctx; return ev ? STOP : RUN; }
static state_t on_stop(int ev, void *ctx) { return IDLE; }

int step(state_t *s, const int *events, int n)
{
    int k = 0, a = 1, b = 2, c = 3;
    do {
        *s = table[*s](events[k], 0);
    } while (++k < n && *s != STOP);
    a = a + b * c - (a - b) - (c - (a + b)) + a % b * c;
    b = (a | b) & c ^ a << 2 >> 1 || !a && b != c;
    c = a < b == b > c;
    a = -(-a) + - -b + ~(~c);
    b = (a = b) + (c += 2);
    c = *&a + (*s)++ + table[0] != 0;
    return k;
}
""")

# One JSON-ish config parser's worth of generated table code, big enough
# to time: 60 accessors over a 60-field struct.
fields = [f"field_{i}" for i in range(60)]
big = ['# 1 "config_gen.c"', "typedef struct config {"]
for i, f in enumerate(fields):
    t = ("int", "long", "double", "const char *", "unsigned short")[i % 5]
    big.append(f"    {t} {f};")
big.append("} config;")
big.append("")
for i, f in enumerate(fields):
    t = ("int", "long", "double", "const char *", "unsigned short")[i % 5]
    big.append(f"{t} config_get_{f}(const config *c, {t} fallback)")
    big.append("{")
    big.append(f"    if (c == 0 || (c->{f} == 0 && {i} % 3 == 0))")
    big.append("        return fallback;")
    big.append(f"    return c->{f};")
    big.append("}")
    big.append(f"void config_set_{f}(config *c, {t} v) {{ if (c) c->{f} = v; }}")
big.append("")
big.append("int config_count_set(const config *c)")
big.append("{")
big.append("    int n = 0;")
for f in fields:
    big.append(f"    n += c->{f} != 0;")
big.append("    return n;")
big.append("}")
write("config_gen.i", "\n".join(big) + "\n")

# Inputs that pycparser refuses, each for one error path.
write("bad_line.i", '# 1 "bad.c"\nint a;\n#line "x.h" 3\nint b;\n')
write("bad_comment.i", "int a; /* not preprocessed */\n")
write("bad_eof.i", "int f(void) {\n    return 1;\n")

JOBS = """\
toks ring.i
show ring.i
showx ring.i
gen ring.i
funcs ring.i
calls ring.i ring_free
explain ring.i
stats ring.i
round ring.i
show hashmap.i
gen hashmap.i
genr hashmap.i
explain hashmap.i
funcs hashmap.i
calls hashmap.i probe
round hashmap.i
showx jsontok.i
gen jsontok.i
toks jsontok.i
stats jsontok.i
round jsontok.i
show decls.i
showx decls.i
gen decls.i
explain decls.i
repr decls.i
round decls.i
toks omp.i
showx omp.i
gen omp.i
funcs omp.i
show fsm.i
gen fsm.i
genr fsm.i
round fsm.i
repr fsm.i
stats config_gen.i
funcs config_gen.i
round config_gen.i
calls config_gen.i config_count_set
show bad_line.i
show bad_comment.i
show bad_eof.i
"""

# One-line snippets: `snip <mode> <C source>`.
SNIPS = """\
show int x;
show int *p, **pp, arr[10], *ptrs[3], (*parr)[3];
explain int *p, **pp, arr[10], *ptrs[3], (*parr)[3];
explain char *(*(*x[3])(void))[5];
explain void (*signal(int, void (*)(int)))(int);
gen void (*signal(int, void (*)(int)))(int);
explain const volatile unsigned long int *const restrict q;
explain struct point { int x, y; } origin, *cursor;
explain union u { int i; float f; } uu;
explain enum color { RED, GREEN = 5, BLUE } c;
explain typedef int (*cmp_t)(const void *, const void *);
explain extern int printf(const char *fmt, ...);
explain static int counter = 0;
explain int m[3][4][5];
show typedef int T; T x; void f(T T);
show typedef int T; void f(void) { T T; T = 1; }
show typedef int T; void f(void) { int T; T * x; }
show typedef int T; void f(void) { T * x; }
show typedef int T; int g(int (T)), h(int (U));
show int a = 1, b = a + 2, c[2] = {1, 2}, d[] = {[1] = 3, [0] = 4};
show struct s { int a; struct { int b; } inner; } v = { .a = 1, .inner.b = 2 };
show int f(void) { return (int){42}; }
show void f(void) { int x = ({ int y = 2; y * 3; }); }
show void f(void) { label: ; goto label; }
show void f(int k) { switch (k) { case 1: case 2: k++; k--; break; case 3: { k = 0; } default: ; } }
gen void f(int k) { switch (k) { case 1: case 2: k++; k--; break; case 3: { k = 0; } default: ; } }
gen int f(int a, int b) { return a ? b ? 1 : 2 : 3; }
gen int f(int a, int b) { return (a + b) * (a - b) / (a % b); }
genr int f(int a, int b) { return (a + b) * (a - b) / (a % b) + (a * b) + (a << (b + 1)); }
gen int f(int a, int b) { a = b = 3; a += b -= 1; return a, b; }
gen int f(int *a) { return *a++ + *(a++) + (*a)++ + -*a + !*a + ~*a + sizeof *a + sizeof(int[3]); }
gen void f(void) { for (;;) ; for (int i = 0, j = 1; i < j; i++, j--) continue; while (0) break; do ; while (0); }
gen void f(void) { if (1) if (2) g(); else h(); }
gen void f(void) { if (1) { if (2) g(); } else h(); }
gen struct { int a : 3; int : 0; unsigned b : 5; } bits;
gen enum { A, B = A + 1, C } e;
gen int x = (unsigned char)-1, y = (int)(long)3.5, z = (int *)0 == 0;
gen char *s = "line one\\n" "line two", c = '\\'', w = L'x';
gen const char *u8s = u8"utf8", *ws = L"wide" L"r";
gen int (*fp)(int) = 0, (*afp[2])(void), *(*pfp)(char);
gen _Static_assert(1, "ok");
gen _Alignas(8) int aligned;
gen int f(void) { return _Alignof(double) + sizeof(char *) + offsetof(struct s, a.b[2]); }
show _Atomic(int) ai; _Atomic int aj; int * _Atomic ak;
gen _Atomic(int) ai; _Atomic int aj; int * _Atomic ak;
show int f(int, char *, ...);
show int f(a, b) int a; char b; { return a + b; }
show int x = 1.5e+10f + 0x1.8p3 + 0X1P-2L + 07 + 10ull + 'ab' + L'\\x41';
toks int x = 1.5e+10f + 0x1.8p3 + 0X1P-2L + 07 + 10ull + 'ab' + L'\\x41';
toks a->b.c ... <<= >>= ++ -- && || <= >= == != += -= *= /= %= &= |= ^= ? : ~ !
toks typedef long L; L a; int L2; struct L { L L; };
showx int{TAB}x ;{NL}{NL}  int  y;{NL}
show int x = 089;
show int x = 1;}
show int x = '\\q';
show int x = '';
show char *s = "\\q";
show int x = 'abcde';
show int x = 'a
show int x = 'a{NL}int y;
show int x = 1 @ 2;
show int x = `1`;
show int f(void) { return 1 +; }
show int f(void) { return 1 }
show int 1x;
show struct { int a; } ;
show typedef int T; int T;
show int T; typedef int T;
show void f(void) { int a; a. 1; }
show int f(void) g(void);
show int x = 1
show x = 1;
show typedef void f(void) {}
show int a[*];
show #include <stdio.h>
show int x; #pragma weak x
show _Pragma("once") int x;
show int x = sizeof(int) ? : 1;
show double d = 1e;
"""

lines = JOBS.splitlines() + ["snip " + s for s in SNIPS.splitlines()]
write("jobs.txt", "\n".join(lines) + "\n")
