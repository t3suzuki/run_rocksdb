import subprocess, os

#ABT_PATH = "/home/tomoya-s/work/github/argobots/install"
#MYLIB_PATH = "/home/tomoya-s/work/pthabt/newlib"

#ABT_PATH = "/home/tomoya-s/mountpoint2/tomoya-s/argobots/install"
#MYLIB_PATH = "/home/tomoya-s/mountpoint2/tomoya-s/pthabt/newlib"

ABT_PATH = "/home/tomoya-s/work/github/ppopp21-preemption-artifact/argobots/install"
MYLIB_PATH = "/home/tomoya-s/mountpoint2/tomoya-s/pthabt/newlib"

def get_db_bench_cmd(mode, op, threads, cache_size, db_path):
    key_size = 32
    val_size = 512
    num = 400 * 1000 * 1000
    #num = 20 * 1000 * 1000
    
    if op == "set":
        benchmarks = "filluniquerandom"
        existing_db = 0
        duration = ""
    else:
        benchmarks = "readrandom"
        existing_db = 1
        duration = "--duration=240 "

    if mode == "spdk":
        block_align = 0
    else:
        block_align = 1
        
    cmd = "./db_bench --use_plain_table=0 --stats_per_interval=0 --stats_interval=1048576 --histogram=0  --use_direct_io_for_flush_and_compaction -use_direct_reads --mmap_read=0 --mmap_write=0 --disable_wal=1 --sync=0 --verify_checksum=1 --compression_type=none --compression_ratio=1 --min_level_to_compress=-1 --key_size={} --value_size={} --prefix_size={} --keys_per_prefix=0 --db={} --cache_size={} --cache_numshardbits=12 --cache_index_and_filter_blocks=0 --pin_l0_filter_and_index_blocks_in_cache=0 --cache_high_pri_pool_ratio=0.5 --bloom_bits=10  --level0_file_num_compaction_trigger=8 --level0_slowdown_writes_trigger=16 --level0_stop_writes_trigger=24 --allow_concurrent_memtable_write=false --write_buffer_size=1073741824 --max_write_buffer_number=4 --target_file_size_base=10485760000 --max_bytes_for_level_base=104857600000 --block_size=4096 --block_align={} -use_data_block_hash_index=1 -use_hash_search=1 --file_opening_threads=1 --benchmarks={} --use_existing_db={} --num={} --threads={} ".format(key_size, val_size, key_size, db_path, cache_size, block_align, benchmarks, existing_db, num, threads) + duration
    return cmd


def run(mode, op, n_core, n_th, cache_size):
    print("mode={}, op={}, n_core={}, n_th={}, cache_size={}".format(mode, op, n_core, n_th, cache_size))
    if mode == "abt" or mode == "pthpth":
        db_path = "/home/tomoya-s/mountpoint2/tomoya-s/rocksdb_abt400m"
    elif mode == "spdk":
        db_path = "/home/tomoya-s/mountpoint2/tomoya-s/rocksdb_spdk4m"
    else:
        db_path = "/home/tomoya-s/mountpoint2/tomoya-s/rocksdb_native400m"
        
    if op == "set":
        print("We are modifying database {}. Are you Sure? (Y/N)".format(db_path))
        x = input()
        assert x == "y"

    subprocess.run("chcpu -e 1-{}".format(n_core-1))
    subprocess.run("chcpu -d {}-39".format(n_core))
    
    my_env = os.environ.copy()
    drive_ids = ["0000:05:00.0","0000:06:00.0"]
    if mode == "abt":
        mylib_build_cmd = "make -C {} ABT_PATH={} N_CORE={} ND={} USE_PREEMPT=0".format(MYLIB_PATH, ABT_PATH, n_core, len(drive_ids))
        process = subprocess.run(mylib_build_cmd.split())
        
        my_env["LD_PRELOAD"] = MYLIB_PATH + "/mylib.so"
        my_env["LD_LIBRARY_PATH"] = ABT_PATH + "/lib"
        my_env["ABT_PREEMPTION_INTERVAL_USEC"] = "10000000"
        #my_env["ABT_THREAD_STACKSIZE"] = "65536"
        #my_env["ABT_THREAD_STACKSIZE"] = "1048576"
        my_env["HOOKED_ROCKSDB_DIR"] = db_path
        my_env["DRIVE_IDS"] = "_".join(drive_ids)
        my_env["ABT_INITIAL_NUM_SUB_XSTREAMS"] = str(n_th + 16)
        my_env["MYFS_SUPERBLOCK_PATH"] = "/root/myfs_superblock"
        #my_env["LIBDEBUG"] = MYLIB_PATH + "/debug.so"
        cmd = get_db_bench_cmd(mode, op, n_th, cache_size, db_path)
    elif mode == "spdk":
        cmd = get_db_bench_cmd(mode, op, n_th, cache_size, db_path)
        cmd += " --spdk=../rocksdb.json --spdk_bdev=Nvme0n1 --spdk_cache_size=4096"
        #cmd = "taskset -c 0-{} ".format(n_core-1) + cmd
        #cmd = "taskset -c 0-{} ".format(n_core) + cmd
    elif mode == "pthpth":
        mylib_build_cmd = "make pth -C {} ABT_PATH={} N_CORE={} ND={} USE_PREEMPT=1".format(MYLIB_PATH, ABT_PATH, n_core, len(drive_ids))
        process = subprocess.run(mylib_build_cmd.split())
        
        my_env["LD_PRELOAD"] = MYLIB_PATH + "/pthpth.so"
        my_env["HOOKED_ROCKSDB_DIR"] = db_path
        my_env["DRIVE_IDS"] = "_".join(drive_ids)
        my_env["ABT_INITIAL_NUM_SUB_XSTREAMS"] = str(n_th)
        my_env["MYFS_SUPERBLOCK_PATH"] = "/root/myfs_superblock"
        #my_env["LIBDEBUG"] = MYLIB_PATH + "/debug.so"
        cmd = "taskset -c 0-{} ".format(n_core-1) + get_db_bench_cmd(mode, op, n_th, cache_size, db_path)
    else:
        cmd = "taskset -c 0-{} ".format(n_core-1) + get_db_bench_cmd(mode, op, n_th, cache_size, db_path)
    print(cmd)
    
    res = subprocess.run(cmd.split(), env=my_env, capture_output=True)
    print("captured stdout: {}".format(res.stdout.decode()))
    print("captured stderr: {}".format(res.stderr.decode()))

