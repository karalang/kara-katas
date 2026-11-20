// LeetCode #1736: Latest Time by Replacing Hidden Digits -- the bench
// (time.kara): each hidden digit the largest its neighbours allow.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* the latest time, "hh:mm", in a fresh allocation */
static char *maximum_time(const char *time) {
    char *t = malloc(6);
    memcpy(t, time, 6);
    if (t[0] == '?') t[0] = (t[1] == '?' || t[1] <= '3') ? '2' : '1';
    if (t[1] == '?') t[1] = t[0] == '2' ? '3' : '9';
    if (t[3] == '?') t[3] = '5';
    if (t[4] == '?') t[4] = '9';
    return t;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    long count = 1000000, rounds = 10, seed = 1736;
    char (*times)[6] = malloc(sizeof(*times) * count);
    for (long i = 0; i < count; i++) {
        long t = next_random(&seed) % 1440;
        char shown[12];
        snprintf(shown, sizeof shown, "%ld%ld:%ld%ld", t / 60 / 10, t / 60 % 10, t % 60 / 10, t % 60 % 10);
        for (int j = 0; j < 5; j++)
            times[i][j] = (shown[j] != ':' && next_random(&seed) % 2 == 0) ? '?' : shown[j];
        times[i][5] = '\0';
    }
    long sum = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (long i = 0; i < count; i++) {
            char *b = maximum_time(times[i]);
            sum += b[1] - 48;
            check = (check * 31 + b[0] * 1000L + b[1] * 100L + b[3] * 10L + b[4] + r) % 1000000007;
            free(b);
        }
    }
    free(times);
    printf("%ld times, %ld rounds: hour digits sum to %ld, checksum %ld\n", count, rounds, sum, check);
    return 0;
}
