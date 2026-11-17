// LeetCode #2215: Find the Difference of Two Arrays -- bench mirror of
// difference.kara: each array put in a hash set (open addressing, linear
// probing), and each list the numbers of one set the other lacks.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAP 4096
typedef struct {
    long keys[CAP];
    char used[CAP];
} Set;

static unsigned long hash(long x) {
    unsigned long h = (unsigned long)x * 0x9E3779B97F4A7C15UL;
    return h >> 52;
}

static void set_clear(Set *s) { memset(s->used, 0, CAP); }

static void set_insert(Set *s, long x) {
    unsigned long i = hash(x);
    while (s->used[i]) {
        if (s->keys[i] == x) return;
        i = (i + 1) & (CAP - 1);
    }
    s->used[i] = 1;
    s->keys[i] = x;
}

static int set_contains(const Set *s, long x) {
    unsigned long i = hash(x);
    while (s->used[i]) {
        if (s->keys[i] == x) return 1;
        i = (i + 1) & (CAP - 1);
    }
    return 0;
}

static Set first, second;

// the two lists into out0/out1, their lengths into n0/n1
static void find_difference(const long *nums1, long n1, const long *nums2, long n2, long *out0, long *len0, long *out1, long *len1) {
    set_clear(&first);
    set_clear(&second);
    for (long i = 0; i < n1; i++) set_insert(&first, nums1[i]);
    for (long i = 0; i < n2; i++) set_insert(&second, nums2[i]);
    *len0 = *len1 = 0;
    for (long i = 0; i < CAP; i++)
        if (first.used[i] && !set_contains(&second, first.keys[i])) out0[(*len0)++] = first.keys[i];
    for (long i = 0; i < CAP; i++)
        if (second.used[i] && !set_contains(&first, second.keys[i])) out1[(*len1)++] = second.keys[i];
}

static long seed = 2215;
static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static long a[200][1000], b[200][1000];

int main(void) {
    long spreads[3] = {30, 300, 1000};
    for (int p = 0; p < 200; p++) {
        // 1000 numbers each, spread over -30..30, -300..300 and -1000..1000
        long spread = spreads[p % 3];
        for (int i = 0; i < 1000; i++) a[p][i] = next_random() % (2 * spread + 1) - spread;
        for (int i = 0; i < 1000; i++) b[p][i] = next_random() % (2 * spread + 1) - spread;
    }
    static long out0[1000], out1[1000];
    long check = 0;
    for (int p = 0; p < 200; p++) {
        for (int r = 0; r < 10; r++) {
            // punch: one number of the first array moves before each answer
            a[p][r * 97] = (a[p][r * 97] + 1001) % 2001 - 1000;
            long n0, n1;
            find_difference(a[p], 1000, b[p], 1000, out0, &n0, out1, &n1);
            // the lists come in any order: their lengths and sums do not
            long s0 = 0, s1 = 0;
            for (long i = 0; i < n0; i++) s0 += out0[i];
            for (long i = 0; i < n1; i++) s1 += out1[i];
            check = (check * 31 + n0) % 1000000007;
            check = (check * 31 + s0 + 1000000) % 1000000007;
            check = (check * 31 + n1) % 1000000007;
            check = (check * 31 + s1 + 1000000) % 1000000007;
        }
    }
    printf("200 pairs of 1000, 10 punches: checksum %ld\n", check);
    return 0;
}
