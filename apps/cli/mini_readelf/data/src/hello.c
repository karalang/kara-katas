#include <stdio.h>
#include <string.h>
static int counter = 3;
int shared_total;
extern int helper(int);
int add(int a, int b) { return a + b + counter; }
int main(int argc, char **argv) {
    char buf[32];
    strncpy(buf, argc > 1 ? argv[1] : "world", sizeof buf - 1);
    buf[31] = 0;
    printf("hello %s %d\n", buf, add(argc, 2));
    return 0;
}
