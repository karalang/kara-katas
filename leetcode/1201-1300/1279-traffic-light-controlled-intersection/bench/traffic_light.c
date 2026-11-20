// LeetCode #1279 bench, in C: the ★ arm (the green road behind a mutex,
// held while a car turns its light and crosses) over 2000 runs of 20 cars,
// a pthread for each car, on random roads and started in a random order;
// each run's log judged by the statement read literally.
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { long long kind, x; } event;

typedef struct {
    pthread_mutex_t lock;
    long long green;
} traffic_light;

typedef struct {
    pthread_mutex_t lock;
    event events[64];
    int len;
} log_t;

typedef struct {
    traffic_light *light;
    log_t *log;
    long long car, road, direction;
} car_t;

static void push(log_t *log, long long kind, long long x) {
    pthread_mutex_lock(&log->lock);
    log->events[log->len].kind = kind;
    log->events[log->len].x = x;
    log->len++;
    pthread_mutex_unlock(&log->lock);
}

static void car_arrived(traffic_light *t, car_t *c) {
    pthread_mutex_lock(&t->lock);
    if (t->green != c->road) {
        push(c->log, 0, c->road);
        t->green = c->road;
    }
    push(c->log, 1, c->car);
    pthread_mutex_unlock(&t->lock);
}

static void *car_task(void *arg) {
    car_t *c = arg;
    car_arrived(c->light, c);
    return NULL;
}

static long long seed = 1279;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int judge(const long long *directions, const log_t *log) {
    long long green = 1;
    int crossed[20] = {0};
    for (int e = 0; e < log->len; e++) {
        long long kind = log->events[e].kind, x = log->events[e].x;
        if (kind == 0) {
            if (x == green) return 0;
            green = x;
        } else {
            long long road = directions[x] <= 2 ? 1 : 2;
            if (road != green || crossed[x]) return 0;
            crossed[x] = 1;
        }
    }
    for (int i = 0; i < 20; i++)
        if (!crossed[i]) return 0;
    return 1;
}

int main(void) {
    long long cars = 0, valid = 0;
    for (int r = 0; r < 2000; r++) {
        long long directions[20];
        int order[20];
        for (int i = 0; i < 20; i++) directions[i] = next_random() % 4 + 1;
        for (int i = 0; i < 20; i++) order[i] = i;
        for (int i = 19; i >= 1; i--) {
            int j = (int)(next_random() % (i + 1));
            int t = order[i];
            order[i] = order[j];
            order[j] = t;
        }
        traffic_light light = {PTHREAD_MUTEX_INITIALIZER, 1};
        log_t log = {PTHREAD_MUTEX_INITIALIZER, {{0, 0}}, 0};
        car_t args[20];
        pthread_t threads[20];
        for (int k = 0; k < 20; k++) {
            int i = order[k];
            args[k] = (car_t){&light, &log, i, directions[i] <= 2 ? 1 : 2, directions[i]};
            pthread_create(&threads[k], NULL, car_task, &args[k]);
        }
        for (int k = 0; k < 20; k++) pthread_join(threads[k], NULL);
        for (int e = 0; e < log.len; e++)
            if (log.events[e].kind == 1) cars++;
        valid += judge(directions, &log);
    }
    printf("2000 runs of 20 cars: %lld cars crossed, %lld valid\n", cars, valid);
    return 0;
}
