// LeetCode #703 bench: the heap arm in C. See the .kara twin for the
// workload.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t k;
    int64_t *heap;
    int64_t len;
} KthLargest;

static int64_t add(KthLargest *s, int64_t val) {
    int64_t *h = s->heap;
    if (s->len < s->k) {
        h[s->len] = val;
        s->len += 1;
        int64_t i = s->len - 1;
        while (i > 0) {
            int64_t parent = (i - 1) / 2;
            if (h[parent] <= h[i]) {
                break;
            }
            int64_t t = h[parent];
            h[parent] = h[i];
            h[i] = t;
            i = parent;
        }
    } else if (val > h[0]) {
        h[0] = val;
        int64_t n = s->len;
        int64_t i = 0;
        for (;;) {
            int64_t left = 2 * i + 1;
            int64_t right = left + 1;
            int64_t least = i;
            if (left < n && h[left] < h[least]) {
                least = left;
            }
            if (right < n && h[right] < h[least]) {
                least = right;
            }
            if (least == i) {
                break;
            }
            int64_t t = h[least];
            h[least] = h[i];
            h[i] = t;
            i = least;
        }
    }
    return h[0];
}

static KthLargest make(int64_t k, const int64_t *nums, int64_t n) {
    KthLargest s = {k, malloc(sizeof(int64_t) * (size_t)k), 0};
    for (int64_t i = 0; i < n; i++) {
        add(&s, nums[i]);
    }
    return s;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 703;
    int64_t checksum = 0;
    int64_t changes = 0;
    for (int round = 0; round < 5; round++) {
        for (int64_t stream = 0; stream < 10; stream++) {
            int64_t k = 50 * (stream + 1);
            int64_t price = 100000;
            int64_t *nums = malloc(sizeof(int64_t) * 1000);
            for (int i = 0; i < 1000; i++) {
                price += next_random(&seed) % 201 - 90;
                nums[i] = price;
            }
            KthLargest s = make(k, nums, 1000);
            free(nums);
            int64_t last = 0;
            for (int i = 0; i < 200000; i++) {
                price += next_random(&seed) % 201 - 90;
                int64_t answer = add(&s, price);
                if (answer != last) {
                    changes += 1;
                }
                last = answer;
                checksum = (checksum * 31 + answer) % 1000000007;
            }
            free(s.heap);
        }
    }
    printf("5 rounds of 10 streams of 200000 prices: answer changed %lld "
           "times, checksum %lld\n",
           (long long)changes, (long long)checksum);
    return 0;
}
