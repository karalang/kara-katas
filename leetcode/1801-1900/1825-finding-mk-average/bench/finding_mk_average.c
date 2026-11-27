// LeetCode #1825: Finding MK Average -- the bench in C: the fenwick arm over
// 20 calls on windows of 1000 to 49999 numbers, each call adding the same 10^5
// numbers of 1 to 10^5, built once, and asking for the average after every
// hundredth; each window and its cut are drawn from the checksum so far. The
// Fenwick trees are the arm every mirror language writes the same way; the ★
// arm's ordered bags have no counterpart in C, Go or Python's standard
// library.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TOP 100000

typedef struct {
    int64_t m, k;
    int64_t *window; // a ring of m + 1 slots
    int64_t head, len;
    int64_t *count, *total;
} MkAverage;

static MkAverage mk_new(int64_t m, int64_t k) {
    MkAverage a = {m, k, malloc((size_t)(m + 1) * sizeof(int64_t)), 0, 0,
                   calloc(TOP + 1, sizeof(int64_t)), calloc(TOP + 1, sizeof(int64_t))};
    return a;
}

static void mk_free(MkAverage *a) {
    free(a->window);
    free(a->count);
    free(a->total);
}

static void change(MkAverage *a, int64_t x, int64_t by) {
    for (int64_t i = x; i <= TOP; i += i & -i) {
        a->count[i] += by;
        a->total[i] += by * x;
    }
}

// the sum of the t smallest numbers of the window
static int64_t smallest(const MkAverage *a, int64_t t) {
    int64_t at = 0, left = t, sum = 0;
    for (int64_t step = 1 << 16; step > 0; step /= 2) {
        if (at + step <= TOP && a->count[at + step] <= left) {
            at += step;
            left -= a->count[at];
            sum += a->total[at];
        }
    }
    return sum + left * (at + 1);
}

static void add_element(MkAverage *a, int64_t num) {
    a->window[(a->head + a->len) % (a->m + 1)] = num;
    a->len++;
    change(a, num, 1);
    if (a->len > a->m) {
        int64_t old = a->window[a->head];
        a->head = (a->head + 1) % (a->m + 1);
        a->len--;
        change(a, old, -1);
    }
}

static int64_t calculate_mk_average(const MkAverage *a) {
    if (a->len < a->m) return -1;
    return (smallest(a, a->m - a->k) - smallest(a, a->k)) / (a->m - 2 * a->k);
}

static int64_t seed = 1825;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t *nums = malloc(100000 * sizeof(int64_t));
    for (int64_t i = 0; i < 100000; i++) {
        int64_t hi = next_random();
        nums[i] = 1 + (hi * 32768 + next_random()) % 100000;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 20; call++) {
        int64_t m = 1000 + (check + call) % 49000;
        int64_t k = 1 + (check * 7 + call) % ((m - 1) / 2);
        MkAverage avg = mk_new(m, k);
        for (int64_t i = 0; i < 100000; i++) {
            add_element(&avg, nums[i]);
            if (i % 100 == 99) check = (check * 31 + calculate_mk_average(&avg) + 2) % 1000000007;
        }
        mk_free(&avg);
    }
    printf("20 calls: checksum %lld\n", (long long)check);
    free(nums);
    return 0;
}
