// LeetCode #1801: Number of Orders in the Backlog -- the bench in C: the ★
// arm over 400 random lists of 500 orders built once, 10000 calls.
#include <stdint.h>
#include <stdio.h>

typedef struct {
    int32_t price;
    int64_t amount;
} Order;

// a binary heap of (price, amount) pairs: `max` gives the largest first,
// else the smallest, comparing the price and then the amount
typedef struct {
    Order items[512];
    int len;
    int max;
} Heap;

static int before(const Heap *h, Order a, Order b) {
    int less = a.price < b.price || (a.price == b.price && a.amount < b.amount);
    int more = a.price > b.price || (a.price == b.price && a.amount > b.amount);
    return h->max ? more : less;
}

static void push(Heap *h, Order o) {
    int i = h->len++;
    h->items[i] = o;
    while (i > 0) {
        int up = (i - 1) / 2;
        if (!before(h, h->items[i], h->items[up])) break;
        Order t = h->items[i];
        h->items[i] = h->items[up];
        h->items[up] = t;
        i = up;
    }
}

static Order pop(Heap *h) {
    Order top = h->items[0];
    h->items[0] = h->items[--h->len];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = l + 1, best = i;
        if (l < h->len && before(h, h->items[l], h->items[best])) best = l;
        if (r < h->len && before(h, h->items[r], h->items[best])) best = r;
        if (best == i) break;
        Order t = h->items[i];
        h->items[i] = h->items[best];
        h->items[best] = t;
        i = best;
    }
    return top;
}

static Heap buys, sells;

static int32_t get_number_of_backlog_orders(int32_t orders[][3], int n) {
    buys.len = 0;
    buys.max = 1;
    sells.len = 0;
    sells.max = 0;
    for (int i = 0; i < n; i++) {
        int32_t price = orders[i][0];
        int64_t amount = orders[i][1];
        if (orders[i][2] == 0) {
            while (amount > 0 && sells.len > 0 && sells.items[0].price <= price) {
                Order o = pop(&sells);
                if (o.amount > amount) {
                    push(&sells, (Order){o.price, o.amount - amount});
                    amount = 0;
                } else {
                    amount -= o.amount;
                }
            }
            if (amount > 0) push(&buys, (Order){price, amount});
        } else {
            while (amount > 0 && buys.len > 0 && buys.items[0].price >= price) {
                Order o = pop(&buys);
                if (o.amount > amount) {
                    push(&buys, (Order){o.price, o.amount - amount});
                    amount = 0;
                } else {
                    amount -= o.amount;
                }
            }
            if (amount > 0) push(&sells, (Order){price, amount});
        }
    }
    int64_t total = 0;
    for (int i = 0; i < buys.len; i++) total += buys.items[i].amount;
    for (int i = 0; i < sells.len; i++) total += sells.items[i].amount;
    return (int32_t)(total % 1000000007);
}

static int64_t seed = 1801;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t lists[400][500][3];
    for (int l = 0; l < 400; l++)
        for (int x = 0; x < 500; x++) {
            lists[l][x][0] = (int32_t)(1 + next_random() % 1000);
            lists[l][x][1] = (int32_t)(1 + next_random() % 1000);
            lists[l][x][2] = (int32_t)(next_random() % 2);
        }
    int64_t check = 0;
    for (int64_t call = 0; call < 10000; call++) {
        check = (check * 31 + get_number_of_backlog_orders(lists[(check + call) % 400], 500)) % 1000000007;
    }
    printf("10000 calls over 400 lists of 500 orders: checksum %lld\n", (long long)check);
    return 0;
}
