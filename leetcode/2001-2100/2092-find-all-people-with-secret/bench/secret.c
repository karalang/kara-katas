// LeetCode #2092: Find All People With Secret -- C mirror of the ★ arm's
// benchmark (secret.kara): the same 10 gatherings, each answered 4 times by
// the same stable sort and union-find, the copy, parents and answer in
// `malloc`'d buffers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000
#define M 100000

typedef struct {
    int64_t x, y, t;
} Meeting;

static int64_t seed = 2092;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t find(int64_t *parent, int64_t x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

// a stable merge sort by time, as the other languages' sort_by_key is
static void sort_by_time(Meeting *a, Meeting *tmp, int64_t n) {
    for (int64_t w = 1; w < n; w *= 2) {
        for (int64_t lo = 0; lo < n; lo += 2 * w) {
            int64_t mid = lo + w < n ? lo + w : n, hi = lo + 2 * w < n ? lo + 2 * w : n;
            int64_t i = lo, j = mid, k = lo;
            while (i < mid && j < hi) tmp[k++] = a[j].t < a[i].t ? a[j++] : a[i++];
            while (i < mid) tmp[k++] = a[i++];
            while (j < hi) tmp[k++] = a[j++];
        }
        memcpy(a, tmp, n * sizeof(Meeting));
    }
}

static int64_t *find_all_people(int64_t n, const Meeting *meetings, int64_t m, int64_t first, int64_t *len) {
    Meeting *s = malloc(m * sizeof(Meeting)), *tmp = malloc(m * sizeof(Meeting));
    memcpy(s, meetings, m * sizeof(Meeting));
    sort_by_time(s, tmp, m);
    free(tmp);
    int64_t *parent = malloc(n * sizeof(int64_t));
    for (int64_t p = 0; p < n; p++) parent[p] = p;
    parent[first] = 0;
    int64_t i = 0;
    while (i < m) {
        int64_t j = i;
        while (j < m && s[j].t == s[i].t) {
            int64_t rx = find(parent, s[j].x), ry = find(parent, s[j].y);
            if (rx < ry) parent[ry] = rx;
            else parent[rx] = ry;
            j++;
        }
        for (int64_t k = i; k < j; k++) {
            if (find(parent, s[k].x) != 0) parent[s[k].x] = s[k].x;
            if (find(parent, s[k].y) != 0) parent[s[k].y] = s[k].y;
        }
        i = j;
    }
    int64_t *knows = malloc(n * sizeof(int64_t)), c = 0;
    for (int64_t p = 0; p < n; p++)
        if (find(parent, p) == 0) knows[c++] = p;
    free(parent);
    free(s);
    *len = c;
    return knows;
}

int main(void) {
    Meeting *gatherings = malloc((size_t)10 * M * sizeof(Meeting));
    for (int g = 0; g < 10; g++) {
        for (int k = 0; k < M; k++) {
            int64_t a = next_random(), b = next_random();
            int64_t x = (a * 32768 + b) % N;
            int64_t c = next_random(), d = next_random();
            int64_t y = (x + 1 + (c * 32768 + d) % (N - 1)) % N;
            Meeting mt = {x, y, next_random() % 1000 + 1};
            gatherings[(size_t)g * M + k] = mt;
        }
    }
    int64_t total = 0, check = 0;
    for (int round = 0; round < 4; round++) {
        for (int g = 0; g < 10; g++) {
            int64_t len;
            int64_t *got = find_all_people(N, gatherings + (size_t)g * M, M, round * 10 + g + 1, &len);
            total += len;
            for (int64_t k = 0; k < len; k++) check = (check * 31 + got[k]) % 1000000007;
            free(got);
        }
    }
    printf("40 answers: %lld people, checksum %lld\n", (long long)total, (long long)check);
    free(gatherings);
    return 0;
}
