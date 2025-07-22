import datetime

import pandas as pd
from datetime import date
import os
from enum import Enum


class Researcher:

    def __init__(self, dni, email, name, surname, second_surname, orcid, ini_date, end_date, sex, personal_web):
        self.dni = dni
        self.email = email
        self.name = name
        self.surname = surname
        self.second_surname = second_surname
        self.orcid = orcid
        self.ini_date = ini_date
        self.end_date = end_date
        self.sex = sex
        self.personal_web = personal_web

    def __str__(self):
        return (
            f"\nResearcher:\n"
            f"  DNI: {self.dni}\n"
            f"  Email: {self.email}\n"
            f"  Name: {self.name}\n"
            f"  Surname: {self.surname}\n"
            f"  Second Surname: {self.second_surname}\n"
            f"  ORCID: {self.orcid}\n"
            f"  End Date: {self.end_date}\n"
            f"  Ini Date: {self.ini_date}\n"
            f"  Sex: {self.sex}\n"
            f"  Personal web: {self.personal_web}\n"
        )

    def copy(self):
        return Researcher(self.dni,
                          self.email,
                          self.name,
                          self.surname,
                          self.second_surname,
                          self.orcid,
                          self.ini_date,
                          self.end_date,
                          self.sex,
                          self.personal_web)


class A3_Field(Enum):
    DNI = 5
    EMAIL = 9
    NAME = 2
    SURNAME = 3
    SECOND_SURNAME = 4
    ORCID = 13
    INI_DATE = 14
    END_DATE = 15
    SEX = 7
    PERSONAL_WEB = -1


class IMarina_Field(Enum):
    DNI = 6
    EMAIL = 12
    NAME = 1
    SURNAME = 2
    SECOND_SURNAME = 3
    ORCID = 35
    INI_DATE = 18
    END_DATE = 19
    SEX = 8
    PERSONAL_WEB = 13


def sanitize_date(date_dirty):
    if isinstance(date_dirty, datetime.datetime):
        return date_dirty
    elif type(date_dirty) is pd._libs.tslibs.nattype.NaTType:
        return None
    elif isinstance(date_dirty, str):
        return datetime.datetime.strptime(date_dirty.strip("'"), "%d/%m/%Y")
    elif isinstance(date_dirty, float):
        return None
    else:
        raise ValueError("Unknown type for date to sanitize")


def parse_imarina_row_data(row):
    data = Researcher(dni=row.values[IMarina_Field.DNI.value], email=row.values[IMarina_Field.EMAIL.value],
                      orcid=row.values[IMarina_Field.ORCID.value], name=row.values[IMarina_Field.NAME.value],
                      surname=row.values[IMarina_Field.SURNAME.value],
                      second_surname=row.values[IMarina_Field.SECOND_SURNAME.value],
                      ini_date=sanitize_date(row.values[IMarina_Field.INI_DATE.value]),
                      end_date=sanitize_date(row.values[IMarina_Field.END_DATE.value]),
                      sex=row.values[IMarina_Field.SEX.value],
                      personal_web=row.values[IMarina_Field.PERSONAL_WEB.value])
    return data


def parse_a3_row_data(row):
    data = Researcher(dni=row.values[A3_Field.DNI.value], email=row.values[A3_Field.EMAIL.value],
                      orcid=row.values[A3_Field.ORCID.value],
                      name=row.values[A3_Field.NAME.value],
                      surname=row.values[A3_Field.SURNAME.value],
                      second_surname=row.values[A3_Field.SECOND_SURNAME.value],
                      ini_date=sanitize_date(row.values[A3_Field.INI_DATE.value]),
                      end_date=sanitize_date(row.values[A3_Field.END_DATE.value]),
                      sex=row.values[A3_Field.SEX.value],
                      personal_web="https://iciq.es")
    return data


def unparse_researcher_to_imarina_row(data: Researcher, empty_output_row):
    empty_output_row.iat[0, IMarina_Field.DNI.value] = data.dni
    empty_output_row.iat[0, IMarina_Field.EMAIL.value] = data.email
    empty_output_row.iat[0, IMarina_Field.ORCID.value] = data.orcid
    empty_output_row.iat[0, IMarina_Field.NAME.value] = data.name
    empty_output_row.iat[0, IMarina_Field.SURNAME.value] = data.surname
    empty_output_row.iat[0, IMarina_Field.SECOND_SURNAME.value] = data.second_surname
    empty_output_row.iat[0, IMarina_Field.INI_DATE.value] = data.ini_date.strftime("%d/%m/%Y")
    empty_output_row.iat[0, IMarina_Field.END_DATE.value] = data.end_date.strftime("%d/%m/%Y")
    empty_output_row.iat[0, IMarina_Field.SEX.value] = data.sex
    empty_output_row.iat[0, IMarina_Field.PERSONAL_WEB.value] = data.personal_web


