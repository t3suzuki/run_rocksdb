N_CORE ?= 1
ND ?= 2

ABT_PATH ?= $(HOME)/work/github/ppopp21-preemption-artifact/argobots/install

FLAGS = -O3 -g -march=native
FLAGS += -fpic
FLAGS += -DN_CORE=$(N_CORE) -DND=$(ND)
FLAGS += -DUSED_BLOCKS=4
FLAGS += -I./pthabt/newlib
all:
	g++ $(FLAGS) -c pthabt/newlib/nvme.cc  -fno-exceptions -I $(ABT_PATH)/include
	gcc $(FLAGS) nvme.o abt_backup.c -lstdc++ -o abt_backup
	gcc $(FLAGS) nvme.o abt_restore.c -lstdc++ -o abt_restore

run:
	DRIVE_IDS=0000:0f:00.0_0000:0e:00.0 ./abt_backup
	DRIVE_IDS=0000:0f:00.0_0000:0e:00.0 ./abt_restore

clean:
	rm -f *~
	rm -f abt_backup abt_restore nvme.o my.dat
