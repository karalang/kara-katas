// LeetCode #2747: Count Zero Request Servers -- the bench (servers.kara in
// C): the logs sorted by time with `qsort`, the queries in time order, and
// a window of logs sliding forward with a count for each server.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SIZE 100000

typedef struct { int64_t time, server; } Log;

static int by_time(const void *a, const void *b) {
    const Log *x = a, *y = b;
    if (x->time != y->time) return x->time < y->time ? -1 : 1;
    return (x->server > y->server) - (x->server < y->server);
}

static const int64_t *sort_queries;

static int by_query(const void *a, const void *b) {
    int64_t i = *(const int64_t *)a, j = *(const int64_t *)b;
    if (sort_queries[i] != sort_queries[j]) return sort_queries[i] < sort_queries[j] ? -1 : 1;
    return (i > j) - (i < j);
}

static void count_servers(int64_t n, const int64_t (*logs)[2], int64_t nl, int64_t x, const int64_t *queries, int64_t nq, int64_t *answers) {
    Log *sorted = malloc(sizeof(Log) * nl);
    for (int64_t i = 0; i < nl; i++) { sorted[i].time = logs[i][1]; sorted[i].server = logs[i][0]; }
    qsort(sorted, nl, sizeof(Log), by_time);
    int64_t *order = malloc(sizeof(int64_t) * nq);
    for (int64_t i = 0; i < nq; i++) order[i] = i;
    sort_queries = queries;
    qsort(order, nq, sizeof(int64_t), by_query);
    int64_t *requests = calloc(n + 1, sizeof(int64_t));
    int64_t busy = 0, start = 0, end = 0;
    for (int64_t k = 0; k < nq; k++) {
        int64_t i = order[k], q = queries[i];
        while (end < nl && sorted[end].time <= q) {
            int64_t s = sorted[end].server;
            if (requests[s] == 0) busy++;
            requests[s]++;
            end++;
        }
        while (start < end && sorted[start].time < q - x) {
            int64_t s = sorted[start].server;
            requests[s]--;
            if (requests[s] == 0) busy--;
            start++;
        }
        answers[i] = n - busy;
    }
    free(sorted); free(order); free(requests);
}

static int64_t seed = 2747;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int count = 10, rounds = 3;
    const int64_t n = 100000;
    int64_t (*logs)[SIZE][2] = malloc(sizeof(int64_t) * count * SIZE * 2);
    int64_t (*queries)[SIZE] = malloc(sizeof(int64_t) * count * SIZE);
    int64_t xs[10];
    for (int k = 0; k < count; k++) {
        xs[k] = wide() % 100000 + 1;
        for (int i = 0; i < SIZE; i++) {
            logs[k][i][0] = next_random() % n + 1;
            int64_t hi = next_random();
            logs[k][i][1] = (hi * 32768 + next_random()) % 1000000 + 1;
        }
        for (int i = 0; i < SIZE; i++) {
            int64_t hi = next_random();
            queries[k][i] = xs[k] + 1 + (hi * 32768 + next_random()) % (1000000 - xs[k]);
        }
    }
    int64_t *answers = malloc(sizeof(int64_t) * SIZE);
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            count_servers(n, (const int64_t (*)[2])logs[k], SIZE, xs[k], queries[k], SIZE, answers);
            for (int i = 0; i < SIZE; i++) {
                sum += answers[i];
                check = (check * 31 + answers[i] + r) % 1000000007;
            }
        }
    }
    printf("%d cases of 100000 logs and queries, %d rounds: answers sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(logs); free(queries); free(answers);
    return 0;
}
