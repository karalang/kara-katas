// LeetCode #2070: Most Beautiful Item for Each Query -- C mirror of the ★
// arm's benchmark (beauty.kara): 20 shops of 100000 items and 100000
// queries each, prices, beauties and queries up to 10^9. The items are
// pairs in one array; the sort is a stable merge sort by price, as Kāra's
// `sort_by_key` is stable.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t price, beauty; } Item;

static void merge_sort(Item *a, Item *tmp, size_t n) {
    if (n < 2) return;
    size_t h = n / 2;
    merge_sort(a, tmp, h);
    merge_sort(a + h, tmp, n - h);
    size_t i = 0, j = h, k = 0;
    while (i < h && j < n) tmp[k++] = a[j].price < a[i].price ? a[j++] : a[i++];
    while (i < h) tmp[k++] = a[i++];
    while (j < n) tmp[k++] = a[j++];
    memcpy(a, tmp, n * sizeof(Item));
}

static void maximum_beauty(const Item *items, size_t n, const int64_t *queries, size_t m, int64_t *out) {
    Item *s = malloc(n * sizeof(Item)), *tmp = malloc(n * sizeof(Item));
    memcpy(s, items, n * sizeof(Item));
    merge_sort(s, tmp, n);
    int64_t *best = malloc(n * sizeof(int64_t)), most = 0;
    for (size_t i = 0; i < n; i++) {
        if (s[i].beauty > most) most = s[i].beauty;
        best[i] = most;
    }
    for (size_t k = 0; k < m; k++) {
        size_t lo = 0, hi = n;
        while (lo < hi) {
            size_t mid = lo + (hi - lo) / 2;
            if (s[mid].price <= queries[k]) lo = mid + 1; else hi = mid;
        }
        out[k] = lo == 0 ? 0 : best[lo - 1];
    }
    free(s); free(tmp); free(best);
}

static int64_t seed = 2070;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t up_to(int64_t top) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % top + 1;
}

int main(void) {
    size_t n = 100000;
    Item *items = malloc(n * sizeof(Item));
    int64_t *queries = malloc(n * sizeof(int64_t)), *out = malloc(n * sizeof(int64_t));
    int64_t sum = 0, check = 0;
    for (int s = 0; s < 20; s++) {
        for (size_t i = 0; i < n; i++) {
            items[i].price = up_to(1000000000);
            items[i].beauty = up_to(1000000000);
        }
        for (size_t i = 0; i < n; i++) queries[i] = up_to(1000000000);
        maximum_beauty(items, n, queries, n, out);
        for (size_t i = 0; i < n; i++) {
            sum += out[i];
            check = (check * 31 + out[i]) % 1000000007;
        }
    }
    printf("20 shops: sum %lld, checksum %lld\n", (long long)sum, (long long)check);
    free(items); free(queries); free(out);
    return 0;
}
