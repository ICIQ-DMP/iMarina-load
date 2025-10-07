
from datetime import date, datetime

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
        end_date=date(2025, 10, 5),
        code_center=4)
    assert is_visitor(researcher) == True


def test_isnot_visitor():
    researcher = Researcher(
        ini_date=date(2023, 9, 30),
        end_date=date(2025, 10, 5),
        code_center=4)
    assert is_visitor(researcher) == False


def test_is_not_visitor_no_start_date():
    researcher = Researcher(
        code_center=4,
        ini_date=None,
        end_date=date(2025, 1, 1)

    )
    assert is_visitor(researcher) is False

def test_is_not_visitor_no_end_date():
    researcher = Researcher(
        code_center=4,
        ini_date=datetime(2025, 1, 1),
        end_date=None

    )
    assert is_visitor(researcher) is True
