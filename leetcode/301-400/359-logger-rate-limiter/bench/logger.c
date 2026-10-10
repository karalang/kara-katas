// Benchmark for #359 -- mirror of logger.kara.
// The map is an open-addressing hash table of owned string keys (FNV-1a),
// sized well beyond the 100 distinct messages the workload can produce.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAP 16384

typedef struct { char *key; int64_t next_ok; } Slot;

static Slot table[CAP];

static uint64_t fnv(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) { h ^= (unsigned char)*s; h *= 1099511628211ULL; }
    return h;
}

// Takes ownership of message, as the Kara version's `own String` does.
static int should_print_message(int64_t timestamp, char *message) {
    uint64_t i = fnv(message) & (CAP - 1);
    while (table[i].key && strcmp(table[i].key, message) != 0) i = (i + 1) & (CAP - 1);
    if (table[i].key) {
        if (timestamp < table[i].next_ok) { free(message); return 0; }
        free(message);
    } else {
        table[i].key = message;
    }
    table[i].next_ok = timestamp + 10;
    return 1;
}

int main(void) {
    int64_t seed = 359, t = 0, printed = 0, checksum = 0;
    for (int n = 0; n < 1000000; n++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        t += (seed / 65536) % 8 == 0 ? 1 : 0;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t id = (seed / 65536) % 100;
        char *message = malloc(16);
        snprintf(message, 16, "msg%lld", (long long)id);
        int ok = should_print_message(t, message);
        if (ok) printed++;
        checksum = (checksum * 3 + (ok ? 1 : 2)) % 1000000007;
    }
    printf("%lld of 1000000 calls printed, checksum %lld\n", (long long)printed, (long long)checksum);
    for (int i = 0; i < CAP; i++) free(table[i].key);
    return 0;
}
