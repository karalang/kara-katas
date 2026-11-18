// LeetCode #2254: Design Video Sharing Platform -- the benchmark's C mirror
// of videos.kara: the videos in an array indexed by id, a flag for the
// ones held, and the freed ids in a binary min-heap, smallest first.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define CALLS 25000

typedef struct {
    int64_t kind, a, b, c;
    char text[9];
} Call;

typedef struct {
    char content[9];
    int64_t length, views, likes, dislikes;
    int held;
} Video;

static Call calls[CALLS];
static Video slots[CALLS];
static int64_t slot_count;
static int64_t heap[CALLS];
static int64_t heap_len;

static void heap_push(int64_t id) {
    int64_t at = heap_len++;
    heap[at] = id;
    while (at > 0 && heap[(at - 1) / 2] > heap[at]) {
        int64_t t = heap[at]; heap[at] = heap[(at - 1) / 2]; heap[(at - 1) / 2] = t;
        at = (at - 1) / 2;
    }
}

static int64_t heap_pop(void) {
    int64_t top = heap[0];
    heap[0] = heap[--heap_len];
    int64_t at = 0;
    for (;;) {
        int64_t least = at;
        for (int64_t child = 2 * at + 1; child <= 2 * at + 2; child++)
            if (child < heap_len && heap[child] < heap[least]) least = child;
        if (least == at) break;
        int64_t t = heap[at]; heap[at] = heap[least]; heap[least] = t;
        at = least;
    }
    return top;
}

static int held(int64_t id) { return id < slot_count && slots[id].held; }

static int64_t check, answered;

static void tally(const char *answer) {
    for (const char *p = answer; *p; p++) check = (check * 131 + (unsigned char)*p) % 1000000007;
    check = (check * 131 + 1) % 1000000007;
    answered++;
}

static void run(int64_t count) {
    slot_count = 0;
    heap_len = 0;
    char buf[64];
    for (int64_t i = 0; i < count; i++) {
        Call *call = &calls[i];
        int64_t id = call->a;
        switch (call->kind) {
        case 0: {
            int64_t at = heap_len > 0 ? heap_pop() : slot_count++;
            Video *v = &slots[at];
            strcpy(v->content, call->text);
            v->length = (int64_t)strlen(call->text);
            v->views = v->likes = v->dislikes = 0;
            v->held = 1;
            snprintf(buf, sizeof buf, "%lld", (long long)at);
            tally(buf);
            break;
        }
        case 1:
            if (held(id)) {
                slots[id].held = 0;
                heap_push(id);
            }
            break;
        case 2:
            if (!held(id)) {
                tally("-1");
            } else {
                Video *v = &slots[id];
                v->views++;
                int64_t last = call->c < v->length - 1 ? call->c : v->length - 1;
                int64_t n = last + 1 - call->b;
                memcpy(buf, v->content + call->b, (size_t)n);
                buf[n] = 0;
                tally(buf);
            }
            break;
        case 3:
            if (held(id)) slots[id].likes++;
            break;
        case 4:
            if (held(id)) slots[id].dislikes++;
            break;
        case 5:
            if (held(id)) snprintf(buf, sizeof buf, "[%lld, %lld]", (long long)slots[id].likes, (long long)slots[id].dislikes);
            else strcpy(buf, "[-1]");
            tally(buf);
            break;
        default:
            snprintf(buf, sizeof buf, "%lld", (long long)(held(id) ? slots[id].views : -1));
            tally(buf);
        }
    }
}

static int64_t seed = 2254;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void calls_of(int64_t count, int64_t longest) {
    int64_t uploads = 0;
    for (int64_t i = 0; i < count; i++) {
        Call *call = &calls[i];
        int64_t pick = next_random() % 10;
        int64_t id = next_random() % (uploads + 2);
        call->a = id;
        if (pick < 3) {
            int64_t length = next_random() % (longest - 2) + 3;
            for (int64_t k = 0; k < length; k++) call->text[k] = (char)('0' + next_random() % 10);
            call->text[length] = 0;
            call->kind = 0;
            uploads++;
        } else if (pick == 3) {
            call->kind = 1;
        } else if (pick < 6) {
            call->b = next_random() % 3;
            call->c = call->b + next_random() % 8 + 1;
            call->kind = 2;
        } else {
            call->kind = pick - 3;
        }
    }
}

int main(void) {
    for (int t = 0; t < 120; t++) {
        calls_of(CALLS, 8);
        run(CALLS);
    }
    printf("120 platforms of 25000 calls: %lld answers, checksum %lld\n", (long long)answered, (long long)check);
    return 0;
}
