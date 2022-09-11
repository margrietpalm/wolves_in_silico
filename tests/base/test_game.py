from wolves_in_silico.base.game import Result

def test_result():
    nciv = [3,2,2]
    nwolves = [1,1,0]
    result = Result(nciv=nciv, nwolves=nwolves, civ_win=True)
    assert result.nciv == nciv
    assert result.nwolves == nwolves
    assert len(result.time) == len(nciv)
    assert result.civ_win == True
    assert result.wolf_win == False