// LeetCode #2301: Match Substring After Replacement -- the bench, the ★
// arm in C. A table of which letter may stand for which, then every start
// of sub in s checked against it.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum { CASES = 50, N = 20000, K = 40, M = 1000 };

static bool can[128 * 128];

static bool match_replacement(const char *s, int n, const char *sub, int k, const char (*maps)[2], int m) {
    memset(can, 0, sizeof can);
    for (int c = 0; c < 128; c++) can[c * 128 + c] = true;
    for (int i = 0; i < m; i++) can[(unsigned char)maps[i][0] * 128 + (unsigned char)maps[i][1]] = true;
    for (int start = 0; start <= n - k; start++) {
        bool all = true;
        for (int j = 0; j < k; j++) {
            if (!can[(unsigned char)sub[j] * 128 + (unsigned char)s[start + j]]) {
                all = false;
                break;
            }
        }
        if (all) return true;
    }
    return false;
}

static int64_t seed = 2301;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char texts[CASES][N], subs[CASES][K], maps[CASES][M][2];
    for (int c = 0; c < CASES; c++) {
        for (int i = 0; i < N; i++) texts[c][i] = "ab"[next_random() % 2];
        for (int j = 0; j < K; j++) {
            int64_t r = next_random() % 4;
            subs[c][j] = r < 2 ? 'c' : "ab"[r - 2];
        }
        maps[c][0][0] = 'c'; maps[c][0][1] = 'a';
        maps[c][1][0] = 'c'; maps[c][1][1] = 'b';
        for (int i = 2; i < M; i++) {
            maps[c][i][0] = "xyz"[next_random() % 3];
            maps[c][i][1] = "ab"[next_random() % 2];
        }
    }
    int64_t check = 0;
    for (int p = 0; p < 20; p++)
        for (int c = 0; c < CASES; c++) {
            bool ok = match_replacement(texts[(c + p) % CASES], N, subs[c], K, maps[c], M);
            check = (check * 31 + (ok ? c + 1 : 0)) % 1000000007;
        }
    printf("20 passes over 50 cases of 20000 letters: checksum %lld\n", (long long)check);
    return 0;
}
