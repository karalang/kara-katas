// LeetCode #2179: Count Good Triplets in an Array -- the benchmark's C
// mirror of triplets.kara, over pointers and a length.

#include <stdio.h>
#include <stdlib.h>

static long long good_triplets(const long long *nums1, const long long *nums2, long long n) {
    long long *place = calloc(n, sizeof(long long));
    for (long long i = 0; i < n; i++) place[nums2[i]] = i;
    long long *tree = calloc(n + 1, sizeof(long long));
    long long total = 0;
    for (long long i = 0; i < n; i++) {
        long long p = place[nums1[i]];
        long long smaller = 0;
        long long j = p;
        while (j > 0) {
            smaller += tree[j];
            j -= j & -j;
        }
        long long larger = (n - 1 - p) - (i - smaller);
        total += smaller * larger;
        j = p + 1;
        while (j <= n) {
            tree[j] += 1;
            j += j & -j;
        }
    }
    free(place);
    free(tree);
    return total;
}

static long long seed = 2179;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long *shuffled(long long n) {
    long long *perm = malloc(n * sizeof(long long));
    for (long long i = 0; i < n; i++) perm[i] = i;
    for (long long i = n - 1; i > 0; i--) {
        long long a = next_random();
        long long b = next_random();
        long long j = (a * 32768 + b) % (i + 1);
        long long t = perm[i];
        perm[i] = perm[j];
        perm[j] = t;
    }
    return perm;
}

int main(void) {
    long long n = 100000;
    long long *first = shuffled(n);
    long long *second = shuffled(n);
    long long check = 0;
    for (int r = 0; r < 40; r++) {
        long long a = next_random();
        long long b = next_random();
        long long offset = (a * 32768 + b) % n;
        long long *rotated = malloc(n * sizeof(long long));
        for (long long i = 0; i < n; i++) rotated[i] = second[(i + offset) % n];
        long long found = good_triplets(first, rotated, n);
        check = (check * 31 + found % 1000000007) % 1000000007;
        free(rotated);
    }
    printf("40 solves: checksum %lld\n", check);
    free(first);
    free(second);
    return 0;
}
