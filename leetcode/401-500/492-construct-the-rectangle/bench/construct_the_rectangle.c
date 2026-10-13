// Benchmark for #492: C mirror of the ★ arm (down from the square root);
// see construct_the_rectangle.kara.
#include <math.h>
#include <stdio.h>

#define COUNT 200000

static void construct_rectangle(long long area, long long sides[2]) {
    long long width = (long long)sqrt((double)area);
    while (width * width > area) {
        width--;
    }
    while ((width + 1) * (width + 1) <= area) {
        width++;
    }
    while (area % width != 0) {
        width--;
    }
    sides[0] = area / width;
    sides[1] = width;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 200,000 random areas from 1 to ten million, built once, then each
    // solved once.
    static long long areas[COUNT];
    long long seed = 492;
    for (int i = 0; i < COUNT; i++) {
        long long high = next_random(&seed);
        areas[i] = 1 + (high * 32768 + next_random(&seed)) % 10000000;
    }
    long long squares = 0, thin = 0, checksum = 0;
    for (int i = 0; i < COUNT; i++) {
        long long sides[2];
        construct_rectangle(areas[i], sides);
        if (sides[0] == sides[1]) {
            squares++;
        }
        if (sides[1] == 1) {
            thin++;
        }
        checksum = (checksum * 31 + sides[0] - sides[1]) % 1000000007;
    }
    printf("200000 areas: %lld squares, %lld of width 1, checksum %lld\n", squares, thin, checksum);
    return 0;
}
