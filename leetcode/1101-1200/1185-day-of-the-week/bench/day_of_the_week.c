// LeetCode #1185: Day of the Week -- the ★ arm in C: the days from
// 1 January 1971, a Friday, to the date, and that many days on from Friday;
// the name copied into a fresh string, as the other languages build one.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int is_leap(int64_t year) { return (year % 4 == 0 && year % 100 != 0) || year % 400 == 0; }

static const char *NAMES[7] = {"Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"};
static const int64_t MONTH_DAYS[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

static char *day_of_the_week(int64_t day, int64_t month, int64_t year) {
    int64_t days = 0;
    for (int64_t y = 1971; y < year; y++) days += is_leap(y) ? 366 : 365;
    for (int64_t m = 1; m < month; m++) days += MONTH_DAYS[m - 1];
    if (month > 2 && is_leap(year)) days += 1;
    days += day - 1;
    return strdup(NAMES[days % 7]);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1185;
    static int64_t dates[10000][3];
    for (int k = 0; k < 10000; k++) {
        int64_t year = 1971 + next_random(&seed) % 130;
        int64_t month = 1 + next_random(&seed) % 12;
        int64_t length = month == 2 && is_leap(year) ? 29 : MONTH_DAYS[month - 1];
        int64_t day = 1 + next_random(&seed) % length;
        dates[k][0] = day; dates[k][1] = month; dates[k][2] = year;
    }
    int rounds = 100;
    int64_t check = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < 10000; k++) {
            char *name = day_of_the_week(dates[k][0], dates[k][1], dates[k][2]);
            check = (check * 131 + (int64_t)strlen(name) * 7 + (unsigned char)name[0] + r) % 1000000007;
            free(name);
        }
    printf("%d rounds of 10000 dates: checksum %lld\n", rounds, (long long)check);
    return 0;
}
