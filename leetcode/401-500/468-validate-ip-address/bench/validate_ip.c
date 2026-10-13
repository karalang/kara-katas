// Benchmark for #468: mirror of validate_ip.kara (the ★ arm: split on the
// separator) on the same workload. The parts are found by scanning for
// the separator; the answer is a static string, where the Kāra arm
// builds a fresh String.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool ipv4_part(const char *part, size_t length) {
    if (length == 0 || length > 3) {
        return false;
    }
    int64_t value = 0;
    for (size_t i = 0; i < length; i++) {
        char c = part[i];
        if (!(c >= '0' && c <= '9')) {
            return false;
        }
        value = value * 10 + (c - 48);
    }
    if (length > 1 && part[0] == '0') {
        return false;
    }
    return value <= 255;
}

static bool is_hex(char c) {
    return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
}

static bool ipv6_group(const char *group, size_t length) {
    if (length == 0 || length > 4) {
        return false;
    }
    for (size_t i = 0; i < length; i++) {
        if (!is_hex(group[i])) {
            return false;
        }
    }
    return true;
}

static const char *valid_ip_address(const char *query_ip) {
    if (strchr(query_ip, '.') != NULL) {
        int parts = 0;
        const char *start = query_ip;
        for (;;) {
            const char *end = strchr(start, '.');
            size_t length = end ? (size_t)(end - start) : strlen(start);
            if (!ipv4_part(start, length)) {
                return "Neither";
            }
            parts += 1;
            if (!end) {
                break;
            }
            start = end + 1;
        }
        if (parts == 4) {
            return "IPv4";
        }
    } else if (strchr(query_ip, ':') != NULL) {
        int groups = 0;
        const char *start = query_ip;
        for (;;) {
            const char *end = strchr(start, ':');
            size_t length = end ? (size_t)(end - start) : strlen(start);
            if (!ipv6_group(start, length)) {
                return "Neither";
            }
            groups += 1;
            if (!end) {
                break;
            }
            start = end + 1;
        }
        if (groups == 8) {
            return "IPv6";
        }
    }
    return "Neither";
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char pick(const char *alphabet, int64_t *seed) {
    return alphabet[next_random(seed) % (int64_t)strlen(alphabet)];
}

// Room for the longest query: 9 groups of up to 5 digits and 8 colons.
static char *random_query(int64_t *seed) {
    char *s = malloc(64);
    size_t n = 0;
    int64_t kind = next_random(seed) % 5;
    int64_t fault = next_random(seed) % 8;
    if (kind < 2) {
        static const int64_t counts[2] = {3, 5};
        int64_t parts = fault == 4 ? counts[next_random(seed) % 2] : 4;
        int64_t at = next_random(seed) % parts;
        for (int64_t p = 0; p < parts; p++) {
            if (p > 0) {
                s[n++] = '.';
            }
            int64_t value = next_random(seed) % 256;
            if (p == at && fault == 5) {
                s[n++] = '0';
            }
            if (p == at && fault == 6) {
                value = 256 + next_random(seed) % 744;
            }
            if (p == at && fault == 7) {
                if (next_random(seed) % 2 == 0) {
                    s[n++] = pick("aeFx", seed);
                }
                continue;
            }
            n += (size_t)sprintf(s + n, "%lld", (long long)value);
        }
    } else if (kind < 4) {
        static const int64_t counts[2] = {7, 9};
        int64_t groups = fault == 4 ? counts[next_random(seed) % 2] : 8;
        int64_t at = next_random(seed) % groups;
        for (int64_t g = 0; g < groups; g++) {
            if (g > 0) {
                s[n++] = ':';
            }
            if (g == at && fault == 6) {
                continue;
            }
            int64_t length = (g == at && fault == 5) ? 5 : 1 + next_random(seed) % 4;
            int64_t bad = (g == at && fault == 7) ? next_random(seed) % length : -1;
            for (int64_t i = 0; i < length; i++) {
                if (i == bad) {
                    s[n++] = pick("gGxz", seed);
                } else {
                    s[n++] = pick("0123456789abcdefABCDEF", seed);
                }
            }
        }
    } else {
        int64_t length = 1 + next_random(seed) % 15;
        for (int64_t i = 0; i < length; i++) {
            s[n++] = pick("0123456789aF.:g", seed);
        }
    }
    s[n] = '\0';
    return s;
}

int main(void) {
    const int64_t count = 100000;
    const int64_t rounds = 20;
    int64_t seed = 468;
    char **queries = malloc(sizeof(char *) * (size_t)count);
    for (int64_t i = 0; i < count; i++) {
        queries[i] = random_query(&seed);
    }
    int64_t ipv4 = 0, ipv6 = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            const char *answer = valid_ip_address(queries[i]);
            int64_t code;
            if (strcmp(answer, "IPv4") == 0) {
                ipv4 += 1;
                code = 1;
            } else if (strcmp(answer, "IPv6") == 0) {
                ipv6 += 1;
                code = 2;
            } else {
                code = 3;
            }
            checksum = (checksum * 7 + code + i) % 1000000007;
        }
    }
    printf("%lld rounds of %lld queries: %lld IPv4, %lld IPv6, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)ipv4, (long long)ipv6, (long long)checksum);
    for (int64_t i = 0; i < count; i++) {
        free(queries[i]);
    }
    free(queries);
    return 0;
}
