#! /usr/bin/env python3
import sys
def mask_to_core_range(mask_str):
    try:
        mask_int = int(mask_str, 16)
    except ValueError:
        raise ValueError("Invalid CPU mask format. Please provide a valid hex string.")
    result=[]
    start=None
    bin_str=str(bin(mask_int)).split("b")[1]
    bin_str=bin_str[::-1]
    for i, char in enumerate(bin_str):
        if char == '1' and start is None:
            start = i
        elif char == '0' and start is not None:
            if start == i-1:
                result.append(f"{start}")
            else:
                result.append(f"{start}-{i-1}")
            start = None
        elif char == '1' and start is not None:
            pass  # Consecutive 1s
    if start is not None:
        if start == (len(bin_str)-1):
            result.append(f"{start}")
        else:
            result.append(f"{start}-{len(bin_str)-1}")
    return "["+','.join(result)+"]"

def process_masks(mask_values):
    output_string = ""
    for mask_str in mask_values:
        try:
            core_range = mask_to_core_range(mask_str)
            output_string += f" {core_range}"
            output_string +=","
        except ValueError as e:
            print(f"Error processing mask '{mask_str}': {e}")
            return None
    return output_string[:-1]

def usage():
    print("Usage: python verify.py [<prefix>]:<mask_values>")
    print("     mandatory argument: mask_values    hexadecimal mask values separeted with \",\"")
    print("     optional argument:  prefix         any string before mask value. if provided, \":\" should be the separeter between <prefix> and <mask_values>")
    print("Examples: ")
    print("     verify.py --cpu-bind=verbose,mask_cpu:0x00000003,0x0000000c,0x00000030")
    print("             output: --cpu-bind=verbose,mask_cpu: [0-1], [2-3], [4-5]")
    print("     verify.py --cpu-bind=mask_cpu:0x00000003,0x0000000c,0x00000030,0x00000300,0x00000c00,0x00003000")
    print("             output: --cpu-bind=mask_cpu: [0-1], [2-3], [4-5], [8-9], [10-11], [12-13]")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Insufficient arguments. Please provide at least 1 arguments.")
        print("Usage: python verify.py [<prefix>]:<mask_values>")
        sys.exit(1)
    
    if sys.argv[1]=="--help" or sys.argv[1]=="-h" or sys.argv[1]=="-H":
            usage()
            sys.exit(1)

    mask_values = sys.argv[1].split(":")[-1].split(",")
    prefix_string = sys.argv[1].split(":")[0]
    final_string = process_masks(mask_values)
    if final_string:
        print(prefix_string+ ":" +final_string)
