// Benchmark for #489: C mirror of the ★ arm (backtracking); see
// robot_room_cleaner.kara. C has no hash set, so the visited cells (in
// the robot's own coordinates, which can be negative) are an
// open-addressing table written out here.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100

static const long long STEP[4][2] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};

typedef struct {
    long long *room, *cleaned; // N * N each, copied in
    long long row, col, calls, budget;
    int facing;
} Robot;

static int forward(Robot *b) {
    b->calls++;
    if (b->calls > b->budget) {
        return 0;
    }
    long long r = b->row + STEP[b->facing][0], c = b->col + STEP[b->facing][1];
    if (r < 0 || r >= N || c < 0 || c >= N || b->room[r * N + c] == 0) {
        return 0;
    }
    b->row = r;
    b->col = c;
    return 1;
}

static void turn_right(Robot *b) {
    b->calls++;
    if (b->calls <= b->budget) {
        b->facing = (b->facing + 1) % 4;
    }
}

static void clean(Robot *b) {
    b->calls++;
    if (b->calls <= b->budget) {
        b->cleaned[b->row * N + b->col]++;
    }
}

typedef struct {
    long long *keys; // packed (row, col); EMPTY marks a free slot
    long long capacity, size;
} Visited;

#define EMPTY (-4611686018427387904LL) // -2^62, no cell packs to it

static long long pack(long long row, long long col) {
    return row * 1000003 + col;
}

static void visited_init(Visited *v, long long capacity) {
    v->capacity = capacity;
    v->size = 0;
    v->keys = malloc(sizeof(long long) * capacity);
    for (long long k = 0; k < capacity; k++) {
        v->keys[k] = EMPTY;
    }
}

static long long slot(const Visited *v, long long key) {
    unsigned long long h = (unsigned long long)key * 0x9E3779B97F4A7C15ULL;
    long long at = (long long)(h >> 20) & (v->capacity - 1);
    while (v->keys[at] != EMPTY && v->keys[at] != key) {
        at = (at + 1) & (v->capacity - 1);
    }
    return at;
}

static int contains(const Visited *v, long long key) {
    return v->keys[slot(v, key)] == key;
}

static void insert(Visited *v, long long key) {
    if (2 * (v->size + 1) > v->capacity) {
        Visited bigger;
        visited_init(&bigger, v->capacity * 2);
        for (long long k = 0; k < v->capacity; k++) {
            if (v->keys[k] != EMPTY) {
                bigger.keys[slot(&bigger, v->keys[k])] = v->keys[k];
                bigger.size++;
            }
        }
        free(v->keys);
        *v = bigger;
    }
    long long at = slot(v, key);
    if (v->keys[at] != key) {
        v->keys[at] = key;
        v->size++;
    }
}

static void explore(Robot *robot, long long row, long long col, int facing, Visited *visited) {
    insert(visited, pack(row, col));
    clean(robot);
    int d = facing;
    for (int i = 0; i < 4; i++) {
        long long nr = row + STEP[d][0], nc = col + STEP[d][1];
        if (!contains(visited, pack(nr, nc)) && forward(robot)) {
            explore(robot, nr, nc, d, visited);
            turn_right(robot);
            turn_right(robot);
            forward(robot);
            turn_right(robot);
            turn_right(robot);
        }
        turn_right(robot);
        d = (d + 1) % 4;
    }
}

static void clean_room(Robot *robot) {
    Visited visited;
    visited_init(&visited, 1024);
    explore(robot, 0, 0, 0, &visited);
    free(visited.keys);
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    static long long rooms[300][N * N], starts[300][2];
    long long seed = 489;
    for (int k = 0; k < 300; k++) {
        for (int i = 0; i < N * N; i++) {
            rooms[k][i] = next_random(&seed) % 4 == 0 ? 0 : 1;
        }
        starts[k][0] = next_random(&seed) % N;
        starts[k][1] = next_random(&seed) % N;
        rooms[k][starts[k][0] * N + starts[k][1]] = 1;
    }
    long long total = 0, checksum = 0, cells = N * N;
    for (int k = 0; k < 300; k++) {
        Robot robot;
        robot.room = malloc(sizeof(long long) * cells);
        memcpy(robot.room, rooms[k], sizeof(long long) * cells);
        robot.cleaned = calloc(cells, sizeof(long long));
        robot.row = starts[k][0];
        robot.col = starts[k][1];
        robot.facing = 0;
        robot.calls = 0;
        robot.budget = 16 * cells * cells + 1000;
        clean_room(&robot);
        long long cleaned = 0;
        for (long long r = 0; r < N; r++) {
            for (long long c = 0; c < N; c++) {
                if (robot.cleaned[r * N + c] > 0) {
                    cleaned++;
                    checksum = (checksum * 31 + r * 100 + c) % 1000000007;
                }
            }
        }
        total += cleaned;
        checksum = (checksum * 31 + robot.calls) % 1000000007;
        free(robot.room);
        free(robot.cleaned);
    }
    printf("300 rooms of 100 by 100: %lld cells cleaned, checksum %lld\n", total, checksum);
    return 0;
}
