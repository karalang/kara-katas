// LeetCode #1718: Construct the Lexicographically Largest Valid Sequence
// -- the bench (sequence.kara): the first empty slot filled with the
// largest number that fits, backtracking when none does.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int place(int *seq, char *used, long len, long at, int n) {
    while (at < len && seq[at] != 0) {
        at++;
    }
    if (at == len) {
        return 1;
    }
    for (int v = n; v >= 1; v--) {
        if (used[v]) {
            continue;
        }
        if (v > 1 && (at + v >= len || seq[at + v] != 0)) {
            continue;
        }
        used[v] = 1;
        seq[at] = v;
        if (v > 1) {
            seq[at + v] = v;
        }
        if (place(seq, used, len, at + 1, n)) {
            return 1;
        }
        used[v] = 0;
        seq[at] = 0;
        if (v > 1) {
            seq[at + v] = 0;
        }
    }
    return 0;
}

/* the answer for n written into out, which holds 2n - 1 values */
static void construct_distanced_sequence(int n, int *out) {
    long len = 2 * n - 1;
    char *used = calloc(n + 1, 1);
    memset(out, 0, sizeof(int) * len);
    place(out, used, len, 0, n);
    free(used);
}

int main(void) {
    long rounds = 2000;
    long values = 0;
    long check = 0;
    for (long r = 0; r < rounds; r++) {
        for (int n = 1; n <= 20; n++) {
            int *seq = malloc(sizeof(int) * (2 * n - 1));
            construct_distanced_sequence(n, seq);
            for (int i = 0; i < 2 * n - 1; i++) {
                values++;
                check = (check * 31 + seq[i] + r) % 1000000007;
            }
            free(seq);
        }
    }
    printf("every n from 1 to 20, %ld rounds: %ld values, checksum %ld\n", rounds, values, check);
    return 0;
}
