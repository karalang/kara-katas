#include <stdio.h>

int main(int argc, char **argv) {
    for (int i = 1; i < argc; i++)
        printf("hello, %s\n", argv[i]);
    return argc > 1 ? 0 : 1;
}
