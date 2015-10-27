__author__ = 'def'

import sys, os

def rename(filepath, str_to_remove, str_to_add):
    print 'Rename: %s -> %s' % (filepath, filepath[:-len(str_to_remove)] + str_to_add)
    os.rename(filepath, filepath[:-len(str_to_remove)] + str_to_add)

if __name__  == '__main__':
    src_dir = os.path.abspath(sys.argv[1])
    print 'Source dir: ' + src_dir

    equivalence_pcbWay = {'-B_Cu.gbr':'.GBL',
                          '-B_Mask.gbr':'.GBS',
                          '-B_SilkS.gbr':'.GBO',
                          '-F_Cu.gbr':'.GTL',
                          '-F_Mask.gbr':'.GTS',
                          '-F_SilkS.gbr':'.GTO',
                          '-Edge_Cuts.gbr':'.GKO',
                          '.drl':'.DRL'}

    for filename in os.listdir(src_dir):
        for ending in equivalence_pcbWay.keys():
            if filename.endswith(ending):
                rename(os.path.join(src_dir, filename), ending, equivalence_pcbWay[ending])
