"""Tests for lisc.objects.base."""

from py.test import raises

from lisc.data.term import Term
from lisc.objects.base import Base

from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

def test_base():

    assert Base()

def test_get_item(tbase_terms):

    out = tbase_terms['label0']
    assert isinstance(out, Term)
    assert out.label == 'label0'

def test_iter(tbase_terms):

    for term in tbase_terms:
        assert isinstance(term, Term)

def test_get_index(tbase_terms):

    ind = tbase_terms.get_index('label0')
    assert ind == 0

def test_get_term(tbase_terms):

    # Test accessing with index
    out1 = tbase_terms.get_term(0)
    assert isinstance(out1, Term)
    assert out1.label == 'label0'

    # Test accessing with label
    out2 = tbase_terms.get_term('label0')
    assert isinstance(out2, Term)
    assert out2.label == 'label0'

    # Check that the same element accessed in different ways is the same
    assert out1 == out2

def test_add_terms_list(tbase):

    terms = [['word'], ['thing', 'same']]
    tbase.add_terms(terms)
    assert tbase.terms == terms

    inclusions = [['need'], ['required']]
    tbase.add_terms(inclusions, 'inclusions')
    assert tbase.inclusions == inclusions

    exclusions = [['not'], ['this']]
    tbase.add_terms(exclusions, 'exclusions')
    assert tbase.exclusions == exclusions

    assert tbase.has_terms

def test_add_terms_str(tbase):

    terms = ['word', ['thing', 'same']]
    incls = ['need', 'required']
    excls = ['not', 'this']

    terms_expected = [['word'], ['thing', 'same']]
    incls_expected = [['need'], ['required']]
    excls_expected = [['not'], ['this']]

    tbase.add_terms(terms, 'terms')
    tbase.add_terms(incls, 'inclusions')
    tbase.add_terms(excls, 'exclusions')

    assert tbase.terms == terms_expected
    assert tbase.inclusions == incls_expected
    assert tbase.exclusions == excls_expected

    assert tbase.has_terms

def test_add_terms_append(tbase):

    terms1 = [['word'], ['thing', 'same']]
    terms2 = [['added']]

    tbase.add_terms(terms1)
    tbase.add_terms(terms2, append=True)

    assert tbase.n_terms == len(terms1) + len(terms2)
    assert tbase.terms[0] == terms1[0]
    assert tbase.terms[-1] == terms2[-1]

    assert tbase.has_terms

def test_add_terms_term(tbase, tterm):

    tbase.add_terms(tterm)
    assert tbase.labels[0] == tterm.label
    assert tbase.terms[0] == tterm.search
    assert tbase.inclusions[0] == tterm.inclusions
    assert tbase.exclusions[0] == tterm.exclusions

    terms = [tterm, tterm]
    tbase.add_terms(terms)
    assert tbase.n_terms == len(terms)
    assert tbase.labels[1] == tterm.label
    assert tbase.terms[1] == tterm.search
    assert tbase.inclusions[1] == tterm.inclusions
    assert tbase.exclusions[1] == tterm.exclusions

def test_add_terms_file(tdb, tbase):

    tbase.add_terms('test_terms', directory=tdb)
    assert tbase.terms

    tbase.add_terms('test_inclusions', 'inclusions', directory=tdb)
    assert tbase.inclusions

    tbase.add_terms('test_exclusions', 'exclusions', directory=tdb)
    assert tbase.exclusions

    assert tbase.has_terms

def test_add_labels(tbase):

    # Test explicitly added labels, alone
    labels = ['first', 'second']
    tbase.add_labels(labels, check_consistency=False)
    assert tbase.labels == tbase._labels == labels

    # Clear object for next test
    tbase.unload_terms('all', False)

    # Test explicitly added labels, when terms are present
    terms = ['word', 'thing']
    tbase.add_terms(terms)
    tbase.add_labels(labels)
    assert tbase.labels == tbase._labels == labels

    # Clear object for next test
    tbase.unload_terms('all', False)

    # Test not adding labels, when terms are present
    tbase.add_terms(terms)
    assert tbase._labels == [None, None]
    assert tbase.labels == terms

def tests_check_terms(tbase_terms):

    tbase_terms.check_terms()
    tbase_terms.check_terms('inclusions')
    tbase_terms.check_terms('exclusions')

def test_drop_term(tbase_terms):

    n_terms = tbase_terms.n_terms
    tbase_terms.drop_term('label1')
    assert 'label1' not in tbase_terms.labels
    for attr in ['terms', '_labels', 'inclusions', 'exclusions']:
        assert len(getattr(tbase_terms, attr)) == n_terms - 1

def test_unload_terms(tbase_terms):

    tbase_terms.unload_terms('inclusions')
    assert not tbase_terms.inclusions

    tbase_terms.unload_terms('exclusions')
    assert not tbase_terms.exclusions

    tbase_terms.unload_terms('terms')

    assert not tbase_terms.terms
    assert not tbase_terms.n_terms

def test_unload_terms_all(tbase_terms):

    tbase_terms.unload_terms('all')
    assert not tbase_terms.inclusions
    assert not tbase_terms.exclusions
    assert not tbase_terms.terms
    assert not tbase_terms.n_terms

def test_unload_labels(tbase_terms):

    tbase_terms.unload_labels()
    assert tbase_terms._labels == [None, None]

def test_set_none_labels(tbase):

    tbase.terms = [['first'], ['second']]
    assert tbase._labels == []
    tbase._set_none_labels()
    assert tbase._labels == [None, None]

def test_check_term_consistency(tbase_terms):

    tbase_terms._check_term_consistency()

    tbase_terms.exclusions = ['need', 'required']
    tbase_terms._check_term_consistency()

    tbase_terms.exclusions = ['not', 'avoid']
    tbase_terms._check_term_consistency()

    tbase_terms._labels = ['label0', 'label1']
    tbase_terms._check_term_consistency()

    with raises(InconsistentDataError):
        tbase_terms.inclusions = ['need']
        tbase_terms._check_term_consistency()

    with raises(InconsistentDataError):
        tbase_terms.exclusions = ['not', 'avoid', 'bad']
        tbase_terms._check_term_consistency()

    with raises(InconsistentDataError):
        tbase_terms._labels = ['label1', 'label2', 'label3']
        tbase_terms._check_term_consistency()

def test_check_labels(tbase, tbase_terms):

    terms = [['search0'], ['search1']]
    tbase.terms = terms
    tbase._check_labels()
    tbase._labels == [None, None]

    tbase_terms._labels = ['label1', 'label2']
    tbase_terms._check_labels()
