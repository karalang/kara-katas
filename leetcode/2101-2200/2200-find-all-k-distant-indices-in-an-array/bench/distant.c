// benchmark's C mirror of distant.kara (LeetCode #2200, the ★ arm): the
// key's windows, a `next` index.
#include <stdio.h>
#include <stdlib.h>

static int find_k_distant_indices(const long long *nums, int n, long long key, long long k, long long *out) {
    int len = 0;
    long long next = 0;
    for (long long j = 0; j < n; j++) {
        if (nums[j] != key) continue;
        long long from = j - k > next ? j - k : next;
        long long to = j + k < n - 1 ? j + k : n - 1;
        for (long long i = from; i <= to; i++) out[len++] = i;
        next = to + 1;
    }
    return len;
}

static long long seed = 2200;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static long long nums[1000][1000];
    static long long keys[1000], ks[1000];
    long long tops[3] = {50, 200, 1000};
    for (int c = 0; c < 1000; c++) {
        for (int i = 0; i < 1000; i++) nums[c][i] = next_random() % tops[c % 3] + 1;
        keys[c] = nums[c][next_random() % 1000];
        ks[c] = next_random() % 20 + 1;
    }
    long long *out = malloc(sizeof(long long) * 1000);
    long long check = 0;
    for (int pass = 0; pass < 600; pass++) {
        for (int c = 0; c < 1000; c++) {
            int len = find_k_distant_indices(nums[c], 1000, keys[c], ks[c], out);
            check = (check * 31 + len) % 1000000007;
            if (len > 0) check = (check * 31 + out[len / 2]) % 1000000007;
        }
    }
    printf("600 passes over 1000 arrays: checksum %lld\n", check);
    free(out);
    return 0;
}
