// LeetCode #1115: Print FooBar Alternately -- the bench in C: a POSIX
// thread per method, two semaphores as the ★ arm's two turn channels,
// foo's holding one permit, and the log behind a mutex.
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int n;
    sem_t foo_turn, bar_turn;
} FooBar;

typedef struct {
    pthread_mutex_t mu;
    char *text;
    size_t len;
} Log;

static void print_word(Log *log, const char *word) {
    pthread_mutex_lock(&log->mu);
    size_t k = strlen(word);
    memcpy(log->text + log->len, word, k);
    log->len += k;
    pthread_mutex_unlock(&log->mu);
}

typedef struct {
    FooBar *fb;
    Log *log;
} Job;

static void *foo(void *arg) {
    Job *j = arg;
    for (int i = 0; i < j->fb->n; i++) {
        sem_wait(&j->fb->foo_turn);
        print_word(j->log, "foo");
        sem_post(&j->fb->bar_turn);
    }
    return NULL;
}

static void *bar(void *arg) {
    Job *j = arg;
    for (int i = 0; i < j->fb->n; i++) {
        sem_wait(&j->fb->bar_turn);
        print_word(j->log, "bar");
        sem_post(&j->fb->foo_turn);
    }
    return NULL;
}

// Runs n rounds; the log goes to `out`, its length returned.
static size_t run(int n, int bar_first, char *out) {
    FooBar fb;
    fb.n = n;
    sem_init(&fb.foo_turn, 0, 1);
    sem_init(&fb.bar_turn, 0, 0);
    Log log;
    pthread_mutex_init(&log.mu, NULL);
    log.text = out;
    log.len = 0;
    Job job = {&fb, &log};
    pthread_t a, b;
    if (bar_first) {
        pthread_create(&b, NULL, bar, &job);
        pthread_create(&a, NULL, foo, &job);
    } else {
        pthread_create(&a, NULL, foo, &job);
        pthread_create(&b, NULL, bar, &job);
    }
    pthread_join(a, NULL);
    pthread_join(b, NULL);
    sem_destroy(&fb.foo_turn);
    sem_destroy(&fb.bar_turn);
    pthread_mutex_destroy(&log.mu);
    out[log.len] = 0;
    return log.len;
}

int main(void) {
    char want[1201];
    want[0] = 0;
    for (int i = 0; i < 200; i++) strcat(want, "foobar");
    char *out = malloc(1201);
    int alternating = 0;
    long long check = 0;
    for (int r = 0; r < 1000; r++) {
        size_t len = run(200, r % 2 == 1, out);
        if (strcmp(out, want) == 0) alternating++;
        check = (check * 31 + (long long)len + r) % 1000000007;
    }
    free(out);
    printf("1000 runs of 200 rounds: %d alternating, checksum %lld\n", alternating, check);
    return 0;
}
