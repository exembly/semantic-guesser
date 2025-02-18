"""
Implementation of the MDL (Minimum Description Length) model,
as described in Hang Li and Naoki Abe (1998).

@author: Rafa
"""

import math


def pc(f, s):
    """^P(C) - probability of a category to occur in the sample.
    Equation 12 in Li & Abe (1998).

    f -> f(C), the total frequency of words in class C in the sample S
    s -> |S|, # of words in the sample

    """
    return float(f) / s


def pn(pc, c):
    """^P(n) - probability of a category to occur in the sample, normalized
       by its number of children.
       Equation 11 in Li & Abe (1998).

       pc - ^P(C), probability of a category to occur in the sample.
       c  - |C|,  # of children of a class (1 for leaves)

    """
    return float(pc) / c


def ddl(pn_list):
    """L(S|T,teta) - data description length.
    Equation 10 in Li & Abe (1998).

    pn_list - list of tuples of the form (f, pn), where f is the frequency of the class
    and pn is its ^P(n) value.

    """
    result = 0
    for f, pn in pn_list:
        if pn > 0.0:
            result += math.log(pn, 2) * f

    return -result


def pdl(len_cut, s_length):
    """ L(teta|T) - parameter description length.
    Equation 9 in Li & Abe (1998).

    len_cut  - number of nodes in the cut
    s_length - sample size (# of words)

    """
    k = len_cut - 1
    # We can use k or k+1. See Appendix A of Li and Abe (1998)


    return k * math.log(s_length, 2) / 2


def compute_ddl(cut, sample_size, estimator = None):
    """ Computes the data description length of a cut.
    This function just 'extracts' from the cut the exact info needed to calculate ddl,
    and calls ddl. It's just a bridge...

    cut - a list of tuples of the form (class_name, frequency, # of children (leaves) )
    """
    if estimator is not None:
        prob = estimator.probability
    else:
        prob = lambda node: pc(node.value, sample_size)

    return ddl([(node.value, pn(prob(node), node.leaf_count)) for node in cut])


def compute_pdl(cut, sample_size):
    """ Computes the data description length of a cut.
    This function just 'extracts' from the cut the exact info needed to calculate pdl,
    and calls pdl. It's just a bridge...

    cut - a list of tuples of the form ( class_name, frequency, # of children (leaves) )
    """
    return pdl(len(cut), sample_size)


def compute_dl(cut, sample_size, estimator=None):
    """ Computes the description length of a cut. """
    return compute_ddl(cut, sample_size, estimator) + compute_pdl(cut, sample_size)


def test_cut(cut, sample_size):
    ddl = compute_ddl(cut, sample_size)
    pdl = compute_pdl(cut, sample_size)

    print("""Cut: {}
    Data description length: {}
    Parameter description length: {}
    Description length: {}
    """.format(cut, ddl, pdl, ddl + pdl))
