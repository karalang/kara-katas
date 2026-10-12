// Benchmark for #399: mirror of evaluate_division.kara (union-find with weights).
// C has no map type, so the index of variable names is an open-addressing
// hash table of heap-allocated strings (FNV-1a), rebuilt for each system the
// way the other mirrors build a fresh map; names are formatted with snprintf
// as the others format theirs.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 128
#define MAXV 64

typedef struct {
    char *key[SLOTS];
    int val[SLOTS];
} Index;

static uint64_t fnv(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) {
        h ^= (unsigned char)*s;
        h *= 1099511628211ULL;
    }
    return h;
}

static int lookup(Index *ix, const char *name) {
    uint64_t h = fnv(name) % SLOTS;
    while (ix->key[h]) {
        if (strcmp(ix->key[h], name) == 0) return ix->val[h];
        h = (h + 1) % SLOTS;
    }
    return -1;
}

static void put(Index *ix, const char *name, int v) {
    uint64_t h = fnv(name) % SLOTS;
    while (ix->key[h]) h = (h + 1) % SLOTS;
    ix->key[h] = strdup(name);
    ix->val[h] = v;
}

static int find(int *parent, double *weight, int i) {
    int p = parent[i];
    if (p == i) return i;
    int root = find(parent, weight, p);
    weight[i] = weight[i] * weight[p];
    parent[i] = root;
    return root;
}

typedef struct {
    char *a, *b;
} Pair;

static void calc_equation(Pair *equations, double *values, int ne, Pair *queries, int nq, double *answers) {
    Index ix;
    memset(&ix, 0, sizeof ix);
    int parent[MAXV];
    double weight[MAXV];
    int n = 0;
    for (int k = 0; k < ne; k++) {
        int a = lookup(&ix, equations[k].a);
        if (a < 0) { a = n++; put(&ix, equations[k].a, a); parent[a] = a; weight[a] = 1.0; }
        int b = lookup(&ix, equations[k].b);
        if (b < 0) { b = n++; put(&ix, equations[k].b, b); parent[b] = b; weight[b] = 1.0; }
        int ra = find(parent, weight, a);
        int rb = find(parent, weight, b);
        if (ra != rb) {
            weight[ra] = values[k] * weight[b] / weight[a];
            parent[ra] = rb;
        }
    }
    for (int q = 0; q < nq; q++) {
        double answer = -1.0;
        int i = lookup(&ix, queries[q].a);
        if (i >= 0) {
            int j = lookup(&ix, queries[q].b);
            if (j >= 0 && find(parent, weight, i) == find(parent, weight, j)) {
                answer = weight[i] / weight[j];
            }
        }
        answers[q] = answer;
    }
    for (int h = 0; h < SLOTS; h++) free(ix.key[h]);
}

static int64_t seed = 3991;

static int64_t step(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static double pow2(int64_t k) {
    double x = 1.0;
    for (int64_t i = 0; i < (k < 0 ? -k : k); i++) x = x * 2.0;
    return k < 0 ? 1.0 / x : x;
}

static int64_t exponent(double x) {
    double v = x;
    int64_t k = 0;
    while (v >= 2.0) { v = v / 2.0; k++; }
    while (v < 1.0) { v = v * 2.0; k--; }
    return k;
}

static char *name(int64_t i) {
    char buf[24];
    snprintf(buf, sizeof buf, "v%lld", (long long)i);
    return strdup(buf);
}

int main(int argc, char **argv) {
    int64_t systems = argc > 1 ? atoll(argv[1]) : 100000;
    int64_t answered = 0, checksum = 0;
    for (int64_t s = 0; s < systems; s++) {
        int64_t m = 2 + step() % 39;
        int64_t hidden[MAXV];
        for (int64_t i = 0; i < m; i++) hidden[i] = step() % 9 - 4;
        Pair equations[20], queries[20];
        double values[20], answers[20];
        for (int e = 0; e < 20; e++) {
            int64_t a = step() % m;
            int64_t b = step() % m;
            equations[e].a = name(a);
            equations[e].b = name(b);
            values[e] = pow2(hidden[a] - hidden[b]);
        }
        for (int q = 0; q < 20; q++) {
            int64_t a = step() % (m + 2);
            int64_t b = step() % (m + 2);
            queries[q].a = name(a);
            queries[q].b = name(b);
        }
        calc_equation(equations, values, 20, queries, 20, answers);
        for (int q = 0; q < 20; q++) {
            double x = answers[q];
            if (x < 0.0) {
                checksum = (checksum * 31 + 1) % 1000000007;
            } else {
                answered++;
                checksum = (checksum * 31 + exponent(x) + 50) % 1000000007;
            }
        }
        for (int e = 0; e < 20; e++) {
            free(equations[e].a); free(equations[e].b);
            free(queries[e].a); free(queries[e].b);
        }
    }
    printf("%lld systems: %lld answered, checksum %lld\n", (long long)systems, (long long)answered, (long long)checksum);
    return 0;
}
