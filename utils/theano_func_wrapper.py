""" Helper function to abstract the creation of Theano functions for
    symbolic variables.
"""
import theano
import numpy as np
import hashlib

# It is expensive to create the Theano functions, so once we've done it
# we cache the results for future calls
_func_cache = {}

def seval(expr, syms, vals, defaults=None, givens=[]):
    """
    Evaluate the symbolic expression which depends on a set of symbolic variables,
    given a set of variable bindings.
    expr : Theano variable to be evaluated
    syms : dictionary of symbolic variables
    vals : dictionary of values to assign to the symbolic vars in syms
           key structure should mimic that of syms
    
    defaults : an optional dictionary providing backup values for 
               syms keys not found in vals.
    """
    # Look for a function handle corresponding to this expression with these givens
    hash_value = lambda v: hashlib.sha1(v).hexdigest() if \
                           isinstance(v, np.ndarray) else v
    hashable_givens = tuple(map(lambda (k,v): (k, hash_value(v)), givens))
    hashable_syms = tuple(map(lambda v: hash_value(v), _flatten(syms)))
    key = (expr, hashable_syms, hashable_givens)
    if key in _func_cache.keys():
        #print "DBG: Found key %s in cache" % str(key)
        f = _func_cache[key]
        #print "DBG: Calling expr: %s" % str(expr)
    else:
        # Create a callable theano function and cache it
        print "DBG: Compiling expr: %s" % str(expr)
        sargs = _flatten(syms)
        if len(givens) == 0:
            # print "DBG: Compiling expression %s with no givens" % expr
            f = theano.function(sargs, expr,
                                on_unused_input='ignore')
        else:
            # print "DBG: Compiling expression %s with givens: %s" % (expr, str(givens))
            f = theano.function(sargs, expr,
                                givens=givens,
                                on_unused_input='ignore')
        _func_cache[key] = f
    
    # Easiest thing to do is call the function with all symbolic variables
    args = _extract_vals(syms,vals,defaults)
    return f(*args) 

def _flatten(d):
    """ Pack a hierarchical dictionary of variables into a list
        Sorting is important as it ensures the function is called with 
        the inputs in the same order each time!
    """
    l = []
    # This sorting is important!
    for (k,v) in sorted(d.items(), key=lambda t: t[0]):
        if isinstance(v, dict):
            lv = _flatten(v)
            for v2 in lv:
                l.append(v2)
        else:
            l.append(v)
    return l

def _extract_vals(syms, vals, defaults=None):
    """
    Extract corresponding values for each symbolic variable in syms
    """
    l = []
    # This sorting is important!
    for (sk,sv) in sorted(syms.items(), key=lambda t: t[0]):
        # It should be a bit faster to try and except rather than checking
        vv = None
        try:
            vv = vals[sk]
        except Exception as e:
            # sk is not in vals
            pass
        
        # Also look in defaults
        vd = None
        try:
            vd = defaults[sk]
        except Exception as e:
            # sk is not in defaults
            pass

        if vv is None and vd is None:
            raise Exception("Key %s not found in either vals or defaults!" % sk)

        if isinstance(sv, dict):
            # If sv is a dictionary, recurse
            lv = _extract_vals(sv,vv,vd)
            for lvv in lv:
                l.append(lvv)
        else:
            # Otherwise, append the value to the list
            v = vv if (vv is not None) else vd
            l.append(v)
        
    return l
