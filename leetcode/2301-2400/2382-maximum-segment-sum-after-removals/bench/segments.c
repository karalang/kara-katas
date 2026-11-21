// LeetCode #2382: Maximum Segment Sum After Removals -- the bench, the ★
// arm in C: the removals undone in reverse with a union-find, each root
// keeping its segment's sum. The tables and the answer are allocated in
// each call, as the other languages' are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t find(int64_t *parent, int64_t x) {
    int64_t root = x;
    while (parent[root] != root) {
        parent[root] = parent[parent[root]];
        root = parent[root];
    }
    return root;
}

static void join(int64_t *parent, int64_t *sum, int64_t a, int64_t b) {
    int64_t ra = find(parent, a);
    int64_t rb = find(parent, b);
    if (ra != rb) {
        parent[ra] = rb;
        sum[rb] += sum[ra];
    }
}

static int64_t *maximum_segment_sum(const int64_t *nums, const int64_t *remove_queries, int64_t n) {
    int64_t *parent = malloc(n * sizeof(int64_t));
    int64_t *sum = calloc(n, sizeof(int64_t));
    char *back = calloc(n, 1);
    int64_t *answer = calloc(n, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        parent[i] = i;
    }
    int64_t best = 0;
    for (int64_t k = n - 1; k >= 1; k--) {
        int64_t x = remove_queries[k];
        back[x] = 1;
        sum[x] = nums[x];
        if (x > 0 && back[x - 1]) {
            join(parent, sum, x - 1, x);
        }
        if (x + 1 < n && back[x + 1]) {
            join(parent, sum, x + 1, x);
        }
        int64_t s = sum[find(parent, x)];
        if (s > best) {
            best = s;
        }
        answer[k - 1] = best;
    }
    free(parent);
    free(sum);
    free(back);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t high = next_random(seed);
    return high * 32768 + next_random(seed);
}

static int64_t arrays[10][N];
static int64_t orders[10][N];

int main(void) {
    // 10 arrays of 10^5 values, array a's values from 1 to 10^a, each with
    // its own random order of removals
    int64_t seed = 2382;
    for (int a = 0; a < 10; a++) {
        int64_t top = 1;
        for (int k = 0; k < a; k++) {
            top *= 10;
        }
        for (int i = 0; i < N; i++) {
            arrays[a][i] = 1 + wide(&seed) % top;
        }
        for (int i = 0; i < N; i++) {
            orders[a][i] = i;
        }
        for (int64_t i = N - 1; i >= 1; i--) {
            int64_t j = wide(&seed) % (i + 1);
            int64_t t = orders[a][i];
            orders[a][i] = orders[a][j];
            orders[a][j] = t;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++) {
        for (int a = 0; a < 10; a++) {
            int64_t *answer = maximum_segment_sum(arrays[a], orders[a], N);
            for (int i = 0; i < N; i++) {
                check = (check * 31 + answer[i] + p) % 1000000007;
            }
            free(answer);
        }
    }
    printf("10 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    return 0;
}
