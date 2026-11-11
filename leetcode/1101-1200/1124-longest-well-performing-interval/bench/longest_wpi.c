// LeetCode #1124: Longest Well-Performing Interval -- the bench in C, the ★
// arm with a hash map from score to first index: open addressing over a
// table of 2^15 slots, cleared for each call, the score mixed by a
// multiplicative hash. The same 16 schedules and 300 rounds.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define SLOTS (1 << 15)

static int64_t keys[SLOTS], vals[SLOTS];
static unsigned char used[SLOTS];

static size_t slot_of(int64_t key) {
    uint64_t x = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    size_t at = (size_t)(x >> 49);
    while (used[at] && keys[at] != key) at = (at + 1) & (SLOTS - 1);
    return at;
}

static int64_t longest_wpi(const int *hours, int n) {
    memset(used, 0, sizeof used);
    int64_t score = 0, best = 0;
    for (int64_t i = 0; i < n; i++) {
        score += hours[i] > 8 ? 1 : -1;
        if (score > 0) {
            best = i + 1;
        } else {
            size_t p = slot_of(score - 1);
            if (used[p] && i - vals[p] > best) best = i - vals[p];
            size_t q = slot_of(score);
            if (!used[q]) {
                used[q] = 1;
                keys[q] = score;
                vals[q] = i;
            }
        }
    }
    return best;
}

static int64_t seed = 1124;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int schedules[16][10000];

int main(void) {
    for (int j = 0; j < 16; j++)
        for (int i = 0; i < 10000; i++) schedules[j][i] = (int)(next_random() % 17);
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 300; round++) {
        for (int64_t j = 0; j < 16; j++) {
            int at = (int)((round * 7919 + j * 104729) % 10000);
            int h = schedules[j][at];
            schedules[j][at] = h > 8 ? h - 9 : 9 + h % 8;
            int64_t answer = longest_wpi(schedules[j], 10000);
            total += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("300 rounds over 16 schedules of 10^4 days: answers total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
