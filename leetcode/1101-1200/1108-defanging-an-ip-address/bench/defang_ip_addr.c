// LeetCode #1108: Defanging an IP Address -- the bench in C: the ★ arm
// (one pass, each period written as `[.]`) over 1024 random addresses,
// each round replacing one address with a new one and defanging every
// address again. Each answer is its own `malloc`, freed after use, as
// each is its own `String` in the other languages.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static char *defang_ip_addr(const char *address, size_t n, size_t *len) {
    char *out = malloc(n + 7);
    size_t k = 0;
    for (size_t i = 0; i < n; i++) {
        if (address[i] == '.') {
            out[k++] = '[';
            out[k++] = '.';
            out[k++] = ']';
        } else {
            out[k++] = address[i];
        }
    }
    out[k] = 0;
    *len = k;
    return out;
}

static int64_t seed = 1108;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct { char *s; size_t n; } Str;

static Str random_address(void) {
    int64_t a = next_random() % 256;
    int64_t b = next_random() % 256;
    int64_t c = next_random() % 256;
    int64_t d = next_random() % 256;
    char buf[32];
    int n = snprintf(buf, sizeof buf, "%lld.%lld.%lld.%lld", (long long)a, (long long)b, (long long)c, (long long)d);
    Str r = { malloc((size_t)n + 1), (size_t)n };
    memcpy(r.s, buf, (size_t)n + 1);
    return r;
}

int main(void) {
    static Str addresses[1024];
    for (int i = 0; i < 1024; i++) addresses[i] = random_address();
    int64_t length = 0, check = 0, calls = 0;
    for (int64_t round = 0; round < 10000; round++) {
        int64_t j = (round * 7919) % 1024;
        free(addresses[j].s);
        addresses[j] = random_address();
        for (int i = 0; i < 1024; i++) {
            size_t len;
            char *d = defang_ip_addr(addresses[i].s, addresses[i].n, &len);
            length += (int64_t)len;
            if (calls % 64 == 0)
                for (size_t k = 0; k < len; k++) check = (check * 31 + (unsigned char)d[k]) % 1000000007;
            calls++;
            free(d);
        }
    }
    printf("10000 rounds over 1024 addresses: %lld calls, %lld characters, checksum %lld\n", (long long)calls, (long long)length, (long long)check);
    return 0;
}
