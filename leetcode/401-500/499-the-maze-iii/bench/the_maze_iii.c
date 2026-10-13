// Benchmark for #499: C mirror of the ★ arm (Dijkstra over the places
// the ball stops); see the_maze_iii.kara. The queue is a binary min-heap
// of (distance, instructions, row, column), compared in that order with
// strcmp for the instructions; each pushed entry owns a fresh
// heap-allocated copy of its instructions, as each Kāra entry owns its
// String.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100
#define MAZES 1000

typedef struct {
    int64_t dist;
    char *path;
    int row, col;
} Entry;

typedef struct {
    Entry *items;
    int64_t len, cap;
} Heap;

static int less(const Entry *a, const Entry *b) {
    if (a->dist != b->dist) {
        return a->dist < b->dist;
    }
    int k = strcmp(a->path, b->path);
    if (k != 0) {
        return k < 0;
    }
    if (a->row != b->row) {
        return a->row < b->row;
    }
    return a->col < b->col;
}

static void heap_push(Heap *h, Entry e) {
    if (h->len == h->cap) {
        h->cap = h->cap ? h->cap * 2 : 16;
        h->items = realloc(h->items, h->cap * sizeof(Entry));
    }
    int64_t i = h->len++;
    h->items[i] = e;
    while (i > 0) {
        int64_t parent = (i - 1) / 2;
        if (!less(&h->items[i], &h->items[parent])) {
            break;
        }
        Entry t = h->items[i];
        h->items[i] = h->items[parent];
        h->items[parent] = t;
        i = parent;
    }
}

static Entry heap_pop(Heap *h) {
    Entry top = h->items[0];
    h->items[0] = h->items[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < h->len && less(&h->items[l], &h->items[m])) {
            m = l;
        }
        if (r < h->len && less(&h->items[r], &h->items[m])) {
            m = r;
        }
        if (m == i) {
            break;
        }
        Entry t = h->items[i];
        h->items[i] = h->items[m];
        h->items[m] = t;
        i = m;
    }
    return top;
}

static char *extend(const char *path, char name) {
    size_t n = strlen(path);
    char *out = malloc(n + 2);
    memcpy(out, path, n);
    out[n] = name;
    out[n + 1] = 0;
    return out;
}

// Returns the instructions, which the caller frees, or NULL when the
// hole cannot be reached.
static char *find_shortest_way(int8_t maze[N][N], int br, int bc, int hr, int hc) {
    static const int dr[4] = {1, 0, 0, -1};
    static const int dc[4] = {0, -1, 1, 0};
    static const char names[4] = {'d', 'l', 'r', 'u'};
    static uint8_t done[N][N];
    memset(done, 0, sizeof(done));
    Heap h = {0};
    char *start = malloc(1);
    start[0] = 0;
    heap_push(&h, (Entry){0, start, br, bc});
    char *answer = NULL;
    while (h.len > 0) {
        Entry e = heap_pop(&h);
        if (done[e.row][e.col]) {
            free(e.path);
            continue;
        }
        done[e.row][e.col] = 1;
        if (e.row == hr && e.col == hc) {
            answer = e.path;
            break;
        }
        for (int k = 0; k < 4; k++) {
            int r = e.row, c = e.col;
            int64_t steps = 0;
            while (r + dr[k] >= 0 && r + dr[k] < N && c + dc[k] >= 0 && c + dc[k] < N && maze[r + dr[k]][c + dc[k]] == 0) {
                r += dr[k];
                c += dc[k];
                steps++;
                if (r == hr && c == hc) {
                    break;
                }
            }
            if (steps > 0 && !done[r][c]) {
                heap_push(&h, (Entry){e.dist + steps, extend(e.path, names[k]), r, c});
            }
        }
        free(e.path);
    }
    for (int64_t i = 0; i < h.len; i++) {
        free(h.items[i].path);
    }
    free(h.items);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 1,000 mazes of 100 by 100 (the problem's most), a wall in each
    // cell with odds of 1 in 4, with a ball and a hole in two different
    // open cells, built once. Then each is solved once.
    static int8_t all[MAZES][N][N];
    static int balls[MAZES][2], holes[MAZES][2];
    static int open[N * N][2];
    int64_t seed = 499;
    for (int k = 0; k < MAZES; k++) {
        int64_t count = 0;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (next_random(&seed) % 4 == 0) {
                    all[k][r][c] = 1;
                } else {
                    all[k][r][c] = 0;
                    open[count][0] = r;
                    open[count][1] = c;
                    count++;
                }
            }
        }
        int64_t a = next_random(&seed) % count;
        int64_t b = next_random(&seed) % (count - 1);
        if (b >= a) {
            b++;
        }
        balls[k][0] = open[a][0];
        balls[k][1] = open[a][1];
        holes[k][0] = open[b][0];
        holes[k][1] = open[b][1];
    }
    int64_t reached = 0, letters = 0, checksum = 0;
    for (int k = 0; k < MAZES; k++) {
        char *way = find_shortest_way(all[k], balls[k][0], balls[k][1], holes[k][0], holes[k][1]);
        const char *text = way ? way : "impossible";
        if (way) {
            reached++;
            letters += (int64_t)strlen(way);
        }
        for (const char *p = text; *p; p++) {
            checksum = (checksum * 31 + *p) % 1000000007;
        }
        free(way);
    }
    printf("%d mazes of 100 by 100: the hole reached in %lld, %lld instructions in all, checksum %lld\n", MAZES, (long long)reached, (long long)letters, (long long)checksum);
    return 0;
}
