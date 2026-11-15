// LeetCode #2138: Divide a String Into Groups of Size k -- the benchmark,
// the same algorithm as divide.kara: each group its own allocation.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char **groups;
    int64_t len;
} Groups;

static Groups divide_string(const char *s, int64_t n, int64_t k, char fill) {
    Groups out;
    out.groups = malloc(sizeof(char *) * (size_t)((n + k - 1) / k));
    out.len = 0;
    for (int64_t start = 0; start < n; start += k) {
        int64_t end = start + k < n ? start + k : n;
        char *group = malloc((size_t)k + 1);
        memcpy(group, s + start, (size_t)(end - start));
        for (int64_t j = end - start; j < k; j++) group[j] = fill;
        group[k] = 0;
        out.groups[out.len++] = group;
    }
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    int64_t seed = 2138;
    char *strings[1000];
    for (int i = 0; i < 1000; i++) {
        strings[i] = malloc(101);
        for (int j = 0; j < 100; j++) strings[i][j] = alphabet[next_random(&seed) % 26];
        strings[i][100] = 0;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < 100; r++) {
        for (int i = 0; i < 1000; i++) {
            int64_t at = next_random(&seed) % 100;
            strings[i][at] = alphabet[next_random(&seed) % 26];
            int64_t k = next_random(&seed) % 100 + 1;
            char fill = alphabet[next_random(&seed) % 26];
            char *s = malloc(101);
            memcpy(s, strings[i], 101);
            Groups g = divide_string(s, 100, k, fill);
            total += g.len;
            const char *last = g.groups[g.len - 1];
            for (int64_t j = 0; j < k; j++) check = (check * 131 + (unsigned char)last[j]) % 1000000007;
            for (int64_t j = 0; j < g.len; j++) free(g.groups[j]);
            free(g.groups);
            free(s);
        }
    }
    printf("100000 solves: %lld groups, checksum %lld\n", (long long)total, (long long)check);
    for (int i = 0; i < 1000; i++) free(strings[i]);
    return 0;
}
