
# assert condition
# exemple
# assert 0==0 --> BON
# assert 0==1 --> PAS BON -> ERREUR
from pytest import approx 

GLOBAL = 1.256

def test_bidon():
    assert 1 == 1
    assert 0 == 0

def test_bidon2():
    assert 0 == 0  

def test_bidon3():
    condition = "a" == "a"
    assert condition     

def test_bidon4():
    assert GLOBAL > 1 

def test_bidon5():
    assert approx(1.0000001) == 1
