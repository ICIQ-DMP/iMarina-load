import pandas as pd
from datetime import date
import os
from enum import Enum


class Researcher:

    def __init__(self, dni, email, name, surname, second_surname, orcid, end_date):
        self.dni = dni
        self.email = email
        self.name = name
        self.surname = surname
        self.second_surname = second_surname
        self.orcid = orcid
        self.end_date = end_date

    def __str__(self):
        return (
            f"\nResearcher:\n"
            f"  DNI: {self.dni}\n"
            f"  Email: {self.email}\n"
            f"  Name: {self.name}\n"
            f"  Surname: {self.surname}\n"
            f"  Second Surname: {self.second_surname}\n"
            f"  ORCID: {self.orcid}\n"
            f"  End Date: {self.end_date}"
        )


class A3_Field(Enum):
    DNI = 5
    EMAIL = 9
    NAME = 2
    SURNAME = 3
    SECOND_SURNAME = 4
    ORCID = 13
    END_DATE = 15


class IMarina_Field(Enum):
    DNI = 6
    EMAIL = 12
    NAME = 1
    SURNAME = 2
    SECOND_SURNAME = 3
    ORCID = 35
    END_DATE = 19


def parse_imarina_row_data(row):
    data = Researcher(dni=row.values[IMarina_Field.DNI.value], email=row.values[IMarina_Field.EMAIL.value],
                      orcid=row.values[IMarina_Field.ORCID.value], name=row.values[IMarina_Field.NAME.value],
                      surname=row.values[IMarina_Field.SURNAME.value],
                      second_surname=row.values[IMarina_Field.SECOND_SURNAME.value],
                      end_date=row.values[IMarina_Field.END_DATE.value])
    return data


def parse_a3_row_data(row):
    data = Researcher(dni=row.values[A3_Field.DNI.value], email=row.values[A3_Field.EMAIL.value],
               orcid=row.values[A3_Field.ORCID.value],
               name=row.values[A3_Field.NAME.value],
               surname=row.values[A3_Field.SURNAME.value],
               second_surname=row.values[A3_Field.SECOND_SURNAME.value],
               end_date=row.values[A3_Field.END_DATE.value])
    return data


def unparse_researcher_to_a3_row_data(data: Researcher, empty_output_row):
    empty_output_row[A3_Field.DNI.value] = data.dni
    empty_output_row[A3_Field.EMAIL.value] = data.email
    empty_output_row[A3_Field.ORCID.value] = data.orcid
    empty_output_row[A3_Field.NAME.value] = data.name
    empty_output_row[A3_Field.SURNAME.value] = data.surname
    empty_output_row[A3_Field.SECOND_SURNAME.value] = data.second_surname

    return empty_output_row


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
    print("no match")
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
        raise ValueError("Data " + str(search_data) + " is not present in A3 data.")
    else:
        return matches


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

    # Phase 1: Check if the researchers in iMarina are still in A3
    not_present = 0
    for index, row in im_data.iterrows():
        print("Processing data from: " + row.values[1] + " " + row.values[2])

        researcher_data = parse_imarina_row_data(row)
        try:
            a3_data_matching_rows = search_a3_data(researcher_data, a3_data)
            msg = ""
            for row_i in a3_data_matching_rows:
                msg += str(row_i)

            print("found these matching rows: " + msg)
            #input()
            # Check if its position has changed. If it has, add current imarina row to output with end date to the
            # corresponding field. Add a new line with same data with the new position and dates to determine to output.
            # If it has not changed, add current imarina row to output as is.
        except ValueError as e:  # TODO change custom except
            print("row data " + str(researcher_data) + " is not present on a3 data. Internal error is: " + str(e))
            not_present += 1
            # Complete this bloc, add row data to output_data

            # Crear un diccionario con las claves del DataFrame de salida
            empty_row = {col for col in output_data.columns}

            print("empty row: " + str(empty_row))
            print("parsed data: " + str(researcher_data))
            unparse_researcher_to_a3_row_data(researcher_data, empty_row)
            print("unparsed row: " + str(empty_row))

            updated_row_df = pd.DataFrame([empty_row])
            output_data = pd.concat([output_data, updated_row_df], ignore_index=True)

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
