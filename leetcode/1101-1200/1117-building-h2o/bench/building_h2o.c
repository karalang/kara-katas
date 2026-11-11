// LeetCode #1117: Building H2O -- the bench in C: a POSIX thread per
// atom. A hydrogen puts its record, holding the semaphore it waits on,
// in a ring of two guarded by a mutex and two counting semaphores; an
// oxygen takes the bonding mutex, takes two hydrogens off the ring,
// releases itself, posts each hydrogen's semaphore with its own `out`
// semaphore to say it is out on, and waits on that twice.
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    sem_t go;
    sem_t *out;
} Hydrogen;

typedef struct {
    pthread_mutex_t bonding;
    pthread_mutex_t ring_mu;
    sem_t slots, items;
    Hydrogen *ring[2];
    int head, tail;
} H2O;

typedef struct {
    pthread_mutex_t mu;
    char text[64];
    int len;
} Log;

typedef struct {
    H2O *h2o;
    Log *log;
} Job;

static void say(Log *log, char c) {
    pthread_mutex_lock(&log->mu);
    log->text[log->len++] = c;
    pthread_mutex_unlock(&log->mu);
}

static void *hydrogen(void *arg) {
    Job *j = arg;
    H2O *h = j->h2o;
    Hydrogen me;
    sem_init(&me.go, 0, 0);
    sem_wait(&h->slots);
    pthread_mutex_lock(&h->ring_mu);
    h->ring[h->tail] = &me;
    h->tail = (h->tail + 1) % 2;
    pthread_mutex_unlock(&h->ring_mu);
    sem_post(&h->items);
    sem_wait(&me.go);
    say(j->log, 'H');
    sem_post(me.out);
    sem_destroy(&me.go);
    return NULL;
}

static void *oxygen(void *arg) {
    Job *j = arg;
    H2O *h = j->h2o;
    pthread_mutex_lock(&h->bonding);
    Hydrogen *gos[2];
    for (int i = 0; i < 2; i++) {
        sem_wait(&h->items);
        pthread_mutex_lock(&h->ring_mu);
        gos[i] = h->ring[h->head];
        h->head = (h->head + 1) % 2;
        pthread_mutex_unlock(&h->ring_mu);
        sem_post(&h->slots);
    }
    say(j->log, 'O');
    sem_t out;
    sem_init(&out, 0, 0);
    for (int i = 0; i < 2; i++) {
        gos[i]->out = &out;
        sem_post(&gos[i]->go);
    }
    sem_wait(&out);
    sem_wait(&out);
    sem_destroy(&out);
    pthread_mutex_unlock(&h->bonding);
    return NULL;
}

static int run(const char *water, int n, char *out) {
    H2O h;
    pthread_mutex_init(&h.bonding, NULL);
    pthread_mutex_init(&h.ring_mu, NULL);
    sem_init(&h.slots, 0, 2);
    sem_init(&h.items, 0, 0);
    h.head = h.tail = 0;
    Log log;
    pthread_mutex_init(&log.mu, NULL);
    log.len = 0;
    Job job = {&h, &log};
    pthread_t threads[60];
    for (int i = 0; i < n; i++)
        pthread_create(&threads[i], NULL, water[i] == 'H' ? hydrogen : oxygen, &job);
    for (int i = 0; i < n; i++) pthread_join(threads[i], NULL);
    pthread_mutex_destroy(&h.bonding);
    pthread_mutex_destroy(&h.ring_mu);
    sem_destroy(&h.slots);
    sem_destroy(&h.items);
    pthread_mutex_destroy(&log.mu);
    memcpy(out, log.text, (size_t)log.len);
    out[log.len] = 0;
    return log.len;
}

int main(void) {
    long long seed = 1117;
    int whole = 0;
    long long check = 0;
    char water[61], out[64];
    for (int r = 0; r < 500; r++) {
        for (int i = 0; i < 20; i++) memcpy(water + 3 * i, "OHH", 3);
        water[60] = 0;
        for (int j = 0; j < 60; j++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int k = j + (int)(seed / 65536 % (60 - j));
            char t = water[j];
            water[j] = water[k];
            water[k] = t;
        }
        int len = run(water, 60, out);
        int molecules = 0;
        for (int i = 0; i < len / 3; i++) {
            int hs = (out[3 * i] == 'H') + (out[3 * i + 1] == 'H') + (out[3 * i + 2] == 'H');
            if (hs == 2) molecules++;
        }
        if (molecules == 20) whole++;
        check = (check * 31 + len + r) % 1000000007;
    }
    printf("500 runs of 20 molecules: %d with every molecule whole, checksum %lld\n", whole, check);
    return 0;
}
