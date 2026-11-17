// benchmark's C mirror of collisions.kara (LeetCode #2211, the ★ arm):
// skip the leading 'L's and the trailing 'R's and count the cars between
// that are not 'S'. The cars are copied out first, as the other mirrors
// collect them.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t count_collisions(const char *directions) {
    long n = (long)strlen(directions);
    char *cars = malloc(n);
    memcpy(cars, directions, n);
    long lo = 0;
    while (lo < n && cars[lo] == 'L') lo++;
    long hi = n;
    while (hi > lo && cars[hi - 1] == 'R') hi--;
    int64_t count = 0;
    for (long i = lo; i < hi; i++)
        if (cars[i] != 'S') count++;
    free(cars);
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2211;
    const char letters[3] = {'L', 'R', 'S'};
    char *roads[20];
    for (long r = 0; r < 20; r++) {
        // a run of left-movers at the front and right-movers at the back,
        // each r thousand cars long, around random cars
        roads[r] = malloc(100001);
        for (long i = 0; i < 100000; i++) {
            if (i < r * 1000) roads[r][i] = 'L';
            else if (i >= 100000 - r * 1000) roads[r][i] = 'R';
            else roads[r][i] = letters[next_random(&seed) % 3];
        }
        roads[r][100000] = 0;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++)
        for (long r = 0; r < 20; r++) check = (check * 31 + count_collisions(roads[r]) + p) % 1000000007;
    printf("10 passes over 20 roads: checksum %lld\n", (long long)check);
    for (long r = 0; r < 20; r++) free(roads[r]);
    return 0;
}
