// Benchmark for #817: Linked List Components -- mirror of the ★ arm (count
// the ends), with the same workload as linked_list_components.kara. The
// set of nums is an open-addressing hash table, sized for nums and freed
// after each count.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static uint64_t mix(int64_t key) {
    uint64_t x = (uint64_t)key;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

typedef struct {
    int64_t *keys;
    char *used;
    size_t cap;
} Set;

static void set_insert(Set *s, int64_t key) {
    size_t at = mix(key) & (s->cap - 1);
    while (s->used[at] && s->keys[at] != key) {
        at = (at + 1) & (s->cap - 1);
    }
    s->used[at] = 1;
    s->keys[at] = key;
}

static int set_contains(const Set *s, int64_t key) {
    size_t at = mix(key) & (s->cap - 1);
    while (s->used[at]) {
        if (s->keys[at] == key) {
            return 1;
        }
        at = (at + 1) & (s->cap - 1);
    }
    return 0;
}

static int64_t num_components(const ListNode *head, const int64_t *nums, int64_t m) {
    Set wanted;
    wanted.cap = 16;
    while (wanted.cap < 2 * (size_t)m) {
        wanted.cap *= 2;
    }
    wanted.keys = malloc(wanted.cap * sizeof(int64_t));
    wanted.used = calloc(wanted.cap, 1);
    for (int64_t i = 0; i < m; i++) {
        set_insert(&wanted, nums[i]);
    }
    int64_t count = 0;
    for (const ListNode *node = head; node != NULL; node = node->next) {
        if (set_contains(&wanted, node->val) &&
            (node->next == NULL || !set_contains(&wanted, node->next->val))) {
            count++;
        }
    }
    free(wanted.keys);
    free(wanted.used);
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 64, N = 10000 };
    const int64_t rounds = 8000;
    int64_t seed = 817;
    static ListNode *lists[COUNT];
    static int64_t *inside[COUNT], *outside[COUNT];
    static int64_t ins[COUNT], outs[COUNT];
    int64_t order[N];
    for (int g = 0; g < COUNT; g++) {
        for (int64_t v = 0; v < N; v++) {
            order[v] = v;
        }
        for (int64_t i = 0; i < N; i++) {
            int64_t j = i + next_random(&seed) % (N - i);
            int64_t t = order[i];
            order[i] = order[j];
            order[j] = t;
        }
        ListNode *head = NULL;
        for (int64_t k = 0; k < N; k++) {
            ListNode *node = malloc(sizeof(ListNode));
            node->val = order[N - 1 - k];
            node->next = head;
            head = node;
        }
        lists[g] = head;
        for (int64_t i = 0; i < N; i++) {
            int64_t j = i + next_random(&seed) % (N - i);
            int64_t t = order[i];
            order[i] = order[j];
            order[j] = t;
        }
        int64_t m = 1 + next_random(&seed) % (N - 1);
        inside[g] = malloc(m * sizeof(int64_t));
        outside[g] = malloc((N - m) * sizeof(int64_t));
        for (int64_t i = 0; i < N; i++) {
            if (i < m) {
                inside[g][i] = order[i];
            } else {
                outside[g][i - m] = order[i];
            }
        }
        ins[g] = m;
        outs[g] = N - m;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int g = (int)(round % COUNT);
        int64_t a = next_random(&seed) % ins[g];
        int64_t b = next_random(&seed) % outs[g];
        int64_t swapped = inside[g][a];
        inside[g][a] = outside[g][b];
        outside[g][b] = swapped;
        int64_t answer = num_components(lists[g], inside[g], ins[g]);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    printf("%lld rounds of %d nodes: total %lld, checksum %lld\n", (long long)rounds, N,
           (long long)total, (long long)checksum);
    return 0;
}
