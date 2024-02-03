#include <stdint.h>
#include "nvme.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>


#define MYFS_BLOCK_SIZE (2*1024*1024)
#define BUF_SIZE (4096)

int
main()
{
  uint64_t lba;
  char buf[BUF_SIZE];
  int used_blocks = USED_BLOCKS;
  
  nvme_init();

  int fd = open("my.dat", O_RDWR|O_CREAT, 0);
  
  for (lba=0; lba<used_blocks*MYFS_BLOCK_SIZE/512; lba+=8) {
    int rid = nvme_read_req(lba, BUF_SIZE/512, 0, BUF_SIZE, buf);
    while (1)
      if (nvme_check(rid))
	break;
    write(fd, buf, BUF_SIZE);
  }
  close(fd);
}
