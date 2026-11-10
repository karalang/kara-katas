// LeetCode #2071: Maximum Number of Tasks You Can Assign -- C mirror of
// the ★ arm's benchmark (tasks.kara): 12 problems of 50000 tasks and 50000
// workers, strengths up to 1000000000, 0 to 11000 pills of strength
// 10000000.
// The deque is a plain array the size of the tasks, a head and a tail.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static bool can_do(const int64_t *tasks, const int64_t *workers, int64_t m, int64_t k, int64_t pills,
                   int64_t strength, int64_t *waiting) {
    int64_t left = pills, head = 0, tail = 0, next = 0;
    for (int64_t j = m - k; j < m; j++) {
        int64_t w = workers[j];
        while (next < k && tasks[next] <= w + strength) waiting[tail++] = tasks[next++];
        if (head == tail) return false;
        if (waiting[head] <= w) {
            head++;
        } else {
            if (left == 0) return false;
            left--;
            tail--;
        }
    }
    return true;
}

static int64_t max_task_assign(int64_t *tasks, int64_t n, int64_t *workers, int64_t m, int64_t pills,
                               int64_t strength) {
    qsort(tasks, n, sizeof *tasks, cmp);
    qsort(workers, m, sizeof *workers, cmp);
    int64_t *waiting = malloc(n * sizeof *waiting);
    int64_t lo = 0, hi = n < m ? n : m;
    while (lo < hi) {
        int64_t mid = (lo + hi + 1) / 2;
        if (can_do(tasks, workers, m, mid, pills, strength, waiting))
            lo = mid;
        else
            hi = mid - 1;
    }
    free(waiting);
    return lo;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void strengths(int64_t *out, int64_t n, int64_t low, int64_t high, int64_t *seed) {
    for (int64_t i = 0; i < n; i++) {
        int64_t a = next_random(seed);
        int64_t b = next_random(seed);
        out[i] = low + (a * 32768 + b) % (high - low + 1);
    }
}

int main(void) {
    int64_t seed = 2071, total = 0, check = 0;
    int64_t *tasks = malloc(50000 * sizeof *tasks), *workers = malloc(50000 * sizeof *workers);
    for (int64_t t = 0; t < 12; t++) {
        strengths(tasks, 50000, 0, 1000000000, &seed);
        strengths(workers, 50000, 0, 1000000000, &seed);
        int64_t a = max_task_assign(tasks, 50000, workers, 50000, t * 1000, 10000000);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    printf("12 problems: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(tasks);
    free(workers);
    return 0;
}
