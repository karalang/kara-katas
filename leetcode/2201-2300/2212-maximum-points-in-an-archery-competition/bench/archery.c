// benchmark's C mirror of archery.kara (LeetCode #2212, the ★ arm): all
// 2^12 sets of sections tried as bit masks, Bob paying alice[k] + 1 arrows
// for each, the best he can afford kept, and the arrows left over put in
// section 0.
#include <stdint.h>
#include <stdio.h>

static void maximum_bob_points(int64_t num_arrows, const int64_t *alice, int64_t *bob) {
    int64_t best_mask = 0, best_points = -1;
    for (int64_t mask = 0; mask < 4096; mask++) {
        int64_t cost = 0, points = 0;
        for (int k = 0; k < 12; k++) {
            if ((mask >> k & 1) == 1) {
                cost += alice[k] + 1;
                points += k;
            }
        }
        if (cost <= num_arrows && points > best_points) {
            best_points = points;
            best_mask = mask;
        }
    }
    int64_t left = num_arrows;
    for (int k = 0; k < 12; k++) {
        bob[k] = 0;
        if ((best_mask >> k & 1) == 1) {
            bob[k] = alice[k] + 1;
            left -= bob[k];
        }
    }
    bob[0] += left;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2212;
    static int64_t ns[3000], alices[3000][12];
    for (int c = 0; c < 3000; c++) {
        // up to 10^5 arrows, Alice's shot into 12 sections in random shares
        int64_t n = next_random(&seed) * 4 % 100000 + 1;
        int64_t left = n;
        for (int k = 0; k < 11; k++) {
            int64_t take = next_random(&seed) % (left / 4 + 1);
            alices[c][k] = take;
            left -= take;
        }
        alices[c][11] = left;
        ns[c] = n;
    }
    int64_t check = 0, bob[12];
    for (int c = 0; c < 3000; c++) {
        maximum_bob_points(ns[c], alices[c], bob);
        for (int k = 0; k < 12; k++) check = (check * 31 + bob[k]) % 1000000007;
    }
    printf("3000 contests: checksum %lld\n", (long long)check);
    return 0;
}
