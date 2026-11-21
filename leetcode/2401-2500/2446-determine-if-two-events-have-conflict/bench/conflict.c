// LeetCode #2446: Determine if Two Events Have Conflict -- the bench, the
// ★ arm: the four `HH:MM` strings compared as text.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int have_conflict(char **event1, char **event2) {
    return strcmp(event1[0], event2[1]) <= 0 && strcmp(event2[0], event1[1]) <= 0;
}

static int64_t seed = 2446;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *clock_text(int64_t minute) {
    char *s = malloc(6);
    snprintf(s, 6, "%02lld:%02lld", (long long)(minute / 60), (long long)(minute % 60));
    return s;
}

int main(void) {
    const int64_t n = 100000;
    char ***events = malloc(n * sizeof(char **));
    for (int64_t i = 0; i < n; i++) {
        int64_t a = next_random() % 1440;
        int64_t b = next_random() % 1440;
        events[i] = malloc(2 * sizeof(char *));
        events[i][0] = clock_text(a < b ? a : b);
        events[i][1] = clock_text(a < b ? b : a);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 300; p++)
        for (int64_t i = 0; i < n; i++) {
            int64_t j = (7 * i + p + 1) % n;
            int64_t answer = have_conflict(events[i], events[j]) ? 1 : 0;
            check = (check * 31 + answer + p) % 1000000007;
        }
    printf("300 passes over 10^5 events: checksum %lld\n", (long long)check);
    for (int64_t i = 0; i < n; i++) {
        free(events[i][0]);
        free(events[i][1]);
        free(events[i]);
    }
    free(events);
    return 0;
}
