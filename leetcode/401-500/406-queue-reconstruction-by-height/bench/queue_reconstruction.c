// Benchmark for #406: mirror of queue_reconstruction.kara (tallest first,
// each inserted at its k). The sort is a stable merge sort on (-h, k), as
// the other mirrors' library sorts are; inserts shift the array with
// memmove.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t h, k;
} Person;

static int before(Person a, Person b) {
    if (a.h != b.h) return a.h > b.h;
    return a.k < b.k;
}

static void merge_sort(Person *a, Person *tmp, int64_t n) {
    if (n < 2) return;
    int64_t mid = n / 2;
    merge_sort(a, tmp, mid);
    merge_sort(a + mid, tmp, n - mid);
    int64_t i = 0, j = mid, t = 0;
    while (i < mid && j < n) tmp[t++] = before(a[j], a[i]) ? a[j++] : a[i++];
    while (i < mid) tmp[t++] = a[i++];
    while (j < n) tmp[t++] = a[j++];
    memcpy(a, tmp, n * sizeof(Person));
}

static Person *reconstruct_queue(Person *people, int64_t n) {
    Person *tmp = malloc(n * sizeof(Person));
    merge_sort(people, tmp, n);
    free(tmp);
    Person *queue = malloc(n * sizeof(Person));
    int64_t len = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t at = people[i].k;
        memmove(queue + at + 1, queue + at, (len - at) * sizeof(Person));
        queue[at] = people[i];
        len++;
    }
    return queue;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t queues = argc > 1 ? atoll(argv[1]) : 1000;
    int64_t n = 2000;
    int64_t seed = 406, rebuilt = 0, checksum = 0;
    Person *line = malloc(n * sizeof(Person));
    Person *people = malloc(n * sizeof(Person));
    for (int64_t t = 0; t < queues; t++) {
        int64_t count[51] = {0};
        for (int64_t i = 0; i < n; i++) {
            int64_t h = 1 + step(&seed) % 50;
            int64_t k = 0;
            for (int64_t g = h; g < 51; g++) k += count[g];
            count[h]++;
            line[i] = (Person){h, k};
        }
        memcpy(people, line, n * sizeof(Person));
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = step(&seed) % (i + 1);
            Person x = people[i];
            people[i] = people[j];
            people[j] = x;
        }
        Person *q = reconstruct_queue(people, n);
        if (memcmp(q, line, n * sizeof(Person)) == 0) rebuilt++;
        for (int64_t i = 0; i < n; i++) {
            checksum = (checksum * 31 + q[i].h * 10000 + q[i].k) % 1000000007;
        }
        free(q);
    }
    free(line);
    free(people);
    printf("%lld queues of %lld people: %lld rebuilt, checksum %lld\n", (long long)queues, (long long)n, (long long)rebuilt, (long long)checksum);
    return 0;
}
