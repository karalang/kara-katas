// LeetCode #990: Satisfiability of Equality Equations -- bench, the ★
// arm (union-find with path halving), the same algorithm and workload
// as equations_possible.kara. Each equation is a 4-character string.
#include <stdint.h>
#include <stdio.h>

static int64_t find(int64_t *parent, int64_t x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static int equations_possible(char (*equations)[5], int n) {
    int64_t parent[26];
    for (int i = 0; i < 26; i++) parent[i] = i;
    for (int i = 0; i < n; i++) {
        const char *e = equations[i];
        if (e[1] == '=') {
            int64_t a = find(parent, e[0] - 97);
            int64_t b = find(parent, e[3] - 97);
            parent[a] = b;
        }
    }
    for (int i = 0; i < n; i++) {
        const char *e = equations[i];
        if (e[1] == '!' && find(parent, e[0] - 97) == find(parent, e[3] - 97)) return 0;
    }
    return 1;
}

static int64_t seed = 990;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char sets[20][500][5];

int main(void) {
    int rounds = 6000;
    for (int i = 0; i < 20; i++) {
        for (int j = 0; j < 500; j++) {
            char *e = sets[i][j];
            e[0] = (char)(97 + next_random() % 26);
            int unequal = next_random() % 256 < i % 2;
            e[1] = unequal ? '!' : '=';
            e[2] = '=';
            e[3] = (char)(97 + next_random() % 26);
            e[4] = 0;
        }
    }
    int64_t sat = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int ok = equations_possible(sets[(r + i) % 20], 500);
            if (ok) sat++;
            check = (check * 31 + (ok ? 2 : 1)) % 1000000007;
        }
    }
    printf("%d rounds over 20 sets of 500 equations: %lld satisfiable, checksum %lld\n", rounds,
           (long long)sat, (long long)check);
    return 0;
}
