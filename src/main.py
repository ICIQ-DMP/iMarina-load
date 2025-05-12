import pandas as pd
from datetime import date
import os
from enum import Enum


class Researcher:

    def __init__(self, dni, email, name, surname, second_surname, orcid):
        self.dni = ""
        self.email = ""
        self.name = ""
        self.surname = ""
        self.second_surname = ""
        self.orcid = ""


class A3_Field(Enum):
    DNI = 5
    EMAIL = 9
    NAME = 2
    SURNAME = 3
    SECOND_SURNAME = 4
    ORCID = 13


class IMarina_Field(Enum):
    DNI = 6
    EMAIL = 12
    NAME = 1
    SURNAME = 2
    SECOND_SURNAME = 3
    ORCID = 35


def parse_imarina_row_data(row):
    data = Researcher(dni=row.values[IMarina_Field.DNI.value], email=row.values[IMarina_Field.EMAIL.value],
                      orcid=row.values[IMarina_Field.ORCID.value], name=row.values[IMarina_Field.NAME.value],
                      surname=row.values[IMarina_Field.SURNAME.value],
                      second_surname=row.values[IMarina_Field.SECOND_SURNAME.value])
    return data


def parse_a3_row_data(row):
    data = Researcher(dni=row.values[A3_Field.DNI.value], email=row.values[A3_Field.EMAIL.value],
               orcid=row.values[A3_Field.ORCID.value],
               name=row.values[A3_Field.NAME.value],
               surname=row.values[A3_Field.SURNAME.value],
               second_surname=row.values[A3_Field.SECOND_SURNAME.value])
    return data


def unparse_a3_row_data(data, row):
    row.values[A3_Field.DNI.value] = data["dni"]
    a3_data = {"dni": row.values[A3_Field.DNI.value], "email": row.values[A3_Field.EMAIL.value],
               "ORCID": row.values[A3_Field.ORCID.value],
               "name": row.values[A3_Field.NAME.value],
               "surname": row.values[A3_Field.SURNAME.value],
               "second_surname": row.values[A3_Field.SECOND_SURNAME.value]}

    return a3_data


def is_same_person(imarina_row, a3_row):
    if isinstance(imarina_row.orcid, str) and isinstance(a3_row.orcid, str):
        if imarina_row.orcid.replace("-", "").__eq__(a3_row.orcid):
            print("ORCID match")
            return True
    if imarina_row.dni.__eq__(a3_row.dni):
        return True
    if imarina_row.email.__eq__(a3_row.email):
        return True
    return False


def is_in_a3(search_data, a3):
    for index, row in a3.iterrows():
        row_data = parse_a3_row_data(row)
        if is_same_person(search_data, row_data):
            return True
    return False


def main():
    # Repo root
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Output dir
    OUTPUT_PATH = os.path.join(ROOT_DIR, 'output', "iMarina_upload_" + date.today().__str__() + ".xlsx")
    INPUT_DIR = os.path.join(ROOT_DIR, 'input')

    # Get A3 data
    A3_PATH = os.path.join(INPUT_DIR, "A3.xlsx")
    A3_DATA = pd.read_excel(A3_PATH, header=2)
    A3_DATA = A3_DATA.iloc[3:]

    # Get iMarina last upload data
    IM_PATH = os.path.join(INPUT_DIR, "iMarina.xlsx")
    IM_DATA = pd.read_excel(IM_PATH, header=0)

    OUTPUT_DATA = IM_DATA[0:0]  # retains columns, types, and headers if any

    # Phase 1: Check if the researchers in iMarina are still in A3
    not_present = 0
    for index, row in IM_DATA.iterrows():
        print("Processing data from: " + row.values[1] + " " + row.values[2])

        row_data = parse_imarina_row_data(row)
        if is_in_a3(row_data, A3_DATA):
            # Check if its position has changed. If it has, add current imarina row to output with end date to the
            # corresponding field. Add a new line with same data with the new position and dates to determine to output.
            # If it has not changed, add current imarina row to output as is.
            pass

        else:  # not in a3
            # Add current imarina row to output with the end date with the corresponding value and field to notify end
            # of contract
            not_present += 1


    # Phase 2: Add researchers in A3 that are not present in iMarina
    # For each researcher in A3, check if they are not present in iMarina
    # If they are not present, it has a code 4 and its begin and end date is outside a range
    # to determine from fields to determine, then the current row from A3 corresponds to ICREA researcher or predoc
    # with CSC, so its data from A3 needs to be added to the output.
    OUTPUT_DATA.to_excel(OUTPUT_PATH, index=False)





if __name__ == "__main__":
    main()
