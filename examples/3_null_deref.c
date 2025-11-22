#include <stdio.h>

void maybe_null(int *p) {
if (p[0] == 0) { // no null check on the pointer itself
printf("zero");
}
}