// LeetCode #1713: Minimum Operations to Make a Subsequence -- the C mirror
// of the bench (operations.kara): a hash map of the target's places and
// the smallest tail of each rising run, found by binary search, on 20
// random problems of 100000 values, each answered 5 times.
//
// C has no map: this one is open addressing with linear probing, keys
// hashed by a multiply, a table of 2^18 slots made for each answer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS (1 << 18)

typedef struct {
    int32_t key;
    int used;
    long place;
} Slot;

static size_t slot_of(const Slot *table, int32_t key) {
    size_t i = (size_t)(((uint32_t)key * 2654435769u) >> 14);
    while (table[i].used && table[i].key != key) {
        i = (i + 1) & (SLOTS - 1);
    }
    return i;
}

static int min_operations(const int32_t *target, long m, const int32_t *arr, long n) {
    Slot *place = calloc(SLOTS, sizeof(Slot));
    for (long i = 0; i < m; i++) {
        size_t s = slot_of(place, target[i]);
        place[s].used = 1;
        place[s].key = target[i];
        place[s].place = i;
    }
    long *tails = malloc(sizeof(long) * (m + 1));
    long len = 0;
    for (long k = 0; k < n; k++) {
        size_t s = slot_of(place, arr[k]);
        if (!place[s].used) {
            continue;
        }
        long p = place[s].place;
        long lo = 0;
        long hi = len;
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            if (tails[mid] < p) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        tails[lo] = p;
        if (lo == len) {
            len++;
        }
    }
    free(tails);
    free(place);
    return (int)(m - len);
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static long long wide(long long *seed) {
    long long a = next_random(seed);
    return a * 32768 + next_random(seed);
}

int main(void) {
    const int count = 20;
    const long long rounds = 5;
    const long n = 100000;
    long long seed = 1713;
    int32_t *targets = malloc(sizeof(int32_t) * count * n);
    int32_t *arrs = malloc(sizeof(int32_t) * count * n);
    for (int p = 0; p < count; p++) {
        int32_t *target = targets + p * n;
        for (long i = 0; i < n; i++) {
            target[i] = (int32_t)i;
        }
        for (long i = n - 1; i >= 1; i--) {
            long j = (long)(wide(&seed) % (i + 1));
            int32_t t = target[i];
            target[i] = target[j];
            target[j] = t;
        }
        for (long i = 0; i < n; i++) {
            target[i] = target[i] * 10000 + (int32_t)(next_random(&seed) % 10000);
        }
        int32_t *arr = arrs + p * n;
        for (long i = 0; i < n; i++) {
            if (next_random(&seed) % 2 == 0) {
                arr[i] = target[wide(&seed) % n];
            } else {
                arr[i] = (int32_t)(wide(&seed) % 1000000000);
            }
        }
    }
    long long sum = 0;
    long long check = 0;
    for (long long r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            long long answer = min_operations(targets + p * n, n, arrs + p * n, n);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of %ld values, %lld rounds: answers sum to %lld, checksum %lld\n", count, n, rounds, sum, check);
    free(targets);
    free(arrs);
    return 0;
}
