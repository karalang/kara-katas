// LeetCode #1344 bench in C: the ★ arm (the hour hand 30 degrees an hour
// plus half a degree a minute, the minute hand 6 a minute, and the smaller
// of the gap and 360 less it) on the same 3 * 10^7 times.
#include <math.h>
#include <stdint.h>
#include <stdio.h>

static double angle_clock(int hour, int minutes) {
    double hour_hand = (hour % 12) * 30.0 + minutes * 0.5;
    double minute_hand = minutes * 6.0;
    double gap = fabs(hour_hand - minute_hand);
    return fmin(gap, 360.0 - gap);
}

int main(void) {
    int64_t check = 0;
    for (int64_t i = 0; i < 30000000; i++) {
        int64_t since = (i + check) % 720;
        int64_t hour = since / 60;
        if (hour == 0) hour = 12;
        double a = angle_clock((int)hour, (int)(since % 60));
        check = (check * 31 + (int64_t)(2.0 * a)) % 1000000007;
    }
    printf("3 * 10^7 times: checksum %lld\n", (long long)check);
    return 0;
}
