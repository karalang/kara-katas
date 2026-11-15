// LeetCode #1574: Shortest Subarray to be Removed to Make Array Sorted --
// bench: the ★ arm (a sorted prefix joined to a sorted suffix by two
// pointers) over 20 arrays of 500000 values, each a rising first half, a
// stretch of random values and a rising second half that starts low, built
// once; then 3 rounds answering all 20, 60 answers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t shortest(const int64_t *arr, int64_t n) {
    int64_t left = 0;
    while (left + 1 < n && arr[left] <= arr[left + 1]) {
        left++;
    }
    if (left == n - 1) {
        return 0;
    }
    int64_t right = n - 1;
    while (right > 0 && arr[right - 1] <= arr[right]) {
        right--;
    }
    int64_t best = min64(n - left - 1, right);
    int64_t j = right;
    for (int64_t i = 0; i < left + 1; i++) {
        while (j < n && arr[j] < arr[i]) {
            j++;
        }
        best = min64(best, j - i - 1);
    }
    return best;
}

static int64_t seed = 1574;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    const int64_t n = 500000;
    int64_t *arrays[20];
    for (int a = 0; a < 20; a++) {
        int64_t middle = next_random() % 1000 + 1;
        int64_t start = (n - middle) / 2;
        int64_t *arr = malloc(sizeof(int64_t) * n);
        int64_t v = 0;
        for (int64_t i = 0; i < n; i++) {
            if (i == start + middle) {
                v = next_random() % 1000;
            }
            if (i >= start && i < start + middle) {
                arr[i] = next_random() % 4000000;
            } else {
                v += next_random() % 8;
                arr[i] = v;
            }
        }
        arrays[a] = arr;
    }
    int64_t check = 0, total = 0;
    for (int r = 0; r < 3; r++) {
        for (int a = 0; a < 20; a++) {
            int64_t length = shortest(arrays[a], n);
            total += length;
            check = mix(check, length);
        }
    }
    printf("60 answers over 20 arrays of %lld values: lengths total %lld, checksum %lld\n", (long long)n,
           (long long)total, (long long)check);
    for (int a = 0; a < 20; a++) {
        free(arrays[a]);
    }
    return 0;
}
