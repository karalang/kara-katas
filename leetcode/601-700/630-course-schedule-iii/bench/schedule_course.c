// LeetCode #630: Course Schedule III -- C mirror of the Kāra bench.
//
// The ★ arm's greedy over the same inputs and rounds: the courses, a
// flat array of (duration, last day) pairs, copied and sorted by last
// day, and a binary max-heap of the durations taken.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t duration;
    int64_t last;
} Course;

static int by_last(const void *a, const void *b) {
    int64_t x = ((const Course *)a)->last, y = ((const Course *)b)->last;
    return (x > y) - (x < y);
}

static void heap_push(int64_t *heap, int64_t *len, int64_t v) {
    int64_t i = (*len)++;
    heap[i] = v;
    while (i > 0 && heap[(i - 1) / 2] < heap[i]) {
        int64_t p = (i - 1) / 2, t = heap[p];
        heap[p] = heap[i];
        heap[i] = t;
        i = p;
    }
}

static int64_t heap_pop(int64_t *heap, int64_t *len) {
    int64_t top = heap[0];
    heap[0] = heap[--(*len)];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < *len && heap[l] > heap[m]) m = l;
        if (r < *len && heap[r] > heap[m]) m = r;
        if (m == i) break;
        int64_t t = heap[m];
        heap[m] = heap[i];
        heap[i] = t;
        i = m;
    }
    return top;
}

static int64_t schedule_course(const Course *courses, int64_t n) {
    Course *order = malloc(n * sizeof(Course));
    memcpy(order, courses, n * sizeof(Course));
    qsort(order, n, sizeof(Course), by_last);
    int64_t *heap = malloc(n * sizeof(int64_t));
    int64_t len = 0, time = 0;
    for (int64_t i = 0; i < n; i++) {
        time += order[i].duration;
        heap_push(heap, &len, order[i].duration);
        if (time > order[i].last) {
            time -= heap_pop(heap, &len);
        }
    }
    free(order);
    free(heap);
    return len;
}

static int64_t seed = 630;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { INPUTS = 20, ROUNDS = 200, COUNT = 10000 };
    Course *all[INPUTS];
    for (int i = 0; i < INPUTS; i++) {
        int64_t longest = 10 + next_random() % 991;
        all[i] = malloc(COUNT * sizeof(Course));
        for (int j = 0; j < COUNT; j++) {
            int64_t duration = 1 + next_random() % longest;
            int64_t last = 1 + next_random() % 10000;
            all[i][j].duration = duration;
            all[i][j].last = last;
        }
    }
    int64_t sum = 0, checksum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t c = schedule_course(all[(r * 7) % INPUTS], COUNT);
        sum += c;
        checksum = (checksum * 31 + c) % 1000000007;
    }
    printf("%d inputs, %d rounds: total %lld, checksum %lld\n", INPUTS, ROUNDS, (long long)sum, (long long)checksum);
    for (int i = 0; i < INPUTS; i++) free(all[i]);
    return 0;
}
