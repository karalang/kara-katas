// LeetCode #1226 bench: the ★ arm in C over the same 3 runs of n = 50000 as
// the Kāra bench: a POSIX thread per philosopher, a `pthread_mutex_t` for
// each fork, the lower-numbered fork taken first, the log under its own
// mutex.
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int p, fork, op; } Entry;

typedef struct {
    pthread_mutex_t forks[5];
} DiningPhilosophers;

typedef struct {
    pthread_mutex_t lock;
    Entry *items;
    long len, cap;
} Log;

static void log_push(Log *log, int p, int fork, int op) {
    pthread_mutex_lock(&log->lock);
    if (log->len == log->cap) {
        log->cap = log->cap ? log->cap * 2 : 16;
        log->items = realloc(log->items, log->cap * sizeof(Entry));
    }
    log->items[log->len++] = (Entry){p, fork, op};
    pthread_mutex_unlock(&log->lock);
}

// The callbacks LeetCode passes, as the entries they log.
static void wants_to_eat(DiningPhilosophers *t, int philosopher, Log *log) {
    int left = philosopher, right = (philosopher + 4) % 5;
    int first = left < right ? left : right, second = left < right ? right : left;
    pthread_mutex_lock(&t->forks[first]);
    pthread_mutex_lock(&t->forks[second]);
    log_push(log, philosopher, 1, 1);  // pickLeftFork
    log_push(log, philosopher, 2, 1);  // pickRightFork
    log_push(log, philosopher, 0, 3);  // eat
    log_push(log, philosopher, 1, 2);  // putLeftFork
    log_push(log, philosopher, 2, 2);  // putRightFork
    pthread_mutex_unlock(&t->forks[second]);
    pthread_mutex_unlock(&t->forks[first]);
}

typedef struct {
    DiningPhilosophers *table;
    Log *log;
    int p;
    long n;
} Task;

static void *philosopher(void *arg) {
    Task *task = arg;
    for (long i = 0; i < task->n; i++) wants_to_eat(task->table, task->p, task->log);
    return NULL;
}

static Log run(long n, const int *order) {
    DiningPhilosophers table;
    for (int f = 0; f < 5; f++) pthread_mutex_init(&table.forks[f], NULL);
    Log log = {.items = NULL, .len = 0, .cap = 0};
    pthread_mutex_init(&log.lock, NULL);
    pthread_t threads[5];
    Task tasks[5];
    for (int k = 0; k < 5; k++) {
        tasks[k] = (Task){&table, &log, order[k], n};
        pthread_create(&threads[k], NULL, philosopher, &tasks[k]);
    }
    for (int k = 0; k < 5; k++) pthread_join(threads[k], NULL);
    for (int f = 0; f < 5; f++) pthread_mutex_destroy(&table.forks[f]);
    pthread_mutex_destroy(&log.lock);
    return log;
}

static int judge(long n, const Log *log) {
    int holder[5] = {-1, -1, -1, -1, -1};
    long meals[5] = {0};
    for (long i = 0; i < log->len; i++) {
        Entry e = log->items[i];
        int f = e.fork == 1 ? e.p : (e.p + 4) % 5;
        if (e.op == 1) {
            if (holder[f] != -1) return 0;
            holder[f] = e.p;
        } else if (e.op == 2) {
            if (holder[f] != e.p) return 0;
            holder[f] = -1;
        } else {
            if (holder[e.p] != e.p || holder[(e.p + 4) % 5] != e.p) return 0;
            meals[e.p]++;
        }
    }
    for (int k = 0; k < 5; k++)
        if (meals[k] != n || holder[k] != -1) return 0;
    return 1;
}

int main(void) {
    const int orders[3][5] = {{0, 1, 2, 3, 4}, {4, 3, 2, 1, 0}, {2, 0, 4, 1, 3}};
    long calls = 0, valid = 0;
    for (int r = 0; r < 3; r++) {
        Log log = run(50000, orders[r]);
        calls += log.len;
        valid += judge(50000, &log);
        free(log.items);
    }
    printf("3 runs of n = 50000: %ld calls, %ld valid\n", calls, valid);
    return 0;
}
