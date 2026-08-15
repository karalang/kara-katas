/* Benchmark workload for LeetCode #275 — H-Index II.
 *
 * Algorithm-for-algorithm mirror of hsearch.kara. See that file's header for
 * what this lane measures and why the array is sized at 2 MiB. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t h_index_prefix(const int64_t *citations, int64_t n) {
    int64_t lo = 0, hi = n;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (citations[mid] >= n - mid) hi = mid;
        else lo = mid + 1;
    }
    return n - lo;
}

int main(void) {
    const int64_t size = 262144;
    const int64_t queries = 6000000;

    int64_t *citations = malloc((size_t)size * sizeof(int64_t));
    int64_t state = 275275, cur = 0;
    for (int64_t i = 0; i < size; i++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        cur += (state / 256) % 3;
        citations[i] = cur;
    }
    int64_t top = citations[size - 1];

    int64_t sink = 0;
    for (int64_t q = 0; q < queries; q++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        int64_t n = 1 + (state / 256) % size;
        sink = (sink * 131 + h_index_prefix(citations, n)) % 1000000007;
    }

    printf("%lld\n", (long long)sink);
    printf("size %lld queries %lld top %lld\n",
           (long long)size, (long long)queries, (long long)top);
    free(citations);
    return 0;
}
