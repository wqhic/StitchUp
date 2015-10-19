import sys, getopt
import os
import time

def main(argv):
    linaddrsfile = ''
    bitfile = ''
    try:
            opts, args = getopt.getopt(argv, "hl:b", ["la=", "bit="])
    except getopt.GetoptError:
            print 'Usage: python injectErros.py --la <linear addresses>.la --bit <bitstream>'
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python injectErros.py --la <linear addresses>.la --bit <bitstream>'
            sys.exit()
        if opt in ("-l", "--la"):
            linaddrsfile = arg
        if opt in ("-b", "--bit"):
            bitfile = arg
    assert(linaddrsfile != '')
    assert(bitfile != '')
    inputfile = open(linaddrsfile, 'r')
    addrLines = inputfile.readlines()
    inputfile.close()

    reconfig_cmd = 'cat ' + bitfile + ' > /dev/xdevcfg'
    exec_cmd = '../sw_driver/bin/hlsKicker >> res.csv'
    init_cmd = '../sw_driver/bin/injectSetup'
    rep_cmd = '../sw_driver/bin/repairErrors'
    fin_cmd = '../sw_driver/bin/injectFinish'
    check_cmd = '../sw_driver/bin/checkINITLED'
    reset_pl_cmd ='../sw_driver/bin/reset_pl'

    os.system(reset_pl_cmd)
    os.system(reconfig_cmd)
    os.system(init_cmd)

    for addr in addrLines:
        inject_cmd = 'timeout 5 ../sw_driver/bin/injectOnly ' + str(addr)
        os.system(inject_cmd)
    	exec_cmd = 'timeout 5 ../sw_driver/bin/hlsKicker {}'.format(addr)
        os.system(exec_cmd)
	os.system(inject_cmd)
	time.sleep(0.0105)
	if os.system(check_cmd) == 0:
	    os.system(reset_pl_cmd)
	    os.system(reconfig_cmd)
    	    os.system(init_cmd)

    os.system(fin_cmd)


if __name__ == "__main__":
    main(sys.argv[1:])

