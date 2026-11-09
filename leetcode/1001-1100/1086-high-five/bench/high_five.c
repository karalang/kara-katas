// Benchmark: LeetCode #1086 High Five -- mirrors high_five.kara: the
// scores grouped by student in an ordered map (here an array of groups
// kept sorted by id, found by binary search), each student's scores
// copied and sorted high to low and the first five averaged, over 200
// lists of 1000 items built once.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t id;
    int64_t *v;
    int64_t n, cap;
} Group;

static int desc(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (y > x) - (y < x);
}

// Writes [id, average] pairs into out; returns how many students.
static int64_t high_five(const int64_t (*items)[2], int64_t n, int64_t (*out)[2]) {
    Group *groups = malloc(sizeof(Group) * (size_t)(n ? n : 1));
    int64_t ng = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t id = items[i][0];
        int64_t lo = 0, hi = ng;
        while (lo < hi) {
            int64_t mid = (lo + hi) / 2;
            if (groups[mid].id < id) lo = mid + 1; else hi = mid;
        }
        if (lo == ng || groups[lo].id != id) {
            memmove(&groups[lo + 1], &groups[lo], sizeof(Group) * (size_t)(ng - lo));
            groups[lo].id = id;
            groups[lo].cap = 4;
            groups[lo].n = 0;
            groups[lo].v = malloc(sizeof(int64_t) * 4);
            ng++;
        }
        Group *g = &groups[lo];
        if (g->n == g->cap) {
            g->cap *= 2;
            g->v = realloc(g->v, sizeof(int64_t) * (size_t)g->cap);
        }
        g->v[g->n++] = items[i][1];
    }
    for (int64_t k = 0; k < ng; k++) {
        Group *g = &groups[k];
        int64_t *sorted = malloc(sizeof(int64_t) * (size_t)g->n);
        memcpy(sorted, g->v, sizeof(int64_t) * (size_t)g->n);
        qsort(sorted, (size_t)g->n, sizeof(int64_t), desc);
        int64_t top = 0;
        for (int64_t j = 0; j < 5 && j < g->n; j++) top += sorted[j];
        out[k][0] = g->id;
        out[k][1] = top / 5;
        free(sorted);
        free(g->v);
    }
    free(groups);
    return ng;
}

static int64_t seed = 1086;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t lists[200][1000][2];

int main(void) {
    int64_t rounds = 50;
    for (int64_t t = 0; t < 200; t++) {
        int64_t k = 50 + t % 150;
        int64_t ids[200];
        int64_t nids = 0;
        char taken[1001] = {0};
        while (nids < k) {
            int64_t id = next_random() % 1000 + 1;
            if (!taken[id]) {
                taken[id] = 1;
                ids[nids++] = id;
            }
        }
        for (int64_t i = 0; i < 1000; i++) {
            int64_t id = i < 5 * k ? ids[i % k] : ids[next_random() % k];
            lists[t][i][0] = id;
            lists[t][i][1] = next_random() % 101;
        }
        for (int64_t i = 999; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t a = lists[t][i][0], b = lists[t][i][1];
            lists[t][i][0] = lists[t][j][0];
            lists[t][i][1] = lists[t][j][1];
            lists[t][j][0] = a;
            lists[t][j][1] = b;
        }
    }
    int64_t students = 0, check = 0;
    static int64_t out[1000][2];
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 200; i++) {
            int64_t m = high_five(lists[(r * 7 + i) % 200], 1000, out);
            students += m;
            for (int64_t j = 0; j < m; j++) check = (check * 31 + out[j][0] * 101 + out[j][1]) % 1000000007;
        }
    }
    printf("%lld rounds over 200 lists of 1000 items: %lld students, checksum %lld\n", (long long)rounds,
           (long long)students, (long long)check);
    return 0;
}
