// LeetCode #2409: Count Days Spent Together -- the bench, the ★ arm in C:
// each "MM-DD" read from its bytes into a day of the year, the shared stay
// from the later arrival to the earlier departure.

#include <stdint.h>
#include <stdio.h>

static const int64_t BEFORE[12] = {0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334};
static int64_t seed = 2409;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t day_of_year(const char *date) {
    int64_t month = (date[0] - '0') * 10 + date[1] - '0';
    int64_t day = (date[3] - '0') * 10 + date[4] - '0';
    return BEFORE[month - 1] + day;
}

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }
static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t count_days_together(const char *aa, const char *la, const char *ab, const char *lb) {
    int64_t first = max64(day_of_year(aa), day_of_year(ab));
    int64_t last = min64(day_of_year(la), day_of_year(lb));
    return max64(last - first + 1, 0);
}

int main(void) {
    static const int lengths[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    static char names[365][6];
    int n = 0;
    for (int m = 0; m < 12; m++)
        for (int d = 0; d < lengths[m]; d++) snprintf(names[n++], 6, "%02d-%02d", m + 1, d + 1);
    static int stays[100000][4];
    for (int i = 0; i < 100000; i++) {
        int64_t a = next_random() % 365, b = next_random() % 365;
        int64_t c = next_random() % 365, d = next_random() % 365;
        stays[i][0] = (int)min64(a, b);
        stays[i][1] = (int)max64(a, b);
        stays[i][2] = (int)min64(c, d);
        stays[i][3] = (int)max64(c, d);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++)
        for (int i = 0; i < 100000; i++)
            check = (check * 31 + count_days_together(names[stays[i][0]], names[stays[i][1]], names[stays[i][2]], names[stays[i][3]]) + p) % 1000000007;
    printf("100 passes over 10^5 pairs of stays: checksum %lld\n", (long long)check);
    return 0;
}
