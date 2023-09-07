
#BENCH_EXE=../db_bench
BENCH_EXE=ABT_THREAD_STACKSIZE=65536 LD_PRELOAD=/home/tomoya-s/pthabt/newlib/mylib.so ../db_bench
#DB_FILE=/tmp/rocksdb
DB_FILE=/home/tomoya-s/mountpoint/tomoya-s/rocksdb
#NUM=52428800
NUM=524288
CACHE_SIZE=1048576
#TIME=7200
TIME=10
STAT=--statistics=0 --stats_per_interval=0 --stats_interval=1048576
THREAD=8
#STAT=--statistics=1 --stats_per_interval=0 --stats_interval=$(STAT_INTERVAL)

run:
	$(BENCH_EXE) --db=$(DB_FILE) --num_levels=6 --key_size=20 --prefix_size=20 --keys_per_prefix=0 --value_size=100 --cache_size=$(CACHE_SIZE) --cache_numshardbits=6 --compression_type=none --compression_ratio=1 --min_level_to_compress=-1 --disable_seek_compaction=1 --write_buffer_size=134217728 --max_write_buffer_number=2 --level0_file_num_compaction_trigger=8 --target_file_size_base=134217728 --max_bytes_for_level_base=1073741824 --disable_wal=1 --sync=0 --verify_checksum=1 --delete_obsolete_files_period_micros=314572800 --max_background_compactions=4 --max_background_flushes=0 --level0_slowdown_writes_trigger=16 --level0_stop_writes_trigger=24 $(STAT) --histogram=0 --use_plain_table=1 --open_files=-1 --mmap_read=0 --mmap_write=0 --memtablerep=prefix_hash --bloom_bits=10 --bloom_locality=1 --duration=$(TIME) --benchmarks=readwhilewriting --use_existing_db=1 --num=$(NUM) --threads=$(THREAD) --benchmark_write_rate_limit=81920 --allow_concurrent_memtable_write=false --use_direct_reads=1

set:
	$(BENCH_EXE) --db=$(DB_FILE) --num_levels=6 --key_size=20 --prefix_size=20 --keys_per_prefix=0 --value_size=100 --cache_size=$(CACHE_SIZE) --cache_numshardbits=6 --compression_type=none --compression_ratio=1 --min_level_to_compress=-1 --disable_seek_compaction=1 --write_buffer_size=134217728 --max_write_buffer_number=2 --level0_file_num_compaction_trigger=8 --target_file_size_base=134217728 --max_bytes_for_level_base=1073741824 --disable_wal=0 --disable_wal --sync=0 --verify_checksum=1 --delete_obsolete_files_period_micros=314572800 --max_background_compactions=4 --max_background_flushes=0 --level0_slowdown_writes_trigger=16 --level0_stop_writes_trigger=24 --statistics=0 --stats_per_interval=0 --stats_interval=1048576 --histogram=0 --use_plain_table=1 --open_files=-1 --mmap_read=1 --mmap_write=0 --memtablerep=prefix_hash --bloom_bits=10 --bloom_locality=1 --benchmarks=filluniquerandom --use_existing_db=0 --num=$(NUM) --threads=8 --allow_concurrent_memtable_write=false
