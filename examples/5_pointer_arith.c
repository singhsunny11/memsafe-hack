#include <stdio.h>

void iterate(char *buf, size_t n) {
for (int i = 0; i <= n; i++) { // off-by-one → may read out of bounds
putchar(buf[i]);
}
}