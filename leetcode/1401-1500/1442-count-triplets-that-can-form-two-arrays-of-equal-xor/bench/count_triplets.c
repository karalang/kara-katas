#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* The C mirror of count_triplets.kara: a fresh hash table for every array,
   open addressing over 1024 slots, as the Kara arm makes a fresh Map. The
   prefix xors of numbers below 1024 are below 1024 too. */
typedef struct {
    int32_t key;
    int used;
    int64_t times, places;
} Slot;

static int32_t count_triplets(const int32_t *arr, int n) {
    Slot *seen = calloc(1024, sizeof(Slot));
    uint32_t at = 0;
    seen[at].key = 0, seen[at].used = 1, seen[at].times = 1, seen[at].places = 0;
    int32_t x = 0;
    int64_t count = 0;
    for (int k = 0; k < n; k++) {
        x ^= arr[k];
        at = ((uint32_t)x * 2654435761u) >> 22;
        while (seen[at].used && seen[at].key != x) at = (at + 1) & 1023;
        int64_t times = seen[at].used ? seen[at].times : 0;
        int64_t places = seen[at].used ? seen[at].places : 0;
        count += times * k - places;
        seen[at].key = x, seen[at].used = 1, seen[at].times = times + 1, seen[at].places = places + k + 1;
    }
    free(seen);
    return (int32_t)count;
}

int main(void) {
    int64_t seed = 1442;
    static int32_t arrays[2000][300];
    for (int a = 0; a < 2000; a++)
        for (int i = 0; i < 300; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            arrays[a][i] = (int32_t)(1 + seed / 65536 % 1023);
        }
    int64_t check = 0;
    for (int r = 0; r < 50; r++)
        for (int a = 0; a < 2000; a++) check = (check * 131 + count_triplets(arrays[a], 300)) % 1000000007;
    printf("10^5 arrays of 300: checksum %lld\n", (long long)check);
    return 0;
}
