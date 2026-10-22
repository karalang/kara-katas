// Benchmark for #853: Car Fleet -- C twin of the Kāra ★ arm (closest to
// the target first).
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct { int64_t p, s; } Car;

static int cmp_car(const void *x, const void *y) {
    const Car *a = x, *b = y;
    if (a->p != b->p) return (a->p > b->p) - (a->p < b->p);
    return (a->s > b->s) - (a->s < b->s);
}

static int64_t car_fleet(int64_t target, const int64_t *position, const int64_t *speed, int64_t n) {
    Car *cars = malloc(sizeof(Car) * n);
    for (int64_t i = 0; i < n; i++) cars[i] = (Car){position[i], speed[i]};
    qsort(cars, n, sizeof(Car), cmp_car);
    int64_t fleets = 0, far = 0, fast = 1;
    for (int64_t i = n - 1; i >= 0; i--) {
        int64_t p = cars[i].p, s = cars[i].s;
        if ((target - p) * fast > far * s) {
            fleets++;
            far = target - p;
            fast = s;
        }
    }
    free(cars);
    return fleets;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

#define N 100000
#define TARGET 1000000

int main(void) {
    const int64_t count = 64, rounds = 150, n = N, target = TARGET;
    int64_t seed = 853;
    static int64_t positions[64][N], speeds[64][N];
    static unsigned char taken[TARGET];
    for (int64_t g = 0; g < count; g++) {
        int64_t top = 1 + (g % 8) * 142857;
        for (int64_t i = 0; i < target; i++) taken[i] = 0;
        int64_t m = 0;
        while (m < n) {
            int64_t p = (next_random(&seed) * 32768 + next_random(&seed)) % target;
            if (!taken[p]) {
                taken[p] = 1;
                positions[g][m++] = p;
            }
        }
        for (int64_t i = 0; i < n; i++) speeds[g][i] = 1 + (next_random(&seed) * 32768 + next_random(&seed)) % top;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t g = round % count;
        int64_t f = car_fleet(target, positions[g], speeds[g], n);
        total += f;
        checksum = (checksum * 31 + f) % 1000000007;
    }
    printf("%lld rounds of %lld roads: fleets sum to %lld, checksum %lld\n", (long long)rounds, (long long)count,
           (long long)total, (long long)checksum);
    return 0;
}
