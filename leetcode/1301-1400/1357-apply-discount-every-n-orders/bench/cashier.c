// LeetCode #1357 bench -- C: the prices in a hash table from product to
// price (open addressing, linear probing), and a count of the customers so
// far.
#include <math.h>
#include <stdint.h>
#include <stdio.h>

#define SLOTS 512

typedef struct {
    int32_t n, discount, served;
    int32_t key[SLOTS], value[SLOTS];
} Cashier;

static uint32_t slot_of(int32_t key) { return ((uint32_t)key * 2654435761u) >> 23; }

static void cashier_new(Cashier *c, int32_t n, int32_t discount, const int32_t *products,
                        const int32_t *prices, int count) {
    c->n = n;
    c->discount = discount;
    c->served = 0;
    for (int i = 0; i < SLOTS; i++) c->key[i] = 0;
    for (int i = 0; i < count; i++) {
        uint32_t s = slot_of(products[i]);
        while (c->key[s] != 0 && c->key[s] != products[i]) s = (s + 1) & (SLOTS - 1);
        c->key[s] = products[i];
        c->value[s] = prices[i];
    }
}

static int32_t price_of(const Cashier *c, int32_t key) {
    uint32_t s = slot_of(key);
    while (c->key[s] != key) s = (s + 1) & (SLOTS - 1);
    return c->value[s];
}

static double get_bill(Cashier *c, const int32_t *product, const int32_t *amount, int m) {
    c->served++;
    double bill = 0.0;
    for (int i = 0; i < m; i++) bill += (double)(price_of(c, product[i]) * amount[i]);
    if (c->served % c->n == 0) return bill * (double)(100 - c->discount) / 100.0;
    return bill;
}

static int64_t seed = 1357;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t cents(double bill) { return (int64_t)round(bill * 100.0); }

int main(void) {
    // 20 cashiers, each selling the products 1 to 200 at prices from 1 to
    // 1000, with n from 1 to 10 and a discount from 0 to 100, built once;
    // then 10^6 bills, each of 1 to 20 products bought 1 to 1000 times,
    // all drawn from the checksum so far, every bill folded into it in cents
    static Cashier cashiers[20];
    static int32_t lists[20][200];
    for (int k = 0; k < 20; k++) {
        int32_t prices[200];
        for (int i = 0; i < 200; i++) lists[k][i] = i + 1;
        for (int i = 0; i < 200; i++) {
            int64_t j = i + next_random() % (200 - i);
            int32_t t = lists[k][i];
            lists[k][i] = lists[k][j];
            lists[k][j] = t;
        }
        for (int i = 0; i < 200; i++) prices[i] = (int32_t)(1 + next_random() % 1000);
        int32_t n = (int32_t)(1 + next_random() % 10);
        int32_t discount = (int32_t)(next_random() % 101);
        cashier_new(&cashiers[k], n, discount, lists[k], prices, 200);
    }
    int64_t check = 0;
    int32_t product[20], amount[20];
    for (int64_t r = 0; r < 1000000; r++) {
        int64_t k = check % 20;
        int64_t m = 1 + (check / 20) % 20;
        for (int64_t j = 0; j < m; j++) {
            product[j] = lists[k][(check / 7 + j * 37) % 200];
            amount[j] = (int32_t)(1 + (check + j) % 1000);
        }
        check = (check * 31 + cents(get_bill(&cashiers[k], product, amount, (int)m)) + r) % 1000000007;
    }
    printf("1000000 bills over 20 cashiers: checksum %lld\n", (long long)check);
    return 0;
}
