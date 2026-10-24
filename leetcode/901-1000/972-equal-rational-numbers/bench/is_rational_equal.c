// Benchmark: LeetCode #972 Equal Rational Numbers -- the ★ arm, both as
// fractions in lowest terms, on 1000 random pairs of strings. Mirrors
// is_rational_equal.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t gcd(int64_t a, int64_t b) { return b == 0 ? a : gcd(b, a % b); }

static void fraction(const char *s, int64_t *num, int64_t *den) {
    int64_t whole = 0, shift = 1, rep = 0, nines = 0;
    int part = 0;
    for (; *s; s++) {
        char c = *s;
        if (c == '.') {
            part = 1;
        } else if (c == '(') {
            part = 2;
        } else if (c != ')') {
            int64_t d = c - '0';
            if (part == 2) {
                rep = rep * 10 + d;
                nines = nines * 10 + 9;
            } else {
                whole = whole * 10 + d;
                if (part == 1) shift *= 10;
            }
        }
    }
    int64_t n, m;
    if (nines == 0) {
        n = whole;
        m = shift;
    } else {
        n = whole * nines + rep;
        m = shift * nines;
    }
    int64_t g = gcd(n, m);
    *num = n / g;
    *den = m / g;
}

static int is_rational_equal(const char *s, const char *t) {
    int64_t a, da, b, db;
    fraction(s, &a, &da);
    fraction(t, &b, &db);
    return a == b && da == db;
}

static int64_t seed = 972;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

typedef struct {
    int64_t int_part;
    char non[8], rep[8];
    int dot;
} Num;

static void digits(char *out, int64_t len) {
    for (int64_t i = 0; i < len; i++) out[i] = (char)('0' + next_random() % 10);
    out[len] = 0;
}

static void text(const Num *x, char *out) {
    int k = sprintf(out, "%lld", (long long)x->int_part);
    if (x->dot || x->non[0] || x->rep[0]) out[k++] = '.';
    k += sprintf(out + k, "%s", x->non);
    if (x->rep[0]) k += sprintf(out + k, "(%s)", x->rep);
    out[k] = 0;
}

static Num random_num(void) {
    Num x;
    int64_t len = 1 + next_random() % 4;
    x.int_part = next_random() % 10;
    for (int64_t i = 1; i < len; i++) x.int_part = x.int_part * 10 + next_random() % 10;
    digits(x.non, next_random() % 5);
    if (next_random() % 3 == 0) {
        x.rep[0] = 0;
    } else {
        digits(x.rep, 1 + next_random() % 4);
    }
    x.dot = next_random() % 2 == 0;
    return x;
}

static Num variant(const Num *x) {
    Num y = *x;
    int64_t steps = 1 + next_random() % 3;
    for (int64_t s = 0; s < steps; s++) {
        int64_t kind = next_random() % 7;
        size_t r = strlen(y.rep), n = strlen(y.non);
        if (kind == 0 && r > 0 && n < 4) {
            char first = y.rep[0];
            y.non[n] = first;
            y.non[n + 1] = 0;
            memmove(y.rep, y.rep + 1, r - 1);
            y.rep[r - 1] = first;
        } else if (kind == 1 && r > 0 && 2 * r <= 4) {
            memcpy(y.rep + r, y.rep, r);
            y.rep[2 * r] = 0;
        } else if (kind == 2 && r == 0 && n < 4) {
            y.non[n] = '0';
            y.non[n + 1] = 0;
        } else if (kind == 3 && r == 0) {
            strcpy(y.rep, "0");
        } else if (kind == 4 && r == 0) {
            if (n > 0 && y.non[n - 1] != '0') {
                y.non[n - 1]--;
                strcpy(y.rep, "9");
            } else if (n == 0 && y.int_part > 0) {
                y.int_part--;
                strcpy(y.rep, "9");
            }
        } else if (kind == 5 && r > 0 && strspn(y.rep, "0") == r) {
            y.rep[0] = 0;
            y.dot = 1;
        } else if (kind == 6 && r % 2 == 0 && r > 0 && memcmp(y.rep, y.rep + r / 2, r / 2) == 0) {
            y.rep[r / 2] = 0;
        }
    }
    return y;
}

static void nudge(char *s) {
    size_t len = strlen(s);
    size_t places[32], count = 0;
    for (size_t i = 0; i < len; i++)
        if (s[i] >= '0' && s[i] <= '9') places[count++] = i;
    size_t at = places[next_random() % (int64_t)count];
    int64_t old = s[at] - '0';
    int64_t nw = next_random() % 9;
    if (nw >= old) nw++;
    if (at == 0 && nw == 0 && len > 1 && s[1] >= '0' && s[1] <= '9') {
        nw = 1 + old % 9;
        if (nw == old) nw = 9;
    }
    s[at] = (char)('0' + nw);
}

int main(void) {
    enum { ROUNDS = 1000, COUNT = 1000 };
    static char ss[COUNT][32], ts[COUNT][32];
    for (int c = 0; c < COUNT; c++) {
        Num x = random_num();
        text(&x, ss[c]);
        if (c % 3 == 0) {
            Num y = variant(&x);
            text(&y, ts[c]);
        } else if (c % 3 == 1) {
            Num y = variant(&x);
            text(&y, ts[c]);
            nudge(ts[c]);
        } else {
            Num y = random_num();
            text(&y, ts[c]);
        }
    }
    int64_t equal = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++) {
        for (int i = 0; i < COUNT; i++) {
            int k = (r + i) % COUNT;
            if (is_rational_equal(ss[k], ts[k])) {
                equal++;
                check = (check * 2 + 1) % 1000000007;
            } else {
                check = check * 2 % 1000000007;
            }
        }
    }
    printf("%d rounds over %d pairs: %lld equal, checksum %lld\n", ROUNDS, COUNT, (long long)equal, (long long)check);
    return 0;
}
