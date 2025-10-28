
from src.main import has_changed_jobs, A3_Field

from dataclasses import dataclass

from datetime import date, datetime




translator = {
    A3_Field.JOB_DESCRIPTION: {
        "Investigador": "Researcher",
        "Técnico": "Technician",
        "Group Leader Starting Career": "Group Leader",
        "Director/a Administrativo/a": "Administrative/Director",
        "Coordinador/a científico/a de laboratorio": "Scientific Coordinator",



    }
}


@dataclass
class Researcher:
    name: str
    job_description: str
    ini_date: date | None = None
    end_date: date | None = None
    ini_prorrog: date | None = None
    end_prorrog: date | None = None
    date_termination: date | None = None


def d(s: str):  # petit helper per fer dates ràpid
    return datetime.strptime(s, "%d/%m/%Y").date()


# test para comprobar si el researcher ha cambiado de posicion is True if has_changed_job
def test_change_position():
    """Detecta si ha canviat la posició (job_description)."""
    a3 = Researcher("Immaculada Escofet", "Administrative/Director", ini_date=d("03/03/2025"))
    im = Researcher("Immaculada Escofet", "Scientific Coordinator", ini_date=d("14/11/2011"))
    assert has_changed_jobs(a3, im, translator) is True




