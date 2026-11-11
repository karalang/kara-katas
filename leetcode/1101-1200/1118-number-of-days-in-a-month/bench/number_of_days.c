// LeetCode #1118: Number of Days in a Month -- the bench in C, the ★ arm's
// `switch` over the same 10^6 months and 40 rounds.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int is_leap(int32_t year) {
    return (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
}

static int32_t number_of_days(int32_t year, int32_t month) {
    switch (month) {
    case 2: return is_leap(year) ? 29 : 28;
    case 4: case 6: case 9: case 11: return 30;
    default: return 31;
    }
}

static int64_t seed = 1118;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int32_t *years = malloc(1000000 * sizeof(int32_t));
    int32_t *months = malloc(1000000 * sizeof(int32_t));
    for (int i = 0; i < 1000000; i++) {
        years[i] = (int32_t)(1583 + next_random() % 517);
        months[i] = (int32_t)(1 + next_random() % 12);
    }
    int64_t total = 0, check = 0;
    int32_t last = 0;
    for (int round = 0; round < 40; round++) {
        for (int64_t i = 0; i < 1000000; i++) {
            int32_t d = number_of_days(years[i] + (last & 1), months[i]);
            total += d;
            if (i % 64 == 0) check = (check * 31 + d) % 1000000007;
            last = d;
        }
    }
    printf("40 rounds over 10^6 months: %lld days, checksum %lld\n", (long long)total, (long long)check);
    free(years);
    free(months);
    return 0;
}
