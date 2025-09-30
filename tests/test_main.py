from datetime import date

from main import Researcher, is_visitor


def test_build_upload_excel():
    assert False


def test_upload_excel():
    return True


def test_build_translations():
    assert False


# test de prueba suma
def test_demo():
    assert 1 + 1 == 2


def test_researcher():
    assert False


def test_is_visitor():
    researcher = Researcher(
            ini_date=date(2025, 9, 30),
            end_date=date(2025, 9, 31),
            employee_code=4)
    assert is_visitor(researcher) == True



