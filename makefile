ENVS=LD_LIBRARY_PATH=/home/tomoya-s/work/github/argobots/install/lib ABT_THREAD_STACKSIZE=65536  LD_PRELOAD=/home/tomoya-s/work/pthabt/newlib/mylib.so

#EXE=$(ENVS) ./db_bench
EXE=./db_bench

DBFILE=/home/tomoya-s/mountpoint/tomoya-s/dbfile
#DBFILE=/tmp/myfile4

N_TH=8
NUM=26214400
KEY_SIZE=20
VALUE_SIZE=100

DB_OPTS=--db=$(DBFILE) --num=$(NUM)
IO_OPTS=--use_direct_io_for_flush_and_compaction -use_direct_reads --mmap_read=0 --mmap_write=0 --disable_wal=1 --sync=0 --verify_checksum=0
IO_OPTS=--use_direct_io_for_flush_and_compaction --mmap_write=0 --disable_wal=1 --sync=0 --verify_checksum=0
STATS_OPTS=--stats_per_interval=0 --stats_interval=1048576 --histogram=0 --statistics=0
FORMAT_OPTS=--use_plain_table=1
COMPRESS_OPTS=--compression_type=none --compression_ratio=1 --min_level_to_compress=-1
APP_OPTS=--key_size=$(KEY_SIZE) --value_size=$(VALUE_SIZE) --prefix_size=$(KEY_SIZE) --keys_per_prefix=0
#CACHE_OPTS=--cache_size=1048576 --cache_numshardbits=6
CACHE_OPTS=--cache_size=0 --cache_numshardbits=6
BLOOM_OPTS=--bloom_bits=10 --bloom_locality=1
LSM_OPTS=--level0_file_num_compaction_trigger=8 --level0_slowdown_writes_trigger=16 --level0_stop_writes_trigger=24 --memtablerep=prefix_hash --allow_concurrent_memtable_write=false --write_buffer_size=134217728 --max_write_buffer_number=2 --target_file_size_base=134217728 --max_bytes_for_level_base=1073741824

COMMON_OPTS=$(FORMAT_OPTS) $(STATS_OPTS) $(IO_OPTS) $(COMPRESS_OPTS) $(APP_OPTS) $(DB_OPTS) $(CACHE_OPTS) $(BLOOM_OPTS) $(LSM_OPTS)

SET_OPTS=--benchmarks=filluniquerandom --use_existing_db=0 --threads=1 --enable_pipelined_write=true
RUN_OPTS=--benchmarks=readwhilewriting --use_existing_db=1 --duration=60 --threads=$(N_TH)


set:
	$(EXE) $(COMMON_OPTS) $(SET_OPTS)

run:
	$(EXE) $(COMMON_OPTS) $(RUN_OPTS)
