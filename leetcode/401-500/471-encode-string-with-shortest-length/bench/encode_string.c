// Benchmark for #471 -- C mirror of the ★ arm (encode_string.kara):
// interval DP over the encodings, with the shortest unit found where t
// first appears again in t + t (strstr). Every encoding is its own
// heap string, as in the other languages.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *dup_range(const char *s, size_t len) {
    char *out = malloc(len + 1);
    memcpy(out, s, len);
    out[len] = '\0';
    return out;
}

// Returns a new heap string; the caller frees it.
static char *encode(const char *s) {
    size_t n = strlen(s);
    char **best = calloc(n * n, sizeof(char *));
    size_t *blen = calloc(n * n, sizeof(size_t));
    char *doubled = malloc(2 * n + 1);
    for (size_t len = 1; len <= n; len++) {
        for (size_t i = 0; i + len <= n; i++) {
            size_t j = i + len - 1;
            char *shortest = dup_range(s + i, len);
            size_t slen = len;
            memcpy(doubled, s + i, len);
            memcpy(doubled + len, s + i, len);
            doubled[2 * len] = '\0';
            size_t unit = 1 + (size_t)(strstr(doubled + 1, shortest) - (doubled + 1));
            if (unit < len) {
                size_t inner = blen[i * n + i + unit - 1];
                size_t plen = (size_t)snprintf(NULL, 0, "%zu", len / unit) + 2 + inner;
                if (plen < slen) {
                    char *packed = malloc(plen + 1);
                    snprintf(packed, plen + 1, "%zu[%s]", len / unit, best[i * n + i + unit - 1]);
                    free(shortest);
                    shortest = packed;
                    slen = plen;
                }
            }
            for (size_t k = i; k < j; k++) {
                size_t a = blen[i * n + k], b = blen[(k + 1) * n + j];
                if (a + b < slen) {
                    char *joined = malloc(a + b + 1);
                    memcpy(joined, best[i * n + k], a);
                    memcpy(joined + a, best[(k + 1) * n + j], b + 1);
                    free(shortest);
                    shortest = joined;
                    slen = a + b;
                }
            }
            best[i * n + j] = shortest;
            blen[i * n + j] = slen;
        }
    }
    char *out = dup_range(best[n - 1], blen[n - 1]);
    for (size_t x = 0; x < n * n; x++) free(best[x]);
    free(best);
    free(blen);
    free(doubled);
    return out;
}

// ---- bench ------------------------------------------------------------------

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

// Appends to *buf (growing it); *len is its length.
static void push(char **buf, size_t *len, size_t *cap, const char *src, size_t n) {
    if (*len + n + 1 > *cap) {
        while (*len + n + 1 > *cap) *cap *= 2;
        *buf = realloc(*buf, *cap);
    }
    memcpy(*buf + *len, src, n);
    *len += n;
    (*buf)[*len] = '\0';
}

static char *random_string(long long *seed, long long letters, long long depth, size_t *out_len) {
    size_t cap = 16, len = 0;
    char *s = malloc(cap);
    s[0] = '\0';
    long long pieces = 1 + next_random(seed) % 4;
    for (long long p = 0; p < pieces; p++) {
        if (depth > 0 && next_random(seed) % 2 == 0) {
            size_t ulen;
            char *unit = random_string(seed, letters, depth - 1, &ulen);
            long long copies = 2 + next_random(seed) % 11;
            for (long long c = 0; c < copies; c++) push(&s, &len, &cap, unit, ulen);
            free(unit);
        } else {
            char c = (char)(97 + next_random(seed) % letters);
            push(&s, &len, &cap, &c, 1);
        }
    }
    *out_len = len;
    return s;
}

int main(void) {
    int count = 400;
    size_t size = 150;
    long long seed = 471;
    char **strings = malloc(count * sizeof(char *));
    for (int c = 0; c < count; c++) {
        long long letters = 2 + next_random(&seed) % 2;
        size_t cap = 16, len = 0;
        char *s = malloc(cap);
        s[0] = '\0';
        while (len < size) {
            size_t plen;
            char *piece = random_string(&seed, letters, 2, &plen);
            push(&s, &len, &cap, piece, plen);
            free(piece);
        }
        s[size] = '\0';
        strings[c] = s;
    }
    long long total = 0, checksum = 0;
    for (int i = 0; i < count; i++) {
        char *e = encode(strings[i]);
        long long elen = (long long)strlen(e);
        total += elen;
        checksum = (checksum * 31 + elen) % 1000000007;
        free(e);
    }
    printf("%d strings of %zu letters: %lld letters encoded, checksum %lld\n", count, size, total, checksum);
    for (int c = 0; c < count; c++) free(strings[c]);
    free(strings);
    return 0;
}
