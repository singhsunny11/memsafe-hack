#include <stdlib.h>
#include <string.h>

char *bad_alloc(size_t n) {
char *p = (char *)malloc(n);
if (!p) return NULL;
strcpy(p, "hello world"); // copies without checking n → overflow risk
return p;
}