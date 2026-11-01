// LeetCode #1036: Escape a Large Maze -- bench
// Mirrors ./escape_maze.kara; see ../README.md § Benchmarks. C has no set,
// so each square is one integer x * side + y in an open-addressing table
// with a multiplicative hash, and the queue is a growable array; Kāra's
// Set hashes the pair with SipHash-1-3.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *keys;
    int64_t cap, len;
} set_t;

static void set_init(set_t *s, int64_t cap) {
    s->cap = cap;
    s->len = 0;
    s->keys = malloc(sizeof(int64_t) * (size_t)cap);
    memset(s->keys, 0xff, sizeof(int64_t) * (size_t)cap);
}

static int64_t slot(const set_t *s, int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    int64_t i = (int64_t)(h >> 20) & (s->cap - 1);
    while (s->keys[i] != -1 && s->keys[i] != key) i = (i + 1) & (s->cap - 1);
    return i;
}

static int set_has(const set_t *s, int64_t key) { return s->keys[slot(s, key)] == key; }

static void set_add(set_t *s, int64_t key);

static void set_grow(set_t *s) {
    set_t bigger;
    set_init(&bigger, s->cap * 2);
    for (int64_t i = 0; i < s->cap; i++)
        if (s->keys[i] != -1) set_add(&bigger, s->keys[i]);
    free(s->keys);
    *s = bigger;
}

static void set_add(set_t *s, int64_t key) {
    if ((s->len + 1) * 2 > s->cap) set_grow(s);
    int64_t i = slot(s, key);
    if (s->keys[i] != key) {
        s->keys[i] = key;
        s->len++;
    }
}

static int not_fenced(const set_t *blocked, int64_t fx, int64_t fy, int64_t tx, int64_t ty, int64_t side) {
    int64_t limit = blocked->len * (blocked->len - 1) / 2;
    static const int64_t dirs[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    set_t seen;
    set_init(&seen, 16);
    int64_t cap = 16, head = 0, tail = 0;
    int64_t *queue = malloc(sizeof(int64_t) * 2 * (size_t)cap);
    set_add(&seen, fx * side + fy);
    queue[0] = fx;
    queue[1] = fy;
    tail = 1;
    int free_ = 0;
    while (head < tail) {
        int64_t x = queue[2 * head], y = queue[2 * head + 1];
        head++;
        if ((x == tx && y == ty) || seen.len > limit) {
            free_ = 1;
            break;
        }
        for (int d = 0; d < 4; d++) {
            int64_t nx = x + dirs[d][0], ny = y + dirs[d][1];
            if (nx >= 0 && nx < side && ny >= 0 && ny < side && !set_has(blocked, nx * side + ny) && !set_has(&seen, nx * side + ny)) {
                set_add(&seen, nx * side + ny);
                if (tail == cap) {
                    cap *= 2;
                    queue = realloc(queue, sizeof(int64_t) * 2 * (size_t)cap);
                }
                queue[2 * tail] = nx;
                queue[2 * tail + 1] = ny;
                tail++;
            }
        }
    }
    free(queue);
    free(seen.keys);
    return free_;
}

static int is_escape_possible(const int64_t (*blocked)[2], int n, int64_t sx, int64_t sy, int64_t tx, int64_t ty) {
    const int64_t side = 1000000;
    set_t walls;
    set_init(&walls, 16);
    for (int i = 0; i < n; i++) set_add(&walls, blocked[i][0] * side + blocked[i][1]);
    int answer = not_fenced(&walls, sx, sy, tx, ty, side) && not_fenced(&walls, tx, ty, sx, sy, side);
    free(walls.keys);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int rounds = 4;
    int64_t seed = 1036;
    static int64_t blocked[30][200][2];
    int64_t ends[30][4];
    for (int k = 0; k < 30; k++) {
        int64_t cx = next_random(&seed) % 900000 + 50000;
        int64_t cy = next_random(&seed) % 900000 + 50000;
        if (k % 3 == 2) {
            for (int i = 0; i < 200; i++) {
                blocked[k][i][0] = i;
                blocked[k][i][1] = 199 - i;
            }
            ends[k][0] = 200; ends[k][1] = 0; ends[k][2] = cx; ends[k][3] = cy;
        } else {
            for (int i = 0; i < 50; i++) {
                int64_t *b = blocked[k][4 * i];
                b[0] = cx + i; b[1] = cy + 50 - i;
                b[2] = cx + 50 - i; b[3] = cy - i;
                b[4] = cx - i; b[5] = cy - 50 + i;
                b[6] = cx - 50 + i; b[7] = cy + i;
            }
            if (k % 3 == 0) {
                ends[k][0] = cx + 10; ends[k][1] = cy - 10; ends[k][2] = 0; ends[k][3] = 0;
            } else {
                ends[k][0] = cx + 60; ends[k][1] = cy; ends[k][2] = 999999; ends[k][3] = 999999;
            }
        }
    }
    int escapes = 0;
    int64_t check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < 30; k++) {
            int answer = is_escape_possible((const int64_t (*)[2])blocked[k], 200, ends[k][0], ends[k][1], ends[k][2], ends[k][3]);
            if (answer) escapes++;
            check = (check * 131 + (answer ? 2 : 1)) % 1000000007;
        }
    }
    printf("30 mazes of 200 blocks, %d rounds: %d escapes, checksum %lld\n", rounds, escapes, (long long)check);
    return 0;
}
