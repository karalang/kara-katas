// LeetCode #2059: Minimum Operations to Convert Number -- C mirror of the
// ★ arm's benchmark (ops.kara): the same 16000 problems, each answered by
// one breadth-first search over the values 0 to 1000, the queue a ring of
// 1001 (value, steps) pairs.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t minimum_operations(const int64_t *nums, int64_t len, int64_t start, int64_t goal) {
    bool seen[1001];
    int64_t qx[1001], qs[1001];
    int64_t head = 0, tail = 0;
    memset(seen, 0, sizeof seen);
    seen[start] = true;
    qx[tail] = start;
    qs[tail] = 0;
    tail++;
    while (head < tail) {
        int64_t x = qx[head], steps = qs[head];
        head++;
        for (int64_t i = 0; i < len; i++) {
            int64_t n = nums[i];
            int64_t ys[3] = {x + n, x - n, x ^ n};
            for (int k = 0; k < 3; k++) {
                int64_t y = ys[k];
                if (y == goal) {
                    return steps + 1;
                }
                if (y >= 0 && y <= 1000 && !seen[y]) {
                    seen[y] = true;
                    qx[tail] = y;
                    qs[tail] = steps + 1;
                    tail++;
                }
            }
        }
    }
    return -1;
}

static int64_t seed = 2059;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t draw(int64_t n, int64_t spread, int64_t *nums) {
    int64_t len = 0;
    while (len < n) {
        int64_t x;
        if (next_random() % 8 == 0) {
            int64_t hi = next_random();
            x = (hi * 32768 + next_random()) % 2000000001 - 1000000000;
        } else {
            x = next_random() % (2 * spread + 1) - spread;
        }
        bool dup = false;
        for (int64_t i = 0; i < len; i++) {
            if (nums[i] == x) {
                dup = true;
                break;
            }
        }
        if (!dup) {
            nums[len++] = x;
        }
    }
    return len;
}

int main(void) {
    static const int64_t spreads[4] = {5, 50, 300, 1500};
    int64_t nums[16];
    int64_t unreachable = 0, total = 0, check = 0;
    for (int r = 0; r < 16000; r++) {
        int64_t n = next_random() % 16 + 1;
        int64_t spread = spreads[next_random() % 4];
        int64_t len = draw(n, spread, nums);
        int64_t start = next_random() % 1001;
        int64_t goal = next_random() % 1401 - 200;
        if (goal == start) {
            goal += 1;
        }
        int64_t ops = minimum_operations(nums, len, start, goal);
        if (ops < 0) {
            unreachable++;
        }
        total += ops;
        check = (check * 31 + ops + 2) % 1000000007;
    }
    printf("16000 problems: %lld unreachable, sum %lld, checksum %lld\n", (long long)unreachable,
           (long long)total, (long long)check);
    return 0;
}
