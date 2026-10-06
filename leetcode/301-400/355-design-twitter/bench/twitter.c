// Bench for LeetCode #355 -- C mirror of twitter.kara (the starred arm):
// per-user tweet lists merged newest-first through a priority queue.
//
// Users are the dense ids 0..USERS-1, so the per-user maps are arrays indexed
// by user id and a follow set is a growable list of ids with a membership
// matrix to keep it a set. The merge is the same binary-heap merge.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define USERS 1000
#define POSTS 300000
#define FOLLOWS 100000
#define FEEDS 300000

typedef struct { int64_t time, id; } Tweet;
typedef struct { Tweet *items; int64_t len, cap; } TweetList;
typedef struct { int64_t *items; int64_t len, cap; } IdList;
typedef struct { int64_t time, tweet, author, index; } Candidate;

static TweetList tweets[USERS];
static IdList followees[USERS];
static unsigned char following[USERS][USERS];
static int64_t clock_now = 0;

static void post_tweet(int64_t user, int64_t id) {
    TweetList *l = &tweets[user];
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, (size_t)l->cap * sizeof(Tweet));
    }
    clock_now += 1;
    l->items[l->len++] = (Tweet){clock_now, id};
}

static void follow(int64_t follower, int64_t followee) {
    if (following[follower][followee]) return;
    following[follower][followee] = 1;
    IdList *l = &followees[follower];
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, (size_t)l->cap * sizeof(int64_t));
    }
    l->items[l->len++] = followee;
}

// Max-heap in the Kāra arm's derived-Ord order: time, tweet, author, index.
static int outranks(const Candidate *a, const Candidate *b) {
    if (a->time != b->time) return a->time > b->time;
    if (a->tweet != b->tweet) return a->tweet > b->tweet;
    if (a->author != b->author) return a->author > b->author;
    return a->index > b->index;
}

static Candidate heap[USERS + 1];
static int64_t heap_len;

static void heap_push(Candidate c) {
    int64_t i = heap_len++;
    heap[i] = c;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (!outranks(&heap[i], &heap[p])) break;
        Candidate t = heap[i]; heap[i] = heap[p]; heap[p] = t;
        i = p;
    }
}

static Candidate heap_pop(void) {
    Candidate top = heap[0];
    heap[0] = heap[--heap_len];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, best = i;
        if (l < heap_len && outranks(&heap[l], &heap[best])) best = l;
        if (r < heap_len && outranks(&heap[r], &heap[best])) best = r;
        if (best == i) break;
        Candidate t = heap[i]; heap[i] = heap[best]; heap[best] = t;
        i = best;
    }
    return top;
}

static int64_t news_feed(int64_t user, int64_t *feed) {
    heap_len = 0;
    if (tweets[user].len > 0) {
        int64_t last = tweets[user].len - 1;
        heap_push((Candidate){tweets[user].items[last].time, tweets[user].items[last].id, user, last});
    }
    for (int64_t k = 0; k < followees[user].len; k++) {
        int64_t a = followees[user].items[k];
        if (a == user || tweets[a].len == 0) continue;
        int64_t last = tweets[a].len - 1;
        heap_push((Candidate){tweets[a].items[last].time, tweets[a].items[last].id, a, last});
    }
    int64_t n = 0;
    while (n < 10 && heap_len > 0) {
        Candidate c = heap_pop();
        feed[n++] = c.tweet;
        if (c.index > 0) {
            Tweet older = tweets[c.author].items[c.index - 1];
            heap_push((Candidate){older.time, older.id, c.author, c.index - 1});
        }
    }
    return n;
}

int main(void) {
    int64_t seed = 355;
    for (int64_t i = 0; i < POSTS; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        post_tweet(seed % USERS, i);
    }
    for (int64_t i = 0; i < FOLLOWS; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t a = seed % USERS;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        follow(a, seed % USERS);
    }
    int64_t sink = 0, feed[10];
    for (int64_t i = 0; i < FEEDS; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t n = news_feed(seed % USERS, feed);
        for (int64_t k = 0; k < n; k++) sink = (sink * 31 + feed[k]) % 1000000007;
    }
    printf("%lld\n", (long long)sink);
    return 0;
}
