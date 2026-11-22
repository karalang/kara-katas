// LeetCode #2848: Points That Intersect With Cars -- the bench,
// mirrored from points.kara: each car marks its points on a road of
// 100, and the marked ones are counted.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t number_of_points(const int64_t *cars, long n) {
    bool covered[101] = {false};
    for (long i = 0; i < n; i++)
        for (int64_t x = cars[2 * i]; x <= cars[2 * i + 1]; x++) covered[x] = true;
    int64_t count = 0;
    for (int x = 0; x < 101; x++)
        if (covered[x]) count++;
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const long count = 10000, rounds = 50;
    int64_t seed = 2848;
    int64_t *cars = malloc(count * 100 * 2 * sizeof(int64_t));
    long *starts = malloc(count * sizeof(long)), *lens = malloc(count * sizeof(long));
    long at = 0;
    for (long c = 0; c < count; c++) {
        long n = next_random(&seed) % 100 + 1;
        starts[c] = at;
        lens[c] = n;
        for (long i = 0; i < n; i++) {
            int64_t start = next_random(&seed) % 100 + 1;
            int64_t a = next_random(&seed);
            int64_t length = a % (next_random(&seed) % 100 + 1);
            int64_t end = start + length < 100 ? start + length : 100;
            cars[2 * at] = start;
            cars[2 * at + 1] = end;
            at++;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (long c = 0; c < count; c++) {
            int64_t points = number_of_points(cars + 2 * starts[c], lens[c]);
            total += points;
            check = (check * 31 + points + r) % 1000000007;
        }
    }
    printf("%ld parkings, %ld rounds: %lld points, checksum %lld\n", count, rounds, (long long)total, (long long)check);
    free(cars);
    free(starts);
    free(lens);
    return 0;
}
