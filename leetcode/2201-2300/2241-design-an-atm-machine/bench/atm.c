// LeetCode #2241: Design an ATM Machine -- the benchmark's C mirror of
// atm.kara: the counts of the five banknotes, smallest first; a
// withdrawal plans as many of each as fit, largest first, and takes the
// plan only when it pays the whole amount.
#include <stdint.h>
#include <stdio.h>

typedef struct {
    int64_t counts[5];
} Atm;

static const int64_t values[5] = {20, 50, 100, 200, 500};

static void deposit(Atm *atm, const int64_t *banknotes_count) {
    for (int i = 0; i < 5; i++) atm->counts[i] += banknotes_count[i];
}

// writes the plan, or a single -1, into `out`; returns its length
static int withdraw(Atm *atm, int64_t amount, int64_t *out) {
    int64_t left = amount;
    for (int i = 4; i >= 0; i--) {
        int64_t take = left / values[i];
        out[i] = take < atm->counts[i] ? take : atm->counts[i];
        left -= out[i] * values[i];
    }
    if (left != 0) {
        out[0] = -1;
        return 1;
    }
    for (int i = 0; i < 5; i++) atm->counts[i] -= out[i];
    return 5;
}

static int64_t seed = 2241;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t paid = 0, check = 0, counts[5], answer[5];
    for (int m = 0; m < 200; m++) {
        Atm atm = {{0, 0, 0, 0, 0}};
        for (int c = 0; c < 5000; c++) {
            if (next_random() % 2 == 0) {
                for (int i = 0; i < 5; i++) counts[i] = wide_random() % 1000000001;
                deposit(&atm, counts);
            } else {
                int64_t amount = (wide_random() % 100000000 + 1) * 10;
                int n = withdraw(&atm, amount, answer);
                if (answer[0] >= 0) paid++;
                for (int i = 0; i < n; i++) check = (check * 31 + answer[i] % 1000000007 + 1) % 1000000007;
            }
        }
    }
    printf("200 machines of 5000 calls: %lld withdrawals paid, checksum %lld\n", (long long)paid, (long long)check);
    return 0;
}