def merge_a3_into_imarina(a3: Researcher, imarina: Researcher):
    ret = imarina.copy()
    ret.dni = a3.dni
    ret.email = a3.email
    ret.orcid = a3.orcid
    ret.name = a3.name
    ret.surname = a3.surname
    ret.second_surname = a3.second_surname
    ret.ini_date = a3.ini_date
    ret.end_date = a3.end_date
    ret.sex = a3.sex


def build_translations():
    r = {}
    r[IMarina_Field.SEX] = {}
    r[IMarina_Field.SEX]["Mujer"] = "Woman"
    r[IMarina_Field.SEX]["Hombre"] = "Man"


def is_same_person(imarina_row, a3_row):
    if isinstance(imarina_row.orcid, str) and isinstance(a3_row.orcid, str):
        if imarina_row.orcid.replace("-", "") == a3_row.orcid:
            print("ORCID match")
            return True
    if imarina_row.dni == a3_row.dni:
        print("DNI match")
        return True
    if imarina_row.email == a3_row.email:
        print("email match: iMarina email: " + str(imarina_row.email) + " a3 match: " + str(a3_row.email))
        return True
    return False


def is_in_a3(search_data, a3):
    for index, row in a3.iterrows():
        row_data = parse_a3_row_data(row)
        if is_same_person(search_data, row_data):
            return True
    return False


def search_a3_data(search_data, a3):
    matches = []
    for index, row in a3.iterrows():
        row_data = parse_a3_row_data(row)
        if is_same_person(search_data, row_data):
            matches.append(row_data)

    if len(matches) == 0:
        raise ValueError("Data from " + str(search_data.email) + " is not present in A3 data.")
    else:
        return matches


def build_empty_row(imarina_dataframe):
    empty_output_dataframe = imarina_dataframe[0:0].copy()  # retains columns, types, and headers if any
    empty_output_dataframe.loc[0] = [None] * len(imarina_dataframe.columns)
    return empty_output_dataframe


def main():
    today = date.today()

    # Repo root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Output dir
    output_path = os.path.join(root_dir, 'output', "iMarina_upload_" + date.today().__str__() + ".xlsx")
    input_dir = os.path.join(root_dir, 'input')

    # Get A3 data
    a3_path = os.path.join(input_dir, "A3.xlsx")
    a3_data = pd.read_excel(a3_path, header=2)
    a3_data = a3_data.iloc[3:]

    # Get iMarina last upload data
    im_path = os.path.join(input_dir, "iMarina.xlsx")
    im_data = pd.read_excel(im_path, header=0)

    output_data = im_data[0:0]  # retains columns, types, and headers if any
    empty_row_output_data = build_empty_row(imarina_dataframe=im_data)

    # Phase 1: Check if the researchers in iMarina are still in A3
    not_present = 0
    for index, row in im_data.iterrows():
        print("Processing data from: " + row.values[1] + " " + row.values[2])

        researcher_imarina = parse_imarina_row_data(row)
        try:
            researchers_matched_a3 = search_a3_data(researcher_imarina, a3_data)
            msg = ""
            for row_i in researchers_matched_a3:
                msg += str(row_i)

            #print("found these matching rows: " + msg)
            #input()

            # Check if its position has changed. If it has, add current imarina row to output with end date to the
            # corresponding field. Add a new line with same data with the new position and dates to determine to output.
            # If it has not changed, add current imarina row to output as is.
        except ValueError as e:  # TODO change custom except
            print(
                "row data from " + str(researcher_imarina.name) + " is not present on a3 data. Adding to iMarina with "
                                                                  "end of "
                                                                  "contract date. " + str(e))
            not_present += 1

            # Use end time already in iMarina if present, if not set to today
            researcher_imarina.end_date = today

            empty_row = empty_row_output_data.copy()
            unparse_researcher_to_imarina_row(researcher_imarina, empty_row)
            #print("unparsed row: " + str(empty_row))

            #print("empty row cols " + str(empty_row.columns))
            #print("output row cols " + str(output_data.columns))
            output_data = pd.concat([output_data, empty_row], ignore_index=True)

            #print("output data " + str(output_data))
            #input()

            # not in a3, but present in last iMarina load
            # Add current iMarina row to output with the end date with the corresponding value and field to notify end
            # of contract
            # Convertir en DataFrame de una sola fila y añadir al output

    # Phase 2: Add researchers in A3 that are not present in iMarina
    # For each researcher in A3, check if they are not present in iMarina
    # If they are not present, it has a code 4 and its begin and end date is outside a range
    # to determine from fields to determine, then the current row from A3 corresponds to ICREA researcher or predoc
    # with CSC, so its data from A3 needs to be added to the output.
    output_data.to_excel(output_path, index=False)


if __name__ == "__main__":
    main()
