// Benchmark: LeetCode #997 Find the Town Judge -- the ★ arm, one score
// per person, on random towns of 1000 people and 10000 trusts,
// LeetCode's largest. Mirrors find_judge.kara, .rs, .py and go-seq/.
// The trusts are rows reached through pointers, as LeetCode's C
// signature has them.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_judge(int64_t n, int64_t **trust, int64_t m) {
    int64_t *score = calloc((size_t)n + 1, sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        score[trust[i][0]]--;
        score[trust[i][1]]++;
    }
    int64_t judge = -1;
    for (int64_t person = 1; person <= n; person++) {
        if (score[person] == n - 1) {
            judge = person;
            break;
        }
    }
    free(score);
    return judge;
}

static int64_t seed = 997;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t *pair(int64_t a, int64_t b) {
    int64_t *p = malloc(sizeof(int64_t) * 2);
    p[0] = a;
    p[1] = b;
    return p;
}

// 1000 people and 10000 different trusts: in even towns 999 of them are
// everyone else trusting a judge, and the rest are at random
static int64_t **random_town(int a) {
    int64_t **pairs = malloc(sizeof(int64_t *) * 10000);
    bool *seen = calloc(2000 * 1001, sizeof(bool));
    int64_t len = 0, judge = 0;
    if (a % 2 == 0) {
        judge = 1 + next_random() % 1000;
        for (int64_t p = 1; p <= 1000; p++) {
            if (p != judge) {
                seen[p * 2000 + judge] = true;
                pairs[len++] = pair(p, judge);
            }
        }
    }
    while (len < 10000) {
        int64_t x = 1 + next_random() % 1000, y = 1 + next_random() % 1000;
        if (x != y && x != judge && !seen[x * 2000 + y]) {
            seen[x * 2000 + y] = true;
            pairs[len++] = pair(x, y);
        }
    }
    free(seen);
    return pairs;
}

int main(void) {
    int rounds = 1000;
    int64_t **towns[20];
    for (int a = 0; a < 20; a++) towns[a] = random_town(a);
    int64_t judges = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int64_t got = find_judge(1000, towns[(r + i) % 20], 10000);
            if (got > 0) judges++;
            check = (check * 31 + got + 2) % 1000000007;
        }
    }
    printf("%d rounds over 20 towns of 1000 people: %lld judges, checksum %lld\n", rounds, (long long)judges,
           (long long)check);
    return 0;
}
