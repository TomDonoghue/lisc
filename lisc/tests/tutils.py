"""Helper functions for testing lisc."""

import pkg_resources as pkg
from functools import wraps
from os.path import join as pjoin

from lisc.objects.base import Base
from lisc.data import Articles, ArticlesAll, Term
from lisc.core.modutils import safe_import
from lisc.utils.db import SCDB, check_directory

plt = safe_import('.pyplot', 'matplotlib')

###################################################################################################
###################################################################################################

class TestDB(SCDB):
    """Overloads the SCDB object as database object for tests."""

    def __init__(self):

        # Initialize from normal database object
        base = pkg.resource_filename(__name__, 'test_db')
        SCDB.__init__(self, base=base)

def create_term_files(directory):
    """Creates some test term files."""

    path = check_directory(directory, 'terms')

    with open(pjoin(path, 'test_terms.txt'), 'w') as term_file:
        term_file.write('word\nthing, same')

    with open(pjoin(path, 'test_inclusions.txt'), 'w') as incl_file:
        incl_file.write('need\nrequired')

    with open(pjoin(path, 'test_exclusions.txt'), 'w') as excl_file:
        excl_file.write('not\navoid')

    with open(pjoin(path, 'test_exclusions_line.txt'), 'w') as excl_file2:
        excl_file2.write('not\n')

def create_api_files(directory):
    """Create test API key file."""

    path = check_directory(directory, 'base')

    with open(pjoin(path, 'api_key.txt'), 'w') as term_file:
        term_file.write('123abc')

def load_base(set_terms=False, set_clusions=False):
    """Helper function to load Base object for testing."""

    base = Base()

    if set_terms:
        base.add_terms([['test1', 'test sin'], ['test2', 'uh oh']])

    if set_clusions:
        base.add_terms([['yeh', 'definitely'], ['need', 'required']], 'inclusions')
        base.add_terms([['exc1', 'blehh'], ['exc2', 'meh']], 'exclusions')

    return base

def load_arts(add_data=False, n_data=1):
    """Helper function to load Articles object for testing."""

    arts = Articles(Term('label', ['search'], ['inclusion'], ['exclusion']))

    if add_data:
        for ind in range(n_data):

            arts.add_data('ids', 1)
            arts.add_data('titles', 'title')
            arts.add_data('journals', ['science', 'sc'])
            arts.add_data('authors', [('A', 'B', 'C', 'D')])
            arts.add_data('words', 'Lots of words data.')
            arts.add_data('keywords', ['lots', 'of', 'keywords'])
            arts.add_data('years', 2112)
            arts.add_data('dois', 'doi_str')

    return arts

def load_arts_all():
    """Helper function to load ArticlesAll object for testing."""

    arts = load_arts(add_data=True, n_data=2)
    arts_all = ArticlesAll(arts)

    return arts_all

def plot_test(func):
    """Decorator for simple testing of plotting functions.

    Notes
    -----
    This decorator closes all plots prior to the test.
    After running the test function, it checks an axis was created with data.
    It therefore performs a minimal test - asserting the plots exists, with no accuracy checking.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        plt.close('all')

        func(*args, **kwargs)

        ax = plt.gca()
        assert ax.has_data()

    return wrapper

def optional_test(dependency):
    """Decorator to only run a test if the specified optional dependency is present.

    Parameters
    ----------
    dependency : str
        The name of an optional dependency to test import of.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if safe_import(dependency):
                return func(*args, **kwargs)

        return wrapper

    return decorator
