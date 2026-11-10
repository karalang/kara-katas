// LeetCode #2061: Number of Spaces Cleaning Robot Cleaned -- C mirror of
// the ★ arm's benchmark (robot.kara): 600 spiral rooms of 200 to 300 by
// 200 to 300, the robot walked one move at a time, states and cells kept
// in flat arrays of bytes allocated per room.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const int64_t DR[4] = {0, 1, 0, -1};
static const int64_t DC[4] = {1, 0, -1, 0};

static int64_t number_of_clean_rooms(const int64_t *room, int64_t m, int64_t n) {
    char *seen = calloc((size_t)(m * n * 4), 1);
    char *cleaned = calloc((size_t)(m * n), 1);
    int64_t count = 0, r = 0, c = 0, d = 0;
    while (!seen[(r * n + c) * 4 + d]) {
        seen[(r * n + c) * 4 + d] = 1;
        if (!cleaned[r * n + c]) {
            cleaned[r * n + c] = 1;
            count++;
        }
        int64_t nr = r + DR[d], nc = c + DC[d];
        if (nr >= 0 && nr < m && nc >= 0 && nc < n && room[nr * n + nc] == 0) {
            r = nr;
            c = nc;
        } else {
            d = (d + 1) % 4;
        }
    }
    free(seen);
    free(cleaned);
    return count;
}

static int64_t seed = 2061;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t *spiral(int64_t m, int64_t n) {
    int64_t *room = calloc((size_t)(m * n), sizeof(int64_t));
    int64_t top = 0, left = 0, bottom = m - 1, right = n - 1;
    for (;;) {
        if (top + 2 > bottom) break;
        room[(top + 1) * n + left] = 1;
        top += 2;
        if (left + 2 > right) break;
        room[top * n + right - 1] = 1;
        right -= 2;
        if (bottom - 2 < top) break;
        room[(bottom - 1) * n + right] = 1;
        bottom -= 2;
        if (right - 2 < left) break;
        room[bottom * n + left + 1] = 1;
        left += 2;
    }
    return room;
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int t = 0; t < 600; t++) {
        int64_t m = next_random() % 101 + 200;
        int64_t n = next_random() % 101 + 200;
        int64_t *room = spiral(m, n);
        int64_t a = number_of_clean_rooms(room, m, n);
        free(room);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    printf("600 rooms: %lld cleaned, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
