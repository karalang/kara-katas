// LeetCode #874 bench: C mirror of robot_sim.kara (the ★ arm) on the same
// 600 walks. C has no hash set, so the obstacles go into an
// open-addressing table with linear probing.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 10000
#define CAP 32768

static int64_t keys[CAP];
static unsigned char used[CAP];

static size_t slot(int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    return (size_t)(h >> 49) & (CAP - 1);
}

static void put(int64_t key) {
    size_t s = slot(key);
    while (used[s] && keys[s] != key) s = (s + 1) & (CAP - 1);
    used[s] = 1;
    keys[s] = key;
}

static int has(int64_t key) {
    size_t s = slot(key);
    while (used[s]) {
        if (keys[s] == key) return 1;
        s = (s + 1) & (CAP - 1);
    }
    return 0;
}

static int64_t square(int64_t x, int64_t y) { return (x + 200000) * 400001 + (y + 200000); }

static int64_t robot_sim(const int64_t *commands, int n, const int64_t (*obstacles)[2], int m) {
    memset(used, 0, sizeof used);
    for (int i = 0; i < m; i++) put(square(obstacles[i][0], obstacles[i][1]));
    static const int64_t dx[4] = {0, 1, 0, -1}, dy[4] = {1, 0, -1, 0};
    int facing = 0;
    int64_t x = 0, y = 0, best = 0;
    for (int i = 0; i < n; i++) {
        int64_t c = commands[i];
        if (c == -2) {
            facing = (facing + 3) % 4;
        } else if (c == -1) {
            facing = (facing + 1) % 4;
        } else {
            for (int64_t s = 0; s < c; s++) {
                int64_t nx = x + dx[facing], ny = y + dy[facing];
                if (has(square(nx, ny))) break;
                x = nx;
                y = ny;
                if (x * x + y * y > best) best = x * x + y * y;
            }
        }
    }
    return best;
}

static int64_t seed = 874;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t command_lists[20][N];
static int64_t obstacle_lists[20][N][2];

int main(void) {
    for (int k = 0; k < 20; k++) {
        int64_t turns = 2 + k % 3;
        for (int i = 0; i < N; i++) {
            if (next_random() % turns == 0)
                command_lists[k][i] = -1 - next_random() % 2;
            else
                command_lists[k][i] = next_random() % 9 + 1;
        }
        int64_t reach = 100 + 10 * k;
        for (int i = 0; i < N; i++) {
            obstacle_lists[k][i][0] = next_random() % (2 * reach + 1) - reach;
            obstacle_lists[k][i][1] = next_random() % (2 * reach + 1) - reach;
        }
    }
    int64_t total = 0, check = 0;
    for (int k = 0; k < 600; k++) {
        int64_t answer = robot_sim(command_lists[k % 20], N, (const int64_t (*)[2])obstacle_lists[(k * 7 + k / 20) % 20], N);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    printf("600 walks of 10000 commands among 10000 obstacles: distances sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
