// LeetCode #2782: Number of Unique Categories -- the bench in C: the ★
// arm over 1000 sets of 100 elements from up to 100 categories, all
// drawn first, then each answered 100 times through the judge's handler,
// whose questions are counted.
#include <stdint.h>
#include <stdio.h>

#define COUNT 1000
#define N 100

static int64_t seed = 2782;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    int64_t categories[N];
    int64_t n;
    int64_t asked;
} CategoryHandler;

static int have_same_category(CategoryHandler *h, int64_t a, int64_t b) {
    h->asked++;
    return a >= 0 && b >= 0 && a < h->n && b < h->n && h->categories[a] == h->categories[b];
}

static int64_t number_of_categories(int64_t n, CategoryHandler *handler) {
    int64_t representatives[N], count = 0;
    for (int64_t i = 0; i < n; i++) {
        int found = 0;
        for (int64_t j = 0; j < count && !found; j++) found = have_same_category(handler, representatives[j], i);
        if (!found) representatives[count++] = i;
    }
    return count;
}

static CategoryHandler handlers[COUNT];

int main(void) {
    int rounds = 100;
    for (int c = 0; c < COUNT; c++) {
        int64_t k = next_random() % 100 + 1;
        for (int i = 0; i < N; i++) handlers[c].categories[i] = next_random() % k;
        handlers[c].n = N;
        handlers[c].asked = 0;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = number_of_categories(N, &handlers[c]);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    int64_t asked = 0;
    for (int c = 0; c < COUNT; c++) asked += handlers[c].asked;
    printf("%d sets of 100, %d rounds: categories sum to %lld after %lld questions, checksum %lld\n", COUNT, rounds, (long long)total, (long long)asked, (long long)check);
    return 0;
}
