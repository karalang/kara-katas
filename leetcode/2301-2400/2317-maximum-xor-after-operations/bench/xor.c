// LeetCode #2317: Maximum XOR After Operations -- the bench, the ★ arm in
// C. The operation can clear any of a number's bits and set none, so the
// most is the OR of all the numbers.

#include <stdint.h>
#include <stdio.h>

enum { ARRAYS = 20, LEN = 100000 };

static int64_t maximum_xor(const int64_t *nums, int64_t n) {
    int64_t all = 0;
    for (int64_t i = 0; i < n; i++)
        all |= nums[i];
    return all;
}

static int64_t seed = 2317;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[ARRAYS][LEN];
    for (int a = 0; a < ARRAYS; a++) {
        int64_t mask = 0;
        for (int k = 0; k < a + 4; k++)
            mask |= (int64_t)1 << (next_random() % 27);
        for (int i = 0; i < LEN; i++) {
            int64_t hi = next_random();
            arrays[a][i] = (hi * 32768 + next_random()) % 100000001 & mask;
        }
    }
    int64_t check = 0;
    for (int p = 0; p < 100; p++)
        for (int a = 0; a < ARRAYS; a++)
            check = (check * 31 + maximum_xor(arrays[(a + p) % ARRAYS], LEN)) % 1000000007;
    printf("100 passes over 20 arrays of 10^5 numbers: checksum %lld\n", (long long)check);
    return 0;
}
