// LeetCode #1319 bench, C mirror of the Kāra bench: the ★ arm (union-find
// with halved paths and the smaller group hung under the larger) on 4
// networks of 10^5 computers built once; then 25 passes, each moving one
// cable of every network to a pair chosen by the checksum so far,
// answering it and folding the answer plus the pass into the checksum.
// Each call takes fresh parent and size arrays, two `malloc`s, as the Kāra
// arm takes two fresh `Vec`s.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *u, *v;
    int64_t m;
} Net;

static int64_t find(int64_t *parent, int64_t x) {
    int64_t at = x;
    while (parent[at] != at) {
        parent[at] = parent[parent[at]];
        at = parent[at];
    }
    return at;
}

static int64_t make_connected(int64_t n, const Net *net) {
    if (net->m < n - 1) return -1;
    int64_t *parent = malloc((size_t)n * sizeof(int64_t));
    int64_t *size = malloc((size_t)n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        parent[i] = i;
        size[i] = 1;
    }
    int64_t groups = n;
    for (int64_t k = 0; k < net->m; k++) {
        int64_t a = find(parent, net->u[k]);
        int64_t b = find(parent, net->v[k]);
        if (a != b) {
            int64_t big = size[a] >= size[b] ? a : b;
            int64_t small = size[a] >= size[b] ? b : a;
            parent[small] = big;
            size[big] += size[small];
            groups--;
        }
    }
    free(parent);
    free(size);
    return groups - 1;
}

static int64_t seed = 1319;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(int64_t k) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % k;
}

int main(void) {
    const int64_t n = 100000;
    Net nets[4];
    for (int kind = 0; kind < 4; kind++) {
        Net *net = &nets[kind];
        net->u = malloc(100000 * sizeof(int64_t));
        net->v = malloc(100000 * sizeof(int64_t));
        net->m = 0;
        if (kind == 1) {
            for (int64_t i = 1; i < n; i++) {
                net->u[net->m] = i - 1;
                net->v[net->m] = i;
                net->m++;
            }
            for (int64_t k = net->m - 1; k >= 1; k--) {
                int64_t j = wide(k + 1);
                int64_t tu = net->u[k], tv = net->v[k];
                net->u[k] = net->u[j];
                net->v[k] = net->v[j];
                net->u[j] = tu;
                net->v[j] = tv;
            }
        } else if (kind == 2) {
            for (int64_t g = 0; g < n / 10; g++)
                for (int64_t a = 0; a < 10; a++) {
                    net->u[net->m] = 10 * g + a;
                    net->v[net->m] = 10 * g + (a + 1) % 10;
                    net->m++;
                }
        } else {
            int64_t m = kind == 0 ? n : n - 1;
            while (net->m < m) {
                int64_t a = wide(n);
                int64_t b = wide(n);
                if (a != b) {
                    net->u[net->m] = a;
                    net->v[net->m] = b;
                    net->m++;
                }
            }
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 25; pass++) {
        for (int t = 0; t < 4; t++) {
            Net *net = &nets[t];
            int64_t a = check % n;
            int64_t b = (a + 1 + (check / 7) % (n - 1)) % n;
            int64_t k = check % net->m;
            net->u[k] = a;
            net->v[k] = b;
            int64_t got = make_connected(n, net);
            check = (check * 31 + got + 1 + pass) % 1000000007;
        }
    }
    printf("25 passes over 4 networks of 10^5: checksum %lld\n", (long long)check);
    for (int t = 0; t < 4; t++) {
        free(nets[t].u);
        free(nets[t].v);
    }
    return 0;
}
