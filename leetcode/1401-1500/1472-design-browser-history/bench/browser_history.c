// LeetCode #1472: Design Browser History -- bench, C mirror of
// browser_history.kara. Each visit copies its page as the Kāra and Rust
// histories do; back and forward hand back the stored page, not a copy.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char **pages;
    int64_t len, cap, at, end;
} BrowserHistory;

static char *copy(const char *s) {
    size_t n = strlen(s) + 1;
    char *c = malloc(n);
    memcpy(c, s, n);
    return c;
}

static void history_new(BrowserHistory *h, const char *homepage) {
    h->cap = 4;
    h->pages = malloc(sizeof(char *) * h->cap);
    h->pages[0] = copy(homepage);
    h->len = 1;
    h->at = 0;
    h->end = 1;
}

static void history_free(BrowserHistory *h) {
    for (int64_t i = 0; i < h->len; i++) free(h->pages[i]);
    free(h->pages);
}

static void visit(BrowserHistory *h, const char *url) {
    h->at += 1;
    if (h->at < h->len) {
        free(h->pages[h->at]);
        h->pages[h->at] = copy(url);
    } else {
        if (h->len == h->cap) {
            h->cap *= 2;
            h->pages = realloc(h->pages, sizeof(char *) * h->cap);
        }
        h->pages[h->len++] = copy(url);
    }
    h->end = h->at + 1;
}

static const char *back(BrowserHistory *h, int32_t steps) {
    h->at = h->at - steps < 0 ? 0 : h->at - steps;
    return h->pages[h->at];
}

static const char *forward(BrowserHistory *h, int32_t steps) {
    h->at = h->at + steps > h->end - 1 ? h->end - 1 : h->at + steps;
    return h->pages[h->at];
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t fold(int64_t check, const char *url) {
    for (const unsigned char *b = (const unsigned char *)url; *b; b++)
        check = (check * 131 + *b) % 1000000007;
    return check;
}

int main(void) {
    static char pool[1000][32];
    for (int i = 0; i < 1000; i++) snprintf(pool[i], sizeof pool[i], "site%d.example.com", i);
    int64_t seed = 1472, check = 0;
    for (int s = 0; s < 400; s++) {
        BrowserHistory h;
        history_new(&h, "home.example.com");
        for (int c = 0; c < 5000; c++) {
            int64_t r = next_random(&seed) % 3;
            int64_t x = next_random(&seed);
            if (r == 0)
                visit(&h, pool[x % 1000]);
            else if (r == 1)
                check = fold(check, back(&h, (int32_t)(1 + x % 10)));
            else
                check = fold(check, forward(&h, (int32_t)(1 + x % 10)));
        }
        history_free(&h);
    }
    printf("400 sessions of 5000 calls: checksum %lld\n", (long long)check);
    return 0;
}
