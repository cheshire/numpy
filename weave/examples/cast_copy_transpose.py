""" Cast Copy Tranpose is used in Numeric's LinearAlgebra.py to convert
    C ordered arrays to Fortran order arrays before calling Fortran
    functions.  A couple of C implementations are provided here that 
    show modest speed improvements.  One is an "inplace" transpose that
    does an in memory transpose of an arrays elements.  This is the
    fastest approach and is beneficial if you don't need to keep the
    original array.    
"""
# C:\home\ej\wrk\scipy\compiler\examples>python cast_copy_transpose.py
# Cast/Copy/Transposing (150,150)array 1 times
#  speed in python: 0.870999932289
#  speed in c: 0.25
#  speed up: 3.48
#  inplace transpose c: 0.129999995232
#  speed up: 6.70

import Numeric
from Numeric import *
import sys
sys.path.insert(0,'..')
import inline_tools
import scalar_spec
from blitz_tools import blitz_type_factories

def _cast_copy_transpose(type,a_2d):
    assert(len(shape(a_2d)) == 2)
    new_array = zeros(shape(a_2d),type)
    #trans_a_2d = transpose(a_2d)
    numeric_type = scalar_spec.numeric_to_blitz_type_mapping[type]
    code = """
           for(int i = 0; i < _Na_2d[0]; i++)
               for(int j = 0; j < _Na_2d[1]; j++)
                   new_array(i,j) = (%s) a_2d(j,i);
           """ % numeric_type
    inline_tools.inline(code,['new_array','a_2d'],
                        type_factories = blitz_type_factories,
                        compiler='gcc',
                        verbose = 1)
    return new_array

def _inplace_transpose(a_2d):
    assert(len(shape(a_2d)) == 2)
    numeric_type = scalar_spec.numeric_to_blitz_type_mapping[a_2d.typecode()]
    code = """
           %s temp;
           for(int i = 0; i < _Na_2d[0]; i++)
               for(int j = 0; j < _Na_2d[1]; j++)
               {
                   temp = a_2d(i,j);
                   a_2d(i,j) = a_2d(j,i);
                   a_2d(j,i) = temp;
               }    
           """ % numeric_type
    inline_tools.inline(code,['a_2d'],
                        type_factories = blitz_type_factories,
                        compiler='gcc',def _cast_copy_transpose(type,a_2d):
    assert(len(shape(a_2d)) == 2)
    new_array = zeros(shape(a_2d),type)
    #trans_a_2d = transpose(a_2d)
    numeric_type = scalar_spec.numeric_to_blitz_type_mapping[type]
    code = """
           for(int i = 0; i < _Na_2d[0]; i++)
               for(int j = 0; j < _Na_2d[1]; j++)
                   new_array(i,j) = (%s) a_2d(j,i);
           """ % numeric_type
    inline_tools.inline(code,['new_array','a_2d'],
                        type_factories = blitz_type_factories,
                        compiler='gcc',
                        verbose = 1)
    return new_array

                        verbose = 1)
    return a_2d

def cast_copy_transpose(type,*arrays):
    results = []
    for a in arrays:
        results.append(_cast_copy_transpose(type,a))
    if len(results) == 1:
        return results[0]
    else:
        return results

def inplace_cast_copy_transpose(*arrays):
    results = []
    for a in arrays:
        results.append(_inplace_transpose(a))
    if len(results) == 1:
        return results[0]
    else:
        return results

def _castCopyAndTranspose(type, *arrays):
    cast_arrays = ()
    for a in arrays:
        if a.typecode() == type:
            cast_arrays = cast_arrays + (copy.copy(Numeric.transpose(a)),)
        else:
            cast_arrays = cast_arrays + (copy.copy(
                                       Numeric.transpose(a).astype(type)),)
    if len(cast_arrays) == 1:
            return cast_arrays[0]
    else:
        return cast_arrays

import time


def compare(m,n):
    a = ones((n,n),Float64)
    type = Float32
    print 'Cast/Copy/Transposing (%d,%d)array %d times' % (n,n,m)
    t1 = time.time()
    for i in range(m):
        for i in range(n):
            b = _castCopyAndTranspose(type,a)
    t2 = time.time()
    py = (t2-t1)
    print ' speed in python:', (t2 - t1)/m
    

    # load into cache    
    b = cast_copy_transpose(type,a)
    t1 = time.time()
    for i in range(m):
        for i in range(n):
            b = cast_copy_transpose(type,a)
    t2 = time.time()
    print ' speed in c:',(t2 - t1)/ m    
    print ' speed up: %3.2f' % (py/(t2-t1))

    # inplace tranpose
    b = _inplace_transpose(a)
    t1 = time.time()
    for i in range(m):
        for i in range(n):
            b = _inplace_transpose(a)
    t2 = time.time()
    print ' inplace transpose c:',(t2 - t1)/ m    
    print ' speed up: %3.2f' % (py/(t2-t1))
    
if __name__ == "__main__":
    m,n = 1,150
    compare(m,n)    
