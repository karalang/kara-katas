// LeetCode #2170: Minimum Operations to Make the Array Alternating -- the
// benchmark's C mirror of alternating.kara, over a pointer and a length,
// each side counted in an open-addressing hash table.

#include <stdio.h>
#include <stdlib.h>

#define CAP 131072

typedef struct { long long key, count; } Slot;

static void top_two(const long long *nums, long long n, long long start,
                    long long first[2], long long second[2]) {
    Slot *table = calloc(CAP, sizeof(Slot));
    for (long long i = start; i < n; i += 2) {
        unsigned long long h = (unsigned long long)nums[i] * 0x9E3779B97F4A7C15ULL;
        long long s = (long long)(h >> 47);
        while (table[s].key != 0 && table[s].key != nums[i]) s = (s + 1) & (CAP - 1);
        table[s].key = nums[i];
        table[s].count += 1;
    }
    first[0] = first[1] = second[0] = second[1] = 0;
    for (long long s = 0; s < CAP; s++) {
        if (table[s].key == 0) continue;
        long long count = table[s].count;
        if (count > first[1]) {
            second[0] = first[0]; second[1] = first[1];
            first[0] = table[s].key; first[1] = count;
        } else if (count > second[1]) {
            second[0] = table[s].key; second[1] = count;
        }
    }
    free(table);
}

static long long minimum_operations(const long long *nums, long long n) {
    long long ef[2], es[2], of[2], os[2];
    top_two(nums, n, 0, ef, es);
    top_two(nums, n, 1, of, os);
    if (ef[0] != of[0]) return n - ef[1] - of[1];
    long long a = ef[1] + os[1], b = es[1] + of[1];
    return n - (a > b ? a : b);
}

static long long seed = 2170;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    long long *row = malloc(400000 * sizeof(long long));
    for (int i = 0; i < 400000; i++) {
        long long a = next_random();
        long long b = next_random();
        row[i] = (a * 32768 + b) % 1000 + 1;
    }
    long long check = 0;
    for (int r = 0; r < 100; r++) {
        long long a = next_random();
        long long b = next_random();
        long long start = (a * 32768 + b) % 300001;
        long long ops = minimum_operations(row + start, 100000);
        check = (check * 31 + ops) % 1000000007;
    }
    printf("100 solves: checksum %lld\n", check);
    free(row);
    return 0;
}
