// LeetCode #649: Dota2 Senate -- C mirror of the Kāra bench.
//
// The ★ arm over the same senates and rounds: a ring-buffer queue of
// each party's senators by when they vote, the front two meeting and the
// earlier going to the back `n` places later.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *items;
    int64_t cap, head, len;
} Queue;

static void push(Queue *q, int64_t v) {
    if (q->len == q->cap) {
        int64_t cap = q->cap ? 2 * q->cap : 8;
        int64_t *items = malloc(cap * sizeof(int64_t));
        for (int64_t i = 0; i < q->len; i++) items[i] = q->items[(q->head + i) % q->cap];
        free(q->items);
        q->items = items;
        q->cap = cap;
        q->head = 0;
    }
    q->items[(q->head + q->len) % q->cap] = v;
    q->len++;
}

static int64_t pop(Queue *q) {
    int64_t v = q->items[q->head];
    q->head = (q->head + 1) % q->cap;
    q->len--;
    return v;
}

static const char *predict_party_victory(const char *senate, int64_t n) {
    Queue radiant = {0}, dire = {0};
    for (int64_t i = 0; i < n; i++) {
        if (senate[i] == 'R') push(&radiant, i);
        else push(&dire, i);
    }
    while (radiant.len > 0 && dire.len > 0) {
        int64_t r = pop(&radiant), d = pop(&dire);
        if (r < d) push(&radiant, r + n);
        else push(&dire, d + n);
    }
    const char *winner = radiant.len > 0 ? "Radiant" : "Dire";
    free(radiant.items);
    free(dire.items);
    return winner;
}

static int64_t seed = 649;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { INPUTS = 20, ROUNDS = 500, SEATS = 100000 };
    char *senates[INPUTS];
    for (int i = 0; i < INPUTS; i++) {
        int64_t radiant = 45 + next_random() % 11;
        senates[i] = malloc(SEATS);
        for (int j = 0; j < SEATS; j++) senates[i][j] = next_random() % 100 < radiant ? 'R' : 'D';
    }
    int64_t wins = 0, checksum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int won = strcmp(predict_party_victory(senates[(r * 7) % INPUTS], SEATS), "Radiant") == 0;
        if (won) wins++;
        checksum = (checksum * 2 + won) % 1000000007;
    }
    printf("%d senates, %d rounds: Radiant wins %lld, checksum %lld\n", INPUTS, ROUNDS, (long long)wins, (long long)checksum);
    for (int i = 0; i < INPUTS; i++) free(senates[i]);
    return 0;
}
