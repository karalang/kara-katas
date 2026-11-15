// benchmark's C mirror of count.kara (LeetCode #2198, the ★ arm): every
// ordered triple of the values held.
#include <stdio.h>

static long long single_divisor_triplet(const long long *nums, int n) {
    long long count[101] = {0};
    for (int i = 0; i < n; i++) count[nums[i]]++;
    long long total = 0;
    for (long long a = 1; a < 101; a++) {
        if (count[a] == 0) continue;
        for (long long b = 1; b < 101; b++) {
            if (count[b] == 0) continue;
            for (long long c = 1; c < 101; c++) {
                if (count[c] == 0) continue;
                long long sum = a + b + c;
                int by_a = sum % a == 0, by_b = sum % b == 0, by_c = sum % c == 0;
                if ((by_a && !by_b && !by_c) || (by_b && !by_a && !by_c) || (by_c && !by_a && !by_b)) {
                    long long second = b == a ? count[b] - 1 : count[b];
                    long long third = count[c] - (c == a ? 1 : 0) - (c == b ? 1 : 0);
                    total += count[a] * second * third;
                }
            }
        }
    }
    return total;
}

static long long seed = 2198;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define N 100000

int main(void) {
    static long long arrays[20][N];
    for (int a = 0; a < 20; a++) {
        long long top = 81 + a;
        for (int i = 0; i < N; i++) arrays[a][i] = next_random() % top + 1;
    }
    long long check = 0;
    for (int pass = 0; pass < 10; pass++)
        for (int a = 0; a < 20; a++)
            check = (check * 31 + single_divisor_triplet(arrays[a], N) % 1000000007) % 1000000007;
    printf("10 passes over 20 arrays: checksum %lld\n", check);
    return 0;
}
