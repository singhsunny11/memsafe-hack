#include <string.h>

void vuln(char *input) {
char buf[16];
strcpy(buf, input); // potential buffer overflow
}