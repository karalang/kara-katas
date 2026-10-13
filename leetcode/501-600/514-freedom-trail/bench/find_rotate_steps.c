// Benchmark for #514: C mirror of the ★ arm (a cost per position of the
// current letter); see find_rotate_steps.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

static Vec clone(const Vec *v) {
    Vec c = {NULL, 0, 0};
    for (int64_t i = 0; i < v->len; i++) push(&c, v->data[i]);
    return c;
}

static int64_t find_rotate_steps(const char *r, int64_t n, const char *key, int64_t m) {
    Vec at[26];
    memset(at, 0, sizeof at);
    for (int64_t j = 0; j < n; j++) push(&at[r[j] - 'a'], j);
    Vec prev_pos = {NULL, 0, 0}, prev_cost = {NULL, 0, 0};
    push(&prev_pos, 0);
    push(&prev_cost, 0);
    for (int64_t c = 0; c < m; c++) {
        Vec pos = clone(&at[key[c] - 'a']);
        Vec cost = {NULL, 0, 0};
        for (int64_t a = 0; a < pos.len; a++) {
            int64_t q = pos.data[a];
            int64_t best = INT64_MAX;
            for (int64_t i = 0; i < prev_pos.len; i++) {
                int64_t d = llabs(prev_pos.data[i] - q);
                int64_t s = prev_cost.data[i] + (d < n - d ? d : n - d);
                if (s < best) best = s;
            }
            push(&cost, best);
        }
        free(prev_pos.data);
        free(prev_cost.data);
        prev_pos = pos;
        prev_cost = cost;
    }
    int64_t fewest = INT64_MAX;
    for (int64_t i = 0; i < prev_cost.len; i++)
        if (prev_cost.data[i] < fewest) fewest = prev_cost.data[i];
    free(prev_pos.data);
    free(prev_cost.data);
    for (int i = 0; i < 26; i++) free(at[i].data);
    return fewest + m;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 400 random rings of 300 letters from all 26, each with a key of
    // 2,000 letters drawn from the ring, solved once each.
    int64_t seed = 514, rings = 400, total = 0, checksum = 0;
    char ring[300], key[2000];
    for (int64_t t = 0; t < rings; t++) {
        for (int i = 0; i < 300; i++) ring[i] = 'a' + next_random(&seed) % 26;
        for (int i = 0; i < 2000; i++) key[i] = ring[next_random(&seed) % 300];
        int64_t steps = find_rotate_steps(ring, 300, key, 2000);
        total += steps;
        checksum = (checksum * 31 + steps) % 1000000007;
    }
    printf("%lld rings of 300 letters, keys of 2000: %lld steps in all, checksum %lld\n",
           (long long)rings, (long long)total, (long long)checksum);
    return 0;
}
