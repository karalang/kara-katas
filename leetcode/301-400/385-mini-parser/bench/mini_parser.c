// Benchmark for #385: mirror of mini_parser.kara (recursive descent).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct NestedInteger {
    int is_list;
    int64_t value;
    struct NestedInteger *items;
    int64_t len, cap;
} NestedInteger;

static void push(NestedInteger *list, NestedInteger item) {
    if (list->len == list->cap) {
        list->cap = list->cap ? list->cap * 2 : 4;
        list->items = realloc(list->items, list->cap * sizeof(NestedInteger));
    }
    list->items[list->len++] = item;
}

static NestedInteger parse_value(const char *b, int64_t n, int64_t *pos) {
    NestedInteger x = {0};
    if (b[*pos] == '[') {
        x.is_list = 1;
        (*pos)++;
        if (b[*pos] == ']') {
            (*pos)++;
            return x;
        }
        for (;;) {
            push(&x, parse_value(b, n, pos));
            if (b[*pos] == ',') {
                (*pos)++;
            } else {
                (*pos)++;
                return x;
            }
        }
    }
    int negative = 0;
    if (b[*pos] == '-') {
        negative = 1;
        (*pos)++;
    }
    int64_t v = 0;
    while (*pos < n && b[*pos] >= '0' && b[*pos] <= '9') {
        v = v * 10 + (b[*pos] - '0');
        (*pos)++;
    }
    x.value = negative ? -v : v;
    return x;
}

static NestedInteger deserialize(const char *s, int64_t n) {
    int64_t pos = 0;
    return parse_value(s, n, &pos);
}

static void release(NestedInteger *x) {
    if (!x->is_list) return;
    for (int64_t i = 0; i < x->len; i++) release(&x->items[i]);
    free(x->items);
}

static void shape(const NestedInteger *x, int64_t *depth, int64_t *count, int64_t *sum) {
    if (!x->is_list) {
        *depth = 0, *count = 1, *sum = x->value;
        return;
    }
    int64_t d = 0, c = 0, s = 0;
    for (int64_t i = 0; i < x->len; i++) {
        int64_t di, ci, si;
        shape(&x->items[i], &di, &ci, &si);
        if (di > d) d = di;
        c += ci;
        s += si;
    }
    *depth = d + 1, *count = c, *sum = s;
}

typedef struct {
    char *buf;
    int64_t len, cap;
} Str;

static void put(Str *s, const char *t) {
    int64_t k = strlen(t);
    while (s->len + k + 1 > s->cap) {
        s->cap = s->cap ? s->cap * 2 : 64;
        s->buf = realloc(s->buf, s->cap);
    }
    memcpy(s->buf + s->len, t, k + 1);
    s->len += k;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static void random_value(int64_t *seed, int64_t depth, Str *out) {
    int64_t r = next(seed) % 10;
    if (depth == 0 || r < 4) {
        char num[32];
        snprintf(num, sizeof num, "%lld", (long long)(next(seed) % 2000001 - 1000000));
        put(out, num);
        return;
    }
    int64_t n = next(seed) % 5;
    put(out, "[");
    for (int64_t i = 0; i < n; i++) {
        if (i > 0) put(out, ",");
        random_value(seed, depth - 1, out);
    }
    put(out, "]");
}

int main(void) {
    int64_t seed = 385;
    Str s = {0};
    put(&s, "[");
    while (s.len < 49000) {
        if (s.len > 1) put(&s, ",");
        random_value(&seed, 5, &s);
    }
    put(&s, "]");
    const int64_t p = 1000000007;
    int64_t checksum = 0;
    for (int q = 0; q < 2000; q++) {
        NestedInteger x = deserialize(s.buf, s.len);
        int64_t depth, count, sum;
        shape(&x, &depth, &count, &sum);
        checksum = ((checksum * 31 + depth * 7 + count) % p + sum % p + p) % p;
        release(&x);
    }
    printf("%lld bytes parsed 2000 times, checksum %lld\n", (long long)s.len, (long long)checksum);
    free(s.buf);
    return 0;
}
