// LeetCode #1742: Maximum Number of Balls in a Box -- the bench
// (balls.kara in C): a count for every digit sum.
#include <stdint.h>
#include <stdio.h>

static int count_balls(int low_limit, int high_limit) {
    int boxes[46] = {0};
    for (int ball = low_limit; ball <= high_limit; ball++) {
        int rest = ball, sum = 0;
        while (rest > 0) {
            sum += rest % 10;
            rest /= 10;
        }
        boxes[sum] += 1;
    }
    int best = boxes[0];
    for (int i = 1; i < 46; i++) if (boxes[i] > best) best = boxes[i];
    return best;
}

static int64_t seed = 1742;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    enum { COUNT = 200, ROUNDS = 20 };
    static int lows[COUNT], highs[COUNT];
    for (int i = 0; i < COUNT; i++) {
        int64_t a = wide() % 100000 + 1;
        int64_t b = wide() % 100000 + 1;
        lows[i] = (int)(a < b ? a : b);
        highs[i] = (int)(a < b ? b : a);
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int i = 0; i < COUNT; i++) {
            int64_t answer = count_balls(lows[i], highs[i]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d ranges inside 1 to 100000, %d rounds: largest boxes sum to %lld, checksum %lld\n", COUNT, ROUNDS, (long long)sum, (long long)check);
    return 0;
}
