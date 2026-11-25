// LeetCode #1376 bench -- C: the ★ arm: each manager's reports in a list
// (here one array of reports grouped by manager, counted first), then a
// breadth-first walk down from the head, each employee hearing the news
// when the manager heard it plus the manager's inform time.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int num_of_minutes(int n, int head_id, const int *manager, const int *inform_time) {
    int *start = calloc((size_t)n + 1, sizeof(int));
    int *reports = malloc((size_t)n * sizeof(int));
    int *heard = calloc((size_t)n, sizeof(int));
    int *queue = malloc((size_t)n * sizeof(int));
    for (int i = 0; i < n; i++) {
        if (manager[i] >= 0) {
            start[manager[i] + 1]++;
        }
    }
    for (int i = 0; i < n; i++) {
        start[i + 1] += start[i];
    }
    int *fill = malloc((size_t)n * sizeof(int));
    for (int i = 0; i < n; i++) {
        fill[i] = start[i];
    }
    for (int i = 0; i < n; i++) {
        if (manager[i] >= 0) {
            reports[fill[manager[i]]++] = i;
        }
    }
    int qh = 0, qt = 0, latest = 0;
    queue[qt++] = head_id;
    while (qh < qt) {
        int u = queue[qh++];
        if (heard[u] > latest) {
            latest = heard[u];
        }
        for (int k = start[u]; k < start[u + 1]; k++) {
            int v = reports[k];
            heard[v] = heard[u] + inform_time[u];
            queue[qt++] = v;
        }
    }
    free(start);
    free(reports);
    free(heard);
    free(queue);
    free(fill);
    return latest;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 10 companies of 10^5 employees, built once; then 200 rounds, each
    // giving one employee of one company a new inform time if it is a
    // manager, and timing that company (see the Kāra bench)
    const int64_t n = 100000;
    int64_t seed = 1376;
    int heads[10];
    int *managers[10];
    int *informs[10];
    int64_t *order = malloc((size_t)n * sizeof(int64_t));
    for (int c = 0; c < 10; c++) {
        for (int64_t i = 0; i < n; i++) {
            order[i] = i;
        }
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random(&seed) % (i + 1);
            int64_t t = order[i];
            order[i] = order[j];
            order[j] = t;
        }
        int *manager = malloc((size_t)n * sizeof(int));
        int *inform = calloc((size_t)n, sizeof(int));
        manager[order[0]] = -1;
        for (int64_t k = 1; k < n; k++) {
            int64_t m = order[next_random(&seed) % k];
            manager[order[k]] = (int)m;
            if (inform[m] == 0) {
                inform[m] = (int)(1 + next_random(&seed) % 1000);
            }
        }
        heads[c] = (int)order[0];
        managers[c] = manager;
        informs[c] = inform;
    }
    int64_t check = 0;
    for (int64_t r = 0; r < 200; r++) {
        int64_t c = check % 10;
        int64_t e = (check / 10) % n;
        if (informs[c][e] > 0) {
            informs[c][e] = (int)(1 + (check + r) % 1000);
        }
        int64_t got = num_of_minutes((int)n, heads[c], managers[c], informs[c]);
        check = (check * 31 + got + r) % 1000000007;
    }
    printf("200 rounds over 10 companies of 100000 employees: checksum %lld\n", (long long)check);
    for (int c = 0; c < 10; c++) {
        free(managers[c]);
        free(informs[c]);
    }
    free(order);
    return 0;
}
