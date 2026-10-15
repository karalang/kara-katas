#include <stdio.h>
#include <stdlib.h>
#include <string.h>
extern const char *greet(const char *who);
extern char *greet_dup(const char *who);
extern int greet_score(int x);
static int counter = 3;
int shared_total;
const char banner[] = "app 1.4";
int add(int a, int b) { return a + b + counter; }
int main(int argc, char **argv) {
    char buf[32];
    strncpy(buf, argc > 1 ? argv[1] : "world", sizeof buf - 1);
    buf[31] = 0;
    char *d = greet_dup(buf);
    printf("%s: %s %s %d\n", banner, greet(buf), d, add(argc, greet_score(2)));
    free(d);
    shared_total += argc;
    return 0;
}
