// LeetCode #1104: Path In Zigzag Labelled Binary Tree -- the bench in C:
// the ★ arm (walking up, each parent half the label's mirror in its row)
// over every label from 1 to 10^6 in a different order each of 8 rounds.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t *path_in_zig_zag_tree(int64_t label, int64_t *len) {
    int64_t depth = 1;
    while (((int64_t)1 << depth) <= label) depth += 1;
    int64_t *path = malloc((size_t)depth * sizeof(int64_t));
    int64_t n = 0, node = label;
    while (depth > 0) {
        path[n++] = node;
        int64_t start = (int64_t)1 << (depth - 1), end = ((int64_t)1 << depth) - 1;
        node = (start + end - node) / 2;
        depth -= 1;
    }
    for (int64_t i = 0, j = n - 1; i < j; i++, j--) {
        int64_t t = path[i]; path[i] = path[j]; path[j] = t;
    }
    *len = n;
    return path;
}

int main(void) {
    int64_t nodes = 0, check = 0;
    for (int64_t round = 0; round < 8; round++) {
        for (int64_t i = 0; i < 1000000; i++) {
            int64_t label = (i * 7919 + round * 104729) % 1000000 + 1;
            int64_t len;
            int64_t *path = path_in_zig_zag_tree(label, &len);
            nodes += len;
            check = (check * 31 + path[len / 2]) % 1000000007;
            free(path);
        }
    }
    printf("8 rounds over the labels 1 to 10^6: %lld nodes on their paths, checksum %lld\n", (long long)nodes, (long long)check);
    return 0;
}
