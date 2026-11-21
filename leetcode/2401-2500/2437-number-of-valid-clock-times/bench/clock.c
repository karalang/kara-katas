// LeetCode #2437: Number of Valid Clock Times -- the bench, the ★ arm:
// the hours that fit the first two characters times the minutes that
// fit the last two.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int fits(const char *pattern, int64_t value) {
    char tens = '0' + value / 10, units = '0' + value % 10;
    return (pattern[0] == '?' || pattern[0] == tens) && (pattern[1] == '?' || pattern[1] == units);
}

static int64_t count_time(const char *time) {
    int64_t hours = 0, minutes = 0;
    for (int64_t h = 0; h < 24; h++)
        if (fits(time, h)) hours++;
    for (int64_t m = 0; m < 60; m++)
        if (fits(time + 3, m)) minutes++;
    return hours * minutes;
}

int main(void) {
    const int64_t n = 1440 * 16;
    char **times = malloc(n * sizeof(char *));
    int64_t k = 0;
    for (int64_t at = 0; at < 1440; at++)
        for (int64_t mask = 0; mask < 16; mask++) {
            char shown[6];
            snprintf(shown, sizeof shown, "%02lld:%02lld", (long long)(at / 60), (long long)(at % 60));
            char *out = malloc(6);
            int digit = 0;
            for (int i = 0; i < 5; i++) {
                if (shown[i] == ':') out[i] = ':';
                else {
                    out[i] = ((mask >> digit) & 1) ? '?' : shown[i];
                    digit++;
                }
            }
            out[5] = 0;
            times[k++] = out;
        }
    int64_t check = 0;
    for (int64_t p = 0; p < 120; p++)
        for (int64_t i = 0; i < n; i++)
            check = (check * 31 + count_time(times[(i * 7 + p) % n]) + p) % 1000000007;
    printf("120 passes over 23040 patterns: checksum %lld\n", (long long)check);
    for (int64_t i = 0; i < n; i++) free(times[i]);
    free(times);
    return 0;
}
