// LeetCode #1202 bench, in C: the ★ arm (a union-find over the indices,
// path halving and union by size; each group's letters, sorted, go back to
// its indices in rising order) on one string of 100000 random letters and
// four sets of pairs drawn once, then 10 rounds over the four, each answer
// folded into a checksum. A group is a run of a by-root index list built
// with counts, as Rust's and Kāra's Vec of Vecs hold the same indices in
// the same order.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long seed = 1202;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long find(long *parent, long x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static int cmp_byte(const void *a, const void *b) {
    return (int)*(const unsigned char *)a - (int)*(const unsigned char *)b;
}

static void smallest_string_with_swaps(const unsigned char *s, long n, const long *pairs, long m,
                                       unsigned char *out) {
    long *parent = malloc(n * sizeof(long));
    long *size = malloc(n * sizeof(long));
    for (long i = 0; i < n; i++) {
        parent[i] = i;
        size[i] = 1;
    }
    for (long p = 0; p < m; p++) {
        long a = find(parent, pairs[2 * p]);
        long b = find(parent, pairs[2 * p + 1]);
        if (a != b) {
            if (size[a] < size[b]) {
                long t = a;
                a = b;
                b = t;
            }
            parent[b] = a;
            size[a] += size[b];
        }
    }
    long *root = malloc(n * sizeof(long));
    long *start = calloc(n + 1, sizeof(long));
    for (long i = 0; i < n; i++) {
        root[i] = find(parent, i);
        start[root[i] + 1]++;
    }
    for (long r = 0; r < n; r++) start[r + 1] += start[r];
    long *fill = malloc(n * sizeof(long));
    memcpy(fill, start, n * sizeof(long));
    long *members = malloc(n * sizeof(long));
    for (long i = 0; i < n; i++) members[fill[root[i]]++] = i;
    unsigned char *letters = malloc(n);
    memcpy(out, s, n);
    for (long r = 0; r < n; r++) {
        long len = start[r + 1] - start[r];
        const long *g = members + start[r];
        for (long k = 0; k < len; k++) letters[k] = s[g[k]];
        qsort(letters, len, 1, cmp_byte);
        for (long k = 0; k < len; k++) out[g[k]] = letters[k];
    }
    free(parent);
    free(size);
    free(root);
    free(start);
    free(fill);
    free(members);
    free(letters);
}

static long *random_pairs(long n, long m) {
    long *pairs = malloc(2 * m * sizeof(long));
    for (long p = 0; p < m; p++) {
        long long hi = next_random();
        pairs[2 * p] = (long)((hi * 32768 + next_random()) % n);
        hi = next_random();
        pairs[2 * p + 1] = (long)((hi * 32768 + next_random()) % n);
    }
    return pairs;
}

int main(void) {
    long n = 100000;
    unsigned char *s = malloc(n);
    for (long i = 0; i < n; i++) s[i] = (unsigned char)('a' + next_random() % 26);
    long *sets[4];
    long counts[4] = {25000, 100000, n - 2, n - 1000};
    sets[0] = random_pairs(n, 25000);
    sets[1] = random_pairs(n, 100000);
    sets[2] = malloc(2 * counts[2] * sizeof(long));
    for (long i = 0; i < counts[2]; i++) {
        sets[2][2 * i] = i;
        sets[2][2 * i + 1] = i + 2;
    }
    sets[3] = malloc(2 * counts[3] * sizeof(long));
    for (long i = 0; i < counts[3]; i++) {
        sets[3][2 * i] = i;
        sets[3][2 * i + 1] = i + 1000;
    }
    unsigned char *t = malloc(n);
    long long check = 0;
    for (int round = 0; round < 10; round++) {
        for (int k = 0; k < 4; k++) {
            smallest_string_with_swaps(s, n, sets[k], counts[k], t);
            for (long i = 0; i < n; i++) check = (check * 131 + t[i]) % 1000000007;
        }
    }
    printf("10 rounds over 4 sets of pairs on 100000 letters: checksum %lld\n", check);
    return 0;
}
