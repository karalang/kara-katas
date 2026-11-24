// LeetCode #1335 bench, C mirror of the Kāra bench: the ★ arm on 20
// schedules of 300 jobs built once, then 30 passes, each setting one job
// of every schedule and the number of days from the checksum so far,
// answering every schedule.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t min_difficulty(const int32_t *job_difficulty, int64_t n, int32_t d) {
    int64_t days = d;
    if (n < days) {
        return -1;
    }
    const int64_t far = INT64_MAX / 2;
    int64_t *best = malloc(sizeof(int64_t) * (n + 1));
    int64_t *next = malloc(sizeof(int64_t) * (n + 1));
    for (int64_t i = 0; i <= n; i++) {
        best[i] = far;
    }
    best[0] = 0;
    for (int64_t day = 1; day <= days; day++) {
        for (int64_t i = 0; i <= n; i++) {
            next[i] = far;
        }
        for (int64_t i = day; i <= n; i++) {
            int64_t hardest = 0;
            for (int64_t j = i - 1; j >= day - 1; j--) {
                if (job_difficulty[j] > hardest) {
                    hardest = job_difficulty[j];
                }
                if (best[j] + hardest < next[i]) {
                    next[i] = best[j] + hardest;
                }
            }
        }
        int64_t *swap = best;
        best = next;
        next = swap;
    }
    int32_t answer = (int32_t)best[n];
    free(best);
    free(next);
    return answer;
}

static int64_t seed = 1335;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 300;
    int32_t *schedules[20];
    for (int t = 0; t < 20; t++) {
        schedules[t] = malloc(sizeof(int32_t) * n);
        for (int64_t i = 0; i < n; i++) {
            schedules[t][i] = (int32_t)(next_random() % 1001);
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 30; pass++) {
        int32_t d = (int32_t)(6 + check % 5);
        for (int t = 0; t < 20; t++) {
            int64_t at = check % n;
            schedules[t][at] = (int32_t)(check / 3 % 1001);
            int32_t answer = min_difficulty(schedules[t], n, d);
            check = (check * 31 + answer + pass) % 1000000007;
        }
    }
    printf("30 passes over 20 schedules of 300 jobs: checksum %lld\n", (long long)check);
    for (int t = 0; t < 20; t++) {
        free(schedules[t]);
    }
    return 0;
}
