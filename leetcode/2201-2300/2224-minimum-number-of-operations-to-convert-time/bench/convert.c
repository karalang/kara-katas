// LeetCode #2224: Minimum Number of Operations to Convert Time -- the
// benchmark's C mirror of convert.kara: each time read from its four
// digits, the gap in minutes cut greedily by 60s, 15s, 5s and 1s.
#include <stdint.h>
#include <stdio.h>

static int64_t minutes_of(const char *time) {
    int64_t d[4];
    int n = 0;
    for (const char *c = time; *c; c++)
        if (*c != ':') d[n++] = *c - '0';
    return (d[0] * 10 + d[1]) * 60 + d[2] * 10 + d[3];
}

static int64_t convert_time(const char *current, const char *correct) {
    static const int64_t steps[4] = {60, 15, 5, 1};
    int64_t gap = minutes_of(correct) - minutes_of(current);
    int64_t operations = 0;
    for (int i = 0; i < 4; i++) {
        operations += gap / steps[i];
        gap %= steps[i];
    }
    return operations;
}

static int64_t seed = 2224;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    // every time of the day as "HH:MM", built once
    static char times[1440][6];
    for (int m = 0; m < 1440; m++) snprintf(times[m], 6, "%02d:%02d", m / 60, m % 60);
    int64_t check = 0;
    for (int i = 0; i < 2000000; i++) {
        int64_t a = next_random() % 1440;
        int64_t b = next_random() % 1440;
        int64_t low = a <= b ? a : b, high = a <= b ? b : a;
        check = (check * 31 + convert_time(times[low], times[high])) % 1000000007;
    }
    printf("2000000 pairs: checksum %lld\n", (long long)check);
    return 0;
}
