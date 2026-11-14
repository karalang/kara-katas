// LeetCode #1153 bench -- mirrors can_convert.kara: the same 64 pairs,
// the same rounds, the ★ arm's arrays.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define N 10000

static bool can_convert(const char *str1, const char *str2, int n) {
    if (memcmp(str1, str2, n) == 0) return true;
    int64_t to[26];
    bool used[26];
    for (int i = 0; i < 26; i++) {
        to[i] = -1;
        used[i] = false;
    }
    int letters = 0;
    for (int i = 0; i < n; i++) {
        int x = str1[i] - 'a';
        int64_t y = str2[i] - 'a';
        if (to[x] == -1) {
            to[x] = y;
        } else if (to[x] != y) {
            return false;
        }
        if (!used[y]) {
            used[y] = true;
            letters++;
        }
    }
    return letters < 26;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char A[64][N], B[64][N];

int main(void) {
    int rounds = 100000;
    int64_t seed = 1153;
    for (int p = 0; p < 64; p++) {
        for (int i = 0; i < N; i++) A[p][i] = 'a' + next_random(&seed) % 26;
        char map[26];
        for (int i = 0; i < 26; i++) map[i] = 'a' + i;
        for (int j = 25; j >= 1; j--) {
            int k = next_random(&seed) % (j + 1);
            char t = map[j];
            map[j] = map[k];
            map[k] = t;
        }
        if (p % 4 < 2) map[next_random(&seed) % 26] = map[25];
        for (int i = 0; i < N; i++) B[p][i] = p % 4 == 3 ? A[p][i] : map[A[p][i] - 'a'];
        if (p % 4 == 1) {
            int at = next_random(&seed) % N;
            B[p][at] = B[p][at] == 'z' ? 'a' : B[p][at] + 1;
        }
    }
    int64_t yes = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        bool ok = can_convert(A[r % 64], B[r % 64], N);
        if (ok) yes++;
        check = (check * 31 + (ok ? 2 : 1) + r % 64) % 1000000007;
    }
    printf("%d rounds over 64 pairs of 10000 letters: %lld convertible, checksum %lld\n", rounds, (long long)yes,
           (long long)check);
    return 0;
}
