// LeetCode #2791: Count Paths That Can Form a Palindrome in a Tree -- the
// bench in C: the ★ arm over 20 random trees of 10^5 nodes with letters
// from a to z, all drawn first, then each answered 5 times. The masks
// seen are counted in an open-addressing hash table, C having no map.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define COUNT 20
#define N 100000
#define SLOTS 262144

static int64_t seed = 2791;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t keys[SLOTS], counts[SLOTS];
static char used[SLOTS];

static uint64_t slot_of(int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    uint64_t i = h >> 46;
    while (used[i] && keys[i] != key) i = (i + 1) & (SLOTS - 1);
    return i;
}

static int64_t get(int64_t key) {
    uint64_t i = slot_of(key);
    return used[i] ? counts[i] : 0;
}

static void add(int64_t key) {
    uint64_t i = slot_of(key);
    if (!used[i]) { used[i] = 1; keys[i] = key; counts[i] = 0; }
    counts[i]++;
}

static int64_t head[N], next_child[N], mask[N], todo[N];

static int64_t count_palindrome_paths(const int64_t *parent, const char *s, int64_t n) {
    for (int64_t i = 0; i < n; i++) head[i] = -1;
    for (int64_t i = n - 1; i >= 1; i--) {
        next_child[i] = head[parent[i]];
        head[parent[i]] = i;
    }
    int64_t top = 0;
    mask[0] = 0;
    todo[top++] = 0;
    while (top > 0) {
        int64_t u = todo[--top];
        for (int64_t c = head[u]; c != -1; c = next_child[c]) {
            mask[c] = mask[u] ^ (1LL << (s[c] - 'a'));
            todo[top++] = c;
        }
    }
    memset(used, 0, sizeof used);
    int64_t paths = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t m = mask[i];
        paths += get(m);
        for (int b = 0; b < 26; b++) paths += get(m ^ (1LL << b));
        add(m);
    }
    return paths;
}

static int64_t parents[COUNT][N];
static char letters[COUNT][N + 1];

int main(void) {
    int rounds = 5;
    for (int c = 0; c < COUNT; c++) {
        parents[c][0] = -1;
        for (int64_t i = 1; i < N; i++) parents[c][i] = wide() % i;
        for (int i = 0; i < N; i++) letters[c][i] = (char)('a' + next_random() % 26);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = count_palindrome_paths(parents[c], letters[c], N);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    printf("%d trees of 10^5, %d rounds: paths sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
