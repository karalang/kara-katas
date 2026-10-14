// Benchmark for #544: C mirror of the ★ arm (rounds, in place); see
// find_contest_match.kara. Each pair is a fresh malloc'd string and the
// two halves it joins are freed, as the Kāra strings are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *find_contest_match(int64_t n, int64_t *len_out) {
    char **teams = malloc(n * sizeof(char *));
    int64_t *lens = malloc(n * sizeof(int64_t));
    for (int64_t t = 1; t <= n; t++) {
        char buf[24];
        int k = snprintf(buf, sizeof buf, "%lld", (long long)t);
        teams[t - 1] = malloc(k + 1);
        memcpy(teams[t - 1], buf, k + 1);
        lens[t - 1] = k;
    }
    for (int64_t m = n; m > 1; m /= 2) {
        for (int64_t i = 0; i < m / 2; i++) {
            int64_t a = lens[i], b = lens[m - 1 - i];
            char *s = malloc(a + b + 4);
            s[0] = '(';
            memcpy(s + 1, teams[i], a);
            s[a + 1] = ',';
            memcpy(s + a + 2, teams[m - 1 - i], b);
            s[a + b + 2] = ')';
            s[a + b + 3] = 0;
            free(teams[i]);
            free(teams[m - 1 - i]);
            teams[i] = s;
            lens[i] = a + b + 3;
        }
    }
    char *out = teams[0];
    *len_out = lens[0];
    free(teams);
    free(lens);
    return out;
}

int main(void) {
    // 200 rounds over every size the problem allows, 2 to 4,096 teams;
    // the length of each answer is summed, and one byte of it, picked
    // by the round and the size, goes into the checksum.
    int64_t total = 0, checksum = 0;
    for (int64_t r = 0; r < 200; r++) {
        for (int64_t n = 2; n <= 4096; n *= 2) {
            int64_t len;
            char *s = find_contest_match(n, &len);
            int64_t b = (unsigned char)s[(r * 7919 + n * 13) % len];
            total += len;
            checksum = (checksum * 31 + b) % 1000000007;
            free(s);
        }
    }
    printf("200 rounds of 2 to 4096 teams: %lld bytes, checksum %lld\n", (long long)total,
           (long long)checksum);
    return 0;
}
