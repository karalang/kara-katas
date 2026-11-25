// LeetCode #1360 bench -- C: each date as its count of days from
// 1971-01-01, the answer the two counts' distance.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const int64_t LENGTHS[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

static int is_leap(int64_t year) {
    return (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
}

static int64_t digits(const char *s, int from, int to) {
    int64_t v = 0;
    for (int i = from; i < to; i++) v = v * 10 + (s[i] - '0');
    return v;
}

static int64_t days_from_1971(const char *date) {
    int64_t year = digits(date, 0, 4);
    int64_t month = digits(date, 5, 7);
    int64_t day = digits(date, 8, 10);
    int64_t days = day - 1;
    for (int64_t y = 1971; y < year; y++) days += is_leap(y) ? 366 : 365;
    for (int64_t m = 1; m < month; m++) {
        days += LENGTHS[m - 1];
        if (m == 2 && is_leap(year)) days += 1;
    }
    return days;
}

static int32_t days_between_dates(const char *date1, const char *date2) {
    int64_t d = days_from_1971(date1) - days_from_1971(date2);
    return (int32_t)(d < 0 ? -d : d);
}

static int64_t seed = 1360;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void random_date(char *out) {
    int64_t year = 1971 + next_random() % 130;
    int64_t month = 1 + next_random() % 12;
    int64_t last = LENGTHS[month - 1];
    if (month == 2 && is_leap(year)) last += 1;
    int64_t day = 1 + next_random() % last;
    snprintf(out, 11, "%04lld-%02lld-%02lld", (long long)year, (long long)month, (long long)day);
}

int main(void) {
    // 1000 dates written once; then 3 * 10^5 questions, each pair of dates
    // drawn from the checksum so far, every answer folded into it
    static char dates[1000][11];
    for (int i = 0; i < 1000; i++) random_date(dates[i]);
    int64_t check = 0;
    for (int64_t r = 0; r < 300000; r++) {
        int64_t a = check % 1000;
        int64_t b = (check / 1000 + r) % 1000;
        check = (check * 31 + days_between_dates(dates[a], dates[b]) + r) % 1000000007;
    }
    printf("300000 questions: checksum %lld\n", (long long)check);
    return 0;
}
