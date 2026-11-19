// LeetCode #2332: The Latest Time to Catch a Bus -- the bench, the ★ arm
// in C. Both lists copied and sorted with `qsort`, the buses fill in
// order from the earliest passengers; the last bus's departure if it
// leaves with room, else its last passenger's time, then a step back
// past every passenger standing at the time tried. O((n + m) log(n + m)).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int ascending(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t latest_time_catch_the_bus(const int64_t *bus_in, int64_t n, const int64_t *pass_in, int64_t m, int64_t capacity) {
    int64_t *buses = malloc(sizeof(int64_t) * (size_t)n);
    int64_t *passengers = malloc(sizeof(int64_t) * (size_t)m);
    memcpy(buses, bus_in, sizeof(int64_t) * (size_t)n);
    memcpy(passengers, pass_in, sizeof(int64_t) * (size_t)m);
    qsort(buses, (size_t)n, sizeof(int64_t), ascending);
    qsort(passengers, (size_t)m, sizeof(int64_t), ascending);
    int64_t next = 0, aboard = 0;
    for (int64_t b = 0; b < n; b++) {
        aboard = 0;
        while (aboard < capacity && next < m && passengers[next] <= buses[b]) {
            aboard++;
            next++;
        }
    }
    int64_t latest = aboard < capacity ? buses[n - 1] : passengers[next - 1];
    int64_t k = next - 1;
    while (k >= 0 && passengers[k] == latest) {
        latest--;
        k--;
    }
    free(buses);
    free(passengers);
    return latest;
}

static int64_t scrambled(int64_t index) { return index * 2654435761LL % 2147483647LL + 2; }

int main(void) {
    static int64_t buses[10][50000], passengers[10][100000];
    for (int64_t k = 0; k < 10; k++) {
        int64_t base = k * 150000;
        for (int64_t i = 0; i < 50000; i++) buses[k][i] = scrambled(base + i);
        for (int64_t i = 0; i < 100000; i++) passengers[k][i] = scrambled(base + 50000 + i);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 5; p++)
        for (int64_t k = 0; k < 10; k++)
            check = (check * 31 + latest_time_catch_the_bus(buses[k], 50000, passengers[k], 100000, 1 + (k + p) % 5)) % 1000000007LL;
    printf("5 passes over 10 cases of 5*10^4 buses and 10^5 passengers: checksum %lld\n", (long long)check);
    return 0;
}
