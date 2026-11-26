// LeetCode #1377 bench -- C: the ★ arm: the chance of the frog being on
// each vertex, moved one second at a time, a vertex with unvisited
// neighbours handing its chance to them in equal shares. C has no
// growable list, so the neighbours are counted first and laid out one
// vertex after another.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static double frog_position(int n, const int (*edges)[2], int m, int t, int target) {
    int *start = calloc((size_t)n + 2, sizeof(int));
    int *adjacent = malloc(sizeof(int) * 2 * (size_t)(m > 0 ? m : 1));
    int *fill = malloc(sizeof(int) * ((size_t)n + 1));
    for (int i = 0; i < m; i++) {
        start[edges[i][0] + 1]++;
        start[edges[i][1] + 1]++;
    }
    for (int v = 0; v <= n; v++) {
        start[v + 1] += start[v];
    }
    for (int v = 0; v <= n; v++) {
        fill[v] = start[v];
    }
    for (int i = 0; i < m; i++) {
        adjacent[fill[edges[i][0]]++] = edges[i][1];
        adjacent[fill[edges[i][1]]++] = edges[i][0];
    }
    char *seen = calloc((size_t)n + 1, 1);
    double *chance = calloc((size_t)n + 1, sizeof(double));
    int *level = malloc(sizeof(int) * ((size_t)n + 1));
    int *next = malloc(sizeof(int) * ((size_t)n + 1));
    int *ahead = malloc(sizeof(int) * ((size_t)n + 1));
    int len = 0;
    seen[1] = 1;
    chance[1] = 1.0;
    level[len++] = 1;
    for (int s = 0; s < t; s++) {
        int nlen = 0;
        for (int k = 0; k < len; k++) {
            int u = level[k];
            int a = 0;
            for (int j = start[u]; j < start[u + 1]; j++) {
                if (!seen[adjacent[j]]) {
                    ahead[a++] = adjacent[j];
                }
            }
            if (a == 0) {
                continue;
            }
            double share = chance[u] / a;
            for (int j = 0; j < a; j++) {
                seen[ahead[j]] = 1;
                chance[ahead[j]] = share;
                next[nlen++] = ahead[j];
            }
            chance[u] = 0.0;
        }
        int *tmp = level;
        level = next;
        next = tmp;
        len = nlen;
    }
    double p = chance[target];
    free(start);
    free(adjacent);
    free(fill);
    free(seen);
    free(chance);
    free(level);
    free(next);
    free(ahead);
    return p;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 50 trees of 100 vertices built once; then 100000 rounds, each asking
    // one tree, a time and a target drawn from the checksum so far for the
    // frog's chance, counted in units of 2^-20 (see the Kāra bench)
    const int64_t n = 100;
    int64_t seed = 1377;
    static int trees[50][99][2];
    int64_t order[100];
    for (int c = 0; c < 50; c++) {
        for (int64_t i = 0; i < n; i++) {
            order[i] = i + 1;
        }
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random(&seed) % (i + 1);
            int64_t tmp = order[i];
            order[i] = order[j];
            order[j] = tmp;
        }
        for (int64_t k = 1; k < n; k++) {
            int64_t back;
            if (c % 2 == 0) {
                back = next_random(&seed) % k;
            } else {
                back = k - 1 - next_random(&seed) % (k < 3 ? k : 3);
            }
            trees[c][k - 1][0] = (int)order[k];
            trees[c][k - 1][1] = (int)order[back];
        }
    }
    int64_t check = 0;
    for (int64_t r = 0; r < 100000; r++) {
        int64_t c = check % 50;
        int64_t t = 1 + (check / 50) % 50;
        int64_t target = 1 + (check / 2500 + r) % n;
        double p = frog_position((int)n, (const int (*)[2])trees[c], (int)n - 1, (int)t, (int)target);
        // p is never negative, so the cast's truncation is the floor
        check = (check * 31 + (int64_t)(p * 1048576.0 + 0.5) + r) % 1000000007;
    }
    printf("100000 rounds over 50 trees of 100 vertices: checksum %lld\n", (long long)check);
    return 0;
}
