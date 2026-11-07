// LeetCode #1061: Lexicographically Smallest Equivalent String -- the
// benchmark, the same union-find as lexi.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t find(int64_t *parent, int64_t x) {
    int64_t root = x;
    while (parent[root] != root) root = parent[root];
    int64_t y = x;
    while (parent[y] != root) {
        int64_t next = parent[y];
        parent[y] = root;
        y = next;
    }
    return root;
}

// The answer is written to `out`, which holds `n` bytes and a terminator.
static void smallest_equivalent(const char *s1, const char *s2, const char *base, char *out) {
    int64_t parent[26];
    for (int64_t i = 0; i < 26; i++) parent[i] = i;
    for (size_t i = 0; s1[i] && s2[i]; i++) {
        int64_t ra = find(parent, s1[i] - 'a');
        int64_t rb = find(parent, s2[i] - 'a');
        if (ra < rb) parent[rb] = ra;
        else parent[ra] = rb;
    }
    size_t n = 0;
    for (; base[n]; n++) out[n] = (char)('a' + find(parent, base[n] - 'a'));
    out[n] = 0;
}

static int64_t seed = 1061;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *random_word(int64_t n, int64_t k) {
    char *s = malloc(n + 1);
    for (int64_t i = 0; i < n; i++) s[i] = (char)('a' + next_random() % k);
    s[n] = 0;
    return s;
}

int main(void) {
    char *s1s[100], *s2s[100], *bases[100];
    for (int p = 0; p < 100; p++) {
        int64_t k = 2 + p % 25;
        s1s[p] = random_word(1000, k);
        s2s[p] = random_word(1000, k);
    }
    for (int b = 0; b < 100; b++) bases[b] = random_word(20000, 26);
    char *answer = malloc(20001);
    int64_t calls = 0, total = 0, check = 0;
    for (int p = 0; p < 100; p++) {
        for (int b = 0; b < 100; b++) {
            smallest_equivalent(s1s[p], s2s[p], bases[b], answer);
            int64_t sum = 0;
            for (size_t i = 0; answer[i]; i++) sum += (unsigned char)answer[i];
            total += sum;
            check = (check * 31 + sum % 1000003) % 1000000007;
            calls++;
        }
    }
    printf("%lld calls: letters sum %lld, checksum %lld\n", (long long)calls, (long long)total,
           (long long)check);
    return 0;
}
