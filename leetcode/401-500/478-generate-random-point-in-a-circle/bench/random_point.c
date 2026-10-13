// Benchmark for #478: C mirror of the ★ arm (darts at the square); see
// random_point.kara.
#include <stdio.h>

typedef struct {
    long long seed;
} Uniform;

static long long step(Uniform *u) {
    u->seed = (u->seed * 1103515245 + 12345) % 2147483648LL;
    return u->seed / 65536;
}

static double next(Uniform *u) {
    long long high = step(u);
    long long low = step(u);
    return (double)(high * 32768 + low) / 1073741824.0;
}

typedef struct {
    double radius, x_center, y_center;
    Uniform rng;
} Solution;

static void rand_point(Solution *s, double *px, double *py) {
    for (;;) {
        double x = 2.0 * next(&s->rng) - 1.0;
        double y = 2.0 * next(&s->rng) - 1.0;
        if (x * x + y * y <= 1.0) {
            *px = s->x_center + s->radius * x;
            *py = s->y_center + s->radius * y;
            return;
        }
    }
}

int main(void) {
    int n = 20000000;
    Solution solution = {10000.0, 20000.0, 30000.0, {478}};
    long long right = 0, checksum = 0;
    for (int i = 0; i < n; i++) {
        double x, y;
        rand_point(&solution, &x, &y);
        if (x > 20000.0) {
            right++;
        }
        checksum = (checksum * 31 + (long long)(x * 1000.0) + (long long)(y * 1000.0)) % 1000000007;
    }
    printf("%d points: %lld right of the centre, checksum %lld\n", n, right, checksum);
    return 0;
}
