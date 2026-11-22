// LeetCode #2895: Minimum Processing Time -- the bench, as
// processing.kara: 20 cases of 25000 processors and 10^5 tasks, each
// answered 20 times by the sorting arm, each sorting fresh copies, by
// qsort.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_value(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

static int64_t min_processing_time(const int64_t *processor_time, int64_t n, const int64_t *tasks) {
    int64_t *free_at = malloc(n * sizeof *free_at);
    int64_t *longest = malloc(4 * n * sizeof *longest);
    memcpy(free_at, processor_time, n * sizeof *free_at);
    memcpy(longest, tasks, 4 * n * sizeof *longest);
    qsort(free_at, n, sizeof *free_at, by_value);
    qsort(longest, 4 * n, sizeof *longest, by_value);
    int64_t finish = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t t = free_at[i] + longest[4 * n - 1 - 4 * i];
        if (t > finish) finish = t;
    }
    free(free_at);
    free(longest);
    return finish;
}

static int64_t seed = 2895;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 20, rounds = 20, n = 25000;
    int64_t *processors = malloc(count * n * sizeof *processors);
    int64_t *tasks = malloc(count * 4 * n * sizeof *tasks);
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < n; i++) processors[c * n + i] = wide() % 1000000000;
        for (int64_t i = 0; i < 4 * n; i++) tasks[c * 4 * n + i] = wide() % 1000000000 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t time = min_processing_time(processors + c * n, n, tasks + c * 4 * n);
            total += time;
            check = (check * 31 + time + r) % 1000000007;
        }
    }
    printf("%lld cases of %lld, %lld rounds: times total %lld, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)total, (long long)check);
    free(processors);
    free(tasks);
    return 0;
}
