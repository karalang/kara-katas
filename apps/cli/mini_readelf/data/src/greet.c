#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static char last[64];
int greet_count = 0;
__thread int greet_depth;
const char *greet_old(const char *who) { snprintf(last, sizeof last, "hi %s", who); greet_count++; return last; }
const char *greet_new(const char *who) { snprintf(last, sizeof last, "hello, %s!", who); greet_count++; return last; }
char *greet_dup(const char *who) { greet_depth++; char *p = malloc(strlen(who) + 8); strcpy(p, "dear "); strcat(p, who); return p; }
static int helper(int x) { return x * 3; }
int greet_score(int x) { return helper(x) + greet_count; }
__asm__(".symver greet_old,greet@GREET_1.0");
__asm__(".symver greet_new,greet@@GREET_2.0");
