// LeetCode #2468: Split Message Based on Limit -- the bench, the ★ arm in
// C: the least part count found with a running sum of the counts'
// digits, each count's digits by `snprintf`, then the parts cut in order
// into strings allocated by `malloc` and written by `snprintf`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t digits(int64_t v) {
    return snprintf(NULL, 0, "%lld", (long long)v);
}

typedef struct {
    char **parts;
    int64_t count;
} Split;

static Split split_message(const char *message, int64_t n, int64_t limit) {
    int64_t digit_sum = 0, parts = 0;
    for (int64_t b = 1; 3 + 2 * digits(b) < limit; b++) {
        digit_sum += digits(b);
        if (b * (limit - 3 - digits(b)) - digit_sum >= n) {
            parts = b;
            break;
        }
    }
    Split out = {NULL, 0};
    if (parts == 0) return out;
    out.parts = malloc(sizeof(char *) * parts);
    out.count = parts;
    int64_t at = 0;
    for (int64_t a = 1; a <= parts; a++) {
        int64_t room = limit - 3 - digits(a) - digits(parts);
        int64_t end = at + room < n ? at + room : n;
        int64_t size = (end - at) + 3 + digits(a) + digits(parts) + 1;
        out.parts[a - 1] = malloc(size);
        snprintf(out.parts[a - 1], size, "%.*s<%lld/%lld>", (int)(end - at), message + at, (long long)a, (long long)parts);
        at = end;
    }
    return out;
}

static int64_t seed = 2468;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    // 20 messages of 10^4 lowercase letters and spaces built once; then
    // 2600 passes, each choosing every message's limit, from 12 to 211,
    // from the checksum so far, then splitting it and folding the part
    // count, the last part's length and the pass into the checksum
    const char *letters = "abcdefghijklmnopqrstuvwxyz ";
    static char messages[20][10001];
    for (int m = 0; m < 20; m++) {
        for (int i = 0; i < 10000; i++) messages[m][i] = letters[next_random() % 27];
        messages[m][10000] = 0;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 2600; p++) {
        for (int m = 0; m < 20; m++) {
            int64_t limit = 12 + check % 200;
            Split s = split_message(messages[m], 10000, limit);
            int64_t last = (int64_t)strlen(s.parts[s.count - 1]);
            check = (check * 31 + s.count + last + p) % 1000000007;
            for (int64_t i = 0; i < s.count; i++) free(s.parts[i]);
            free(s.parts);
        }
    }
    printf("2600 passes over 20 messages of 10^4: checksum %lld\n", (long long)check);
    return 0;
}
