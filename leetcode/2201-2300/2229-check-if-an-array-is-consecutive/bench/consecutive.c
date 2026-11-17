// LeetCode #2229: Check if an Array Is Consecutive -- the benchmark's C
// mirror of consecutive.kara: the span against the count, and an
// open-addressing hash set to find a repeat, C having none of its own.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000
#define SLOTS 262144 /* a power of two, over twice N */

static int64_t keys[SLOTS];
static char used[SLOTS];

static uint64_t slot_of(int64_t key) {
    uint64_t x = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    return (x ^ (x >> 29)) & (SLOTS - 1);
}

static int is_consecutive(const int64_t *nums, int64_t n) {
    for (int i = 0; i < SLOTS; i++) used[i] = 0;
    int64_t smallest = nums[0], largest = nums[0];
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        uint64_t s = slot_of(x);
        while (used[s] && keys[s] != x) s = (s + 1) & (SLOTS - 1);
        if (used[s]) return 0;
        used[s] = 1;
        keys[s] = x;
        if (x < smallest) smallest = x;
        if (x > largest) largest = x;
    }
    return largest - smallest + 1 == n;
}

static int64_t seed = 2229;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t *lists[4];
    for (int l = 0; l < 4; l++) {
        int64_t *nums = malloc(sizeof(int64_t) * N);
        for (int64_t i = 0; i < N; i++) nums[i] = i;
        for (int64_t i = N - 1; i >= 1; i--) {
            int64_t j = wide_random() % (i + 1);
            int64_t t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
        if (l >= 2) {
            int64_t from = wide_random() % N;
            int64_t to = wide_random() % N;
            nums[to] = nums[from];
        }
        lists[l] = nums;
    }
    int yes = 0;
    int64_t check = 0;
    for (int r = 0; r < 25; r++) {
        for (int l = 0; l < 4; l++) {
            // punch: two numbers trade places before each answer
            int64_t i = wide_random() % N;
            int64_t j = wide_random() % N;
            int64_t t = lists[l][i];
            lists[l][i] = lists[l][j];
            lists[l][j] = t;
            int answer = is_consecutive(lists[l], N);
            if (answer) yes++;
            check = (check * 31 + lists[l][i] + (answer ? 1 : 2)) % 1000000007;
        }
    }
    printf("100 answers: %d consecutive, checksum %lld\n", yes, (long long)check);
    for (int l = 0; l < 4; l++) free(lists[l]);
    return 0;
}
