// Benchmark for #539: C mirror of the ★ arm (minutes, sorted); see
// find_min_difference.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// The decimal integer written in s[from..to].
static int64_t parse(const char *s, int from, int to) {
    int64_t n = 0;
    for (int i = from; i < to; i++) n = n * 10 + (s[i] - '0');
    return n;
}

static int64_t minutes(const char *t) { return parse(t, 0, 2) * 60 + parse(t, 3, 5); }

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t find_min_difference(char **time_points, int64_t n) {
    int64_t *mins = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) mins[i] = minutes(time_points[i]);
    qsort(mins, n, sizeof(int64_t), cmp);
    int64_t best = mins[0] + 1440 - mins[n - 1];
    for (int64_t i = 1; i < n; i++)
        if (mins[i] - mins[i - 1] < best) best = mins[i] - mins[i - 1];
    free(mins);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char *clock_of(int64_t minute) {
    char *s = malloc(6);
    snprintf(s, 6, "%02lld:%02lld", (long long)(minute / 60), (long long)(minute % 60));
    return s;
}

int main(void) {
    // 300 lists of 20 to 1,440 distinct times, the first places of a
    // shuffle of the whole day, built once. Then the answer for each
    // list is found 100 times.
    int64_t lists = 300;
    int64_t seed = 539;
    int64_t day[1440];
    for (int64_t m = 0; m < 1440; m++) day[m] = m;
    char ***all = malloc(lists * sizeof(char **));
    int64_t *sizes = malloc(lists * sizeof(int64_t));
    int64_t total_times = 0;
    for (int64_t l = 0; l < lists; l++) {
        int64_t size = 20 + next_random(&seed) % 1421;
        all[l] = malloc(size * sizeof(char *));
        for (int64_t i = 0; i < size; i++) {
            int64_t j = i + next_random(&seed) % (1440 - i);
            int64_t x = day[i];
            day[i] = day[j];
            day[j] = x;
            all[l][i] = clock_of(day[i]);
        }
        sizes[l] = size;
        total_times += size;
    }
    int64_t total = 0, checksum = 0;
    for (int r = 0; r < 100; r++) {
        for (int64_t l = 0; l < lists; l++) {
            int64_t answer = find_min_difference(all[l], sizes[l]);
            total += answer;
            checksum = (checksum * 31 + answer) % 1000000007;
        }
    }
    printf("%lld lists, %lld times, 100 times each: total %lld, checksum %lld\n", (long long)lists,
           (long long)total_times, (long long)total, (long long)checksum);
    return 0;
}
