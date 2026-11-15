// LeetCode #2166: Design Bitset -- the benchmark's C mirror of
// bitset.kara: a bool array, the flip flag and the count of ones.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    bool *bits;
    int64_t size;
    bool flipped;
    int64_t ones;
} Bitset;

static void fix(Bitset *b, int64_t idx) {
    if (b->bits[idx] == b->flipped) {
        b->bits[idx] = !b->flipped;
        b->ones++;
    }
}

static void unfix(Bitset *b, int64_t idx) {
    if (b->bits[idx] != b->flipped) {
        b->bits[idx] = b->flipped;
        b->ones--;
    }
}

static void flip(Bitset *b) {
    b->flipped = !b->flipped;
    b->ones = b->size - b->ones;
}

static char *to_string(const Bitset *b) {
    char *text = malloc((size_t)b->size + 1);
    for (int64_t i = 0; i < b->size; i++) text[i] = b->bits[i] != b->flipped ? '1' : '0';
    text[b->size] = 0;
    return text;
}

static int64_t seed = 2166;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t size = 100000;
    Bitset bits = {calloc((size_t)size, sizeof(bool)), size, false, 0};
    int64_t check = 0;
    for (int64_t i = 0; i < 5000000; i++) {
        if (i % 500000 == 499999) {
            char *text = to_string(&bits);
            for (int64_t k = 0; k < size; k++) check = (check * 31 + (unsigned char)text[k]) % 1000000007;
            free(text);
            continue;
        }
        int64_t pick = next_random() % 16;
        int64_t answer = 0;
        if (pick < 7) {
            int64_t hi = next_random();
            fix(&bits, (hi * 32768 + next_random()) % size);
        } else if (pick < 13) {
            int64_t hi = next_random();
            unfix(&bits, (hi * 32768 + next_random()) % size);
        } else if (pick == 13) {
            flip(&bits);
        } else if (pick == 14) {
            answer = bits.ones == bits.size ? 2 : bits.ones > 0 ? 1 : 0;
        } else {
            answer = bits.ones;
        }
        check = (check * 31 + answer) % 1000000007;
    }
    printf("5000000 calls: checksum %lld\n", (long long)check);
    free(bits.bits);
    return 0;
}
