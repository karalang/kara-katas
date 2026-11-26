// LeetCode #1764: Form Array by Concatenating Subarrays of Another Array --
// the bench in C, mirroring can_choose.kara: greedy, each group matched at
// the first place it fits, compared value by value.
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct { int *v; int len; } Group;
typedef struct { Group groups[10]; int k; int *nums; int n; } Case;

static bool can_choose(const Group *groups, int k, const int *nums, int n) {
    int at = 0;
    for (int g = 0; g < k; g++) {
        int len = groups[g].len;
        for (;;) {
            if (at + len > n) return false;
            bool same = true;
            for (int i = 0; i < len; i++) {
                if (nums[at + i] != groups[g].v[i]) { same = false; break; }
            }
            if (same) break;
            at++;
        }
        at += len;
    }
    return true;
}

static long long seed = 1764;
static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void random_case(Case *c, int k, int most, int values, int gap, bool break_one) {
    c->k = k;
    c->nums = malloc(sizeof(int) * k * (gap + most));
    c->n = 0;
    for (int j = 0; j < k; j++) {
        int filler = next_random() % (gap + 1);
        for (int i = 0; i < filler; i++) c->nums[c->n++] = next_random() % values;
        int len = 1 + next_random() % most;
        int *g = malloc(sizeof(int) * len);
        for (int i = 0; i < len; i++) g[i] = next_random() % values;
        for (int i = 0; i < len; i++) c->nums[c->n++] = g[i];
        c->groups[j].v = g;
        c->groups[j].len = len;
    }
    if (break_one) {
        int g = next_random() % k;
        int at = next_random() % c->groups[g].len;
        c->groups[g].v[at] = next_random() % values;
    }
}

int main(void) {
    static Case cases[200];
    for (int i = 0; i < 200; i++) random_case(&cases[i], 10, 40, 2, 60, i % 2 == 1);
    long long check = 0;
    for (long long call = 0; call < 200000; call++) {
        Case *c = &cases[(check + call * 7919) % 200];
        check = (check * 31 + (can_choose(c->groups, c->k, c->nums, c->n) ? 1 : 0) + call % 7) % 1000000007;
    }
    printf("200000 calls over 200 cases: checksum %lld\n", check);
    return 0;
}
