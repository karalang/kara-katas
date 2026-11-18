// LeetCode #1188: Design Bounded Blocking Queue -- the bench in C: the ★
// arm's two counting semaphores (`sem_t`) and a lock over the values, a
// growable ring as the deque.
#include <pthread.h>
#include <semaphore.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    sem_t slots, items;
    pthread_mutex_t lock;
    int64_t *ring;
    int64_t cap, head, len;
} BoundedBlockingQueue;

static void queue_init(BoundedBlockingQueue *q, int capacity) {
    sem_init(&q->slots, 0, capacity);
    sem_init(&q->items, 0, 0);
    pthread_mutex_init(&q->lock, NULL);
    q->cap = 4;
    q->ring = malloc(q->cap * sizeof(int64_t));
    q->head = q->len = 0;
}

static void queue_free(BoundedBlockingQueue *q) {
    sem_destroy(&q->slots);
    sem_destroy(&q->items);
    pthread_mutex_destroy(&q->lock);
    free(q->ring);
}

// The deque's push_back: grows the ring when it is full.
static void push_back(BoundedBlockingQueue *q, int64_t v) {
    if (q->len == q->cap) {
        int64_t *grown = malloc(2 * q->cap * sizeof(int64_t));
        for (int64_t i = 0; i < q->len; i++) grown[i] = q->ring[(q->head + i) % q->cap];
        free(q->ring);
        q->ring = grown;
        q->head = 0;
        q->cap *= 2;
    }
    q->ring[(q->head + q->len) % q->cap] = v;
    q->len++;
}

static void enqueue(BoundedBlockingQueue *q, int64_t element) {
    sem_wait(&q->slots);
    pthread_mutex_lock(&q->lock);
    push_back(q, element);
    pthread_mutex_unlock(&q->lock);
    sem_post(&q->items);
}

static int64_t dequeue(BoundedBlockingQueue *q) {
    sem_wait(&q->items);
    pthread_mutex_lock(&q->lock);
    int64_t element = q->ring[q->head];
    q->head = (q->head + 1) % q->cap;
    q->len--;
    pthread_mutex_unlock(&q->lock);
    sem_post(&q->slots);
    return element;
}

static int64_t size(BoundedBlockingQueue *q) {
    pthread_mutex_lock(&q->lock);
    int64_t n = q->len;
    pthread_mutex_unlock(&q->lock);
    return n;
}

typedef struct {
    BoundedBlockingQueue *q;
    int64_t round, p;
    int64_t *total;
    pthread_mutex_t *total_lock;
} Task;

static void *produce(void *arg) {
    Task *t = arg;
    for (int64_t k = 0; k < 2500; k++) enqueue(t->q, (t->round * 7919 + t->p * 10007 + k * 31) % 1000);
    return NULL;
}

static void *consume(void *arg) {
    Task *t = arg;
    int64_t sum = 0;
    for (int k = 0; k < 2500; k++) sum += dequeue(t->q);
    pthread_mutex_lock(t->total_lock);
    *t->total += sum;
    pthread_mutex_unlock(t->total_lock);
    return NULL;
}

static int64_t run(int64_t round) {
    BoundedBlockingQueue q;
    queue_init(&q, 16);
    int64_t total = 0;
    pthread_mutex_t total_lock;
    pthread_mutex_init(&total_lock, NULL);
    pthread_t threads[8];
    Task tasks[8];
    for (int i = 0; i < 8; i++) {
        tasks[i] = (Task){&q, round, i, &total, &total_lock};
        pthread_create(&threads[i], NULL, i < 4 ? produce : consume, &tasks[i]);
    }
    for (int i = 0; i < 8; i++) pthread_join(threads[i], NULL);
    int64_t result = total + 1000 * size(&q);
    pthread_mutex_destroy(&total_lock);
    queue_free(&q);
    return result;
}

int main(void) {
    int64_t rounds = 100, check = 0;
    for (int64_t round = 0; round < rounds; round++) check = (check * 131 + run(round)) % 1000000007;
    printf("%lld rounds of 4 producers and 4 consumers moving 10000 values through 16 places: checksum %lld\n",
           (long long)rounds, (long long)check);
    return 0;
}
