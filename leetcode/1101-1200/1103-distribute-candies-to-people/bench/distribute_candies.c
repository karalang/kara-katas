// LeetCode #1103: Distribute Candies to People -- the bench in C: the ★
// arm (gifts of 1, 2, 3, ... in turn, the last whatever is left) over 64
// problems, each round moving every problem's candies.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t *distribute_candies(int64_t candies, int64_t num_people) {
    int64_t *people = calloc((size_t)num_people, sizeof(int64_t));
    int64_t left = candies, gift = 1;
    while (left > 0) {
        int64_t given = gift < left ? gift : left;
        people[(gift - 1) % num_people] += given;
        left -= given;
        gift += 1;
    }
    return people;
}

static int64_t seed = 1103;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t cand[64], num[64];
    for (int j = 0; j < 64; j++) {
        int64_t hi = next_random();
        cand[j] = (hi * 32768 + next_random()) % 1000000000 + 1;
        num[j] = next_random() % 1000 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 200; round++) {
        for (int64_t j = 0; j < 64; j++) {
            int64_t candies = (cand[j] + round * 7919 + j * 104729) % 1000000000 + 1;
            cand[j] = candies;
            int64_t n = num[j];
            int64_t *people = distribute_candies(candies, n);
            total += people[0] + people[n - 1];
            for (int64_t i = 0; i < n; i++) check = (check * 31 + people[i] + 1) % 1000000007;
            free(people);
        }
    }
    printf("200 rounds over 64 problems of up to 10^9 candies: first and last people hold %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
