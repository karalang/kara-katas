// Benchmark for #639: mirror of decode_ways_ii.kara (the ★ arm: the count
// of decodings of every prefix, two at a time) on the same workload.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define M 1000000007
#define LEN 100000
#define ROUNDS 600

static int64_t alone(uint8_t c) {
    if (c == '*') {
        return 9;
    } else if (c == '0') {
        return 0;
    }
    return 1;
}

static int64_t together(uint8_t a, uint8_t b) {
    if (a == '*') {
        if (b == '*') {
            return 15;
        }
        return b <= '6' ? 2 : 1;
    } else if (a == '1') {
        return b == '*' ? 9 : 1;
    } else if (a == '2') {
        if (b == '*') {
            return 6;
        }
        return b <= '6' ? 1 : 0;
    }
    return 0;
}

static int64_t num_decodings(const uint8_t *s, int64_t n) {
    int64_t before = 1;
    int64_t last = alone(s[0]);
    for (int64_t i = 1; i < n; i++) {
        int64_t next = (last * alone(s[i]) + before * together(s[i - 1], s[i])) % M;
        before = last;
        last = next;
    }
    return last;
}

static int64_t seed = 639;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static uint8_t texts[20][LEN];

int main(void) {
    for (int t = 0; t < 20; t++) {
        uint8_t prev = '1';
        for (int i = 0; i < LEN; i++) {
            uint8_t c = '*';
            if (next_random() % 10 >= 3) {
                c = (uint8_t)('1' + next_random() % 9);
                if (next_random() % 100 == 0 && (prev == '1' || prev == '2' || prev == '*')) {
                    c = '0';
                }
            }
            texts[t][i] = c;
            prev = c;
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < ROUNDS; round++) {
        int64_t count = num_decodings(texts[round % 20], LEN);
        total = (total + count) % M;
        checksum = (checksum * 31 + count) % M;
    }
    printf("20 strings of %d characters, %d rounds: total %lld, checksum %lld\n", LEN, ROUNDS, (long long)total, (long long)checksum);
    return 0;
}
