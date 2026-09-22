#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "AppleEffaceableStorage.h"
#include "IOKit.h"

int main() {
    uint8_t buf[4096] = {0};
    int ret = AppleEffaceableStorage__getBytes(buf, sizeof(buf));
    if (ret) {
        fprintf(stderr, "getBytes failed: %d\n", ret);
        return 1;
    }
    fwrite(buf, 1, sizeof(buf), stdout);
    return 0;
}
