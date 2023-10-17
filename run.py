import subprocess, os

ABT_PATH = "/home/tomoya-s/work/github/argobots/install"
MYLIB_PATH = "/home/tomoya-s/work/pthabt/newlib"

def get_db_bench_cmd(op, is_abt, threads, cache_size):
    key_size = 32
    val_size = 512
    num = 400 * 1000 * 1000
    
    if op == "set":
        benchmarks = "filluniquerandom"
        existing_db = 0
        duration = ""
    else:
        benchmarks = "readrandom"
        existing_db = 1
        duration = "--duration 120"
        
    cmd = "./db_bench --use_plain_table=0 --stats_per_interval=0 --stats_interval=1048576 --histogram=0  --use_direct_io_for_flush_and_compaction -use_direct_reads --mmap_read=0 --mmap_write=0 --disable_wal=1 --sync=0 --verify_checksum=1 --compression_type=none --compression_ratio=1 --min_level_to_compress=-1 --key_size={} --value_size={} --prefix_size={} --keys_per_prefix=0 --db={} --cache_size={} --cache_numshardbits=12 --cache_index_and_filter_blocks=0 --pin_l0_filter_and_index_blocks_in_cache=0 --cache_high_pri_pool_ratio=0.5 --cache_low_pri_pool_ratio=0 --bloom_bits=10  --level0_file_num_compaction_trigger=8 --level0_slowdown_writes_trigger=16 --level0_stop_writes_trigger=24 --allow_concurrent_memtable_write=false --write_buffer_size=1073741824 --max_write_buffer_number=4 --target_file_size_base=10485760000 --max_bytes_for_level_base=104857600000 --block_size=4096 --block_align=1 -use_data_block_hash_index=1 -use_hash_search=1 --file_opening_threads=1 --benchmarks={} --use_existing_db={} --num={} --threads={} ".format(key_size, val_size, key_size, db_path, cache_size, benchmarks, existing_db, num, threads) + duration
    return cmd


def run(mode, op, n_core, n_th, cache_size):
    if mode == "abt":
        db_path = "/home/tomoya-s/mountpoint/tomoya-s/rocksdb_abt400m"
    else:
        db_path = "/home/tomoya-s/mountpoint/tomoya-s/rocksdb_native400m"
        
    if op == "set":
        print("We are modifying database {}. Are you Sure? (Y/N)".format(db_path))
        x = input()
        assert x == "y"
    mylib_build_cmd = "make -C {} ABT_PATH={} N_TH={}".format(MYLIB_PATH, ABT_PATH, n_core)
    process = subprocess.run(mylib_build_cmd.split())

    my_env = os.environ.copy()
    if mode == "abt":
        my_env["LD_PRELOAD"] = MYLIB_PATH + "/mylib.so"
        my_env["LD_LIBRARY_PATH"] = ABT_PATH + "/lib"
        my_env["ABT_THREAD_STACKSIZE"] = "65536"
        cmd = get_db_bench_cmd(op, n_th, cache_size)
    else:
        cmd = get_db_bench_cmd(op, n_th, cache_size)
    print(cmd)
    
    process = subprocess.run(cmd.split(), env=my_env)

#run("native", "set", 1, 1, 1024*1024)
#run("abt", "set", 1, 1, 1024*1024)
for n_core in [1,2,4,8]:
    for n_pth in [16,32,64,128,256,512]:
        #run("native", "get", n_core, n_pth, 1024*1024)
        run("native", "get", n_core, n_pth, 1024*1024)
    
