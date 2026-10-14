// Benchmark for #588: C mirror of the ★ arm (a tree of shared nodes);
// see file_system.kara. Each node is a heap block, and a directory keeps
// its entries in an array sorted by name, found by binary search and
// grown by insertion, since C has no sorted map. A file system is freed
// whole after each script.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node Node;

typedef struct {
    char *name;
    Node *child;
} Slot;

struct Node {
    int is_file;
    char *content;
    size_t content_len, content_cap;
    Slot *children;
    size_t len, cap;
};

static Node *new_node(void) {
    return calloc(1, sizeof(Node));
}

static void free_node(Node *n) {
    for (size_t i = 0; i < n->len; i++) {
        free(n->children[i].name);
        free_node(n->children[i].child);
    }
    free(n->children);
    free(n->content);
    free(n);
}

// The index of `name` in n's entries, or where it would go.
static size_t lower_bound(const Node *n, const char *name, size_t name_len, int *found) {
    size_t lo = 0, hi = n->len;
    while (lo < hi) {
        size_t mid = (lo + hi) / 2;
        const char *other = n->children[mid].name;
        size_t other_len = strlen(other);
        size_t k = name_len < other_len ? name_len : other_len;
        int c = memcmp(other, name, k);
        if (c == 0) c = other_len < name_len ? -1 : other_len > name_len ? 1 : 0;
        if (c < 0) lo = mid + 1; else hi = mid;
    }
    *found = 0;
    if (lo < n->len) {
        const char *other = n->children[lo].name;
        *found = strlen(other) == name_len && memcmp(other, name, name_len) == 0;
    }
    return lo;
}

static Node *walk(Node *root, const char *path, int make) {
    Node *n = root;
    const char *p = path;
    while (*p) {
        while (*p == '/') p++;
        if (!*p) break;
        const char *end = p;
        while (*end && *end != '/') end++;
        size_t len = end - p;
        int found;
        size_t at = lower_bound(n, p, len, &found);
        if (!found) {
            if (!make) return NULL;
            if (n->len == n->cap) {
                n->cap = n->cap ? n->cap * 2 : 4;
                n->children = realloc(n->children, n->cap * sizeof(Slot));
            }
            memmove(&n->children[at + 1], &n->children[at], (n->len - at) * sizeof(Slot));
            char *name = malloc(len + 1);
            memcpy(name, p, len);
            name[len] = 0;
            n->children[at].name = name;
            n->children[at].child = new_node();
            n->len++;
        }
        n = n->children[at].child;
        p = end;
    }
    return n;
}

// ---- benchmark --------------------------------------------------------------

enum { LS, MKDIR, ADD, READ };

typedef struct {
    int kind;
    char path[24];
    char content[8];
} Op;

static int64_t seed = 588;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void dir_path(int64_t depth, char *out) {
    size_t len = 0;
    for (int64_t i = 0; i < depth; i++) {
        out[len++] = '/';
        out[len++] = (char)('a' + next_random() % 5);
    }
    out[len] = 0;
}

static void script(Op *ops) {
    static char made[400][24];
    static char files[400][24];
    size_t made_len = 1, files_len = 0, len = 0;
    strcpy(made[0], "/");
    while (len < 300) {
        int64_t roll = next_random() % 10;
        Op *o = &ops[len];
        if (roll < 3) {
            o->kind = LS;
            strcpy(o->path, made[next_random() % (int64_t)made_len]);
        } else if (roll < 4 && files_len > 0) {
            o->kind = READ;
            strcpy(o->path, files[next_random() % (int64_t)files_len]);
        } else if (roll < 7) {
            o->kind = MKDIR;
            dir_path(1 + next_random() % 4, o->path);
            strcpy(made[made_len++], o->path);
        } else {
            o->kind = ADD;
            int64_t k = next_random() % 5;
            dir_path(next_random() % 4, o->path);
            size_t at = strlen(o->path);
            o->path[at] = '/';
            o->path[at + 1] = (char)('f' + k);
            o->path[at + 2] = 0;
            int64_t n = 1 + next_random() % 5;
            for (int64_t i = 0; i < n; i++) o->content[i] = (char)('f' + next_random() % 5);
            o->content[n] = 0;
            strcpy(made[made_len++], o->path);
            strcpy(files[files_len++], o->path);
        }
        len++;
    }
}

int main(void) {
    int64_t count = 200, rounds = 200;
    Op *scripts = malloc(sizeof(Op) * 300 * count);
    for (int64_t g = 0; g < count; g++) script(&scripts[g * 300]);
    int64_t lines = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            Op *ops = &scripts[((round * 7 + g) % count) * 300];
            Node *root = new_node();
            for (int i = 0; i < 300; i++) {
                Op *o = &ops[i];
                if (o->kind == LS) {
                    Node *n = walk(root, o->path, 0);
                    if (n->is_file) {
                        const char *last = strrchr(o->path, '/') + 1;
                        checksum = (checksum * 31 + (int64_t)strlen(last)) % 1000000007;
                    } else {
                        for (size_t j = 0; j < n->len; j++)
                            checksum = (checksum * 31 + (int64_t)strlen(n->children[j].name)) % 1000000007;
                    }
                    lines++;
                } else if (o->kind == MKDIR) {
                    walk(root, o->path, 1);
                } else if (o->kind == ADD) {
                    Node *n = walk(root, o->path, 1);
                    n->is_file = 1;
                    size_t add = strlen(o->content);
                    if (n->content_len + add + 1 > n->content_cap) {
                        n->content_cap = (n->content_len + add + 1) * 2;
                        n->content = realloc(n->content, n->content_cap);
                    }
                    memcpy(n->content + n->content_len, o->content, add + 1);
                    n->content_len += add;
                } else {
                    Node *n = walk(root, o->path, 0);
                    checksum = (checksum * 31 + (int64_t)n->content_len) % 1000000007;
                    lines++;
                }
            }
            free_node(root);
        }
    }
    printf("%lld scripts of 300 commands, %lld rounds: %lld answers, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)lines, (long long)checksum);
    free(scripts);
    return 0;
}
