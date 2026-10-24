// LeetCode #989: Add to Array-Form of Integer -- bench, the ★ arm
// (k carried in from the last digit), the same algorithm and workload
// as add_to_array_form.kara. The answer grows in a doubling array, as
// a Vec does.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *items;
    int64_t len, cap;
} Digits;

static void push(Digits *v, int64_t d) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->items = realloc(v->items, v->cap * sizeof(int64_t));
    }
    v->items[v->len++] = d;
}

static Digits add_to_array_form(const Digits *num, int64_t k) {
    Digits out = {0};
    int64_t carry = k;
    int64_t i = num->len - 1;
    while (i >= 0 || carry > 0) {
        if (i >= 0) {
            carry += num->items[i];
            i -= 1;
        }
        push(&out, carry % 10);
        carry /= 10;
    }
    for (int64_t a = 0, b = out.len - 1; a < b; a++, b--) {
        int64_t t = out.items[a];
        out.items[a] = out.items[b];
        out.items[b] = t;
    }
    return out;
}

static int64_t seed = 989;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static Digits random_num(int64_t n) {
    Digits out = {0};
    for (int64_t i = 0; i < n; i++) {
        int64_t d = next_random() % 10;
        if (i == 0 && d == 0) d = 1;
        push(&out, d);
    }
    return out;
}

int main(void) {
    int rounds = 1000;
    Digits nums[20];
    for (int i = 0; i < 20; i++) nums[i] = random_num(10000);
    int64_t digits = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int64_t k = 1 + next_random() % 10000;
            Digits got = add_to_array_form(&nums[(r + i) % 20], k);
            digits += got.len;
            for (int64_t j = got.len - 6; j < got.len; j++)
                check = (check * 31 + got.items[j] + 1) % 1000000007;
            free(got.items);
        }
    }
    printf("%d rounds over 20 numbers of 10000 digits: %lld digits out, checksum %lld\n", rounds,
           (long long)digits, (long long)check);
    return 0;
}
