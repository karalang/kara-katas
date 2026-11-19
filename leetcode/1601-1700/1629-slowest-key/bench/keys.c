// LeetCode #1629: Slowest Key -- the bench's C mirror: the ★ arm on 1000
// random problems of 1000 presses, all drawn first, each answered 100
// times.

#include <stdint.h>
#include <stdio.h>

enum { PROBLEMS = 1000, N = 1000 };

static char slowest_key(const int32_t *release_times, const char *keys_pressed, int n) {
    int32_t previous = 0, best_time = 0;
    char best_key = 'a';
    for (int i = 0; i < n; i++) {
        int32_t time = release_times[i] - previous;
        char key = keys_pressed[i];
        if (time > best_time || (time == best_time && key > best_key)) {
            best_time = time;
            best_key = key;
        }
        previous = release_times[i];
    }
    return best_key;
}

static int64_t seed = 1629;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t release_times[PROBLEMS][N];
    static char keys_pressed[PROBLEMS][N + 1];
    for (int p = 0; p < PROBLEMS; p++) {
        int64_t time = 0;
        for (int i = 0; i < N; i++) {
            time += next_random() % 1000 + 1;
            release_times[p][i] = (int32_t)time;
            keys_pressed[p][i] = (char)('a' + next_random() % 26);
        }
    }
    int64_t check = 0;
    for (int r = 0; r < 100; r++) {
        for (int p = 0; p < PROBLEMS; p++) {
            char key = slowest_key(release_times[p], keys_pressed[p], N);
            check = (check * 31 + key) % 1000000007;
        }
    }
    printf("1000 problems of 1000 presses, answered 100 times: checksum %lld\n", (long long)check);
    return 0;
}
