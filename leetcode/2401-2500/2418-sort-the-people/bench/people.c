// LeetCode #2418: Sort the People -- the bench, the ★ arm in C: the
// indexes sorted by height, tallest first, and each index's name read out.
// The sort is a stable merge sort, as Kāra's and Rust's `sort_by` are;
// the names are copied out, as the other languages' are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define GROUPS 10
#define PEOPLE 1000

static const int64_t *key;

static void merge_sort(int64_t *a, int64_t *tmp, int n) {
    if (n < 2) return;
    int h = n / 2;
    merge_sort(a, tmp, h);
    merge_sort(a + h, tmp, n - h);
    int i = 0, j = h, k = 0;
    while (i < h && j < n) tmp[k++] = key[a[j]] > key[a[i]] ? a[j++] : a[i++];
    while (i < h) tmp[k++] = a[i++];
    while (j < n) tmp[k++] = a[j++];
    memcpy(a, tmp, sizeof(int64_t) * n);
}

static char **sort_people(char **names, const int64_t *heights, int n) {
    int64_t *order = malloc(sizeof(int64_t) * n), *tmp = malloc(sizeof(int64_t) * n);
    for (int i = 0; i < n; i++) order[i] = i;
    key = heights;
    merge_sort(order, tmp, n);
    char **sorted = malloc(sizeof(char *) * n);
    for (int i = 0; i < n; i++) sorted[i] = strdup(names[order[i]]);
    free(order);
    free(tmp);
    return sorted;
}

static int64_t seed = 2418;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    // 10 groups of 1000 people, names of 1 to 20 letters, distinct heights
    // up to 10^5; each pass sorts every group and folds the first letter
    // of every name, plus the pass
    static char *names[GROUPS][PEOPLE];
    static int64_t heights[GROUPS][PEOPLE];
    int64_t *pool = malloc(sizeof(int64_t) * 100000);
    for (int g = 0; g < GROUPS; g++) {
        for (int k = 0; k < PEOPLE; k++) {
            int64_t len = 1 + next_random() % 20;
            char *s = malloc(len + 1);
            for (int64_t c = 0; c < len; c++) s[c] = (char)('a' + next_random() % 26);
            s[len] = 0;
            names[g][k] = s;
        }
        for (int i = 0; i < 100000; i++) pool[i] = i + 1;
        for (int64_t i = 0; i < PEOPLE; i++) {
            int64_t a = next_random();
            int64_t j = i + (a * 32768 + next_random()) % (100000 - i);
            int64_t t = pool[i];
            pool[i] = pool[j];
            pool[j] = t;
        }
        memcpy(heights[g], pool, sizeof(int64_t) * PEOPLE);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 500; p++) {
        for (int g = 0; g < GROUPS; g++) {
            char **sorted = sort_people(names[g], heights[g], PEOPLE);
            for (int k = 0; k < PEOPLE; k++) {
                check = (check * 31 + (unsigned char)sorted[k][0] + p) % 1000000007;
                free(sorted[k]);
            }
            free(sorted);
        }
    }
    printf("500 passes over 10 groups of 1000 people: checksum %lld\n", (long long)check);
    return 0;
}
