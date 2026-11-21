// LeetCode #2453: Destroy Sequential Targets -- bench, C mirror of
// targets.kara: an open-addressing hash table counts each residue class,
// and a second pass keeps the least value of a largest class.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAP (1 << 18)

static int64_t keys[CAP];
static int64_t counts[CAP];
static char used[CAP];

static size_t slot(int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    size_t i = (size_t)(h >> 46);
    while (used[i] && keys[i] != key) {
        i = (i + 1) & (CAP - 1);
    }
    return i;
}

static int64_t destroy_targets(const int64_t *nums, int64_t n, int64_t space) {
    memset(used, 0, sizeof used);
    for (int64_t i = 0; i < n; i++) {
        int64_t r = nums[i] % space;
        size_t s = slot(r);
        if (!used[s]) {
            used[s] = 1;
            keys[s] = r;
            counts[s] = 0;
        }
        counts[s] += 1;
    }
    int64_t best = 0, answer = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        int64_t c = counts[slot(x % space)];
        if (c > best || (c == best && x < answer)) {
            best = c;
            answer = x;
        }
    }
    return answer;
}

static int64_t seed = 2453;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    int64_t *arrays[10];
    for (int a = 0; a < 10; a++) {
        arrays[a] = malloc(sizeof(int64_t) * n);
        for (int64_t i = 0; i < n; i++) {
            int64_t hi = next_random();
            arrays[a][i] = 1 + (hi * 32768 + next_random()) % 1000000000;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++) {
        for (int64_t a = 0; a < 10; a++) {
            arrays[a][(p * 7919 + a) % n] = 1 + check % 1000000000;
            int64_t space = 1 + (p * 7919 + a * 104729) % 100000;
            check = (check * 31 + destroy_targets(arrays[a], n, space) + p) % 1000000007;
        }
    }
    printf("50 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) free(arrays[a]);
    return 0;
}
