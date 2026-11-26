// LeetCode #1769: Minimum Number of Operations to Move All Balls to Each
// Box -- the bench in C, mirroring min_operations.kara: two sweeps, the
// answer a new array each call.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int *min_operations(const char *boxes, int n) {
    int *answer = calloc(n, sizeof(int));
    int balls = 0, moves = 0;
    for (int i = 0; i < n; i++) {
        answer[i] += moves;
        if (boxes[i] == '1') balls++;
        moves += balls;
    }
    balls = 0;
    moves = 0;
    for (int i = n - 1; i >= 0; i--) {
        answer[i] += moves;
        if (boxes[i] == '1') balls++;
        moves += balls;
    }
    return answer;
}

static long long seed = 1769;
static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char rows[200][2001];
    for (int r = 0; r < 200; r++) {
        long long full = next_random() % 101;
        for (int i = 0; i < 2000; i++) rows[r][i] = next_random() % 100 < full ? '1' : '0';
        rows[r][2000] = 0;
    }
    long long check = 0;
    for (long long call = 0; call < 40000; call++) {
        int *answer = min_operations(rows[(check + call * 7919) % 200], 2000);
        check = (check * 31 + answer[check % 2000]) % 1000000007;
        free(answer);
    }
    printf("40000 calls over 200 rows: checksum %lld\n", check);
    return 0;
}
