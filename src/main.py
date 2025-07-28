import datetime
import logging

import pandas as pd
from datetime import date
import os
from enum import Enum

from log import setup_logger


class Researcher:

    def __init__(self, dni, email, name, surname, second_surname, orcid, ini_date, end_date, sex, personal_web,
                 signature, signature_custom, country):
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
        self.signature = signature
        self.signature_custom = signature_custom
        self.country = country

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
            f"  Signature: {self.signature}\n"
            f"  Signature custom: {self.signature_custom}\n"
            f"  Country: {self.country}\n"
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
                          self.personal_web,
                          self.signature,
                          self.signature_custom,
                          self.country)


class A3_Field(Enum):
    NAME = 2
    SURNAME = 3
    SECOND_SURNAME = 4
    DNI = 5
    SEX = 6
    COUNTRY = 7
    EMAIL = 9
    ORCID = 13
    INI_DATE = 14
    END_DATE = 15
    PERSONAL_WEB = -1
    SIGNATURE = -1
    SIGNATURE_CUSTOM = -1


class IMarina_Field(Enum):
    NAME = 1  # Submit
    SURNAME = 2  # Submit
    SECOND_SURNAME = 3  # Submit
    SIGNATURE = 4  # No submit. Why?
    SIGNATURE_CUSTOM = 5  # No submit. Why?
    DNI = 6  # Submit
    SEX = 8  # Submit
    COUNTRY = 9   # Submit
    EMAIL = 12  # Submit
    PERSONAL_WEB = 13  # Submit
    #ADSCRIPTION_TYPE = 15  # Submit
    #CATEGORY = 16  # Submit
    INI_DATE = 18  # Submit
    END_DATE = 19  # Submit
    #ENTITY = 20  # Submit
    #ENTITY_TYPE = 22  # Submit
    #ENTITY_WEB = 29  # Submit
    ORCID = 35  # Submit


def sanitize_date(date_dirty):
    if type(date_dirty) is pd._libs.tslibs.timestamps.Timestamp:
        return date_dirty
    elif type(date_dirty) is datetime.datetime:
        return date_dirty
    elif type(date_dirty) is pd._libs.tslibs.nattype.NaTType:
        return None
    elif isinstance(date_dirty, str):
        return datetime.datetime.strptime(date_dirty.strip("'"), "%d/%m/%Y")
    elif isinstance(date_dirty, float):
        return None
    else:
        raise ValueError("Unknown type for date to sanitize: " + str(type(date_dirty)) + " value is: " + str(date_dirty))


def parse_imarina_row_data(row):
    data = Researcher(dni=row.values[IMarina_Field.DNI.value], email=row.values[IMarina_Field.EMAIL.value],
                      orcid=row.values[IMarina_Field.ORCID.value], name=row.values[IMarina_Field.NAME.value],
                      surname=row.values[IMarina_Field.SURNAME.value],
                      second_surname=row.values[IMarina_Field.SECOND_SURNAME.value],
                      ini_date=sanitize_date(row.values[IMarina_Field.INI_DATE.value]),
                      end_date=sanitize_date(row.values[IMarina_Field.END_DATE.value]),
                      sex=row.values[IMarina_Field.SEX.value],
                      personal_web=row.values[IMarina_Field.PERSONAL_WEB.value],
                      signature=row.values[IMarina_Field.SIGNATURE.value],
                      signature_custom=row.values[IMarina_Field.SIGNATURE_CUSTOM.value],
                      country=row.values[IMarina_Field.COUNTRY.value])
    return data


def parse_a3_row_data(row):
    translator = build_translations()
    data = Researcher(dni=row.values[A3_Field.DNI.value], email=row.values[A3_Field.EMAIL.value],
                      orcid=row.values[A3_Field.ORCID.value],
                      name=row.values[A3_Field.NAME.value],
                      surname=row.values[A3_Field.SURNAME.value],
                      second_surname=row.values[A3_Field.SECOND_SURNAME.value],
                      ini_date=sanitize_date(row.values[A3_Field.INI_DATE.value]),
                      end_date=sanitize_date(row.values[A3_Field.END_DATE.value]),
                      sex=translator[A3_Field.SEX][row.values[A3_Field.SEX.value]],
                      personal_web="",
                      signature="",
                      signature_custom="",
                      country=translator[A3_Field.COUNTRY][row.values[A3_Field.COUNTRY.value]])
    return data


