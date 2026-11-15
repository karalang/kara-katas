// benchmark's C mirror of jumbled.kara (LeetCode #2191, the ★ arm), over
// a pointer and a length: (value, place) pairs sorted.

#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long long value;
    long long place;
} pair;

static long long mapped(const long long *mapping, long long n) {
    if (n == 0) return mapping[0];
    long long value = 0, place = 1;
    while (n > 0) {
        value += mapping[n % 10] * place;
        place *= 10;
        n /= 10;
    }
    return value;
}

static int by_pair(const void *a, const void *b) {
    const pair *x = a, *y = b;
    if (x->value != y->value) return x->value < y->value ? -1 : 1;
    return x->place < y->place ? -1 : (x->place > y->place);
}

static void sort_jumbled(const long long *mapping, const long long *nums, long long n, pair *keyed, long long *out) {
    for (long long i = 0; i < n; i++) {
        keyed[i].value = mapped(mapping, nums[i]);
        keyed[i].place = i;
    }
    qsort(keyed, n, sizeof(pair), by_pair);
    for (long long i = 0; i < n; i++) out[i] = nums[keyed[i].place];
}

static long long seed = 2191;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long big_random(void) {
    long long a = next_random();
    long long b = next_random();
    return a * 32768 + b;
}

int main(void) {
    long long *row = malloc(sizeof(long long) * 1000000);
    for (int i = 0; i < 1000000; i++) row[i] = big_random() % 1000000000;
    pair *keyed = malloc(sizeof(pair) * 30000);
    long long *out = malloc(sizeof(long long) * 30000);
    long long check = 0;
    for (int r = 0; r < 200; r++) {
        long long mapping[10];
        for (int d = 0; d < 10; d++) mapping[d] = d;
        for (int i = 9; i >= 1; i--) {
            long long j = next_random() % (i + 1);
            long long t = mapping[i];
            mapping[i] = mapping[j];
            mapping[j] = t;
        }
        long long start = big_random() % 970001;
        sort_jumbled(mapping, row + start, 30000, keyed, out);
        for (int i = 0; i < 30000; i++) check = (check * 31 + out[i] % 1000003) % 1000000007;
    }
    printf("200 solves: checksum %lld\n", check);
    free(row);
    free(keyed);
    free(out);
    return 0;
}
