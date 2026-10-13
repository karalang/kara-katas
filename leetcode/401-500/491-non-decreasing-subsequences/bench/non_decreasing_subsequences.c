// Benchmark for #491: C mirror of the ★ arm (backtracking); see
// non_decreasing_subsequences.kara. C has no hash set, so the values tried
// at one depth (at most 15) are kept in an array and scanned. The answers
// go into one growing buffer of numbers, with each answer's length kept
// alongside.
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long long *vals, *lens;
    long long nvals, nlens, capvals, caplens;
} Out;

static void out_push(Out *o, const long long *current, long long len) {
    if (o->nvals + len > o->capvals) {
        o->capvals = o->capvals * 2 + len;
        o->vals = realloc(o->vals, sizeof(long long) * o->capvals);
    }
    if (o->nlens == o->caplens) {
        o->caplens = o->caplens * 2 + 1;
        o->lens = realloc(o->lens, sizeof(long long) * o->caplens);
    }
    for (long long k = 0; k < len; k++) {
        o->vals[o->nvals++] = current[k];
    }
    o->lens[o->nlens++] = len;
}

static void extend(const long long *nums, long long n, long long from, long long *current,
                   long long len, Out *out) {
    if (len >= 2) {
        out_push(out, current, len);
    }
    long long tried[16];
    long long ntried = 0;
    for (long long i = from; i < n; i++) {
        int seen = 0;
        for (long long t = 0; t < ntried; t++) {
            if (tried[t] == nums[i]) {
                seen = 1;
                break;
            }
        }
        if (seen) {
            continue;
        }
        if (len == 0 || nums[i] >= current[len - 1]) {
            tried[ntried++] = nums[i];
            current[len] = nums[i];
            extend(nums, n, i + 1, current, len + 1, out);
        }
    }
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 3000 arrays of 15 numbers, the k-th from k / 2 to k / 2 + 3, so
    // they mostly rise, built once, then each solved once.
    static long long arrays[3000][15];
    long long seed = 491;
    for (int a = 0; a < 3000; a++) {
        for (long long k = 0; k < 15; k++) {
            arrays[a][k] = k / 2 + next_random(&seed) % 4;
        }
    }
    long long total = 0, checksum = 0;
    for (int a = 0; a < 3000; a++) {
        Out out = {0};
        long long current[16];
        extend(arrays[a], 15, 0, current, 0, &out);
        total += out.nlens;
        long long at = 0;
        for (long long s = 0; s < out.nlens; s++) {
            for (long long k = 0; k < out.lens[s]; k++) {
                checksum = (checksum * 31 + out.vals[at++] + 7) % 1000000007;
            }
            checksum = (checksum * 31 + 15) % 1000000007;
        }
        free(out.vals);
        free(out.lens);
    }
    printf("3000 arrays of 15: %lld subsequences, checksum %lld\n", total, checksum);
    return 0;
}
