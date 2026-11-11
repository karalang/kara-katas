// LeetCode #1116: Print Zero Even Odd -- the bench in C: a POSIX thread
// per method, three semaphores as the ★ arm's three turn channels,
// zero's holding one permit, and the log behind a mutex.
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int n;
    sem_t zero_turn, even_turn, odd_turn;
} ZeroEvenOdd;

typedef struct {
    pthread_mutex_t mu;
    char *text;
    size_t len;
} Log;

static void print_number(Log *log, int x) {
    pthread_mutex_lock(&log->mu);
    log->len += (size_t)sprintf(log->text + log->len, "%d", x);
    pthread_mutex_unlock(&log->mu);
}

typedef struct {
    ZeroEvenOdd *z;
    Log *log;
} Job;

static void *zero(void *arg) {
    Job *j = arg;
    for (int i = 1; i <= j->z->n; i++) {
        sem_wait(&j->z->zero_turn);
        print_number(j->log, 0);
        sem_post(i % 2 == 1 ? &j->z->odd_turn : &j->z->even_turn);
    }
    return NULL;
}

static void *even(void *arg) {
    Job *j = arg;
    for (int i = 2; i <= j->z->n; i += 2) {
        sem_wait(&j->z->even_turn);
        print_number(j->log, i);
        sem_post(&j->z->zero_turn);
    }
    return NULL;
}

static void *odd(void *arg) {
    Job *j = arg;
    for (int i = 1; i <= j->z->n; i += 2) {
        sem_wait(&j->z->odd_turn);
        print_number(j->log, i);
        sem_post(&j->z->zero_turn);
    }
    return NULL;
}

static size_t run(int n, const int *order, char *out) {
    ZeroEvenOdd z;
    z.n = n;
    sem_init(&z.zero_turn, 0, 1);
    sem_init(&z.even_turn, 0, 0);
    sem_init(&z.odd_turn, 0, 0);
    Log log;
    pthread_mutex_init(&log.mu, NULL);
    log.text = out;
    log.len = 0;
    Job job = {&z, &log};
    void *(*fns[3])(void *) = {zero, even, odd};
    pthread_t threads[3];
    for (int i = 0; i < 3; i++) pthread_create(&threads[i], NULL, fns[order[i]], &job);
    for (int i = 0; i < 3; i++) pthread_join(threads[i], NULL);
    sem_destroy(&z.zero_turn);
    sem_destroy(&z.even_turn);
    sem_destroy(&z.odd_turn);
    pthread_mutex_destroy(&log.mu);
    out[log.len] = 0;
    return log.len;
}

int main(void) {
    static const int orders[6][3] = {{0, 1, 2}, {0, 2, 1}, {1, 0, 2}, {1, 2, 0}, {2, 0, 1}, {2, 1, 0}};
    char *want = malloc(1024);
    size_t w = 0;
    for (int i = 1; i <= 200; i++) w += (size_t)sprintf(want + w, "0%d", i);
    char *out = malloc(1024);
    int right = 0;
    long long check = 0;
    for (int r = 0; r < 1000; r++) {
        size_t len = run(200, orders[r % 6], out);
        if (strcmp(out, want) == 0) right++;
        check = (check * 31 + (long long)len + r) % 1000000007;
    }
    free(out);
    free(want);
    printf("1000 runs over 1 to 200: %d in order, checksum %lld\n", right, check);
    return 0;
}
