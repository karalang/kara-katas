// LeetCode #1507: Reformat Date -- the bench: 100000 dates built once,
// then each reformatted ten times by the ★ arm: the three words found at
// the spaces, the day's leading digits, the month's place in the table.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *MONTHS[12] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};

static void reformat_date(const char *date, char *out) {
    const char *first = strchr(date, ' ');
    const char *second = strchr(first + 1, ' ');
    long day = 0;
    for (const char *p = date; p < first && *p >= '0' && *p <= '9'; p++) {
        day = day * 10 + (*p - '0');
    }
    int month = 0;
    for (int m = 0; m < 12; m++) {
        if ((size_t)(second - first - 1) == strlen(MONTHS[m]) && strncmp(first + 1, MONTHS[m], 3) == 0) {
            month = m + 1;
            break;
        }
    }
    sprintf(out, "%s-%02d-%02ld", second + 1, month, day);
}

static const char *suffix(long day) {
    if (day == 1 || day == 21 || day == 31) return "st";
    if (day == 2 || day == 22) return "nd";
    if (day == 3 || day == 23) return "rd";
    return "th";
}

static long days_in(long month, long year) {
    static const long days[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int leap = year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
    return month == 1 && leap ? 29 : days[month];
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    long seed = 1507;
    enum { N = 100000 };
    char *dates[N];
    for (int i = 0; i < N; i++) {
        long year = 1900 + next_random(&seed) % 201;
        long month = next_random(&seed) % 12;
        long day = 1 + next_random(&seed) % days_in(month, year);
        char buf[32];
        int len = snprintf(buf, sizeof buf, "%ld%s %s %ld", day, suffix(day), MONTHS[month], year);
        dates[i] = malloc(len + 1);
        memcpy(dates[i], buf, len + 1);
    }
    long check = 0;
    char out[32];
    for (int r = 0; r < 10; r++) {
        for (int i = 0; i < N; i++) {
            reformat_date(dates[i], out);
            for (const unsigned char *p = (const unsigned char *)out; *p; p++) {
                check = (check * 31 + *p + 1) % 1000000007;
            }
        }
    }
    printf("1000000 dates reformatted, 100000 built once: checksum %ld\n", check);
    for (int i = 0; i < N; i++) free(dates[i]);
    return 0;
}
