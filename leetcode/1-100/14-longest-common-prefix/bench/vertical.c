// Benchmark workload — Longest Common Prefix (LeetCode #14).
// C mirror of bench/vertical.kara. Same M/N/K, generator, and sink — see
// that file's header for the workload rationale.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef struct {
    char **items;
    int   *lens;   // O(1) per-string length, mirroring Slice.len()
    int    count;
} Strs;

static char nth_letter(int64_t n) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    return alphabet[n % 26];
}

static char *make_string(int64_t prefix_len, int64_t suffix_id, int *out_len) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    int len = (int)prefix_len + 6;
    char *out = (char *)malloc((size_t)len + 1);
    int p = 0;
    for (int64_t i = 0; i < prefix_len; i++) out[p++] = alphabet[i];
    char sig = nth_letter(suffix_id);
    for (int j = 0; j < 6; j++) out[p++] = sig;
    out[p] = '\0';
    *out_len = len;
    return out;
}

static Strs build_case(int64_t prefix_len, int64_t count) {
    Strs v;
    v.count = (int)count;
    v.items = (char **)malloc(sizeof(char *) * (size_t)count);
    v.lens  = (int *)malloc(sizeof(int) * (size_t)count);
    for (int64_t s = 0; s < count; s++) {
        int len;
        v.items[s] = make_string(prefix_len, s, &len);
        v.lens[s]  = len;
    }
    return v;
}

// Returns the length of the longest common prefix. Mirrors the .kara
// version's "build prefix String, return its .len()" by allocating the
// prefix and freeing it, so the per-iter alloc cost is present in both.
static int64_t longest_common_prefix(const Strs *strs) {
    int n = strs->count;
    if (n == 0) return 0;
    const char *first = strs->items[0];
    int first_len = strs->lens[0];
    int col = 0;
    while (col < first_len) {
        char c = first[col];
        int s = 1;
        int stop = 0;
        for (; s < n; s++) {
            if (col >= strs->lens[s] || strs->items[s][col] != c) { stop = 1; break; }
        }
        if (stop) break;
        col++;
    }
    char *prefix = (char *)malloc((size_t)col + 1);
    memcpy(prefix, first, (size_t)col);
    prefix[col] = '\0';
    int64_t len = (int64_t)strlen(prefix);
    free(prefix);
    return len;
}

int main(void) {
    const int64_t m_cases = 8;
    const int64_t n_strings = 16;
    const int64_t k_iters = 1000000;
    const int64_t prefixes[8] = {0, 2, 4, 7, 10, 13, 16, 20};

    Strs *sets = (Strs *)malloc(sizeof(Strs) * (size_t)m_cases);
    for (int64_t m = 0; m < m_cases; m++) {
        sets[m] = build_case(prefixes[m], n_strings);
    }

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t idx = k % m_cases;
        sum += longest_common_prefix(&sets[idx]);
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
