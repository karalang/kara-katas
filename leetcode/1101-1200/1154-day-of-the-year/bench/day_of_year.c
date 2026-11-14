// LeetCode #1154 bench -- mirrors day_of_year.kara: the same dates, the
// same passes, the ★ arm's table. Each field is parsed as a decimal
// number that refuses a non-digit, as `i64.parse` does.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const int64_t BEFORE[12] = {0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334};

static bool is_leap(int64_t year) { return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0); }

static int64_t parse(const char *s, int from, int to) {
    int64_t n = 0;
    for (int i = from; i < to; i++) {
        if (s[i] < '0' || s[i] > '9') abort();
        n = n * 10 + (s[i] - '0');
    }
    return n;
}

static int64_t day_of_year(const char *date) {
    int64_t year = parse(date, 0, 4);
    int64_t month = parse(date, 5, 7);
    int64_t day = parse(date, 8, 10);
    int64_t leap_day = month > 2 && is_leap(year) ? 1 : 0;
    return BEFORE[month - 1] + day + leap_day;
}

static int64_t days_in(int64_t year, int64_t month) {
    if (month == 2) return year % 400 == 0 || (year % 4 == 0 && year % 100 != 0) ? 29 : 28;
    return 31 - (month - 1) % 7 % 2;
}

static char dates[43829][11];

int main(void) {
    int passes = 1000;
    int count = 0;
    for (int64_t year = 1900; year < 2020; year++)
        for (int64_t month = 1; month < 13; month++)
            for (int64_t day = 1; day < days_in(year, month) + 1; day++)
                snprintf(dates[count++], 11, "%lld-%02lld-%02lld", (long long)year, (long long)month, (long long)day);
    int64_t total = 0, check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int i = 0; i < count; i++) {
            int64_t n = day_of_year(dates[i]);
            total += n;
            check = (check * 31 + n + p) % 1000000007;
        }
    }
    printf("%d passes over %d dates: total %lld, checksum %lld\n", passes, count, (long long)total, (long long)check);
    return 0;
}
