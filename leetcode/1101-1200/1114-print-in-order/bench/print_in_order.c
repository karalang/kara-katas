// LeetCode #1114: Print in Order -- the bench in C: a POSIX thread per
// method, two semaphores as the ★ arm's two one-shot channels, and the
// log behind a mutex.
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    sem_t first_done, second_done;
} Foo;

typedef struct {
    pthread_mutex_t mu;
    char text[32];
} Log;

static void print_word(Log *log, const char *word) {
    pthread_mutex_lock(&log->mu);
    strcat(log->text, word);
    pthread_mutex_unlock(&log->mu);
}

static void first(Foo *f, Log *log) {
    print_word(log, "first");
    sem_post(&f->first_done);
}

static void second(Foo *f, Log *log) {
    sem_wait(&f->first_done);
    print_word(log, "second");
    sem_post(&f->second_done);
}

static void third(Foo *f, Log *log) {
    sem_wait(&f->second_done);
    print_word(log, "third");
}

typedef struct {
    Foo *foo;
    Log *log;
    int k;
} Job;

static void *task(void *arg) {
    Job *j = arg;
    if (j->k == 1) first(j->foo, j->log);
    else if (j->k == 2) second(j->foo, j->log);
    else third(j->foo, j->log);
    return NULL;
}

static size_t run(const int *nums, char *out) {
    Foo foo;
    Log log;
    sem_init(&foo.first_done, 0, 0);
    sem_init(&foo.second_done, 0, 0);
    pthread_mutex_init(&log.mu, NULL);
    log.text[0] = 0;
    pthread_t threads[3];
    Job jobs[3];
    for (int i = 0; i < 3; i++) {
        jobs[i] = (Job){&foo, &log, nums[i]};
        pthread_create(&threads[i], NULL, task, &jobs[i]);
    }
    for (int i = 0; i < 3; i++) pthread_join(threads[i], NULL);
    sem_destroy(&foo.first_done);
    sem_destroy(&foo.second_done);
    pthread_mutex_destroy(&log.mu);
    strcpy(out, log.text);
    return strlen(out);
}

int main(void) {
    static const int orders[6][3] = {{1, 2, 3}, {1, 3, 2}, {2, 1, 3}, {2, 3, 1}, {3, 1, 2}, {3, 2, 1}};
    int in_order = 0;
    long long check = 0;
    char out[32];
    for (int r = 0; r < 10000; r++) {
        size_t len = run(orders[r * 7 % 6], out);
        if (strcmp(out, "firstsecondthird") == 0) in_order++;
        check = (check * 31 + (long long)len) % 1000000007;
    }
    printf("10000 runs: %d printed in order, checksum %lld\n", in_order, check);
    return 0;
}