def unparse_date(date):
    if date is None:
        return ""
    else:
        return date.strftime("%d/%m/%Y")


def unparse_researcher_to_imarina_row(data: Researcher, empty_output_row):
    empty_output_row.iat[0, IMarina_Field.DNI.value] = data.dni
    empty_output_row.iat[0, IMarina_Field.EMAIL.value] = data.email
    empty_output_row.iat[0, IMarina_Field.ORCID.value] = data.orcid
    empty_output_row.iat[0, IMarina_Field.NAME.value] = data.name
    empty_output_row.iat[0, IMarina_Field.SURNAME.value] = data.surname
    empty_output_row.iat[0, IMarina_Field.SECOND_SURNAME.value] = data.second_surname
    empty_output_row.iat[0, IMarina_Field.INI_DATE.value] = unparse_date(data.ini_date)
    empty_output_row.iat[0, IMarina_Field.END_DATE.value] = unparse_date(data.end_date)
    empty_output_row.iat[0, IMarina_Field.SEX.value] = data.sex
    empty_output_row.iat[0, IMarina_Field.PERSONAL_WEB.value] = data.personal_web
    empty_output_row.iat[0, IMarina_Field.SIGNATURE.value] = data.signature
    empty_output_row.iat[0, IMarina_Field.SIGNATURE_CUSTOM.value] = data.signature_custom


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
    ret.personal_web = a3.personal_web
    ret.signature = a3.signature
    ret.signature_custom = a3.signature_custom


def parse_two_columns(df, key: int, value: int, func_apply_key=None, func_apply_value=None):
    val_col = df[value]
    key_col = df[key]

    if func_apply_value is not None:
        val_col = val_col.apply(func_apply_value)
    if func_apply_key is not None:
        key_col = key_col.apply(func_apply_key)

    return dict(zip(key_col, val_col))


def read_dataframe(path, skiprows, header):
    # Read the Excel file, skipping the first 3 rows
    return pd.read_excel(path, skiprows=skiprows, header=header)


def build_countries_translator(path):
    df = read_dataframe(path, 0, None)
    return parse_two_columns(df, 0, 1)


def apply_defaults(researcher: Researcher):
    researcher.personal_web = "https://iciq.es"


def build_translations(countries_path):
    r = {A3_Field.SEX: {}}
    r[A3_Field.SEX]["Mujer"] = "Woman"
    r[A3_Field.SEX]["Hombre"] = "Man"

    countries = build_countries_translator(countries_path)
    for key in countries.keys():
        countries[A3_Field.]

    return r


def is_same_person(imarina_row, a3_row):
    if isinstance(imarina_row.orcid, str) and isinstance(a3_row.orcid, str):
        if imarina_row.orcid.replace("-", "") == a3_row.orcid:
            #print("ORCID match")
            return True
    if imarina_row.dni == a3_row.dni:
        #print("DNI match")
        return True
    if imarina_row.email == a3_row.email:
        #print("email match: iMarina email: " + str(imarina_row.email) + " search_data match: " + str(a3_row.email))
        return True
    return False


def is_in_a3(search_data, a3):
    for index, row in a3.iterrows():
        row_data = parse_a3_row_data(row)
        if is_same_person(search_data, row_data):
            return True
    return False


def search_data(query, search_data, parser):
    matches = []
    for index, row in search_data.iterrows():
        row_data = parser(row)
        if is_same_person(query, row_data):
            matches.append(row_data)
    return matches


def build_empty_row(imarina_dataframe):
    empty_output_dataframe = imarina_dataframe[0:0].copy()  # retains columns, types, and headers if any
    empty_output_dataframe.loc[0] = [None] * len(imarina_dataframe.columns)
    return empty_output_dataframe


