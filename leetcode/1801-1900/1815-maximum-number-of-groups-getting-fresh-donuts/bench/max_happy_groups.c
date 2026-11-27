// LeetCode #1815: Maximum Number of Groups Getting Fresh Donuts -- the
// bench in C: the ★ arm over 3000 cases of 30 groups at a batch of 7 to 9,
// each group's remainder drawn from the batch's lower half, so that no two
// groups pair off and the search meets the most states. The memo is an
// open-addressing hash table keyed by the counts in base 31.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define CAP (1 << 15)

static int64_t keys[CAP];
static int64_t vals[CAP];
static char used[CAP];

static uint64_t mix(uint64_t k) {
    k ^= k >> 33;
    k *= 0xff51afd7ed558ccdULL;
    k ^= k >> 33;
    k *= 0xc4ceb9fe1a85ec53ULL;
    k ^= k >> 33;
    return k;
}

static int64_t best(int64_t b, int64_t *count, int64_t left) {
    int64_t key = 0;
    for (int64_t r = b - 1; r >= 1; r--)
        key = key * 31 + count[r];
    size_t at = mix((uint64_t)key) & (CAP - 1);
    while (used[at] && keys[at] != key)
        at = (at + 1) & (CAP - 1);
    if (used[at])
        return vals[at];
    int64_t top = 0;
    int any = 0;
    for (int64_t r = 1; r < b; r++) {
        if (count[r] > 0) {
            any = 1;
            count[r]--;
            int64_t got = best(b, count, (left + r) % b);
            if (got > top)
                top = got;
            count[r]++;
        }
    }
    if (any && left == 0)
        top++;
    at = mix((uint64_t)key) & (CAP - 1);
    while (used[at] && keys[at] != key)
        at = (at + 1) & (CAP - 1);
    used[at] = 1;
    keys[at] = key;
    vals[at] = top;
    return top;
}

static int64_t max_happy_groups(int64_t b, const int64_t *groups, int n) {
    int64_t count[9] = {0};
    for (int i = 0; i < n; i++)
        count[groups[i] % b]++;
    int64_t happy = count[0];
    count[0] = 0;
    for (int64_t r = 1; r < b; r++) {
        int64_t s = b - r;
        if (r < s) {
            int64_t k = count[r] < count[s] ? count[r] : count[s];
            happy += k;
            count[r] -= k;
            count[s] -= k;
        } else if (r == s) {
            happy += count[r] / 2;
            count[r] %= 2;
        }
    }
    memset(used, 0, sizeof used);
    return happy + best(b, count, 0);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1815;
    int64_t check = 0;
    int64_t groups[30];
    for (int c = 0; c < 3000; c++) {
        int64_t b = 7 + next_random(&seed) % 3;
        for (int k = 0; k < 30; k++) {
            int64_t whole = next_random(&seed) * b;
            groups[k] = whole + 1 + next_random(&seed) % ((b - 1) / 2);
        }
        check = (check * 31 + max_happy_groups(b, groups, 30)) % 1000000007;
    }
    printf("3000 cases: checksum %lld\n", (long long)check);
    return 0;
}
