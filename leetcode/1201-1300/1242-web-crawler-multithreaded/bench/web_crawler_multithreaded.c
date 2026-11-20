// LeetCode #1242 bench: the ★ arm in C, a crawl by levels, each level's
// pages fetched by up to 8 pthreads, each a contiguous part of the level,
// joined in order, over the same 50 webs of 1000 urls, 4 starts and 10
// passes as the Kāra bench. The judge hands back a fresh copy of a page's
// links, as the other languages' do, and the crawl keeps the urls it has
// seen in an open-addressing hash set of strings.
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static unsigned long hash_str(const char *s) {
    unsigned long h = 1469598103934665603UL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211UL;
    return h;
}

// A set of strings it owns, with linear probing.
typedef struct {
    char **slots;
    long cap, len;
} StrSet;

static void set_init(StrSet *s, long cap) {
    s->cap = cap;
    s->len = 0;
    s->slots = calloc(cap, sizeof(char *));
}

static long set_find(const StrSet *s, const char *key) {
    long i = hash_str(key) & (s->cap - 1);
    while (s->slots[i] && strcmp(s->slots[i], key) != 0) i = (i + 1) & (s->cap - 1);
    return i;
}

static void set_grow(StrSet *s);

static int set_insert(StrSet *s, const char *key) {
    if (2 * (s->len + 1) > s->cap) set_grow(s);
    long i = set_find(s, key);
    if (s->slots[i]) return 0;
    s->slots[i] = strdup(key);
    s->len++;
    return 1;
}

static void set_grow(StrSet *s) {
    StrSet t;
    set_init(&t, s->cap * 2);
    for (long i = 0; i < s->cap; i++)
        if (s->slots[i]) {
            t.slots[set_find(&t, s->slots[i])] = s->slots[i];
            t.len++;
        }
    free(s->slots);
    *s = t;
}

static void set_free(StrSet *s) {
    for (long i = 0; i < s->cap; i++) free(s->slots[i]);
    free(s->slots);
}

// The judge: each url's links, found through a hash map from url to index.
typedef struct {
    char **urls;
    long n;
    char ***links;
    long *count, *room;
    long *index;  // open-addressing table of url indices, -1 empty
    long cap;
} Site;

static long site_lookup(const Site *w, const char *url) {
    long i = hash_str(url) & (w->cap - 1);
    while (w->index[i] >= 0) {
        if (strcmp(w->urls[w->index[i]], url) == 0) return w->index[i];
        i = (i + 1) & (w->cap - 1);
    }
    return -1;
}

static char **get_urls(const Site *w, const char *url, long *n) {
    long k = site_lookup(w, url);
    *n = k < 0 ? 0 : w->count[k];
    char **out = malloc((*n + 1) * sizeof(char *));
    for (long i = 0; i < *n; i++) out[i] = strdup(w->links[k][i]);
    return out;
}

static size_t host_len(const char *url) {
    const char *h = url + 7;
    const char *slash = strchr(h, '/');
    return slash ? (size_t)(slash - h) : strlen(h);
}

// One thread's part of a level: urls[lo..hi), each page's links and count.
typedef struct {
    const Site *w;
    char **urls;
    long lo, hi;
    char ***pages;
    long *counts;
} Part;

static void *fetch_part(void *arg) {
    Part *p = arg;
    for (long i = p->lo; i < p->hi; i++) p->pages[i] = get_urls(p->w, p->urls[i], &p->counts[i]);
    return NULL;
}

static long crawl(const char *start, const Site *w) {
    size_t hl = host_len(start);
    StrSet seen;
    set_init(&seen, 64);
    set_insert(&seen, start);
    long len = 1;
    char **level = malloc(sizeof(char *));
    level[0] = strdup(start);
    while (len > 0) {
        char ***pages = malloc(len * sizeof(char **));
        long *counts = malloc(len * sizeof(long));
        long chunk = (len + 7) / 8;
        pthread_t threads[8];
        Part parts[8];
        int nt = 0;
        for (long lo = 0; lo < len; lo += chunk, nt++) {
            parts[nt] = (Part){w, level, lo, lo + chunk < len ? lo + chunk : len, pages, counts};
            pthread_create(&threads[nt], NULL, fetch_part, &parts[nt]);
        }
        for (int t = 0; t < nt; t++) pthread_join(threads[t], NULL);
        long next_len = 0, next_cap = 64;
        char **next_level = malloc(next_cap * sizeof(char *));
        for (long k = 0; k < len; k++) {
            for (long i = 0; i < counts[k]; i++) {
                char *u = pages[k][i];
                if (host_len(u) == hl && strncmp(u + 7, start + 7, hl) == 0 && set_insert(&seen, u)) {
                    if (next_len == next_cap) {
                        next_cap *= 2;
                        next_level = realloc(next_level, next_cap * sizeof(char *));
                    }
                    next_level[next_len++] = u;
                } else {
                    free(u);
                }
            }
            free(pages[k]);
            free(level[k]);
        }
        free(pages);
        free(counts);
        free(level);
        level = next_level;
        len = next_len;
    }
    free(level);
    long found = seen.len;
    set_free(&seen);
    return found;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    const char *names[] = {"news.yahoo.com", "news.google.com", "yahoo.com"};
    long seed = 1242;
    Site webs[50];
    for (int t = 0; t < 50; t++) {
        Site *w = &webs[t];
        w->n = 1000;
        w->urls = malloc(1000 * sizeof(char *));
        w->links = malloc(1000 * sizeof(char **));
        w->count = calloc(1000, sizeof(long));
        w->room = calloc(1000, sizeof(long));
        w->cap = 2048;
        w->index = malloc(w->cap * sizeof(long));
        for (long i = 0; i < w->cap; i++) w->index[i] = -1;
        for (long i = 0; i < 1000; i++) {
            char buf[64];
            snprintf(buf, sizeof buf, "http://%s/page/%ld", names[next_random(&seed) % 3], i);
            w->urls[i] = strdup(buf);
            w->links[i] = NULL;
            long j = hash_str(buf) & (w->cap - 1);
            while (w->index[j] >= 0) j = (j + 1) & (w->cap - 1);
            w->index[j] = i;
        }
        for (int k = 0; k < 5000; k++) {
            long from = next_random(&seed) % 1000;
            long to = next_random(&seed) % 1000;
            if (w->count[from] == w->room[from]) {
                w->room[from] = w->room[from] ? 2 * w->room[from] : 4;
                w->links[from] = realloc(w->links[from], w->room[from] * sizeof(char *));
            }
            w->links[from][w->count[from]++] = strdup(w->urls[to]);
        }
    }
    long check = 0;
    for (int pass = 0; pass < 10; pass++)
        for (int t = 0; t < 50; t++)
            for (int s = 0; s < 4; s++)
                check = (check * 131 + crawl(webs[t].urls[s * 250], &webs[t])) % 1000000007;
    printf("50 webs of 1000 urls, 4 starts, 10 passes: checksum %ld\n", check);
    for (int t = 0; t < 50; t++) {
        Site *w = &webs[t];
        for (long i = 0; i < 1000; i++) {
            for (long k = 0; k < w->count[i]; k++) free(w->links[i][k]);
            free(w->links[i]);
            free(w->urls[i]);
        }
        free(w->urls);
        free(w->links);
        free(w->count);
        free(w->room);
        free(w->index);
    }
    return 0;
}
