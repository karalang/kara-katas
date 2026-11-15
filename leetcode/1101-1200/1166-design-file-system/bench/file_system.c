// LeetCode #1166: Design File System -- the ★ arm's bench in C: one
// open-addressing hash table (FNV-1a) from a made path, copied in, to its
// value.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *key;
    size_t len;
    int64_t value;
} Slot;

typedef struct {
    Slot *slots;
    size_t cap, n;
} FileSystem;

static uint64_t fnv(const char *s, size_t len) {
    uint64_t h = 1469598103934665603ULL;
    for (size_t i = 0; i < len; i++) {
        h ^= (unsigned char)s[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static void fs_init(FileSystem *fs) {
    fs->cap = 16;
    fs->n = 0;
    fs->slots = calloc(fs->cap, sizeof(Slot));
}

static void fs_free(FileSystem *fs) {
    for (size_t i = 0; i < fs->cap; i++) free(fs->slots[i].key);
    free(fs->slots);
}

static Slot *find(const FileSystem *fs, const char *s, size_t len) {
    size_t i = fnv(s, len) & (fs->cap - 1);
    for (;;) {
        Slot *t = &fs->slots[i];
        if (!t->key || (t->len == len && memcmp(t->key, s, len) == 0)) return t;
        i = (i + 1) & (fs->cap - 1);
    }
}

static void grow(FileSystem *fs) {
    Slot *old = fs->slots;
    size_t cap = fs->cap;
    fs->cap *= 2;
    fs->slots = calloc(fs->cap, sizeof(Slot));
    for (size_t i = 0; i < cap; i++)
        if (old[i].key) *find(fs, old[i].key, old[i].len) = old[i];
    free(old);
}

static int create_path(FileSystem *fs, const char *path, int64_t value) {
    size_t len = strlen(path);
    if (len == 0 || (len == 1 && path[0] == '/') || find(fs, path, len)->key) return 0;
    size_t cut = len;
    while (path[cut - 1] != '/') cut--;
    cut--;
    if (cut > 0 && !find(fs, path, cut)->key) return 0;
    if (2 * (fs->n + 1) > fs->cap) grow(fs);
    Slot *t = find(fs, path, len);
    t->key = malloc(len);
    memcpy(t->key, path, len);
    t->len = len;
    t->value = value;
    fs->n++;
    return 1;
}

static int64_t get(const FileSystem *fs, const char *path) {
    Slot *t = find(fs, path, strlen(path));
    return t->key ? t->value : -1;
}

static int64_t seed = 1166;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const char *names[] = {"a", "b", "ab", "le", "leet", "code"};
    static char *paths[16][10000];
    static int creates[16][10000];
    for (int k = 0; k < 16; k++) {
        for (int i = 0; i < 10000; i++) {
            int64_t parts = 1 + next_random() % 5;
            char p[64] = "";
            for (int64_t j = 0; j < parts; j++) {
                strcat(p, "/");
                strcat(p, names[next_random() % 6]);
            }
            paths[k][i] = strdup(p);
            creates[k][i] = next_random() % 4 != 0;
        }
    }
    int64_t made = 0, check = 0;
    for (int r = 0; r < 100; r++) {
        for (int k = 0; k < 16; k++) {
            int64_t from = next_random() % 5000;
            FileSystem fs;
            fs_init(&fs);
            for (int64_t i = from; i < 10000; i++) {
                int64_t a;
                if (creates[k][i]) {
                    a = create_path(&fs, paths[k][i], i);
                    made += a;
                } else {
                    a = get(&fs, paths[k][i]);
                }
                check = (check * 31 + a + 2) % 1000000007;
            }
            fs_free(&fs);
        }
    }
    printf("100 rounds over 16 lists of 10^4 operations: made %lld, checksum %lld\n", (long long)made,
           (long long)check);
    return 0;
}
