// Benchmark for #843: Guess the Word -- C twin of the Kāra ★ arm (minimax
// over the words still possible).
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#define N 100

typedef struct {
    char (*words)[7];
    int64_t n;
    const char *secret;
    int64_t guesses;
    bool found;
} Master;

static int64_t master_guess(Master *m, const char *word) {
    m->guesses++;
    bool listed = false;
    for (int64_t i = 0; i < m->n; i++) {
        if (strcmp(m->words[i], word) == 0) {
            listed = true;
            break;
        }
    }
    if (!listed) return -1;
    if (strcmp(word, m->secret) == 0 && m->guesses <= 10) m->found = true;
    int64_t count = 0;
    for (int k = 0; k < 6; k++)
        if (word[k] == m->secret[k]) count++;
    return count;
}

static int64_t shared(const char *a, const char *b) {
    int64_t count = 0;
    for (int k = 0; k < 6; k++)
        if (a[k] == b[k]) count++;
    return count;
}

static void find_secret_word(char (*words)[7], int64_t n, Master *master) {
    static int64_t same[N][N];
    for (int64_t i = 0; i < n; i++)
        for (int64_t j = 0; j < n; j++) same[i][j] = shared(words[i], words[j]);
    int64_t possible[N], left[N];
    int64_t count = n;
    for (int64_t i = 0; i < n; i++) possible[i] = i;
    while (count > 0) {
        int64_t best = possible[0], best_worst = n + 1;
        for (int64_t a = 0; a < count; a++) {
            int64_t c = possible[a];
            int64_t groups[7] = {0};
            for (int64_t b = 0; b < count; b++) groups[same[c][possible[b]]]++;
            int64_t worst = 0;
            for (int k = 0; k < 6; k++)
                if (groups[k] > worst) worst = groups[k];
            if (worst < best_worst) {
                best_worst = worst;
                best = c;
            }
        }
        int64_t answer = master_guess(master, words[best]);
        if (answer == 6) return;
        int64_t kept = 0;
        for (int64_t b = 0; b < count; b++)
            if (same[best][possible[b]] == answer) left[kept++] = possible[b];
        memcpy(possible, left, (size_t)kept * sizeof(int64_t));
        count = kept;
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 6000;
    int64_t seed = 843;
    static char lists[64][N][7];
    static char secrets[64][7];
    const int64_t ks[4] = {4, 8, 16, 26};
    for (int64_t g = 0; g < count; g++) {
        int64_t k = ks[g % 4];
        int64_t have = 0;
        while (have < N) {
            char w[7];
            for (int i = 0; i < 6; i++) w[i] = (char)(97 + next_random(&seed) % k);
            w[6] = 0;
            bool dup = false;
            for (int64_t i = 0; i < have; i++)
                if (strcmp(lists[g][i], w) == 0) {
                    dup = true;
                    break;
                }
            if (!dup) memcpy(lists[g][have++], w, 7);
        }
        memcpy(secrets[g], lists[g][next_random(&seed) % N], 7);
    }
    int64_t found = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t g = round % count;
        Master master = {lists[g], N, secrets[g], 0, false};
        find_secret_word(lists[g], N, &master);
        if (master.found) found++;
        checksum = (checksum * 31 + master.guesses) % 1000000007;
    }
    printf("%lld rounds of %lld lists: %lld found, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)found, (long long)checksum);
    return 0;
}
