// LeetCode #1622: Fancy Sequence -- the bench in C, mirroring fancy.kara:
// every value stored under the inverse of one map x -> mul x + add, the
// inverse a Fermat power per append.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t power(int64_t base, int64_t exp) {
    int64_t result = 1, b = base % MOD, e = exp;
    while (e > 0) {
        if (e & 1) result = result * b % MOD;
        b = b * b % MOD;
        e >>= 1;
    }
    return result;
}

typedef struct {
    int64_t *stored;
    int64_t len, cap;
    int64_t mul, add;
} Fancy;

static void fancy_init(Fancy *f) {
    f->stored = NULL;
    f->len = f->cap = 0;
    f->mul = 1;
    f->add = 0;
}

static void fancy_append(Fancy *f, int32_t val) {
    if (f->len == f->cap) {
        f->cap = f->cap ? 2 * f->cap : 4;
        f->stored = realloc(f->stored, (size_t)f->cap * sizeof(int64_t));
    }
    int64_t shifted = ((int64_t)val - f->add + MOD) % MOD;
    f->stored[f->len++] = shifted * power(f->mul, MOD - 2) % MOD;
}

static void fancy_add_all(Fancy *f, int32_t inc) { f->add = (f->add + inc) % MOD; }

static void fancy_mult_all(Fancy *f, int32_t m) {
    f->mul = f->mul * m % MOD;
    f->add = f->add * m % MOD;
}

static int32_t fancy_get_index(const Fancy *f, int32_t idx) {
    if (idx >= f->len) return -1;
    return (int32_t)((f->stored[idx] * f->mul + f->add) % MOD);
}

static int64_t seed = 1622;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    int64_t kind;
    int32_t arg;
} Call;

int main(void) {
    enum { SEQUENCES = 50, CALLS = 100000 };
    Call *calls = malloc(sizeof(Call) * SEQUENCES * CALLS);
    for (int s = 0; s < SEQUENCES; s++) {
        int64_t length = 0;
        for (int c = 0; c < CALLS; c++) {
            Call *call = &calls[(size_t)s * CALLS + c];
            int64_t arg = next_random() % 100 + 1;
            int64_t r = next_random() % 10;
            if (r <= 3) {
                *call = (Call){0, (int32_t)arg};
                length++;
            } else if (r <= 5) {
                *call = (Call){1, (int32_t)arg};
            } else if (r <= 7) {
                *call = (Call){2, (int32_t)arg};
            } else {
                int64_t high = next_random();
                int64_t idx = (high * 32768 + next_random()) % (length + length / 4 + 1);
                *call = (Call){3, (int32_t)idx};
            }
        }
    }
    int64_t check = 0, misses = 0;
    for (int s = 0; s < SEQUENCES; s++) {
        Fancy fancy;
        fancy_init(&fancy);
        for (int c = 0; c < CALLS; c++) {
            Call call = calls[(size_t)s * CALLS + c];
            switch (call.kind) {
            case 0: fancy_append(&fancy, call.arg); break;
            case 1: fancy_add_all(&fancy, call.arg); break;
            case 2: fancy_mult_all(&fancy, call.arg); break;
            default: {
                int64_t got = fancy_get_index(&fancy, call.arg);
                if (got == -1) misses++;
                check = (check * 31 + got + 1) % 1000000007;
            }
            }
        }
        free(fancy.stored);
    }
    free(calls);
    printf("50 sequences of 100000 calls: %lld reads past the end, checksum %lld\n",
           (long long)misses, (long long)check);
    return 0;
}
