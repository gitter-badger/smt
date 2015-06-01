#!/bin/csh
#
#PBS -q gpu -l nodes=1:ppn=8:k40c,mem=10g,cput=9999:00:00 -j oe
#
# GPUs: k20m, k20x, k40c

if ($#argv != 1) then
    echo "Usage: $0 <mach_conf>"
    exit 1
endif

set mach=`basename -s".conf" $1`
set folder=`pwd`

echo "Using mach: $mach"
echo "In  folder: $folder"

cd $folder
# Now we should have everything under this folder

# choose tools
switch (`hostname -s`)
  case nv7:
    set cstm_train='~caglayan/git/cslm/cstm_train -N 4'
    breaksw
  case nv10:
  case nv11:
  case nv12:
  case nv13:
    set cstm_train='~caglayan/git/cslm/cstm_train -N 8'
    breaksw
  case nv14:
    set cstm_train='~caglayan/git/cslm/cstm_train -N 5'
    breaksw
  default:
    echo "ERROR; unsupported machine `hostname -s`"; exit(1)
endsw


echo "starting $mach"
$cstm_train --conf $mach.conf >& $mach.log

