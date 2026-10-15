// LeetCode #681: Next Closest Time -- step a minute at a time. Bench.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define ROUNDS 300

static void digits_of(int64_t minutes, int64_t out[4]) {
    int64_t h = minutes / 60, m = minutes % 60;
    out[0] = h / 10;
    out[1] = h % 10;
    out[2] = m / 10;
    out[3] = m % 10;
}

// Writes the answer, "HH:MM" and a NUL, into `out`.
static void next_closest_time(const char *time, char *out) {
    int64_t h = (time[0] - '0') * 10 + (time[1] - '0');
    int64_t m = (time[3] - '0') * 10 + (time[4] - '0');
    bool allowed[10] = {false};
    int64_t d[4];
    digits_of(h * 60 + m, d);
    for (int k = 0; k < 4; k++) allowed[d[k]] = true;
    int64_t now = h * 60 + m;
    for (;;) {
        now = (now + 1) % 1440;
        digits_of(now, d);
        bool ok = true;
        for (int k = 0; k < 4; k++)
            if (!allowed[d[k]]) ok = false;
        if (ok) {
            snprintf(out, 6, "%lld%lld:%lld%lld", (long long)(now / 600),
                     (long long)(now / 60 % 10), (long long)(now % 60 / 10),
                     (long long)(now % 10));
            return;
        }
    }
}

int main(void) {
    char times[1440][6];
    for (int t = 0; t < 1440; t++)
        snprintf(times[t], 6, "%02d:%02d", t / 60, t % 60);
    int64_t sum = 0, wrapped = 0;
    char answer[6];
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int64_t k = 0; k < 1440; k++) {
            int64_t at = (k * 7 + r) % 1440;
            next_closest_time(times[at], answer);
            int64_t then = ((answer[0] - '0') * 10 + (answer[1] - '0')) * 60 +
                           (answer[3] - '0') * 10 + (answer[4] - '0');
            if (then <= at) wrapped++;
            sum = (sum * 1441 + then + 1) % 1000000007;
        }
    }
    printf("%d times: %lld answers on the next day, checksum %lld\n", 1440 * ROUNDS,
           (long long)wrapped, (long long)sum);
    return 0;
}
