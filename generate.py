#! /usr/bin/env python3
import sys

def generate_masks_for_node(num_ranks, threads_per_rank, starting_core, skip_c):
    current_core = starting_core
    col_mask = ""
    for rank in range(num_ranks):
        mask = 0  # Reset mask for each rank
        for core_num in range(current_core, current_core + threads_per_rank):
            mask |= (1 << core_num)
        hex_mask = format(mask, '08x')
        if not main_mask and not col_mask:
            col_mask = f"0x{hex_mask}"
        else:
            col_mask += f",0x{hex_mask}"
        current_core += threads_per_rank + skip_c
    return col_mask

def get_masks(list_repeat_count, list_cores_per_count , s_core):
    global main_mask
    if len(list_repeat_count) == 0 and len(list_cores_per_count) == 0:
        main_mask += generate_masks_for_node(num_ranks, threads_per_rank, s_core, skip_c)
        return None
    else:
        for i in range(list_repeat_count[-1]):
            c=(list_cores_per_count[-1]*i)
            get_masks(list_repeat_count[:-1], list_cores_per_count[:-1], s_core+c )
    return None
def usage():
    print(f"Usage: python generate.py <num_ranks>:<threads_per_rank>:<start>:<stride> [<repeat_count>:<cores_per_count>] ...")
    print("      mandatory arguments: num_ranks                  number of ranks")
    print("                           threads_per_rank           threads per rank")
    print("                           start                      starting core for generating masks")
    print("                           stride                     skips cores in between ranks(stride)")
    print("      optional arguments: <cmd> <repeat_count>:<cores_per_count>       If specified it will generate masks with <cmd> options <repeat_count> times for each <cores_per_count> cores")
    print("                                                                       Can be passed multiple time")
    print("Examples:")
    print("      generate.py 3:2:0:0                 generates masks for 3 ranks, 2 threads per rank, with starting core 0 and without any stride")
    print("      generate.py 3:2:0:0 2:8             generates masks for 3 ranks, 2 threads per rank, with starting core 0 and without any stride, for each 8 cores, 2 times")
    print("      generate.py 3:2:0:0 2:8 4:24        generates same above(generate.py 3:2:0:0 2:8) masks for each 24 cores, 4 times")
    print("      generate.py 3:2:0:0 2:8 4:24 2:96   generates same above(generate.py 3:2:0:0 2:8 4:24) masks for each 96 cores, 2 times")
    print("      generate.py 3:2:0:0 2:8 4:24 2:96   It can be used to mimic AMD 9454 using AMD 9654, 2 socket node")
    print("                                          six cores per CCD on the first two CCDs of each NUMA node on 2 sockets of 9654")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Insufficient arguments. Please provide at least 1 arguments.")
        print("Usage: python generate.py <num_ranks>:<threads_per_rank>:<start>:<stride> [<repeat_count>:<cores_per_count>] ...")
        sys.exit(1)
    
    if sys.argv[1]=="--help" or sys.argv[1]=="-h" or sys.argv[1]=="-H":
            usage()
            sys.exit(1)
    
    args = sys.argv[1].split(':')
    if len(args) != 4:
        print("Error: Invalid mandatory arguments. Please provide 4 integers separated by ':' (colon).")
        print("Usage: python generate.py <num_ranks>:<threads_per_rank>:<start>:<stride> [<repeat_count>:<cores_per_count>] ...")
        sys.exit(1)
    
    num_ranks, threads_per_rank, starting_core, skip_c = map(int, args)
    
    if not all(isinstance(arg, int) for arg in (num_ranks, threads_per_rank, starting_core, skip_c)):
        print("Error: Invalid mandatory arguments. Please provide integers.")
        print("Usage: python generate.py <num_ranks>:<threads_per_rank>:<start>:<stride> [<repeat_count>:<cores_per_count>] ...")
        sys.exit(1)
    
    list_repeat_count=[]
    list_cores_per_count=[]
    if len(sys.argv) > 2:
        for opt in sys.argv[2:]:
            repeat_count, cores_per_count = map(int, opt.split(':'))
            if not all(isinstance(arg, int) for arg in (repeat_count, cores_per_count)):
                print("Usage: python generate.py <num_ranks>:<threads_per_rank>:<start>:<stride> [<repeat_count>:<cores_per_count>] ...")
                sys.exit(1)
            list_cores_per_count.append(cores_per_count)
            list_repeat_count.append(repeat_count)
    
    for val in range(len(list_repeat_count)):
        if val==0:
            cores_per_block=(num_ranks*threads_per_rank)+starting_core+((num_ranks-1)*skip_c)
            e_string=f"Error: Wrong input: {list_cores_per_count[val]} should be greater than ({num_ranks}*{threads_per_rank})+{starting_core}+(({num_ranks}-1)*{skip_c})"
        else:
            cores_per_block=list_cores_per_count[val-1]*list_repeat_count[val-1]
            e_string=f"Error: Wrong input: {list_cores_per_count[val]} should be greater than {list_repeat_count[val-1]}*{list_cores_per_count[val-1]}"
        if list_cores_per_count[val] < cores_per_block:
            print(e_string)
            sys.exit(1)
    
    main_mask = ""
    get_masks(list_repeat_count, list_cores_per_count , starting_core)
    print(f"--cpu-bind=verbose,mask_cpu:{main_mask}")
