// Benchmark workload — greedy O(n log n) Minimum Initial Energy to Finish Tasks.
// C mirror of bench/greedy.kara and bench/greedy.rs. Same N, K, generator,
// sink formula — see those files' headers for the workload rationale.
//
// Built via `clang -O3` in bench.sh.

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct {
    int64_t actual;
    int64_t minimum;
} Task;

static int task_cmp(const void *a, const void *b) {
    const Task *ta = (const Task *)a;
    const Task *tb = (const Task *)b;
    int64_t da = ta->minimum - ta->actual;
    int64_t db = tb->minimum - tb->actual;
    if (db < da) return -1;
    if (db > da) return 1;
    return 0;
}

static int64_t minimum_effort(Task *tasks, size_t n) {
    qsort(tasks, n, sizeof(Task), task_cmp);

    int64_t energy = 0;
    int64_t spent = 0;
    for (size_t i = 0; i < n; i++) {
        int64_t need = spent + tasks[i].minimum;
        if (need > energy) {
            energy = need;
        }
        spent += tasks[i].actual;
    }
    return energy;
}

int main(void) {
    const int64_t N = 50000;
    const int k_iters = 5;

    Task *data = (Task *)malloc((size_t)N * sizeof(Task));
    if (!data) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    }

    for (int64_t i = 0; i < N; i++) {
        int64_t actual = (i * 7) % 100 + 1;
        int64_t minimum = actual + (i * 13) % 50;
        data[i].actual = actual;
        data[i].minimum = minimum;
    }

    int64_t sum = 0;
    for (int k = 0; k < k_iters; k++) {
        sum += minimum_effort(data, (size_t)N);
    }
    printf("%lld\n", (long long)sum);

    free(data);
    return 0;
}
