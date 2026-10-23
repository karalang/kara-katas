// LeetCode #920: Number of Music Playlists -- bench: a table over the
// length and the distinct songs so far. Mirrors num_music_playlists.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t num_music_playlists(int64_t n, int64_t goal, int64_t k) {
    const int64_t modulus = 1000000007;
    int64_t *dp = calloc((goal + 1) * (n + 1), sizeof(int64_t));
    dp[0] = 1;
    for (int64_t i = 1; i <= goal; i++) {
        int64_t top = i < n ? i : n;
        for (int64_t j = 1; j <= top; j++) {
            int64_t fresh = dp[(i - 1) * (n + 1) + j - 1] * (n - j + 1) % modulus;
            int64_t again = j > k ? dp[(i - 1) * (n + 1) + j] * (j - k) % modulus : 0;
            dp[i * (n + 1) + j] = (fresh + again) % modulus;
        }
    }
    int64_t answer = dp[goal * (n + 1) + n];
    free(dp);
    return answer;
}

int main(void) {
    const int64_t top = 64;
    int64_t count = 0, sum = 0, check = 0;
    for (int64_t goal = 1; goal <= top; goal++)
        for (int64_t n = 1; n <= goal; n++)
            for (int64_t k = 0; k < n; k++) {
                int64_t r = num_music_playlists(n, goal, k);
                count++;
                sum += r;
                check = (check * 1000003 + r) % 1000000007;
            }
    printf("every case with goal up to %lld: %lld cases, answers summing to %lld, checksum %lld\n",
           (long long)top, (long long)count, (long long)sum, (long long)check);
    return 0;
}
