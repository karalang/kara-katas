// LeetCode #1144: Decrease Elements To Make Array Zigzag -- the C mirror of
// moves_to_make_zigzag.kara: one pass for each choice of which places are
// lowered, each lowered place brought to one below its smaller neighbour;
// the cheaper choice is the answer.
#include <stdint.h>
#include <stdio.h>

static int64_t moves_to_make_zigzag(const int64_t *nums, int64_t n) {
    int64_t best = INT64_MAX;
    for (int64_t low = 0; low < 2; low++) {
        int64_t moves = 0;
        for (int64_t i = low; i < n; i += 2) {
            int64_t least = INT64_MAX;
            if (i > 0 && nums[i - 1] < least) least = nums[i - 1];
            if (i + 1 < n && nums[i + 1] < least) least = nums[i + 1];
            if (nums[i] >= least) moves += nums[i] - least + 1;
        }
        if (moves < best) best = moves;
    }
    return best;
}

static int64_t seed = 1144;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    // 20 arrays of 1000 values from 1 to 1000, built once. Each of 5000
    // rounds draws one value of every array again and answers every array.
    static int64_t arrays[20][1000];
    for (int a = 0; a < 20; a++)
        for (int i = 0; i < 1000; i++) arrays[a][i] = next_random() % 1000 + 1;
    int64_t total = 0, check = 0;
    for (int r = 0; r < 5000; r++) {
        for (int a = 0; a < 20; a++) {
            int64_t at = next_random() % 1000;
            arrays[a][at] = next_random() % 1000 + 1;
            int64_t answer = moves_to_make_zigzag(arrays[a], 1000);
            total += answer;
            check = (check * 131 + answer + 1) % 1000000007;
        }
    }
    printf("5000 rounds over 20 arrays of 1000 values: answers total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
