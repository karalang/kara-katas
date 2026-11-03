// Benchmark lane for LeetCode 1041 -- C mirror of robot_bounded.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int is_robot_bounded(const char *s, int64_t n) {
    int64_t x = 0, y = 0;
    // north, east, south, west
    int64_t facing = 0;
    for (int64_t i = 0; i < n; i++) {
        char c = s[i];
        if (c == 'G') {
            if (facing == 0) y += 1;
            else if (facing == 1) x += 1;
            else if (facing == 2) y -= 1;
            else x -= 1;
        } else if (c == 'L') {
            facing = (facing + 3) % 4;
        } else {
            facing = (facing + 1) % 4;
        }
    }
    return (x == 0 && y == 0) || facing != 0;
}

static int64_t seed = 1041;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 2000, size = 100, rounds = 500;
    const char letters[3] = {'G', 'L', 'R'};
    char *strings = malloc(count * size);
    for (int64_t k = 0; k < count; k++) {
        for (int64_t i = 0; i < size; i++) {
            int64_t r = next_random() % 10;
            char c;
            if (k % 2 == 0) c = letters[r % 3];
            else if (r < 8) c = 'G';
            else if (r == 8) c = 'L';
            else c = 'R';
            strings[k * size + i] = c;
        }
    }
    int64_t bounded = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t k = 0; k < count; k++) {
            int answer = is_robot_bounded(strings + k * size, size);
            if (answer) bounded += 1;
            check = (check * 131 + (answer ? 2 : 1)) % 1000000007;
        }
    }
    printf("%lld strings of %lld instructions, %lld rounds: %lld bounded, checksum %lld\n", (long long)count,
           (long long)size, (long long)rounds, (long long)bounded, (long long)check);
    free(strings);
    return 0;
}
