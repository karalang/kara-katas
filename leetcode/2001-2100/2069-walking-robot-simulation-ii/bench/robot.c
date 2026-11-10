// LeetCode #2069: Walking Robot Simulation II -- C mirror of the ★
// arm's benchmark (robot.kara): 200 robots of 2 to 100 by 2 to 100, 50000
// calls each, half of them steps of up to 100000 cells.
// `get_pos` writes the cell into a caller's pair and `get_dir` hands back
// a constant name, so C allocates nothing per call.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    int64_t width, height, at;
    bool moved;
} Robot;

static void step(Robot *r, int64_t num) {
    r->moved = true;
    r->at = (r->at + num) % (2 * (r->width + r->height) - 4);
}

static void get_pos(const Robot *r, int64_t p[2]) {
    int64_t w = r->width - 1, h = r->height - 1, at = r->at;
    if (at <= w) {
        p[0] = at, p[1] = 0;
    } else if (at <= w + h) {
        p[0] = w, p[1] = at - w;
    } else if (at <= 2 * w + h) {
        p[0] = 2 * w + h - at, p[1] = h;
    } else {
        p[0] = 0, p[1] = 2 * w + 2 * h - at;
    }
}

static const char *get_dir(const Robot *r) {
    int64_t w = r->width - 1, h = r->height - 1, at = r->at;
    if (at == 0) return r->moved ? "South" : "East";
    if (at <= w) return "East";
    if (at <= w + h) return "North";
    if (at <= 2 * w + h) return "West";
    return "South";
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2069, check = 0;
    for (int64_t t = 0; t < 200; t++) {
        Robot robot = {2 + t % 99, 2 + t * 7 % 99, 0, false};
        for (int k = 0; k < 50000; k++) {
            int64_t kind = next_random(&seed) % 4;
            if (kind < 2) {
                int64_t a = next_random(&seed);
                int64_t b = next_random(&seed);
                step(&robot, (a * 32768 + b) % 100000 + 1);
            } else if (kind == 2) {
                int64_t p[2];
                get_pos(&robot, p);
                check = (check * 31 + p[0] * 1000 + p[1]) % 1000000007;
            } else {
                check = (check * 31 + (int64_t)strlen(get_dir(&robot))) % 1000000007;
            }
        }
    }
    printf("200 robots, 10000000 calls: checksum %lld\n", (long long)check);
    return 0;
}
