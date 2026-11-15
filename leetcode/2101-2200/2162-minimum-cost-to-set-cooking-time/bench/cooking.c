// LeetCode #2162: Minimum Cost to Set Cooking Time -- the benchmark's C
// mirror of cooking.kara: each way's text by snprintf, walked digit by
// digit.

#include <stdint.h>
#include <stdio.h>

static int64_t cost(const char *digits, int64_t start_at, int64_t move_cost, int64_t push_cost) {
    int64_t at = start_at, total = 0;
    for (const char *p = digits; *p; p++) {
        int64_t d = *p - '0';
        if (d != at) {
            total += move_cost;
            at = d;
        }
        total += push_cost;
    }
    return total;
}

static int64_t min_cost_set_time(int64_t start_at, int64_t move_cost, int64_t push_cost, int64_t target_seconds) {
    int64_t minutes = target_seconds / 60, seconds = target_seconds % 60;
    int64_t ways[2][2] = {{minutes, seconds}, {minutes - 1, seconds + 60}};
    int64_t best = INT64_MAX;
    for (int i = 0; i < 2; i++) {
        int64_t m = ways[i][0], s = ways[i][1];
        if (m >= 0 && m <= 99 && s <= 99) {
            char text[24];
            snprintf(text, sizeof text, "%lld", (long long)(m * 100 + s));
            int64_t c = cost(text, start_at, move_cost, push_cost);
            if (c < best) best = c;
        }
    }
    return best;
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int64_t pass = 0; pass < 30; pass++) {
        int64_t move_cost = pass % 10 + 1, push_cost = pass * 3 % 10 + 1;
        for (int64_t start_at = 0; start_at < 10; start_at++) {
            for (int64_t target_seconds = 1; target_seconds < 6040; target_seconds++) {
                int64_t c = min_cost_set_time(start_at, move_cost, push_cost, target_seconds);
                total += c;
                check = (check * 31 + c + pass) % 1000000007;
            }
        }
    }
    printf("1811700 solves: %lld in all, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
