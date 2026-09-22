#include <stdio.h>
#include <stdint.h>
#include <string.h>

// copia diretta da AppleEffaceableStorage.h
int AppleEffaceableStorage__getLocker(uint32_t lockerId, uint8_t *buffer, size_t len);

uint32_t tags[] = {
    0x42414731, // BAG1
    0x454D4621, // EMF!
    0x44594B45, // DYKE? 
    0x4C574D56, // LWMV
    0x46524C45, // FRLE
    0x53434E54, // SCNT
    0x4C57524E, // LWRN
    0x50415353, // PASS
    0x4C4F434B, // LOCK
    0x434E5452, // CNTR
    0x424C464B, // BLFK
    0x46554E54, // FUNT
    0x44464B59, // DFKY
    0x52455452, // RETR - retry?
    0x46414C53, // FALS
    0x43545252, // CTRR
    0x00000000
};

int main() {
    uint8_t buf[256] = {0};
    int i = 0;
    while(tags[i]) {
        memset(buf, 0, sizeof(buf));
        int ret = AppleEffaceableStorage__getLocker(tags[i], buf, sizeof(buf));
        char tag_str[5] = {
            (tags[i] >> 24) & 0xff,
            (tags[i] >> 16) & 0xff,
            (tags[i] >> 8) & 0xff,
            tags[i] & 0xff, 0
        };
        if(ret == 0) {
            printf("FOUND %s (0x%08x): ", tag_str, tags[i]);
            for(int j=0; j<32; j++) printf("%02x", buf[j]);
            printf("\n");
        } else {
            printf("MISS  %s (0x%08x): ret=0x%x\n", tag_str, tags[i], ret);
        }
        i++;
    }
    return 0;
}