def main():
    logger = setup_logger("iMarina-load", "./logs/log.log", level=logging.DEBUG)

    today = date.today()

    # Repo root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Output dir
    output_path = os.path.join(root_dir, 'output', "iMarina_upload_" + datetime.datetime.today().__str__() + ".xlsx")
    input_dir = os.path.join(root_dir, 'input')

    # Get A3 data
    a3_path = os.path.join(input_dir, "A3.xlsx")
    a3_data = pd.read_excel(a3_path, header=2)
    a3_data = a3_data.iloc[3:]

    # Get iMarina last upload data
    im_path = os.path.join(input_dir, "iMarina.xlsx")
    im_data = pd.read_excel(im_path, header=0)

    countries_path = os.path.join(input_dir, "countries.xlsx")

    output_data = im_data[0:0]  # retains columns, types, and headers if any
    empty_row_output_data = build_empty_row(imarina_dataframe=im_data)

    # Phase 1: Check if the researchers in iMarina are still in A3
    not_present = 0
    for index, row in im_data.iterrows():
        print("Processing data from: " + row.values[1] + " " + row.values[2])

        researcher_imarina = parse_imarina_row_data(row)
        researchers_matched_a3 = search_data(researcher_imarina, a3_data, parse_a3_row_data)
        empty_row = empty_row_output_data.copy()
        if len(researchers_matched_a3) == 0:
            # The current researcher in last iMarina load is not present in A3 --> the researcher is no longer in ICIQ.
            print(
                "row data from " + str(
                    researcher_imarina.name) + " is not present on search_data data. Adding to iMarina with "
                                               "end of "
                                               "contract date.")
            not_present += 1

            # Use end time already in iMarina if present, if not, set to today
            if researcher_imarina.end_date is None:
                researcher_imarina.end_date = today

            unparse_researcher_to_imarina_row(researcher_imarina, empty_row)
            output_data = pd.concat([output_data, empty_row], ignore_index=True)
        elif len(researchers_matched_a3) == 1:
            # The current researcher in iMarina is present in A3 --> Corresponds to a researcher still working in ICIQ
            if researcher_imarina.end_date is None:  # iMarina row has end date?
                # how to check position change.
                # If end date not present check if a position change
                # Add a new line
                # with same data with the new position and dates to determine to output.
                # If it has not changed, add current iMarina row to output as is.
                # (end date not present) it is a contract that could be still ongoing
                continue
            # Contract has end date and is already present in ICIQ; it is a history line, so append to output as is
            unparse_researcher_to_imarina_row(researcher_imarina, empty_row)
            output_data = pd.concat([output_data, empty_row], ignore_index=True)
        else:
            raise ValueError("More than one value matched in A3 for researcher " + str(researcher_imarina.name))

    # Phase 2: Add researchers in A3 that are not present in iMarina
    for index, row in a3_data.iterrows():
        researcher_a3 = parse_a3_row_data(row)
        researchers_matched_im = search_data(researcher_a3, im_data, parse_imarina_row_data)
        empty_row = empty_row_output_data.copy()
        if len(researchers_matched_im) == 0:
            logger.info(f"Present in A3 but not on iMarina, is a new researcher to add to iMarina")
            unparse_researcher_to_imarina_row(researcher_a3, empty_row)
            output_data = pd.concat([output_data, empty_row], ignore_index=True)
        elif len(researchers_matched_im) == 1:
            logger.info(f"Present in A3 and also on iMarina, we do not need to do anything because we added it on the "
                        f"previous step")
            pass
        elif len(researchers_matched_im) > 1:
            logger.info(f"Present in A3 and also on iMarina, we do not need to do anything because we added it on the "
                        f"previous step. More than one match. Number: {str(len(researchers_matched_im))}")


    # For each researcher in A3, check if they are not present in iMarina
    # If they are not present, it has a code 4 and its begin and end date is outside a range
    # to determine from fields to determine, then the current row from A3 corresponds to ICREA researcher or predoc
    # with CSC, so its data from A3 needs to be added to the output.
    output_data.to_excel(output_path, index=False)

    # Si grupo  unidad = DIRECCIO, o grupo unidad = GESTIO, o grupo unidad = OUTREACH llavors eliminar del output ( no poner)



if __name__ == "__main__":
    main()
