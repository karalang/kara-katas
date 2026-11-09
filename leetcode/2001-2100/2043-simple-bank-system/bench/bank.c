// LeetCode #2043: Simple Bank System -- the ★ arm in C, the same algorithm
// and workload as bank.kara: the balances in an array indexed by account -
// 1, every call checked whole before anything changes.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *balance;
    int64_t n;
} Bank;

static int exists(const Bank *b, int64_t account) { return account >= 1 && account <= b->n; }

static int transfer(Bank *b, int64_t account1, int64_t account2, int64_t money) {
    if (!exists(b, account1) || !exists(b, account2) || b->balance[account1 - 1] < money) return 0;
    b->balance[account1 - 1] -= money;
    b->balance[account2 - 1] += money;
    return 1;
}

static int deposit(Bank *b, int64_t account, int64_t money) {
    if (!exists(b, account)) return 0;
    b->balance[account - 1] += money;
    return 1;
}

static int withdraw(Bank *b, int64_t account, int64_t money) {
    if (!exists(b, account) || b->balance[account - 1] < money) return 0;
    b->balance[account - 1] -= money;
    return 1;
}

static int64_t seed = 2043;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t big_random(void) {
    int64_t hi = next_random();
    int64_t mid = next_random();
    return (hi * 32768 + mid) * 32768 + next_random();
}

typedef struct {
    int64_t kind, a, b, money;
} Op;

int main(void) {
    const int64_t n = 100000, calls_per = 1000000, top = 1000000;
    int64_t *balance = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) balance[i] = big_random() % (top + 1);
    Op *ops = malloc(sizeof(Op) * calls_per);
    for (int64_t i = 0; i < calls_per; i++) {
        ops[i].kind = next_random() % 3;
        ops[i].a = big_random() % (n + 2);
        ops[i].b = big_random() % (n + 2);
        ops[i].money = big_random() % (top + 1);
    }
    int64_t calls = 0, succeeded = 0, check = 0;
    for (int64_t round = 0; round < 40; round++) {
        Bank bank = {malloc(sizeof(int64_t) * n), n};
        memcpy(bank.balance, balance, sizeof(int64_t) * n);
        for (int64_t i = 0; i < calls_per; i++) {
            const Op *o = &ops[i];
            int ok = o->kind == 0 ? transfer(&bank, o->a, o->b, o->money)
                   : o->kind == 1 ? deposit(&bank, o->a, o->money)
                                  : withdraw(&bank, o->a, o->money);
            calls++;
            if (ok) {
                succeeded++;
                check = (check * 31 + calls + round) % 1000000007;
            }
        }
        free(bank.balance);
    }
    printf("%lld calls: %lld succeed, checksum %lld\n", (long long)calls, (long long)succeeded, (long long)check);
    free(balance);
    free(ops);
    return 0;
}
