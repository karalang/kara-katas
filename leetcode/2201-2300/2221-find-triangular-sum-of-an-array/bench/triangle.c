// LeetCode #2221: Find Triangular Sum of an Array -- bench mirror of
// triangle.kara: the rounds done in place, each writing
// (nums[i] + nums[i + 1]) % 10 over nums[i].
#include <stdio.h>
#include <string.h>

#define A 8
#define N 1000

static long triangular_sum(const long *nums, long n) {
    long row[N];
    memcpy(row, nums, n * sizeof(long));
    for (long live = n - 1; live >= 1; live--)
        for (long i = 0; i < live; i++) row[i] = (row[i] + row[i + 1]) % 10;
    return row[0];
}

static long seed = 2221;
static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static long arrays[A][N];

int main(void) {
    // 1000 digits, the constraints' largest
    for (int a = 0; a < A; a++)
        for (long i = 0; i < N; i++) arrays[a][i] = next_random() % 10;
    long check = 0;
    for (int a = 0; a < A; a++)
        for (long r = 0; r < 8; r++) {
            // punch: one digit is drawn again before each answer
            arrays[a][r * 113] = next_random() % 10;
            check = (check * 31 + triangular_sum(arrays[a], N)) % 1000000007;
        }
    printf("8 arrays of 1000 digits, 8 punches: checksum %ld\n", check);
    return 0;
}
