// LeetCode #2147: Number of Ways to Divide a Long Corridor -- the
// benchmark's C mirror of corridor.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007LL
#define N 100000

static int64_t number_of_ways(const char *corridor, int64_t n) {
    int64_t *seats = malloc(sizeof(int64_t) * (size_t)n);
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        if (corridor[i] == 'S') {
            seats[count++] = i;
        }
    }
    if (count == 0 || count % 2 == 1) {
        free(seats);
        return 0;
    }
    int64_t ways = 1;
    for (int64_t p = 2; p < count; p += 2) {
        ways = ways * (seats[p] - seats[p - 1]) % MOD;
    }
    free(seats);
    return ways;
}

static int64_t seed = 2147;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    char *corridors[4];
    for (int c = 0; c < 4; c++) {
        char *corridor = malloc(N + 1);
        int64_t count = 0;
        for (int i = 0; i < N - 1; i++) {
            if (next_random() % 3 == 0) {
                corridor[i] = 'S';
                count++;
            } else {
                corridor[i] = 'P';
            }
        }
        corridor[N - 1] = count % 2 == 1 ? 'S' : 'P';
        corridor[N] = 0;
        corridors[c] = corridor;
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t round = 0; round < 25; round++) {
        for (int c = 0; c < 4; c++) {
            int64_t i = next_random() % 99999;
            char *place = corridors[c];
            char *next = malloc(N + 1);
            memcpy(next, place, (size_t)i);
            next[i] = place[i + 1];
            next[i + 1] = place[i];
            memcpy(next + i + 2, place + i + 2, (size_t)(N - i - 2) + 1);
            free(place);
            corridors[c] = next;
            int64_t ways = number_of_ways(next, N);
            total = (total + ways) % MOD;
            check = (check * 31 + ways + round) % MOD;
        }
    }
    printf("100 counts: %lld ways in all, checksum %lld\n", (long long)total, (long long)check);
    for (int c = 0; c < 4; c++) {
        free(corridors[c]);
    }
    return 0;
}
