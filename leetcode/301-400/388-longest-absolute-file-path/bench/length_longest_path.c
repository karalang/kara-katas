// Benchmark for #388: mirror of length_longest_path.kara (path lengths by depth).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t length_longest_path(const char *b, int64_t n) {
    int64_t len[64];
    int64_t levels = 1;
    len[0] = 0;
    int64_t best = 0;
    int64_t i = 0;
    while (i < n) {
        int64_t depth = 0;
        while (i < n && b[i] == '\t') {
            depth++;
            i++;
        }
        int64_t start = i;
        int is_file = 0;
        while (i < n && b[i] != '\n') {
            if (b[i] == '.') is_file = 1;
            i++;
        }
        int64_t path = len[depth] + (i - start);
        if (is_file) {
            if (path > best) best = path;
        } else if (depth + 1 < levels) {
            len[depth + 1] = path + 1;
        } else {
            len[levels++] = path + 1;
        }
        i++;
    }
    return best;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

typedef struct {
    char *buf;
    int64_t len, cap;
} Buf;

static void put(Buf *s, char c) {
    if (s->len == s->cap) {
        s->cap = s->cap ? s->cap * 2 : 64;
        s->buf = realloc(s->buf, s->cap);
    }
    s->buf[s->len++] = c;
}

static Buf listing(int64_t *seed, int64_t entries) {
    Buf out = {0};
    int64_t open = 0, depth = 0;
    for (int64_t k = 0; k < entries; k++) {
        int64_t r = step(seed) % 100;
        if (r < 35) {
            depth = open;
        } else if (r >= 70) {
            int64_t up = (r - 70) / 10 + 1;
            depth = up > depth ? 0 : depth - up;
        }
        if (depth > open) depth = open;
        int64_t name_len = step(seed) % 12 + 1;
        int file = step(seed) % 3 == 0;
        if (k > 0) put(&out, '\n');
        for (int64_t t = 0; t < depth; t++) put(&out, '\t');
        for (int64_t t = 0; t < name_len; t++) put(&out, (char)(step(seed) % 26 + 97));
        if (file) {
            put(&out, '.'), put(&out, 'e'), put(&out, 'x'), put(&out, 't');
            open = depth;
        } else {
            open = depth < 6 ? depth + 1 : depth;
        }
    }
    return out;
}

int main(void) {
    int64_t seed = 388;
    Buf listings[200];
    int64_t bytes = 0;
    for (int k = 0; k < 200; k++) {
        listings[k] = listing(&seed, 800);
        bytes += listings[k].len;
    }
    int64_t checksum = 0;
    for (int64_t round = 0; round < 150; round++) {
        for (int k = 0; k < 200; k++) {
            int64_t r = length_longest_path(listings[k].buf, listings[k].len);
            checksum = (checksum * 31 + r + round) % 1000000007;
        }
    }
    printf("%lld bytes in 200 listings, 150 rounds, checksum %lld\n", (long long)bytes, (long long)checksum);
    for (int k = 0; k < 200; k++) free(listings[k].buf);
    return 0;
}
