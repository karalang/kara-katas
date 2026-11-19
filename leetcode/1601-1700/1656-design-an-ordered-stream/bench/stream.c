// LeetCode #1656: Design an Ordered Stream -- the bench's C mirror: the ★
// arm on 2000 random streams of 1000 pairs, each inserted in a random
// order with a value of five random letters, all drawn first. Each value
// inserted and each one returned is its own heap copy, as the other
// languages' strings are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define STREAMS 2000
#define N 1000

typedef struct {
    char **slots;
    int n;
    int next;
} OrderedStream;

static OrderedStream stream_new(int n) {
    OrderedStream s = {calloc(n + 1, sizeof(char *)), n, 1};
    return s;
}

static void stream_free(OrderedStream *s) {
    for (int i = 0; i <= s->n; i++) free(s->slots[i]);
    free(s->slots);
}

// returns how many values the chunk holds, written to `chunk`
static int stream_insert(OrderedStream *s, int id_key, char *value, char **chunk) {
    s->slots[id_key] = value;
    int count = 0;
    while (s->next <= s->n && s->slots[s->next] != NULL) {
        chunk[count++] = strdup(s->slots[s->next]);
        s->next += 1;
    }
    return count;
}

static int64_t seed = 1656;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t ids[STREAMS][N];
    static char values[STREAMS][N][6];
    for (int s = 0; s < STREAMS; s++) {
        int32_t order[N];
        for (int i = 0; i < N; i++) order[i] = i + 1;
        for (int i = N - 1; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int32_t t = order[i];
            order[i] = order[j];
            order[j] = t;
        }
        for (int i = 0; i < N; i++) {
            ids[s][i] = order[i];
            for (int c = 0; c < 5; c++) values[s][i][c] = (char)('a' + next_random() % 26);
            values[s][i][5] = '\0';
        }
    }
    int64_t check = 0, chunks = 0;
    char **chunk = malloc(sizeof(char *) * N);
    for (int s = 0; s < STREAMS; s++) {
        OrderedStream stream = stream_new(N);
        for (int i = 0; i < N; i++) {
            int count = stream_insert(&stream, ids[s][i], strdup(values[s][i]), chunk);
            if (count > 0) chunks += 1;
            for (int k = 0; k < count; k++) {
                for (const char *b = chunk[k]; *b; b++) check = (check * 31 + (unsigned char)*b) % 1000000007;
                free(chunk[k]);
            }
        }
        stream_free(&stream);
    }
    free(chunk);
    printf("2000 streams of 1000 pairs: %lld chunks, checksum %lld\n", (long long)chunks, (long long)check);
    return 0;
}
