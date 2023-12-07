import pytest
#
# """
# conftest.py
# """

# Fixtures are functions, which will run before each test function to which it is applied.
#To make a fixture available to multiple test files, we have to define the fixture function in a file called conftest.py.
@pytest.fixture
def input_value():
    input = 39
    return input

def test_divisible_by_3(input_value):
    assert input_value % 3 == 0

def test_divisible_by_6(input_value):
    assert input_value % 6 != 0

def test_divisible_by_63y(input_pygamber_yas):
    assert input_pygamber_yas % 63 == 0

def test_divisible_by_63n(input_pygamber_yas):
    assert input_pygamber_yas % 63 != 0

@pytest.fixture
def supply_AA_BB_CC():
    aa=25
    bb =35
    cc=45
    return [aa,bb,cc]

def test_comparewithAA(supply_AA_BB_CC):
    zz=25
    assert supply_AA_BB_CC[0]==zz,"aa and zz comparison failed"

def test_comparewithBB(supply_AA_BB_CC):
    zz=35
    assert supply_AA_BB_CC[1]==zz,"bb and zz comparison failed"

def test_comparewithCC(supply_AA_BB_CC):
    zz=45
    assert supply_AA_BB_CC[2]==zz,"cc and zz comparison failed"
