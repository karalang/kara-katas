// LeetCode #1792: Maximum Average Pass Ratio -- the bench in C: the ★ arm
// over 200 random lists of 1000 classes built once, 4000 calls. A binary
// max-heap of (gain, class), ties to the larger class.
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { double g; int64_t i; } Entry;

static int above(Entry a, Entry b) { return a.g > b.g || (a.g == b.g && a.i > b.i); }

static void push(Entry *h, int *len, Entry e) {
    int k = (*len)++;
    h[k] = e;
    while (k > 0) {
        int up = (k - 1) / 2;
        if (!above(h[k], h[up])) break;
        Entry s = h[k]; h[k] = h[up]; h[up] = s;
        k = up;
    }
}

static Entry pop(Entry *h, int *len) {
    Entry top = h[0];
    h[0] = h[--(*len)];
    int k = 0;
    for (;;) {
        int l = 2 * k + 1, r = l + 1, m = k;
        if (l < *len && above(h[l], h[m])) m = l;
        if (r < *len && above(h[r], h[m])) m = r;
        if (m == k) break;
        Entry s = h[k]; h[k] = h[m]; h[m] = s;
        k = m;
    }
    return top;
}

static double gain(int64_t p, int64_t t) { return (double)(p + 1) / (double)(t + 1) - (double)p / (double)t; }

static double max_average_ratio(const int32_t (*classes)[2], int n, int32_t extra) {
    int64_t *pass = malloc(n * sizeof(int64_t)), *total = malloc(n * sizeof(int64_t));
    Entry *heap = malloc(n * sizeof(Entry));
    int len = 0;
    for (int i = 0; i < n; i++) {
        pass[i] = classes[i][0];
        total[i] = classes[i][1];
    }
    for (int i = 0; i < n; i++) push(heap, &len, (Entry){gain(pass[i], total[i]), i});
    for (int32_t s = 0; s < extra; s++) {
        int64_t i = pop(heap, &len).i;
        pass[i]++;
        total[i]++;
        push(heap, &len, (Entry){gain(pass[i], total[i]), i});
    }
    double sum = 0.0;
    for (int i = 0; i < n; i++) sum += (double)pass[i] / (double)total[i];
    free(pass); free(total); free(heap);
    return sum / n;
}

static int64_t seed = 1792;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t lists[200][1000][2];
    for (int l = 0; l < 200; l++)
        for (int c = 0; c < 1000; c++) {
            int64_t t = 1 + next_random() % 1000;
            int64_t p = 1 + next_random() % t;
            lists[l][c][0] = (int32_t)p;
            lists[l][c][1] = (int32_t)t;
        }
    int64_t check = 0;
    for (int64_t call = 0; call < 4000; call++) {
        int64_t extra = 1 + check % 1000;
        double r = max_average_ratio(lists[(check + call) % 200], 1000, (int32_t)extra);
        check = (check * 31 + (int64_t)floor(r * 100000.0 + 0.5)) % 1000000007;
    }
    printf("4000 calls over 200 lists of 1000 classes: checksum %lld\n", (long long)check);
    return 0;
}
