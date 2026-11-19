// LeetCode #1649: Create Sorted Array through Instructions -- the bench's
// C mirror: the ★ arm on 60 random lists of 100000 instructions from 1 to
// 100000, all drawn first. The tree is allocated per call, as the other
// languages do.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LISTS 60
#define N 100000
#define MOD 1000000007LL

static int64_t prefix(const int64_t *tree, int64_t v) {
    int64_t total = 0;
    for (int64_t i = v; i > 0; i -= i & -i) total += tree[i];
    return total;
}

static int32_t create_sorted_array(const int32_t *instructions, size_t n) {
    int64_t top = 0;
    for (size_t i = 0; i < n; i++)
        if (instructions[i] > top) top = instructions[i];
    int64_t *tree = calloc((size_t)top + 1, sizeof *tree);
    int64_t cost = 0;
    for (size_t inserted = 0; inserted < n; inserted++) {
        int64_t v = instructions[inserted];
        int64_t less = prefix(tree, v - 1);
        int64_t greater = (int64_t)inserted - prefix(tree, v);
        cost = (cost + (less < greater ? less : greater)) % MOD;
        for (int64_t i = v; i <= top; i += i & -i) tree[i] += 1;
    }
    free(tree);
    return (int32_t)cost;
}

static int64_t seed = 1649;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t lists[LISTS][N];
    for (int l = 0; l < LISTS; l++)
        for (int i = 0; i < N; i++) lists[l][i] = (int32_t)(next_random() % 100000 + 1);
    int64_t check = 0, total = 0;
    for (int l = 0; l < LISTS; l++) {
        int64_t cost = create_sorted_array(lists[l], N);
        total += cost;
        check = (check * 31 + cost + 1) % 1000000007;
    }
    printf("60 lists of 100000 instructions: costs sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
