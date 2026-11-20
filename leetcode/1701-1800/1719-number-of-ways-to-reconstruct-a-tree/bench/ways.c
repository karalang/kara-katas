// LeetCode #1719: Number Of Ways To Reconstruct A Tree -- the bench
// (ways.kara): the nodes by degree, most first, each hung under the last
// earlier neighbour, which must hold every other neighbour of it.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 501

typedef struct {
    int (*pairs)[2];
    long len;
} problem;

static long degree_of[SIZE];

static int by_degree(const void *a, const void *b) {
    long da = degree_of[*(const int *)a], db = degree_of[*(const int *)b];
    if (da != db) {
        return da > db ? -1 : 1;
    }
    return *(const int *)a - *(const int *)b;
}

static int check_ways(const problem *p) {
    char *linked = calloc(SIZE * SIZE, 1);
    memset(degree_of, 0, sizeof degree_of);
    for (long i = 0; i < p->len; i++) {
        int x = p->pairs[i][0], y = p->pairs[i][1];
        linked[x * SIZE + y] = 1;
        linked[y * SIZE + x] = 1;
        degree_of[x]++;
        degree_of[y]++;
    }
    int nodes[SIZE];
    long n = 0;
    for (int v = 0; v < SIZE; v++) {
        if (degree_of[v] > 0) {
            nodes[n++] = v;
        }
    }
    /* qsort is not stable; ties keep their node order, as a stable sort does */
    qsort(nodes, n, sizeof(int), by_degree);
    int ways = 1;
    if (degree_of[nodes[0]] != n - 1) {
        ways = 0;
    }
    for (long i = 1; i < n && ways > 0; i++) {
        int v = nodes[i];
        int parent = -1;
        for (long j = i - 1; j >= 0; j--) {
            if (linked[v * SIZE + nodes[j]]) {
                parent = nodes[j];
                break;
            }
        }
        if (parent < 0) {
            ways = 0;
            break;
        }
        for (long j = 0; j < n; j++) {
            int u = nodes[j];
            if (u != parent && linked[v * SIZE + u] && !linked[parent * SIZE + u]) {
                ways = 0;
                break;
            }
        }
        if (ways > 0 && degree_of[parent] == degree_of[v]) {
            ways = 2;
        }
    }
    free(linked);
    return ways;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

static problem draw(long *seed) {
    int k = 500;
    int labels[500];
    for (int i = 0; i < 500; i++) {
        labels[i] = i + 1;
    }
    for (int i = 0; i < k; i++) {
        int j = i + (int)(next_random(seed) % (500 - i));
        int t = labels[i];
        labels[i] = labels[j];
        labels[j] = t;
    }
    char *have = calloc((size_t)k * k, 1);
    long parent[500];
    parent[0] = -1;
    for (int i = 1; i < k; i++) {
        if (next_random(seed) % 2 == 0) {
            parent[i] = next_random(seed) % i;
        } else {
            parent[i] = i - 1 - next_random(seed) % (i < 4 ? i : 4);
        }
    }
    for (int i = 1; i < k; i++) {
        long a = parent[i];
        while (a >= 0) {
            have[i * k + a] = 1;
            have[a * k + i] = 1;
            a = parent[a];
        }
    }
    long mode = next_random(seed) % 3;
    long i0 = next_random(seed) % k;
    long j0 = next_random(seed) % k;
    if (i0 != j0 && mode > 0) {
        have[i0 * k + j0] = mode == 2;
        have[j0 * k + i0] = mode == 2;
    }
    problem p;
    p.len = 0;
    for (int i = 0; i < k; i++) {
        for (int j = i + 1; j < k; j++) {
            p.len += have[i * k + j];
        }
    }
    p.pairs = malloc(sizeof(int[2]) * (p.len > 0 ? p.len : 1));
    long at = 0;
    for (int i = 0; i < k; i++) {
        for (int j = i + 1; j < k; j++) {
            if (have[i * k + j]) {
                int a = labels[i], b = labels[j];
                p.pairs[at][0] = a < b ? a : b;
                p.pairs[at][1] = a < b ? b : a;
                at++;
            }
        }
    }
    free(have);
    return p;
}

int main(void) {
    int count = 50;
    long rounds = 50;
    long seed = 1719;
    problem problems[50];
    long pairs = 0;
    for (int c = 0; c < count; c++) {
        problems[c] = draw(&seed);
        pairs += problems[c].len;
    }
    long sum = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (int c = 0; c < count; c++) {
            long answer = check_ways(&problems[c]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of 500 nodes, %ld pairs, %ld rounds: answers sum to %ld, checksum %ld\n", count, pairs, rounds, sum, check);
    for (int c = 0; c < count; c++) {
        free(problems[c].pairs);
    }
    return 0;
}
