// LeetCode #2284: Sender With Largest Word Count -- the bench, the ★
// arm's C twin. An open-addressing table of 64 slots keyed by the
// sender's string (FNV-1a), each message's words counted as its spaces
// plus one, then the largest by total and name.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 64

static const char *largest_word_count(char **messages, char **senders, int n) {
    const char *keys[SLOTS] = {0};
    int64_t totals[SLOTS] = {0};
    for (int i = 0; i < n; i++) {
        int64_t words = 1;
        for (const char *p = messages[i]; *p; p++) {
            if (*p == ' ') words++;
        }
        uint64_t h = 1469598103934665603ULL;
        for (const char *p = senders[i]; *p; p++) h = (h ^ (unsigned char)*p) * 1099511628211ULL;
        size_t at = h & (SLOTS - 1);
        while (keys[at] && strcmp(keys[at], senders[i]) != 0) at = (at + 1) & (SLOTS - 1);
        keys[at] = senders[i];
        totals[at] += words;
    }
    const char *best = "";
    int64_t most = 0;
    for (int s = 0; s < SLOTS; s++) {
        if (!keys[s]) continue;
        if (totals[s] > most || (totals[s] == most && strcmp(keys[s], best) > 0)) {
            best = keys[s];
            most = totals[s];
        }
    }
    return best;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2284;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void word(char *out, int64_t len) {
    for (int64_t i = 0; i < len; i++) out[i] = (char)('a' + next_random() % 26);
    out[len] = '\0';
}

int main(void) {
    static char pool[40][11];
    for (int i = 0; i < 40; i++) {
        int64_t len = next_random() % 10 + 1;
        word(pool[i], len);
    }
    char **messages = malloc(1000 * 100 * sizeof(char *));
    char **senders = malloc(1000 * 100 * sizeof(char *));
    for (int c = 0; c < 1000; c++) {
        int64_t first = next_random() % 20;
        for (int m = 0; m < 100; m++) {
            senders[c * 100 + m] = pool[first + next_random() % 20];
            int64_t w = next_random() % 8 + 1;
            char *message = malloc(8 * 6);
            size_t at = 0;
            for (int64_t j = 0; j < w; j++) {
                if (j > 0) message[at++] = ' ';
                int64_t len = next_random() % 5 + 1;
                word(message + at, len);
                at += len;
            }
            message[at] = '\0';
            messages[c * 100 + m] = message;
        }
    }
    int64_t check = 0;
    for (int p = 0; p < 20; p++) {
        for (int c = 0; c < 1000; c++) {
            const char *best = largest_word_count(messages + c * 100, senders + c * 100, 100);
            int64_t sum = 0;
            for (const char *q = best; *q; q++) sum += (unsigned char)*q;
            check = (check * 31 + sum) % 1000000007;
        }
    }
    for (int i = 0; i < 100000; i++) free(messages[i]);
    free(messages);
    free(senders);
    printf("20 passes over 1000 cases of 100 messages: checksum %lld\n", (long long)check);
    return 0;
}
