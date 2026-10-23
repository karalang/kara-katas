// LeetCode #893 bench: the union-find arm (every pair of words compared by
// their counts of letters at even and at odd positions) on 300 lists of
// 1,000 words of 20 letters. The same algorithm as
// num_special_equiv_groups.kara.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define WORDS 1000
#define LEN 20

static int64_t seed = 893;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t counts[WORDS][52];
static int64_t parent[WORDS];

static int64_t find(int64_t x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static int same(const int64_t *a, const int64_t *b) {
    for (int k = 0; k < 52; k++)
        if (a[k] != b[k]) return 0;
    return 1;
}

static int64_t num_special_equiv_groups(char words[][LEN], int64_t n) {
    for (int64_t w = 0; w < n; w++) {
        memset(counts[w], 0, sizeof counts[w]);
        for (int64_t i = 0; i < LEN; i++) counts[w][words[w][i] - 97 + 26 * (i % 2)]++;
    }
    for (int64_t i = 0; i < n; i++) parent[i] = i;
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = i + 1; j < n; j++) {
            if (same(counts[i], counts[j])) {
                int64_t a = find(i), b = find(j);
                if (a != b) parent[a] = b;
            }
        }
    }
    int64_t groups = 0;
    for (int64_t i = 0; i < n; i++)
        if (find(i) == i) groups++;
    return groups;
}

static char words[WORDS][LEN];

int main(void) {
    int64_t groups = 0, check = 0;
    for (int c = 0; c < 300; c++) {
        int64_t n = 0;
        for (int w = 0; w < WORDS; w++) {
            if (n > 0 && next_random() % 2 == 0) {
                int64_t k = next_random() % n;
                memcpy(words[n], words[k], LEN);
                for (int s = 0; s < LEN; s++) {
                    int64_t i = next_random() % LEN;
                    int64_t j = next_random() % LEN;
                    if (i % 2 == j % 2) {
                        char t = words[n][i];
                        words[n][i] = words[n][j];
                        words[n][j] = t;
                    }
                }
            } else {
                for (int i = 0; i < LEN; i++) words[n][i] = (char)(97 + next_random() % 26);
            }
            n++;
        }
        int64_t got = num_special_equiv_groups(words, n);
        groups += got;
        check = (check * 131 + got) % 1000000007;
    }
    printf("300 lists of 1000 words of 20 letters: %lld groups, checksum %lld\n", (long long)groups, (long long)check);
    return 0;
}
