#include <stdlib.h>

int *create() {
int *p = malloc(sizeof(int));
*p = 42;
free(p);
return p; // returning a pointer to freed memory (use-after-free)
}