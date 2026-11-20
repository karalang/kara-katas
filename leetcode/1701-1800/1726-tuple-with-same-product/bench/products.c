// LeetCode #1726: Tuple with Same Product -- the bench (products.kara):
// every pair's product counted in a hash map, each new pair meeting the
// earlier pairs of its product, 8 tuples each.
//
// C has no map: a table of 2^20 slots probed linearly, the product hashed
// by one multiply, and cleared before each answer. That is less work than
// Kāra's SipHash `Map`, Rust's SipHash `HashMap` or Go's `map` do.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 20
#define ROUNDS 3
#define N 1000
#define TOP 10000
#define BITS 20
#define SLOTS (1 << BITS)

static int32_t keys[SLOTS];
static int32_t counts[SLOTS];

static int32_t tuple_same_product(const int32_t *nums, int n) {
    memset(keys, 0, sizeof keys);
    int32_t tuples = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int32_t p = nums[i] * nums[j];
            uint32_t h = (uint32_t)(((uint64_t)(uint32_t)p * 0x9E3779B97F4A7C15ull) >> (64 - BITS));
            while (keys[h] != 0 && keys[h] != p) {
                h = (h + 1) & (SLOTS - 1);
            }
            if (keys[h] == 0) {
                keys[h] = p;
                counts[h] = 0;
            }
            tuples += 8 * counts[h];
            counts[h]++;
        }
    }
    return tuples;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    static int32_t problems[COUNT][N];
    static int32_t pool[TOP];
    int64_t seed = 1726;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < TOP; i++) {
            pool[i] = i + 1;
        }
        for (int i = 0; i < N; i++) {
            int j = i + (int)(next_random(&seed) % (TOP - i));
            int32_t t = pool[i];
            pool[i] = pool[j];
            pool[j] = t;
        }
        memcpy(problems[c], pool, sizeof(int32_t) * N);
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = tuple_same_product(problems[c], N);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of %d values up to %d, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, TOP, ROUNDS,
           (long long)sum, (long long)check);
    return 0;
}
