# generate.py
generate.py will generate masks for multiple ranks to bind the ranks to cores for srun

## Examples:

`generate.py 3:2:0:0` generates masks for 3 ranks, 2 threads per rank, with starting core 0 and without any stride. <br />

`generate.py 3:2:0:0 2:8`             generates masks for 3 ranks, 2 threads per rank, with starting core 0 and without any stride, for each 8 cores, 2 times <br />

`generate.py 3:2:0:0 2:8 4:24`        generates same above(generate.py 3:2:0:0 2:8) masks for each 24 cores, 4 times <br />

`generate.py 3:2:0:0 2:8 4:24 2:96`   generates same above(generate.py 3:2:0:0 2:8 4:24) masks for each 96 cores, 2 times <br />

`generate.py 3:2:0:0 2:8 4:24 2:96`   It can be used to mimic AMD 9454 using AMD 9654, 2 socket node <br />
                                      six cores per CCD on the first two CCDs of each NUMA node on 2 sockets of 9654 <br />

# verify.py
verify.py will converts hexadecimal mask values to integer core values

## Examples:

verify.py --cpu-bind=verbose,mask_cpu:0x00000003,0x0000000c,0x00000030 <br />
		output: --cpu-bind=verbose,mask_cpu: [0-1], [2-3], [4-5] <br />
  
verify.py --cpu-bind=mask_cpu:0x00000003,0x0000000c,0x00000030,0x00000300,0x00000c00,0x00003000 <br />
		output: --cpu-bind=mask_cpu: [0-1], [2-3], [4-5], [8-9], [10-11], [12-13] <br />
