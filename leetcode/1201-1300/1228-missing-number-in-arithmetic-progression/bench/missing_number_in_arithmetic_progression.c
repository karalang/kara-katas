// LeetCode #1228 bench: the ★ arm in C, over the same 2000 random
// progressions and 2000 passes as the Kāra bench.
#include <stdio.h>
#include <stdlib.h>

static long missing_number(const long *arr, long n) {
    long step = (arr[n - 1] - arr[0]) / n;
    long lo = 0, hi = n - 1;
    while (lo < hi) {
        long mid = (lo + hi) / 2;
        if (arr[mid] == arr[0] + mid * step)
            lo = mid + 1;
        else
            hi = mid;
    }
    return arr[0] + lo * step;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    long seed = 1228;
    long *arrays = malloc(sizeof(long) * 2000 * 1000);
    for (int a = 0; a < 2000; a++) {
        long first = next_random(&seed) % 100001;
        long low = -(first / 1000);
        long high = (100000 - first) / 1000;
        long step = low + next_random(&seed) % (high - low + 1);
        long gone = next_random(&seed) % 999 + 1;
        long *arr = arrays + (long)a * 1000;
        int k = 0;
        for (long i = 0; i < 1001; i++)
            if (i != gone) arr[k++] = first + i * step;
    }
    long check = 0;
    for (int pass = 0; pass < 2000; pass++)
        for (int a = 0; a < 2000; a++)
            check = (check * 131 + missing_number(arrays + (long)a * 1000, 1000)) % 1000000007;
    printf("2000 progressions of 1000 values, 2000 passes: checksum %ld\n", check);
    free(arrays);
    return 0;
}
