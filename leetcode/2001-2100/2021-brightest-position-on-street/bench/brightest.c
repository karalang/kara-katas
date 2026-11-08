// LeetCode #2021: Brightest Position on Street -- the ★ arm's benchmark, a
// mirror of brightest.kara: the events built and sorted per call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t at, delta;
} Event;

static int by_pair(const void *a, const void *b) {
    const Event *x = a, *y = b;
    if (x->at != y->at) return x->at < y->at ? -1 : 1;
    return (x->delta > y->delta) - (x->delta < y->delta);
}

static int64_t brightest_position(const int64_t (*lights)[2], size_t n) {
    Event *events = malloc(2 * n * sizeof(Event));
    for (size_t i = 0; i < n; i++) {
        events[2 * i] = (Event){lights[i][0] - lights[i][1], 1};
        events[2 * i + 1] = (Event){lights[i][0] + lights[i][1] + 1, -1};
    }
    qsort(events, 2 * n, sizeof(Event), by_pair);
    int64_t brightness = 0, best = 0, answer = 0;
    size_t i = 0;
    while (i < 2 * n) {
        int64_t at = events[i].at;
        while (i < 2 * n && events[i].at == at) {
            brightness += events[i].delta;
            i++;
        }
        if (brightness > best) {
            best = brightness;
            answer = at;
        }
    }
    free(events);
    return answer;
}

static int64_t seed = 2021;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int64_t streets[100][10000][2];
    const int64_t spreads[3] = {1000000, 10000000, 100000000};
    const int64_t reaches[3] = {1000, 100000, 1000000};
    for (int s = 0; s < 100; s++) {
        int64_t spread = spreads[s % 3], reach = reaches[s % 3];
        for (int i = 0; i < 10000; i++) {
            int64_t hi = next_random();
            int64_t lo = next_random();
            streets[s][i][0] = (hi * 32768 + lo) % (2 * spread + 1) - spread;
            streets[s][i][1] = next_random() % (reach + 1);
        }
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int r = 0; r < 5; r++) {
        for (int s = 0; s < 100; s++) {
            int64_t answer = brightest_position((const int64_t(*)[2])streets[s], 10000);
            calls++;
            sum += answer;
            check = (check * 31 + answer + 1000000000) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
