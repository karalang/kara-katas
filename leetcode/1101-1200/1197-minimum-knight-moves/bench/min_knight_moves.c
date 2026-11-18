// LeetCode #1197 bench: the ★ arm in C, over the same 2000 random targets
// as the Kāra bench; the queue is an array of (x, y, steps) the size of the
// grid, since each square enters it at most once.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const int64_t MOVES[8][2] = {{1, 2}, {2, 1}, {2, -1}, {1, -2}, {-1, -2}, {-2, -1}, {-2, 1}, {-1, 2}};

static int64_t min_knight_moves(int64_t x, int64_t y) {
    int64_t tx = llabs(x), ty = llabs(y);
    int64_t side = 305;
    char *seen = calloc(side * side, 1);
    int64_t (*queue)[3] = malloc(side * side * sizeof *queue);
    int64_t head = 0, tail = 0, answer = -1;
    queue[tail][0] = 0, queue[tail][1] = 0, queue[tail][2] = 0, tail++;
    seen[2 * side + 2] = 1;
    while (head < tail) {
        int64_t cx = queue[head][0], cy = queue[head][1], steps = queue[head][2];
        head++;
        if (cx == tx && cy == ty) {
            answer = steps;
            break;
        }
        for (int m = 0; m < 8; m++) {
            int64_t nx = cx + MOVES[m][0], ny = cy + MOVES[m][1];
            if (nx >= -2 && ny >= -2 && nx <= 302 && ny <= 302) {
                int64_t k = (nx + 2) * side + ny + 2;
                if (!seen[k]) {
                    seen[k] = 1;
                    queue[tail][0] = nx, queue[tail][1] = ny, queue[tail][2] = steps + 1, tail++;
                }
            }
        }
    }
    free(queue);
    free(seen);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1197;
    int64_t tx[2000], ty[2000];
    for (int i = 0; i < 2000; i++) {
        int64_t s = next_random(&seed) % 301;
        int64_t x = next_random(&seed) % (s + 1);
        int64_t y = s - x;
        tx[i] = next_random(&seed) % 2 == 0 ? x : -x;
        ty[i] = next_random(&seed) % 2 == 0 ? y : -y;
    }
    int64_t check = 0;
    for (int i = 0; i < 2000; i++) {
        int64_t m = min_knight_moves(tx[i], ty[i]);
        check = (check * 131 + m + 1) % 1000000007;
    }
    printf("2000 targets: checksum %lld\n", (long long)check);
    return 0;
}
