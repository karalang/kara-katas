/*
 * LeetCode 631 -- Design Excel Sum Formula, bench mirror in C.
 *
 * The rebuild arm of excel.kara: every formula is the list of cells it
 * reads, and after each write a depth-first walk orders the formula
 * cells and recomputes them all, with `seen` and `order` allocated
 * fresh each time as the Kara program does. Range names are parsed in
 * place rather than split into new strings. Same 2,000 operations, same
 * 60 rounds, same output line.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *items;
    int64_t len, cap;
} List;

static void push(List *l, int64_t v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof(int64_t));
    }
    l->items[l->len++] = v;
}

typedef struct {
    int64_t width, cells;
    int64_t *values;
    List *formulas; /* items == NULL means no formula */
    char *has;
} Excel;

static Excel excel_new(int64_t height, char width) {
    Excel e;
    e.width = width - 'A' + 1;
    e.cells = height * e.width;
    e.values = calloc(e.cells, sizeof(int64_t));
    e.formulas = calloc(e.cells, sizeof(List));
    e.has = calloc(e.cells, 1);
    return e;
}

static void excel_free(Excel *e) {
    for (int64_t i = 0; i < e->cells; i++) free(e->formulas[i].items);
    free(e->formulas);
    free(e->values);
    free(e->has);
}

static int64_t cell(const Excel *e, int64_t row, char column) {
    return (row - 1) * e->width + (column - 'A');
}

static void visit(const Excel *e, int64_t at, char *seen, List *order) {
    if (seen[at]) return;
    seen[at] = 1;
    if (e->has[at]) {
        const List *reads = &e->formulas[at];
        for (int64_t i = 0; i < reads->len; i++) visit(e, reads->items[i], seen, order);
    }
    push(order, at);
}

static void recompute(Excel *e) {
    char *seen = calloc(e->cells, 1);
    List order = {0};
    for (int64_t at = 0; at < e->cells; at++) visit(e, at, seen, &order);
    for (int64_t i = 0; i < order.len; i++) {
        int64_t at = order.items[i];
        if (e->has[at]) {
            const List *reads = &e->formulas[at];
            int64_t total = 0;
            for (int64_t j = 0; j < reads->len; j++) total += e->values[reads->items[j]];
            e->values[at] = total;
        }
    }
    free(order.items);
    free(seen);
}

static void excel_set(Excel *e, int64_t row, char column, int64_t val) {
    int64_t at = cell(e, row, column);
    e->values[at] = val;
    free(e->formulas[at].items);
    e->formulas[at] = (List){0};
    e->has[at] = 0;
    recompute(e);
}

static int64_t excel_get(const Excel *e, int64_t row, char column) {
    return e->values[cell(e, row, column)];
}

/* The zero-based row and column of a name such as `B12`, read up to `end`. */
static void position(const char *name, const char *end, int64_t *row, int64_t *column) {
    *column = name[0] - 'A';
    int64_t r = 0;
    for (const char *p = name + 1; p < end; p++) r = r * 10 + (*p - '0');
    *row = r - 1;
}

static int64_t excel_sum(Excel *e, int64_t row, char column, char **numbers, int64_t count) {
    int64_t at = cell(e, row, column);
    List reads = {0};
    for (int64_t i = 0; i < count; i++) {
        const char *range = numbers[i];
        const char *colon = strchr(range, ':');
        const char *end = range + strlen(range);
        int64_t top, left, bottom, right;
        position(range, colon ? colon : end, &top, &left);
        if (colon) position(colon + 1, end, &bottom, &right);
        else { bottom = top; right = left; }
        for (int64_t r = top; r <= bottom; r++)
            for (int64_t c = left; c <= right; c++) push(&reads, r * e->width + c);
    }
    free(e->formulas[at].items);
    e->formulas[at] = reads;
    e->has[at] = 1;
    recompute(e);
    return e->values[at];
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static char letter(int64_t index) { return (char)('A' + index); }

typedef struct {
    int64_t kind, row, val, count;
    char column;
    char *ranges[3];
} Op;

static Op *make_ops(int64_t count, int64_t *seed) {
    Op *ops = calloc(count, sizeof(Op));
    for (int64_t i = 0; i < count; i++) {
        Op *op = &ops[i];
        op->kind = next_random(seed) % 3;
        op->row = 1 + next_random(seed) % 26;
        op->column = letter(next_random(seed) % 26);
        if (op->kind == 0) {
            op->val = next_random(seed) % 2001 - 1000;
        } else if (op->kind == 1 && op->row > 1) {
            int64_t n = 1 + next_random(seed) % 3;
            for (int64_t k = 0; k < n; k++) {
                int64_t top = 1 + next_random(seed) % (op->row - 1);
                int64_t left = next_random(seed) % 26;
                int64_t bottom = top + next_random(seed) % 2;
                if (bottom > op->row - 1) bottom = op->row - 1;
                int64_t right = left + next_random(seed) % 2;
                if (right > 25) right = 25;
                char *s = malloc(48);
                if (top == bottom && left == right)
                    snprintf(s, 48, "%c%lld", letter(left), (long long)top);
                else
                    snprintf(s, 48, "%c%lld:%c%lld", letter(left), (long long)top,
                             letter(right), (long long)bottom);
                op->ranges[op->count++] = s;
            }
        } else {
            op->kind = 2;
        }
    }
    return ops;
}

int main(void) {
    int64_t seed = 631;
    const int64_t count = 2000, rounds = 60;
    Op *ops = make_ops(count, &seed);
    int64_t sums = 0, checksum = 0, total = 0;
    for (int64_t round = 0; round < rounds; round++) {
        Excel sheet = excel_new(26, 'Z');
        for (int64_t i = 0; i < count; i++) {
            const Op *op = &ops[i];
            int64_t result = 0;
            if (op->kind == 0) {
                excel_set(&sheet, op->row, op->column, op->val);
            } else if (op->kind == 1) {
                result = excel_sum(&sheet, op->row, op->column, (char **)op->ranges, op->count);
                sums++;
            } else {
                result = excel_get(&sheet, op->row, op->column);
            }
            checksum = ((checksum * 31 + result) % 1000000007 + 1000000007) % 1000000007;
        }
        for (int64_t row = 1; row < 27; row++)
            for (int64_t c = 0; c < 26; c++) total += excel_get(&sheet, row, letter(c));
        excel_free(&sheet);
    }
    printf("%lld operations, %lld rounds (%lld sums): checksum %lld, sheet total %lld\n",
           (long long)count, (long long)rounds, (long long)sums, (long long)checksum,
           (long long)total);
    for (int64_t i = 0; i < count; i++)
        for (int64_t k = 0; k < ops[i].count; k++) free(ops[i].ranges[k]);
    free(ops);
    return 0;
}
