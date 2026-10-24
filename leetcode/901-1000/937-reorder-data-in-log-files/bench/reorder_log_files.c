// LeetCode #937: Reorder Data in Log Files -- bench: two lists and a
// sort. Mirrors reorder_log_files.kara, .rs, .py and go-seq/. The logs
// are sorted as pointers, with no copies.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 937;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int compare_letter_logs(const void *pa, const void *pb) {
    const char *a = *(const char *const *)pa;
    const char *b = *(const char *const *)pb;
    const char *ca = strchr(a, ' ') + 1;
    const char *cb = strchr(b, ' ') + 1;
    int c = strcmp(ca, cb);
    if (c != 0) {
        return c;
    }
    // the identifiers, each ending at its space
    size_t la = (size_t)(ca - 1 - a);
    size_t lb = (size_t)(cb - 1 - b);
    int d = memcmp(a, b, la < lb ? la : lb);
    if (d != 0) {
        return d;
    }
    return la < lb ? -1 : la > lb ? 1 : 0;
}

// fills out with the logs in their new order
static void reorder_log_files(char **logs, int64_t n, char **out, char **digits) {
    int64_t letters = 0;
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        char first = strchr(logs[i], ' ')[1];
        if (first >= '0' && first <= '9') {
            digits[count++] = logs[i];
        } else {
            out[letters++] = logs[i];
        }
    }
    qsort(out, (size_t)letters, sizeof(char *), compare_letter_logs);
    memcpy(out + letters, digits, (size_t)count * sizeof(char *));
}

int main(void) {
    const int64_t rounds = 200;
    const int64_t count = 200;
    char *lists[200][100];
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < 100; i++) {
            char *log = malloc(128);
            int len = 0;
            log[len++] = (char)(97 + next_random() % 26);
            len += sprintf(log + len, "%lld", (long long)i);
            int digits = next_random() % 2 == 1;
            int64_t size = 20 + next_random() % 81;
            while (len + 2 <= size) {
                int64_t w = 1 + next_random() % 8;
                if (len + 1 + w > size) {
                    w = size - len - 1;
                }
                log[len++] = ' ';
                for (int64_t k = 0; k < w; k++) {
                    if (digits) {
                        log[len++] = (char)(48 + next_random() % 10);
                    } else {
                        log[len++] = (char)(97 + next_random() % 5);
                    }
                }
            }
            log[len] = '\0';
            lists[c][i] = log;
        }
    }
    char *out[100];
    char *digits[100];
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            reorder_log_files(lists[(r + i) % count], 100, out, digits);
            total += 100;
            for (int k = 0; k < 100; k++) {
                for (const char *p = out[k]; *p != ' '; p++) {
                    check = (check * 131 + (unsigned char)*p) % 1000000007;
                }
            }
        }
    }
    printf("%lld rounds over %lld lists of 100 logs: %lld logs, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)check);
    return 0;
}
