// Benchmark mirror of nested_weight_sum.kara (LeetCode #339): parse a list's
// text into the tree, then walk it. Same lists, rounds and sink.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Nested Nested;
typedef struct {
    Nested *data;
    int64_t len, cap;
} List;
struct Nested {
    int is_list;
    int64_t v;
    List items;
};

static void push(List *l, Nested x) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->data = realloc(l->data, (size_t)l->cap * sizeof(Nested));
    }
    l->data[l->len++] = x;
}

static void free_list(List *l) {
    for (int64_t i = 0; i < l->len; i++)
        if (l->data[i].is_list) free_list(&l->data[i].items);
    free(l->data);
}

static int64_t depth_sum(const List *items, int64_t depth) {
    int64_t total = 0;
    for (int64_t i = 0; i < items->len; i++) {
        const Nested *it = &items->data[i];
        if (it->is_list)
            total += depth_sum(&it->items, depth + 1);
        else
            total += it->v * depth;
    }
    return total;
}

static int64_t weight_sum(const List *items) { return depth_sum(items, 1); }

static List parse_list(const uint32_t *text, int64_t *pos) {
    List items = {0};
    *pos += 1;
    while (text[*pos] != ']') {
        if (text[*pos] == ',') {
            *pos += 1;
        } else if (text[*pos] == '[') {
            Nested n = {1, 0, parse_list(text, pos)};
            push(&items, n);
        } else {
            int64_t sign = 1;
            if (text[*pos] == '-') {
                sign = -1;
                *pos += 1;
            }
            int64_t v = 0;
            while (text[*pos] >= '0' && text[*pos] <= '9') {
                v = v * 10 + (int64_t)(text[*pos] - '0');
                *pos += 1;
            }
            Nested n = {0, sign * v, {0}};
            push(&items, n);
        }
    }
    *pos += 1;
    return items;
}

// The text as an array of code points, as the Kāra arm's chars().collect().
static List parse(const char *text) {
    size_t n = strlen(text);
    uint32_t *cs = malloc(n * sizeof(uint32_t));
    for (size_t i = 0; i < n; i++) cs[i] = (unsigned char)text[i];
    int64_t pos = 0;
    List items = parse_list(cs, &pos);
    free(cs);
    return items;
}

typedef struct {
    char *s;
    size_t len, cap;
} Buf;

static void put(Buf *b, const char *s) {
    size_t n = strlen(s);
    while (b->len + n + 1 > b->cap) {
        b->cap = b->cap ? b->cap * 2 : 64;
        b->s = realloc(b->s, b->cap);
    }
    memcpy(b->s + b->len, s, n + 1);
    b->len += n;
}

static int64_t next(int64_t *state) {
    *state = (*state * 1103515245 + 12345) % 2147483648LL;
    return *state >> 8;
}

static void gen_member(int64_t *state, int64_t depth, int64_t max_depth, Buf *out) {
    if (depth < max_depth && next(state) % 3 == 0) {
        put(out, "[");
        int64_t count = next(state) % 5;
        for (int64_t k = 0; k < count; k++) {
            if (k > 0) put(out, ",");
            gen_member(state, depth + 1, max_depth, out);
        }
        put(out, "]");
    } else {
        char tmp[32];
        snprintf(tmp, sizeof tmp, "%lld", (long long)(next(state) % 201 - 100));
        put(out, tmp);
    }
}

static char *gen_text(int64_t seed, int64_t top, int64_t max_depth) {
    int64_t state = seed;
    Buf out = {0};
    put(&out, "[");
    for (int64_t k = 0; k < top; k++) {
        if (k > 0) put(&out, ",");
        gen_member(&state, 1, max_depth, &out);
    }
    put(&out, "]");
    return out.s;
}

int main(void) {
    char *texts[8];
    for (int64_t s = 0; s < 8; s++) texts[s] = gen_text(s * 7919 + 1, 800, 12);
    int64_t hash = 0;
    for (int r = 0; r < 4000; r++) {
        List items = parse(texts[r % 8]);
        int64_t w = weight_sum(&items);
        free_list(&items);
        hash = (hash * 31 + w + 1000000) % 1000000007;
    }
    printf("%lld\n", (long long)hash);
    for (int s = 0; s < 8; s++) free(texts[s]);
    return 0;
}
