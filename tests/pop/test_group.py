import pytest

from wolves_in_silico.pop.group import Group, Village


class TestGroup:
    @pytest.mark.parametrize('has_major', [True, False])
    def test_init(self, has_major: bool):
        n = 3
        group = Group(size=n, has_major=has_major)
        assert group.size == n
        assert group.has_major == has_major
        assert group.vote_size == n + .5 * has_major

    def test_remove(self):
        n = 3
        group = Group(size=n)
        group.remove()
        assert group.size == n - 1


class TestVillage:
    def test_init(self):
        village = Village(nciv=2, nwolf=2)
        assert village.nwolves == 2
        assert village.nciv == 2

    @pytest.mark.parametrize('rem_wolf', [True, False])
    def test_remove(self, rem_wolf):
        village = Village(nciv=2, nwolf=2)
        village.remove(wolf=rem_wolf)
        assert village.size == 3
        if rem_wolf:
            assert village.nwolves == 1
            assert village.nciv == 2
        else:
            assert village.nwolves == 2
            assert village.nciv == 1
