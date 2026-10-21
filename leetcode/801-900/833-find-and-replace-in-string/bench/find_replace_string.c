// Benchmark for #833: Find And Replace in String -- the ★ arm (a table by index).
//
// Mirrors find_replace_string.kara: each operation whose source occurs at
// its index is recorded in a table at that index, and one walk over the
// string writes each recorded operation's target in place of its source
// and copies the other letters. As in the Kāra program, the table and the
// answer are fresh allocations, the answer growing by doubling.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    int64_t len, cap;
} Str;

static void push(Str *out, const char *p, int64_t len) {
    if (out->len + len > out->cap) {
        int64_t cap = out->cap ? out->cap * 2 : 8;
        while (cap < out->len + len) cap *= 2;
        out->data = realloc(out->data, (size_t)cap);
        out->cap = cap;
    }
    memcpy(out->data + out->len, p, (size_t)len);
    out->len += len;
}

typedef struct {
    char s[1000];
    int64_t n, k;
    int64_t indices[100];
    char sources[100][10];
    int64_t source_lens[100];
    char targets[100][7];
    int64_t target_lens[100];
} Case;

static Str find_replace_string(const Case *c) {
    int64_t n = c->n;
    int64_t *at = malloc((size_t)n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) at[i] = -1;
    for (int64_t k = 0; k < c->k; k++) {
        int64_t i = c->indices[k], len = c->source_lens[k];
        if (i + len <= n && memcmp(c->s + i, c->sources[k], (size_t)len) == 0) at[i] = k;
    }
    Str out = {0, 0, 0};
    int64_t i = 0;
    while (i < n) {
        int64_t k = at[i];
        if (k >= 0) {
            push(&out, c->targets[k], c->target_lens[k]);
            i += c->source_lens[k];
        } else {
            push(&out, c->s + i, 1);
            i += 1;
        }
    }
    free(at);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void swap64(int64_t *a, int64_t *b) {
    int64_t t = *a;
    *a = *b;
    *b = t;
}

int main(void) {
    const int64_t count = 64, rounds = 300000, n = 1000;
    int64_t seed = 833;
    static Case cases[64];
    for (int64_t g = 0; g < count; g++) {
        Case *c = &cases[g];
        c->n = n;
        for (int64_t i = 0; i < n; i++) c->s[i] = (char)('a' + next_random(&seed) % 2);
        int64_t k = 0;
        int64_t pos = next_random(&seed) % 4;
        while (pos < n && k < 100) {
            int64_t room = n - pos < 10 ? n - pos : 10;
            int64_t len = 1 + next_random(&seed) % room;
            memcpy(c->sources[k], c->s + pos, (size_t)len);
            if (next_random(&seed) % 3 == 2) {
                int64_t last = c->sources[k][len - 1] - 97;
                c->sources[k][len - 1] = (char)('a' + (last + 1) % 26);
            }
            c->source_lens[k] = len;
            int64_t tlen = 1 + next_random(&seed) % 7;
            for (int64_t t = 0; t < tlen; t++) c->targets[k][t] = (char)('a' + next_random(&seed) % 26);
            c->target_lens[k] = tlen;
            c->indices[k] = pos;
            k++;
            pos += len + next_random(&seed) % 4;
        }
        c->k = k;
        int64_t i = k;
        while (i > 1) {
            int64_t j = next_random(&seed) % i;
            i -= 1;
            swap64(&c->indices[i], &c->indices[j]);
            swap64(&c->source_lens[i], &c->source_lens[j]);
            swap64(&c->target_lens[i], &c->target_lens[j]);
            char tmp[10];
            memcpy(tmp, c->sources[i], 10);
            memcpy(c->sources[i], c->sources[j], 10);
            memcpy(c->sources[j], tmp, 10);
            memcpy(tmp, c->targets[i], 7);
            memcpy(c->targets[i], c->targets[j], 7);
            memcpy(c->targets[j], tmp, 7);
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        Str out = find_replace_string(&cases[round % count]);
        total += out.len;
        checksum = (checksum * 131 + (unsigned char)out.data[round / count % out.len]) % 1000000007;
        free(out.data);
    }
    printf("%lld rounds of %lld cases: %lld letters, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    return 0;
}
