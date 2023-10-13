ENVS=LD_LIBRARY_PATH=/home/tomoya-s/work/github/argobots/install/lib ABT_THREAD_STACKSIZE=65536  LD_PRELOAD=/home/tomoya-s/work/pthabt/newlib/mylib.so

#ENVS=LIBZPHOOK=../../zpoline/apps/basic/libzphook_basic.so LD_PRELOAD=../../zpoline/libzpoline.so

EXE=$(ENVS) ./db_bench # ABT+SPDK version
#EXE=taskset -c 0 ./db_bench
#EXE=taskset -c 0-3 ./db_bench

DBFILE=/tmp/myfile4 # ABT+SPDK version
#DBFILE=/home/tomoya-s/mountpoint2/tomoya-s/dbfile400m

N_TH=1024
#NUM=76214400
NUM=400000000
#NUM=6621440
#NUM=131072000
#NUM=262144000
KEY_SIZE=64
VALUE_SIZE=512
DURATION=120

DB_OPTS=--db=$(DBFILE)
IO_OPTS=--use_direct_io_for_flush_and_compaction -use_direct_reads --mmap_read=0 --mmap_write=0 --disable_wal=1 --sync=0 --verify_checksum=1
STATS_OPTS=--stats_per_interval=0 --stats_interval=1048576 --histogram=0 #--statistics=1
#FORMAT_OPTS=--use_plain_table=1
FORMAT_OPTS=--use_plain_table=0
COMPRESS_OPTS=--compression_type=none --compression_ratio=1 --min_level_to_compress=-1
APP_OPTS=--key_size=$(KEY_SIZE) --value_size=$(VALUE_SIZE) --prefix_size=$(KEY_SIZE) --keys_per_prefix=0
#CACHE_OPTS=--cache_size=134217728 --cache_numshardbits=6 -cache_index_and_filter_blocks --pin_l0_filter_and_index_blocks_in_cache --cache_high_pri_pool_ratio=0.5 --cache_low_pri_pool_ratio=0
CACHE_OPTS=--cache_size=1048576 --cache_numshardbits=12 --cache_index_and_filter_blocks=0 --pin_l0_filter_and_index_blocks_in_cache=0 --cache_high_pri_pool_ratio=0.5 --cache_low_pri_pool_ratio=0
#CACHE_OPTS=--cache_size=0 --cache_numshardbits=6
BLOOM_OPTS=--bloom_bits=10 #--bloom_locality=1
LSM_OPTS=--level0_file_num_compaction_trigger=8 --level0_slowdown_writes_trigger=16 --level0_stop_writes_trigger=24 --allow_concurrent_memtable_write=false --write_buffer_size=1073741824 --max_write_buffer_number=4
#LSM_OPTS+=--target_file_size_base=134217728 # L1 SST file is 128MB.
#LSM_OPTS+=--max_bytes_for_level_base=1073741824 # Multiple L1 SST files are 1GB in total.
#LSM_OPTS+=--target_file_size_base=5342177280 # L1 SST file is 128MB.
#LSM_OPTS+=--max_bytes_for_level_base=50737418240 # Multiple L1 SST files are 1GB in total.
LSM_OPTS+=--target_file_size_base=10485760000
LSM_OPTS+=--max_bytes_for_level_base=104857600000
LSM_OPTS+=--block_size=4096 --block_align=1 -use_data_block_hash_index=1 -use_hash_search=1
#LSM_OPTS+=--block_align=1
#LSM_OPTS+=--memtablerep=prefix_hash 


COMMON_OPTS=$(FORMAT_OPTS) $(STATS_OPTS) $(IO_OPTS) $(COMPRESS_OPTS) $(APP_OPTS) $(DB_OPTS) $(CACHE_OPTS) $(BLOOM_OPTS) $(LSM_OPTS) --file_opening_threads=1

SET_OPTS=--benchmarks=filluniquerandom --use_existing_db=0 --num=$(NUM) --threads=1
#RUN_OPTS=--benchmarks=readwhilewriting --use_existing_db=1 --duration=60 --threads=$(N_TH)
RUN_OPTS=--benchmarks=readrandom --use_existing_db=1 --duration=$(DURATION) --num=$(NUM) --threads=$(N_TH) -print_access_count_stats
#-readwritepercent

run:
	$(EXE) $(COMMON_OPTS) $(RUN_OPTS)

set:
	dd if=/dev/random of=./myfs_superblock count=1 bs=128M
	$(EXE) $(COMMON_OPTS) $(SET_OPTS)

