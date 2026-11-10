// LeetCode #2079: Watering Plants -- C mirror of the ★ arm's benchmark
// (water.kara): 2000 gardens of 1000 plants built first, then every
// garden answered for 500 cans, from 1000 up by 97 a can.
#include <stdio.h>
#include <stdlib.h>

static long long seed = 2079;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long watering_plants(const long long *plants, long long n, long long capacity) {
    long long steps = 0, can = capacity;
    for (long long i = 0; i < n; i++) {
        if (can < plants[i]) {
            steps += 2 * i;
            can = capacity;
        }
        steps += 1;
        can -= plants[i];
    }
    return steps;
}

int main(void) {
    long long *gardens = malloc(sizeof(long long) * 2000 * 1000);
    for (int g = 0; g < 2000; g++)
        for (int i = 0; i < 1000; i++) gardens[1000 * g + i] = next_random() % 1000 + 1;
    long long total = 0, check = 0;
    for (int g = 0; g < 2000; g++)
        for (int k = 0; k < 500; k++) {
            long long a = watering_plants(gardens + 1000 * g, 1000, 1000 + 97 * k);
            total += a;
            check = (check * 31 + a) % 1000000007;
        }
    printf("1000000 answers: sum %lld, checksum %lld\n", total, check);
    free(gardens);
    return 0;
}
