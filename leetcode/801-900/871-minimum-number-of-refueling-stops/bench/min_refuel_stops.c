// LeetCode #871: Minimum Number of Refueling Stops -- C mirror of the
// bench program (the ★ arm, a heap of the stations passed), with a binary
// max-heap in an array.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t heap[512];

static int64_t min_refuel_stops(int64_t target, int64_t start_fuel, const int64_t *pos, const int64_t *gain, int64_t n) {
    int64_t size = 0, reach = start_fuel, stops = 0, next = 0;
    while (reach < target) {
        while (next < n && pos[next] <= reach) {
            int64_t i = size++;
            heap[i] = gain[next++];
            while (i > 0 && heap[(i - 1) / 2] < heap[i]) {
                int64_t p = (i - 1) / 2, t = heap[p];
                heap[p] = heap[i];
                heap[i] = t;
                i = p;
            }
        }
        if (size == 0) return -1;
        reach += heap[0];
        stops++;
        heap[0] = heap[--size];
        int64_t i = 0;
        for (;;) {
            int64_t l = 2 * i + 1, r = l + 1, m = i;
            if (l < size && heap[l] > heap[m]) m = l;
            if (r < size && heap[r] > heap[m]) m = r;
            if (m == i) break;
            int64_t t = heap[m];
            heap[m] = heap[i];
            heap[i] = t;
            i = m;
        }
    }
    return stops;
}

static int64_t seed = 871;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t random_below(int64_t limit) {
    int64_t hi = next_random();
    int64_t lo = next_random();
    return (hi * 32768 + lo) % limit;
}

static int cmp_i64(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

int main(void) {
    int64_t total = 0, unreachable = 0, check = 0;
    int64_t pos[500], gain[500];
    for (int r = 0; r < 100; r++) {
        int64_t target = random_below(500000000) + 500000001;
        for (int i = 0; i < 500; i++) pos[i] = random_below(target - 1) + 1;
        qsort(pos, 500, sizeof(int64_t), cmp_i64);
        int64_t n = 0;
        for (int i = 0; i < 500; i++)
            if (n == 0 || pos[n - 1] != pos[i]) pos[n++] = pos[i];
        for (int64_t i = 0; i < n; i++) gain[i] = random_below(target / 40) + 1;
        for (int64_t j = 0; j < 400; j++) {
            int64_t a = min_refuel_stops(target, j * (target / 800) + 1, pos, gain, n);
            if (a < 0) unreachable++;
            else total += a;
            check = (check * 31 + a + 1) % 1000000007;
        }
    }
    printf("40000 trips over 100 lists of 500 stations: stops sum to %lld, %lld unreachable, checksum %lld\n",
           (long long)total, (long long)unreachable, (long long)check);
    return 0;
}
