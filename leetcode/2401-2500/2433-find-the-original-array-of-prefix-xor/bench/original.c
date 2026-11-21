// LeetCode #2433: Find The Original Array of Prefix Xor -- the bench, the
// ★ arm: every value its prefix XOR the prefix before, the first its own
// prefix, gathered into a new list.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

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

static Vec find_array(const int64_t *pref, int64_t n) {
    Vec arr = {0, 0, 0};
    int64_t before = 0;
    for (int64_t i = 0; i < n; i++) {
        push(&arr, pref[i] ^ before);
        before = pref[i];
    }
    return arr;
}

static int64_t seed = 2433;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    int64_t *pref = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        int64_t a = next_random();
        pref[i] = (a * 32768 + next_random()) % 1000001;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 1000; p++) {
        pref[(p * 7919) % n] = p;
        Vec arr = find_array(pref, n);
        for (int64_t i = 0; i < arr.len; i++)
            check = (check * 31 + arr.data[i]) % 1000000007;
        free(arr.data);
    }
    printf("1000 passes over 10^5 prefixes: checksum %lld\n", (long long)check);
    free(pref);
    return 0;
}
