// Benchmark for #666: a map of places, walked from the root, as the Kara
// ★ arm. C has no map, so a table indexed by the key, 10 * depth +
// position, stands in for it; every key is below 50.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct {
    bool has[50];
    int64_t value[50];
} Places;

static int64_t walk(const Places *values, int64_t key, int64_t above) {
    if (key >= 50 || !values->has[key]) {
        return 0;
    }
    int64_t sum = above + values->value[key];
    int64_t depth = key / 10;
    int64_t position = key % 10;
    int64_t left = (depth + 1) * 10 + 2 * position - 1;
    int64_t right = left + 1;
    bool has_left = left < 50 && values->has[left];
    bool has_right = right < 50 && values->has[right];
    if (!has_left && !has_right) {
        return sum;
    }
    return walk(values, left, sum) + walk(values, right, sum);
}

static int64_t path_sum(const int64_t *nums, int n) {
    Places values = {{false}, {0}};
    for (int i = 0; i < n; i++) {
        values.has[nums[i] / 10] = true;
        values.value[nums[i] / 10] = nums[i] % 10;
    }
    return walk(&values, 11, 0);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int random_tree(int64_t levels, int64_t chance, int64_t *seed, int64_t *nums) {
    int n = 0;
    nums[n++] = 110 + next_random(seed) % 10;
    int64_t level[8] = {1};
    int width = 1;
    for (int64_t depth = 2; depth <= levels; depth++) {
        int64_t next[8];
        int next_width = 0;
        for (int i = 0; i < width; i++) {
            for (int64_t c = 2 * level[i] - 1; c < 2 * level[i] + 1; c++) {
                if (next_random(seed) % 100 < chance) {
                    next[next_width++] = c;
                    nums[n++] = depth * 100 + c * 10 + next_random(seed) % 10;
                }
            }
        }
        for (int i = 0; i < next_width; i++) {
            level[i] = next[i];
        }
        width = next_width;
    }
    return n;
}

int main(void) {
    int64_t seed = 666;
    int64_t trees[256][15];
    int sizes[256];
    for (int t = 0; t < 256; t++) {
        int64_t chance = 50 + next_random(&seed) % 51;
        sizes[t] = random_tree(4, chance, &seed, trees[t]);
    }
    int64_t rounds = 1000000;
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        sum = (sum * 31 + path_sum(trees[r % 256], sizes[r % 256]) + r) % 1000000007;
    }
    printf("256 trees, %lld rounds: checksum %lld\n", (long long)rounds, (long long)sum);
    return 0;
}
