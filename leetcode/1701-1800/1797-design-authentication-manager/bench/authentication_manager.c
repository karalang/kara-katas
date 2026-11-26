// LeetCode #1797: Design Authentication Manager -- the bench in C: the ★
// arm, a hash map from each token to the second it expires (open
// addressing, FNV-1a over the name), over 50 random scripts of 2000 calls
// built once, 2000 runs. A count walks every slot.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 4096

typedef struct {
    char key[8];
    int used;
    int32_t until;
} Slot;

typedef struct {
    int32_t ttl;
    Slot *slots;
} AuthenticationManager;

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static Slot *find(AuthenticationManager *m, const char *key) {
    uint64_t i = hash(key) & (SLOTS - 1);
    while (m->slots[i].used && strcmp(m->slots[i].key, key) != 0) i = (i + 1) & (SLOTS - 1);
    return &m->slots[i];
}

static void generate(AuthenticationManager *m, const char *token_id, int32_t current_time) {
    Slot *s = find(m, token_id);
    s->used = 1;
    strcpy(s->key, token_id);
    s->until = current_time + m->ttl;
}

static void renew(AuthenticationManager *m, const char *token_id, int32_t current_time) {
    Slot *s = find(m, token_id);
    if (s->used && s->until > current_time) s->until = current_time + m->ttl;
}

static int32_t count_unexpired_tokens(const AuthenticationManager *m, int32_t current_time) {
    int32_t n = 0;
    for (int i = 0; i < SLOTS; i++)
        if (m->slots[i].used && m->slots[i].until > current_time) n++;
    return n;
}

static int64_t seed = 1797;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void name(int64_t k, char *out) {
    int n = 0;
    do {
        out[n++] = "abcdefghijklmnopqrstuvwxyz"[k % 26];
        k /= 26;
    } while (k != 0);
    out[n] = 0;
}

typedef struct {
    int64_t op;
    char token[8];
    int32_t t;
} Call;

int main(void) {
    static Call calls[50][2000];
    static int32_t ttls[50];
    for (int s = 0; s < 50; s++) {
        ttls[s] = (int32_t)(1 + next_random() % 100000);
        int64_t made = 0, now = 0;
        for (int j = 0; j < 2000; j++) {
            now += 1 + next_random() % 100;
            int64_t pick = next_random() % 10;
            Call *c = &calls[s][j];
            c->t = (int32_t)now;
            if (pick < 4) {
                c->op = 0;
                name(made++, c->token);
            } else if (pick < 8) {
                c->op = 1;
                name(next_random() % (made + 2), c->token);
            } else {
                c->op = 2;
                c->token[0] = 0;
            }
        }
    }
    int64_t check = 0;
    AuthenticationManager m;
    m.slots = malloc(SLOTS * sizeof(Slot));
    for (int64_t run = 0; run < 2000; run++) {
        int s = (int)((check + run) % 50);
        m.ttl = ttls[s];
        memset(m.slots, 0, SLOTS * sizeof(Slot));
        for (int j = 0; j < 2000; j++) {
            Call *c = &calls[s][j];
            if (c->op == 0) generate(&m, c->token, c->t);
            else if (c->op == 1) renew(&m, c->token, c->t);
            else check = (check * 31 + count_unexpired_tokens(&m, c->t)) % 1000000007;
        }
    }
    free(m.slots);
    printf("2000 runs over 50 scripts of 2000 calls: checksum %lld\n", (long long)check);
    return 0;
}
