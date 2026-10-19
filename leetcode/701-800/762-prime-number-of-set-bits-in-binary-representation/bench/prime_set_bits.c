// LeetCode 762 — Prime Number of Set Bits in Binary Representation:
// benchmark, the ★ arm in C.
#include <stdint.h>
#include <stdio.h>

static int64_t count_prime_set_bits(int64_t left, int64_t right) {
    int64_t count = 0;
    for (int64_t n = left; n <= right; n++) {
        int bits = 0;
        for (int64_t rest = n; rest > 0; rest &= rest - 1) bits++;
        switch (bits) {
        case 2: case 3: case 5: case 7: case 11: case 13: case 17: case 19:
            count++;
        }
    }
    return count;
}

static int64_t seed = 762;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int rounds = 10000;
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        int64_t high = next_random();
        int64_t left = 1 + (high * 32768 + next_random()) % 990000;
        int64_t count = count_prime_set_bits(left, left + 10000);
        total += count;
        check = (check * 31 + count) % 1000000007;
    }
    printf("%d ranges of 10001 numbers: %lld counted, checksum %lld\n", rounds, (long long)total, (long long)check);
    return 0;
}
