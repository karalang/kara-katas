// LeetCode #929: Unique Email Addresses -- bench: one walk per address and
// a set. Mirrors num_unique_emails.kara. C has no set, so this one is an
// open-addressing hash table of 256 slots keyed by FNV-1a.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 256

static int64_t num_unique_emails(char **emails, int64_t n) {
    static char buf[100 * 101];
    static const char *slot_key[SLOTS];
    static int64_t slot_len[SLOTS];
    memset(slot_key, 0, sizeof slot_key);
    int64_t used = 0, count = 0;
    for (int64_t t = 0; t < n; t++) {
        char *out = buf + used;
        int64_t len = 0;
        int domain = 0, tagged = 0;
        for (const char *p = emails[t]; *p; p++) {
            char c = *p;
            if (domain) {
                out[len++] = c;
            } else if (c == '@') {
                domain = 1;
                out[len++] = c;
            } else if (c == '+') {
                tagged = 1;
            } else if (c != '.' && !tagged) {
                out[len++] = c;
            }
        }
        uint64_t h = 1469598103934665603ULL;
        for (int64_t i = 0; i < len; i++) h = (h ^ (unsigned char)out[i]) * 1099511628211ULL;
        int64_t s = (int64_t)(h & (SLOTS - 1));
        while (slot_key[s] && !(slot_len[s] == len && memcmp(slot_key[s], out, len) == 0)) s = (s + 1) & (SLOTS - 1);
        if (!slot_key[s]) {
            slot_key[s] = out;
            slot_len[s] = len;
            used += len;
            count++;
        }
    }
    return count;
}

static int64_t seed = 929;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 300, count = 100;
    const char *domains[8] = {"@leetcode.com", "@lee.tcode.com", "@example.com", "@mail.example.com",
                              "@a+b.com", "@ab.com", "@kara.dev.com", "@x.com"};
    // count lists of 100 addresses, built once: a local name of 2 to 7
    // letters from "ab" with a dot before about one in four, a tag after a
    // '+' on half of them, and one of eight domains
    char ***lists = malloc(count * sizeof(char **));
    for (int64_t g = 0; g < count; g++) {
        lists[g] = malloc(100 * sizeof(char *));
        for (int64_t t = 0; t < 100; t++) {
            char b[101];
            int64_t len = 0;
            int64_t letters = 2 + next_random() % 6;
            for (int64_t i = 0; i < letters; i++) {
                if (next_random() % 4 == 0) b[len++] = '.';
                b[len++] = (char)('a' + next_random() % 2);
            }
            if (next_random() % 2 == 0) {
                b[len++] = '+';
                int64_t tag = next_random() % 10;
                for (int64_t i = 0; i < tag; i++) b[len++] = (char)('a' + next_random() % 26);
            }
            const char *d = domains[next_random() % 8];
            strcpy(b + len, d);
            lists[g][t] = strdup(b);
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // each round visits every list, starting from a different one
        for (int64_t i = 0; i < count; i++) {
            int64_t a = num_unique_emails(lists[(r + i) % count], 100);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    printf("%lld rounds over %lld lists of 100 addresses: answers summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)total, (long long)check);
    for (int64_t g = 0; g < count; g++) {
        for (int64_t t = 0; t < 100; t++) free(lists[g][t]);
        free(lists[g]);
    }
    free(lists);
    return 0;
}
