// LeetCode #1306 bench in C: the ★ arm (a breadth-first walk from the
// start, the queue an array of n places read from a moving head, since each
// place is queued once) on the same 10 arrays and 300 passes.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool can_reach(const int64_t *arr, int64_t n, int64_t start) {
    bool *seen = calloc((size_t)n, sizeof(bool));
    int64_t *queue = malloc(sizeof(int64_t) * (size_t)n);
    size_t head = 0, tail = 0;
    queue[tail++] = start;
    seen[start] = true;
    bool found = false;
    while (head < tail) {
        int64_t i = queue[head++];
        if (arr[i] == 0) {
            found = true;
            break;
        }
        int64_t jumps[2] = {i + arr[i], i - arr[i]};
        for (int k = 0; k < 2; k++) {
            int64_t j = jumps[k];
            if (j >= 0 && j < n && !seen[j]) {
                seen[j] = true;
                queue[tail++] = j;
            }
        }
    }
    free(seen);
    free(queue);
    return found;
}

static int64_t seed = 1306;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t n = 50000;
    int64_t *arrays[10];
    for (int a = 0; a < 10; a++) {
        arrays[a] = malloc(sizeof(int64_t) * (size_t)n);
        for (int64_t k = 0; k < n; k++) arrays[a][k] = 1 + next_random() % 10;
        arrays[a][next_random() % n] = 0;
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 300; pass++) {
        for (int a = 0; a < 10; a++) {
            arrays[a][check % n] = (check / 7) % 11;
            int64_t start = (check / 13) % n;
            bool got = can_reach(arrays[a], n, start);
            check = (check * 31 + (got ? 1 : 2) + pass) % 1000000007;
        }
    }
    printf("300 passes over 10 arrays of 5 * 10^4: checksum %lld\n", (long long)check);
    return 0;
}
