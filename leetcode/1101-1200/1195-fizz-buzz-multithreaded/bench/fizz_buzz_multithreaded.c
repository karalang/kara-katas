// LeetCode #1195 bench: the ★ arm in C (POSIX `sem_t` and threads), over
// the same 3 runs of n = 200000 as the Kāra bench. Each printer appends a
// copy of its line to a shared list under a mutex, as the other languages'
// printers append a string.

#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    long n;
    sem_t fizz_turn, buzz_turn, fizzbuzz_turn, number_turn;
    pthread_mutex_t lock;
    char **lines;
    long len, cap;
} FizzBuzz;

static void put(FizzBuzz *fb, const char *s) {
    char *copy = strdup(s);
    pthread_mutex_lock(&fb->lock);
    if (fb->len == fb->cap) {
        fb->cap = fb->cap ? fb->cap * 2 : 16;
        fb->lines = realloc(fb->lines, fb->cap * sizeof(char *));
    }
    fb->lines[fb->len++] = copy;
    pthread_mutex_unlock(&fb->lock);
}

static void pass(FizzBuzz *fb, long i) {
    if (i > fb->n) {
        return;
    }
    if (i % 15 == 0) {
        sem_post(&fb->fizzbuzz_turn);
    } else if (i % 3 == 0) {
        sem_post(&fb->fizz_turn);
    } else if (i % 5 == 0) {
        sem_post(&fb->buzz_turn);
    } else {
        sem_post(&fb->number_turn);
    }
}

static void *fizz(void *arg) {
    FizzBuzz *fb = arg;
    for (long i = 1; i <= fb->n; i++) {
        if (i % 3 == 0 && i % 5 != 0) {
            sem_wait(&fb->fizz_turn);
            put(fb, "fizz");
            pass(fb, i + 1);
        }
    }
    return NULL;
}

static void *buzz(void *arg) {
    FizzBuzz *fb = arg;
    for (long i = 1; i <= fb->n; i++) {
        if (i % 5 == 0 && i % 3 != 0) {
            sem_wait(&fb->buzz_turn);
            put(fb, "buzz");
            pass(fb, i + 1);
        }
    }
    return NULL;
}

static void *fizzbuzz(void *arg) {
    FizzBuzz *fb = arg;
    for (long i = 1; i <= fb->n; i++) {
        if (i % 15 == 0) {
            sem_wait(&fb->fizzbuzz_turn);
            put(fb, "fizzbuzz");
            pass(fb, i + 1);
        }
    }
    return NULL;
}

static void *number(void *arg) {
    FizzBuzz *fb = arg;
    char buf[24];
    for (long i = 1; i <= fb->n; i++) {
        if (i % 3 != 0 && i % 5 != 0) {
            sem_wait(&fb->number_turn);
            snprintf(buf, sizeof buf, "%ld", i);
            put(fb, buf);
            pass(fb, i + 1);
        }
    }
    return NULL;
}

int main(void) {
    void *(*roles[4])(void *) = {fizz, buzz, fizzbuzz, number};
    int orders[3][4] = {{0, 1, 2, 3}, {3, 2, 1, 0}, {1, 3, 0, 2}};
    long check = 0;
    for (int r = 0; r < 3; r++) {
        FizzBuzz fb = {.n = 200000};
        sem_init(&fb.fizz_turn, 0, 0);
        sem_init(&fb.buzz_turn, 0, 0);
        sem_init(&fb.fizzbuzz_turn, 0, 0);
        sem_init(&fb.number_turn, 0, 1);
        pthread_mutex_init(&fb.lock, NULL);
        pthread_t threads[4];
        for (int k = 0; k < 4; k++) {
            pthread_create(&threads[k], NULL, roles[orders[r][k]], &fb);
        }
        for (int k = 0; k < 4; k++) {
            pthread_join(threads[k], NULL);
        }
        for (long i = 0; i < fb.len; i++) {
            for (const char *p = fb.lines[i]; *p; p++) {
                check = (check * 131 + (unsigned char)*p) % 1000000007;
            }
            check = (check * 131 + 10) % 1000000007;
            free(fb.lines[i]);
        }
        free(fb.lines);
        sem_destroy(&fb.fizz_turn);
        sem_destroy(&fb.buzz_turn);
        sem_destroy(&fb.fizzbuzz_turn);
        sem_destroy(&fb.number_turn);
        pthread_mutex_destroy(&fb.lock);
    }
    printf("3 runs of n = 200000: checksum %ld\n", check);
    return 0;
}
