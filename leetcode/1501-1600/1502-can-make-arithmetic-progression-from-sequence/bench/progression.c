// LeetCode #1502: Can Make Arithmetic Progression From Sequence -- the
// benchmark, the same algorithm as progression.kara: a copy sorted, every
// gap equal to the first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int can_make(const int64_t *arr, int64_t n) {
    int64_t *a = malloc(n * sizeof(int64_t));
    memcpy(a, arr, n * sizeof(int64_t));
    qsort(a, n, sizeof(int64_t), cmp);
    int64_t d = a[1] - a[0];
    int ok = 1;
    for (int64_t i = 1; i < n - 1; i++) {
        if (a[i + 1] - a[i] != d) { ok = 0; break; }
    }
    free(a);
    return ok;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static int64_t *random_array(int64_t most, int64_t *seed, int64_t *len) {
    int64_t n = next_random(seed) % (most - 1) + 2;
    int64_t kind = next_random(seed) % 3;
    int64_t *arr = malloc(n * sizeof(int64_t));
    if (kind == 2) {
        int64_t spread = next_random(seed) % 50 + 1;
        for (int64_t i = 0; i < n; i++) arr[i] = next_random(seed) % spread - spread / 2;
    } else {
        int64_t start = next_random(seed) % 2001 - 1000;
        int64_t d = next_random(seed) % 21 - 10;
        for (int64_t i = 0; i < n; i++) arr[i] = start + i * d;
        if (kind == 1) {
            int64_t at = next_random(seed) % n;
            arr[at] += next_random(seed) % 2 == 0 ? 1 : -1;
        }
    }
    for (int64_t i = n - 1; i >= 1; i--) {
        int64_t j = next_random(seed) % (i + 1);
        int64_t t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    *len = n;
    return arr;
}

int main(void) {
    int64_t seed = 1502;
    int64_t *arrays[3000], lens[3000];
    for (int i = 0; i < 3000; i++) arrays[i] = random_array(1000, &seed, &lens[i]);
    int64_t can = 0, check = 0;
    for (int r = 0; r < 10; r++) {
        for (int i = 0; i < 3000; i++) {
            int64_t answer = can_make(arrays[i], lens[i]);
            can += answer;
            check = mix(check, answer);
        }
    }
    printf("30000 answers over 3000 arrays of 2 to 1000 numbers: %lld can, checksum %lld\n",
           (long long)can, (long long)check);
    for (int i = 0; i < 3000; i++) free(arrays[i]);
    return 0;
}
