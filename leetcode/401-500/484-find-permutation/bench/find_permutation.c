// Benchmark for #484: C mirror of the ★ arm (1 to n, each run of Ds
// reversed); see find_permutation.kara. The letters are copied out first,
// as the Kāra arm collects its chars into a Vec.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static long long *find_permutation(const char *s, long long *out_n) {
    long long len = (long long)strlen(s);
    char *letters = malloc(len + 1);
    memcpy(letters, s, len + 1);
    long long n = len + 1;
    long long *perm = malloc(sizeof(long long) * n);
    for (long long i = 0; i < n; i++) {
        perm[i] = i + 1;
    }
    long long i = 0;
    while (i < len) {
        if (letters[i] == 'D') {
            long long start = i;
            while (i < len && letters[i] == 'D') {
                i++;
            }
            long long low = start, high = i;
            while (low < high) {
                long long t = perm[low];
                perm[low] = perm[high];
                perm[high] = t;
                low++;
                high--;
            }
        } else {
            i++;
        }
    }
    free(letters);
    *out_n = n;
    return perm;
}

int main(void) {
    char *patterns[20];
    long long seed = 484;
    for (long long p = 0; p < 20; p++) {
        patterns[p] = malloc(100001);
        for (long long j = 0; j < 100000; j++) {
            patterns[p][j] = next_random(&seed) % 20 < p ? 'D' : 'I';
        }
        patterns[p][100000] = 0;
    }
    long long total = 0, checksum = 0;
    for (int r = 0; r < 10; r++) {
        for (int p = 0; p < 20; p++) {
            long long n;
            long long *perm = find_permutation(patterns[p], &n);
            total += n;
            checksum = (checksum * 31 + perm[0] + perm[n / 2] * 7 + perm[n - 1] * 13) % 1000000007;
            free(perm);
        }
    }
    printf("200 solves of 100000 letters: %lld numbers, checksum %lld\n", total, checksum);
    return 0;
}
