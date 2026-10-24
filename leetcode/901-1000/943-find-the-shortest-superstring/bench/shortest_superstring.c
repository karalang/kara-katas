// Benchmark: LeetCode #943 Find the Shortest Superstring -- the ★ arm,
// the most letters saved, on sets of 12 words of 20 letters, LeetCode's
// largest. Mirrors shortest_superstring.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 12
#define LENGTH 20

static int64_t overlap(const char *a, int64_t la, const char *b, int64_t lb) {
    int64_t k = (la < lb ? la : lb) - 1;
    while (k > 0) {
        if (memcmp(a + la - k, b, (size_t)k) == 0) {
            return k;
        }
        k--;
    }
    return 0;
}

// Writes the answer into out and returns its length.
static int64_t shortest_superstring(char words[][LENGTH + 1], int64_t n, char *out) {
    int64_t len[SIZE];
    for (int64_t i = 0; i < n; i++) {
        len[i] = (int64_t)strlen(words[i]);
    }
    int64_t ov[SIZE * SIZE] = {0};
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = 0; j < n; j++) {
            if (i != j) {
                ov[i * n + j] = overlap(words[i], len[i], words[j], len[j]);
            }
        }
    }
    int64_t full = ((int64_t)1 << n) - 1;
    int64_t states = (full + 1) * n;
    int64_t *saved = malloc(sizeof(int64_t) * (size_t)states);
    int64_t *before = malloc(sizeof(int64_t) * (size_t)states);
    for (int64_t s = 0; s < states; s++) {
        saved[s] = -1;
        before[s] = -1;
    }
    for (int64_t mask = 1; mask <= full; mask++) {
        for (int64_t last = 0; last < n; last++) {
            if ((mask >> last) & 1) {
                int64_t rest = mask ^ ((int64_t)1 << last);
                if (rest == 0) {
                    saved[mask * n + last] = 0;
                } else {
                    for (int64_t p = 0; p < n; p++) {
                        if ((rest >> p) & 1) {
                            int64_t s = saved[rest * n + p] + ov[p * n + last];
                            if (s > saved[mask * n + last]) {
                                saved[mask * n + last] = s;
                                before[mask * n + last] = p;
                            }
                        }
                    }
                }
            }
        }
    }
    int64_t last = 0;
    for (int64_t w = 1; w < n; w++) {
        if (saved[full * n + w] > saved[full * n + last]) {
            last = w;
        }
    }
    int64_t order[SIZE];
    int64_t count = 0;
    int64_t mask = full;
    while (last >= 0) {
        order[count++] = last;
        int64_t p = before[mask * n + last];
        mask ^= (int64_t)1 << last;
        last = p;
    }
    int64_t first = order[count - 1];
    memcpy(out, words[first], (size_t)len[first]);
    int64_t at = len[first];
    for (int64_t i = count - 1; i > 0; i--) {
        int64_t a = order[i], b = order[i - 1];
        memcpy(out + at, words[b] + ov[a * n + b], (size_t)(len[b] - ov[a * n + b]));
        at += len[b] - ov[a * n + b];
    }
    free(saved);
    free(before);
    return at;
}

static int64_t seed = 943;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 10, count = 40;
    static char sets[40][SIZE][LENGTH + 1];
    for (int64_t c = 0; c < count; c++) {
        int64_t letters = 2 + next_random() % 3;
        int64_t have = 0;
        while (have < SIZE) {
            char w[LENGTH + 1];
            for (int64_t k = 0; k < LENGTH; k++) {
                w[k] = (char)(next_random() % letters + 97);
            }
            w[LENGTH] = 0;
            int dup = 0;
            for (int64_t h = 0; h < have; h++) {
                if (strcmp(sets[c][h], w) == 0) {
                    dup = 1;
                }
            }
            if (!dup) {
                memcpy(sets[c][have++], w, LENGTH + 1);
            }
        }
    }
    static char out[SIZE * LENGTH + 1];
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t len = shortest_superstring(sets[(r + i) % count], SIZE, out);
            total += len;
            for (int64_t k = 0; k < len; k++) {
                check = (check * 31 + (unsigned char)out[k]) % 1000000007;
            }
        }
    }
    printf("%lld rounds over %lld sets of %d words of %d letters: lengths adding to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, SIZE, LENGTH, (long long)total, (long long)check);
    return 0;
}
