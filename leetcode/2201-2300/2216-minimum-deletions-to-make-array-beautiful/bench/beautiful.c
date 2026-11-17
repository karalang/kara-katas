// LeetCode #2216: Minimum Deletions to Make Array Beautiful -- bench
// mirror of beautiful.kara: a number that would start a pair is deleted
// when the number after it is the same; an odd length left costs one more.
#include <stdio.h>

static long min_deletion(const long *nums, long n) {
    long deleted = 0;
    for (long i = 0; i < n - 1; i++)
        if ((i - deleted) % 2 == 0 && nums[i] == nums[i + 1]) deleted++;
    if ((n - deleted) % 2 == 1) deleted++;
    return deleted;
}

static long seed = 2216;
static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// a draw of 30 bits, since one draw stops at 32767
static long wide_random(void) {
    long high = next_random();
    return high * 32768 + next_random();
}

#define A 60
#define N 100000
static long arrays[A][N];

int main(void) {
    long tops[3] = {1, 3, 100000};
    for (int a = 0; a < A; a++) {
        // 10^5 numbers up to 1, 3 and 10^5 in turn
        for (long i = 0; i < N; i++) arrays[a][i] = wide_random() % (tops[a % 3] + 1);
    }
    long check = 0;
    for (int a = 0; a < A; a++)
        for (long r = 0; r < 20; r++) {
            // punch: one number takes its neighbour's value before each answer
            arrays[a][r * 4999 + 1] = arrays[a][r * 4999];
            check = (check * 31 + min_deletion(arrays[a], N)) % 1000000007;
        }
    printf("60 arrays of 10^5, 20 punches: checksum %ld\n", check);
    return 0;
}