#run("native", "set", 1, 1, 1024*1024)
run("abt", "set", 1, 1, 1024*1024)
#run("abt", "set", 1, 1, 8*1024*1024)
#run("abt", "get", 8, 128, 1024*1024)
#run("abt", "get", 8, 256, 1024*1024)
#run("abt", "get", 8, 128, 1024*1024)
#run("abt", "get", 8, 128, 20*1024*1024*1024)
#run("pthpth", "get", 8, 128, 1024*1024)
#run("pthpth", "get", 8, 128, 20*1024*1024*1024)
#for i in range(0, 16):
#    run("abt", "get", 8, 256, 1024*1024)

#run("spdk", "set", 1, 1, 1*1024*1024)
#run("spdk", "get", 1, 64, 20*1024*1024*1024)
#run("spdk", "get", 1, 64, 1*1024*1024)
#run("spdk", "get", 1, 64, 4*1024*1024)

#run("native", "get", 8, 64, 1024*1024)

# for n_core in [8]:
#     for n_pth in [256,512,128,1024,64]:
#         run("pthpth", "get", n_core, n_pth, 1024*1024)

#for n_core in [8]:
#    for n_pth in [256,512,128,1024,64]:
#        run("abt", "get", n_core, n_pth, 1024*1024)

# for n_core in [8]:
#     for n_pth in [256,512,128,1024,64]:
#         run("pthpth", "get", n_core, n_pth, 20*1024*1024*1024)

#for n_core in [8]:
#     #for n_pth in [256,512,128,1024,64]:
#    for n_pth in [32]:
#         run("pthpth", "get", n_core, n_pth, 20*1024*1024*1024)

# for i in range(0, 16):
#     for n_core in [8]:
#         for n_pth in [128]:
#             run("abt", "get", n_core, n_pth, 1024*1024)

for i in range(0, 16):
    for n_core in [8]:
        for n_pth in [32,64,128,256]:
            run("pthpth", "get", n_core, n_pth, 1024*1024)
    for n_core in [8]:
        for n_pth in [32,64,128,256]:
            run("abt", "get", n_core, n_pth, 1024*1024)
    for n_core in [8]:
        for n_pth in [32,64,128,256]:
            run("pthpth", "get", n_core, n_pth, 20*1024*1024)
    for n_core in [8]:
        for n_pth in [32,64,128,256]:
            run("abt", "get", n_core, n_pth, 20*1024*1024)

# for n_core in [1,2,4,8]:
#     for n_pth in [16,32,64,128,256,512]:
#         run("abt", "get", n_core, n_pth, 20*1024*1024*1024)

#run("abt", "get", 1, 128, 1024*1024)

# for n_core in [1,2,4,8]:
#     for n_pth in [8,16,32,64,128,256]:
#         run("native", "get", n_core, n_pth, 1024*1024)

# for n_core in [1,2,4,8]:
#     for n_pth in [8,16,32,64,128,256]:
#         run("native", "get", n_core, n_pth, 20*1024*1024*1024)
        
# for n_core in [1,2,4,8]:
#     for n_pth in [64,128,256,512]:
#         run("spdk", "get", n_core, n_pth*n_core, 1024*1024)
