// LeetCode #690: Employee Importance -- breadth first, by id. Bench.
//
// 30 companies of 2,000 people, ids 1 to 2000 in random order, each
// person under a random earlier one, are built once, with 100 random
// people to ask about in each; then 80 rounds ask about all of them.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t id;
    int64_t importance;
    int64_t *subordinates;
    int64_t nsubordinates;
} Employee;

static int64_t get_importance(const Employee *employees, int64_t n, int64_t id) {
    int64_t *at = malloc(2001 * sizeof(int64_t));
    for (int64_t i = 0; i < 2001; i++) {
        at[i] = -1;
    }
    for (int64_t i = 0; i < n; i++) {
        at[employees[i].id] = i;
    }
    // A ring buffer, grown by doubling like a VecDeque.
    int64_t cap = 4, head = 0, len = 0;
    int64_t *queue = malloc((size_t)cap * sizeof(int64_t));
    queue[0] = id;
    len = 1;
    int64_t sum = 0;
    while (len > 0) {
        int64_t next = queue[head];
        head = (head + 1) % cap;
        len--;
        const Employee *e = &employees[at[next]];
        sum += e->importance;
        for (int64_t s = 0; s < e->nsubordinates; s++) {
            if (len == cap) {
                int64_t *bigger = malloc((size_t)(2 * cap) * sizeof(int64_t));
                for (int64_t i = 0; i < len; i++) {
                    bigger[i] = queue[(head + i) % cap];
                }
                free(queue);
                queue = bigger;
                head = 0;
                cap *= 2;
            }
            queue[(head + len) % cap] = e->subordinates[s];
            len++;
        }
    }
    free(queue);
    free(at);
    return sum;
}

static int64_t seed = 690;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 30, rounds = 80, size = 2000;
    Employee *companies[30];
    int64_t questions[30][100];
    int64_t *ids = malloc((size_t)size * sizeof(int64_t));
    int64_t *nsubs = malloc((size_t)size * sizeof(int64_t));
    int64_t *bosses = malloc((size_t)size * sizeof(int64_t));
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < size; i++) {
            ids[i] = i + 1;
        }
        for (int64_t i = 0; i < size; i++) {
            int64_t j = i + next_random() % (size - i);
            int64_t t = ids[i];
            ids[i] = ids[j];
            ids[j] = t;
        }
        Employee *company = malloc((size_t)size * sizeof(Employee));
        for (int64_t i = 0; i < size; i++) {
            nsubs[i] = 0;
        }
        bosses[0] = -1;
        for (int64_t i = 1; i < size; i++) {
            bosses[i] = next_random() % i;
            nsubs[bosses[i]]++;
        }
        for (int64_t i = 0; i < size; i++) {
            company[i].subordinates = malloc((size_t)(nsubs[i] > 0 ? nsubs[i] : 1) * sizeof(int64_t));
            company[i].nsubordinates = 0;
        }
        for (int64_t i = 1; i < size; i++) {
            Employee *b = &company[bosses[i]];
            b->subordinates[b->nsubordinates++] = ids[i];
        }
        for (int64_t i = 0; i < size; i++) {
            company[i].id = ids[i];
            company[i].importance = next_random() % 201 - 100;
        }
        companies[c] = company;
        for (int64_t q = 0; q < 100; q++) {
            questions[c][q] = 1 + next_random() % size;
        }
    }
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            for (int64_t q = 0; q < 100; q++) {
                int64_t got = get_importance(companies[c], size, questions[c][q]);
                sum = (sum * 31 + got + 1000000 + r) % 1000000007;
            }
        }
    }
    printf("%lld questions answered, checksum %lld\n", (long long)(count * rounds * 100), (long long)sum);
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < size; i++) {
            free(companies[c][i].subordinates);
        }
        free(companies[c]);
    }
    free(ids);
    free(nsubs);
    free(bosses);
    return 0;
}
