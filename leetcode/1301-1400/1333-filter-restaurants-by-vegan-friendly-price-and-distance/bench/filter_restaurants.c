// LeetCode #1333 bench, C mirror of the Kāra bench: the ★ arm on 20 lists
// of 10^4 restaurants built once, then 100 passes, each setting one rating
// of every list from the checksum so far and drawing the filters from it
// too, answering every list.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int32_t rating;
    int32_t id;
} Pair;

static int by_rating_then_id(const void *x, const void *y) {
    const Pair *a = x;
    const Pair *b = y;
    if (a->rating != b->rating) {
        return a->rating < b->rating ? 1 : -1;
    }
    if (a->id != b->id) {
        return a->id < b->id ? 1 : -1;
    }
    return 0;
}

// the ids written into out, their count returned
static size_t filter_restaurants(int32_t (*restaurants)[5], size_t n, int32_t vegan_friendly, int32_t max_price,
                                 int32_t max_distance, int32_t *out) {
    Pair *kept = malloc(sizeof(Pair) * n);
    size_t k = 0;
    for (size_t i = 0; i < n; i++) {
        int32_t *r = restaurants[i];
        if ((vegan_friendly == 0 || r[2] == 1) && r[3] <= max_price && r[4] <= max_distance) {
            kept[k].rating = r[1];
            kept[k].id = r[0];
            k++;
        }
    }
    qsort(kept, k, sizeof(Pair), by_rating_then_id);
    for (size_t i = 0; i < k; i++) {
        out[i] = kept[i].id;
    }
    free(kept);
    return k;
}

static int64_t seed = 1333;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 10000;
    int32_t (*lists[20])[5];
    for (int t = 0; t < 20; t++) {
        lists[t] = malloc(sizeof(int32_t[5]) * n);
        for (int64_t i = 0; i < n; i++) {
            lists[t][i][0] = (int32_t)(i * 10 + 1 + next_random() % 10);
            lists[t][i][1] = (int32_t)(1 + next_random() % 100000);
            lists[t][i][2] = (int32_t)(next_random() % 2);
            lists[t][i][3] = (int32_t)(1 + next_random() % 100000);
            lists[t][i][4] = (int32_t)(1 + next_random() % 100000);
        }
    }
    int32_t *ids = malloc(sizeof(int32_t) * n);
    int64_t check = 0;
    for (int64_t pass = 0; pass < 100; pass++) {
        int32_t vegan = (int32_t)(pass % 2);
        int32_t max_price = (int32_t)(50000 + check % 50001);
        int32_t max_distance = (int32_t)(50000 + check / 7 % 50001);
        for (int t = 0; t < 20; t++) {
            int64_t at = check % n;
            lists[t][at][1] = (int32_t)(1 + check / 3 % 100000);
            size_t k = filter_restaurants(lists[t], n, vegan, max_price, max_distance, ids);
            check = (check * 31 + (int64_t)k + ids[0] + ids[k / 2] + pass) % 1000000007;
        }
    }
    printf("100 passes over 20 lists of 10^4: checksum %lld\n", (long long)check);
    for (int t = 0; t < 20; t++) {
        free(lists[t]);
    }
    free(ids);
    return 0;
}
