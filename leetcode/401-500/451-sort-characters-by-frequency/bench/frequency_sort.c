// Benchmark for #451: mirror of frequency_sort.kara (count, then sort
// the distinct characters) on 20 random strings of 200,000 characters,
// built once, then each sorted 5 times. C has no hash map, so the
// counts live in an array of 128, indexed by the ASCII code.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t negative;
    char c;
} Entry;

static int compare(const void *a, const void *b) {
    const Entry *x = a, *y = b;
    if (x->negative != y->negative) {
        return x->negative < y->negative ? -1 : 1;
    }
    return (x->c > y->c) - (x->c < y->c);
}

static char *frequency_sort(const char *s, size_t len) {
    int64_t counts[128] = {0};
    for (size_t i = 0; i < len; i++) {
        counts[(unsigned char)s[i]]++;
    }
    Entry order[128];
    int k = 0;
    for (int c = 0; c < 128; c++) {
        if (counts[c] > 0) {
            order[k].negative = -counts[c];
            order[k].c = (char)c;
            k++;
        }
    }
    qsort(order, (size_t)k, sizeof(Entry), compare);
    char *out = malloc(len + 1);
    size_t at = 0;
    for (int i = 0; i < k; i++) {
        memset(out + at, order[i].c, (size_t)-order[i].negative);
        at += (size_t)-order[i].negative;
    }
    out[at] = '\0';
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    enum { COUNT = 20, N = 200000, ROUNDS = 5 };
    const int64_t sizes[4] = {3, 10, 30, 62};
    int64_t seed = 451;
    char *strings[COUNT];
    for (int i = 0; i < COUNT; i++) {
        // From the first 3, 10, 30 or all 62 characters, in turn.
        int64_t k = sizes[i % 4];
        strings[i] = malloc(N + 1);
        for (int j = 0; j < N; j++) {
            strings[i][j] = alphabet[next_random(&seed) % k];
        }
        strings[i][N] = '\0';
    }
    int64_t characters = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++) {
        for (int i = 0; i < COUNT; i++) {
            char *out = frequency_sort(strings[i], N);
            int64_t len = (int64_t)strlen(out);
            characters += len;
            int64_t sample = (int64_t)out[0] * 65536 + (int64_t)out[len / 2] * 256 + (int64_t)out[len - 1];
            checksum = (checksum * 31 + len + sample) % 1000000007;
            free(out);
        }
    }
    for (int i = 0; i < COUNT; i++) {
        free(strings[i]);
    }
    printf("%d rounds on %d strings of %d: %lld characters, checksum %lld\n", ROUNDS, COUNT, N,
           (long long)characters, (long long)checksum);
    return 0;
}
