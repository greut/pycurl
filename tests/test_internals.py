# $Id$
# vi:ts=4:et

import pycurl, sys
try:
    from gc import get_objects
    import gc
    del get_objects
    gc.enable()
except ImportError:
    gc = None

print "Testing", pycurl.version
print pycurl.__file__, pycurl.__COMPILE_DATE__


#####
##### self-test assertion section
#####


# remove an invalid handle: this should fail
if 1:
    m = pycurl.multi_init()
    c = pycurl.init()
    try:
        m.remove_handle(c)
    except pycurl.error:
        pass
    else:
        assert 0, "internal error"
    del m, c


# remove an invalid but closed handle
if 1:
    m = pycurl.multi_init()
    c = pycurl.init()
    c.cleanup()
    m.remove_handle(c)
    del m, c


# add a closed handle: this should fail
if 1:
    m = pycurl.multi_init()
    c = pycurl.init()
    c.cleanup()
    try:
        m.add_handle(c)
    except pycurl.error:
        pass
    else:
        assert 0, "internal error"
    m.cleanup()
    del m, c


# add a handle twice: this should fail
if 1:
    m = pycurl.multi_init()
    c = pycurl.init()
    m.add_handle(c)
    try:
        m.add_handle(c)
    except pycurl.error:
        pass
    else:
        assert 0, "internal error"
    del m, c


# add a handle on multiple stacks: this should fail
if 1:
    m1 = pycurl.multi_init()
    m2 = pycurl.multi_init()
    c = pycurl.init()
    m1.add_handle(c)
    try:
        m2.add_handle(c)
    except pycurl.error:
        pass
    else:
        assert 0, "internal error"
    del m1, m2, c


# move a handle
if 1:
    m1 = pycurl.multi_init()
    m2 = pycurl.multi_init()
    c = pycurl.init()
    m1.add_handle(c)
    m1.remove_handle(c)
    m2.add_handle(c)
    del m1, m2, c


# basic check of reference counting (use a memory checker like valgrind)
if 1:
    c = pycurl.init()
    m = pycurl.multi_init()
    m.add_handle(c)
    del m
    m = pycurl.multi_init()
    c.cleanup()
    del m, c


# basic check of cyclic garbage collection
if 1 and gc:
    c = pycurl.init()
    c.m = pycurl.multi_init()
    c.m.add_handle(c)
    # create some nasty cyclic references
    c.c = c
    c.c.c1 = c
    c.c.c2 = c
    c.c.c3 = c.c
    c.c.c4 = c.m
    c.m.c = c
    # delete
    gc.collect()
    flags = gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_OBJECTS
    flags = flags | gc.DEBUG_STATS
    gc.set_debug(flags)
    gc.collect()
    ##print gc.get_referrers(c)
    ##print gc.get_objects()
    print "Tracked objects:", len(gc.get_objects())
    # if gc.isenabled() this should delete 4 objects:
    #   CurlObject + internal dict, CurlMuliObject + internal dict
    del c
    gc.collect()
    print "Tracked objects:", len(gc.get_objects())


print "All tests passed."