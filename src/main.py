
import logging
import shutil

import pandas as pd

from datetime import date
import datetime



import os
from enum import Enum

import paramiko
from numpy.ma.core import equal
from pycparser.ply.yacc import resultlimit

from log import setup_logger
from arguments import process_parse_arguments
from secret import read_secret


class Researcher:


    def __init__(self, **kwargs):
        self.dni = kwargs.get("dni")
        self.email = kwargs.get("email")
        self.name = kwargs.get("name")
        self.surname = kwargs.get("surname")
        self.second_surname = kwargs.get("second_surname")
        self.orcid = kwargs.get("orcid")
        self.ini_date = kwargs.get("ini_date")
        self.end_date = kwargs.get("end_date")
        self.ini_prorrog = kwargs.get("ini_prorrog")
        self.end_prorrog = kwargs.get("end_prorrog")
        self.date_termination = kwargs.get("date_termination")
        self.sex = kwargs.get("sex")
        self.personal_web = kwargs.get("personal_web")
        self.signature = kwargs.get("signature")
        self.signature_custom = kwargs.get("signature_custom")
        self.country = kwargs.get("country")
        self.born_country = kwargs.get("born_country")
        self.job_description = kwargs.get("job_description")
        self.employee_code = kwargs.get("employee_code")
        self.code_center = kwargs.get("code_center")


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
            f"  Ini Prorrog: {self.ini_prorrog}\n"
            f"  End Prorrog: {self.end_prorrog}\n"
            f"  Date Termination: {self.date_termination}\n"
            f"  Sex: {self.sex}\n"
            f"  Personal web: {self.personal_web}\n"
            f"  Signature: {self.signature}\n"
            f"  Signature custom: {self.signature_custom}\n"
            f"  Country: {self.country}\n"
            f"  Born country: {self.born_country}\n"
            f"  Job description: {self.job_description}\n"
            f"  Code center: {self.code_center}\n"
        )

    def copy(self):
        return Researcher(
            code_center=self.code_center,
            dni=self.dni,
            email=self.email,
            name=self.name,
            surname=self.surname,
            second_surname=self.second_surname,
            orcid=self.orcid,
            ini_date=self.ini_date,
            end_date=self.end_date,
            ini_prorrog=self.ini_prorrog,
            end_prorrog=self.end_prorrog,
            date_termination=self.date_termination,
            sex=self.sex,
            personal_web=self.personal_web,
            signature=self.signature,
            signature_custom=self.signature_custom,
            country=self.country,
            born_country=self.born_country,
            job_description=self.job_description,
                          )


class A3_Field(Enum):
    CODE_CENTER = 1
    NAME = 2
    SURNAME = 3
    SECOND_SURNAME = 4
    DNI = 5
    SEX = 6
    COUNTRY = 7
    BORN_COUNTRY = 8
    EMAIL = 9
    JOB_DESCRIPTION = 10
    ORCID = 13
    INI_DATE = 14
    END_DATE = 15
    INI_PRORROG = 16
    END_PRORROG = 17
    DATE_TERMINATION = 18
    PERSONAL_WEB = -1
    SIGNATURE = -1
    SIGNATURE_CUSTOM = -1
    BIRTH_DATE = -1



class IMarina_Field(Enum):
    NAME = 1  # Submit
    SURNAME = 2  # Submit
    SECOND_SURNAME = 3  # Submit
    SIGNATURE = 4  # No submit. Why?
    SIGNATURE_CUSTOM = 5  # No submit. Why?
    DNI = 6  # Submit
    BIRTH_DATE = 7  # Submit
    SEX = 8  # Submit
    COUNTRY = 9   # Submit
    #BORN_COUNTRY = -1
    EMAIL = 12  # Submit
    PERSONAL_WEB = 13  # Submit
    #ADSCRIPTION_TYPE = 15  # Submit
    JOB_DESCRIPTION = 16  # Submit
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


def parse_imarina_row_data(row, translator):
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
                      country=row.values[IMarina_Field.COUNTRY.value],
                      born_country=row.values[IMarina_Field.COUNTRY.value],
                      job_description=row.values[IMarina_Field.JOB_DESCRIPTION.value]                      )
    return data


def parse_a3_row_data(row, translator):


    default_web = "https://www.iciq.org"
    data = Researcher(code_center=row.values[A3_Field.CODE_CENTER.value],
                      dni=row.values[A3_Field.DNI.value], email=row.values[A3_Field.EMAIL.value],
                      orcid=row.values[A3_Field.ORCID.value],
                      name=row.values[A3_Field.NAME.value],
                      surname=row.values[A3_Field.SURNAME.value],
                      second_surname=row.values[A3_Field.SECOND_SURNAME.value],
                      ini_date=sanitize_date(row.values[A3_Field.INI_DATE.value]),
                      end_date=sanitize_date(row.values[A3_Field.END_DATE.value]),
                      ini_prorrog=sanitize_date(row.values[A3_Field.INI_PRORROG.value]),
                      end_prorrog=sanitize_date(row.values[A3_Field.END_PRORROG.value]),
                      date_termination=sanitize_date(row.values[A3_Field.DATE_TERMINATION.value]),
                      sex=row.values[A3_Field.SEX.value],
                      personal_web=translator[A3_Field.PERSONAL_WEB].get(
                          row.values[A3_Field.JOB_DESCRIPTION.value], default_web
                      ),
                      signature="",
                      signature_custom="",
                      country=row.values[A3_Field.COUNTRY.value],
                      born_country=translator[A3_Field.COUNTRY][row.values[A3_Field.BORN_COUNTRY.value]],
                      job_description=translator[A3_Field.JOB_DESCRIPTION][row.values[A3_Field.JOB_DESCRIPTION.value]]
                      )

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
    empty_output_row.iat[0, IMarina_Field.COUNTRY.value] = data.country
    empty_output_row.iat[0, IMarina_Field.JOB_DESCRIPTION.value] = data.job_description





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


def build_translator(path, skiprows=0):
    df = read_dataframe(path, skiprows, None)
    return parse_two_columns(df, 0, 1)

def apply_defaults(researcher: Researcher):
    researcher.personal_web = "https://iciq.es"


def build_translations(countries_path, jobs_path, personal_web_path):
    r = {A3_Field.SEX: {}}
    r[A3_Field.SEX]["Mujer"] = "Woman"
    r[A3_Field.SEX]["Hombre"] = "Man"

    r[A3_Field.COUNTRY] = {}
    countries = build_translator(countries_path)
    for key in countries.keys():
        r[A3_Field.COUNTRY][key] = countries[key]

    r[A3_Field.JOB_DESCRIPTION] = {}
    jobs = build_translator(jobs_path)
    for key in jobs.keys():
        r[A3_Field.JOB_DESCRIPTION][key] = jobs[key]

    r[A3_Field.PERSONAL_WEB] = {}
    personal_webs = build_translator(personal_web_path, 1)
    for key in personal_webs.keys():
        r[A3_Field.PERSONAL_WEB][key] = personal_webs[key]
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


def search_data(query, search_data, parser, translator):
    matches = []
    for index, row in search_data.iterrows():
        row_data = parser(row, translator)
        if is_same_person(query, row_data):
            matches.append(row_data)
    return matches


def build_empty_row(imarina_dataframe):
    empty_output_dataframe = imarina_dataframe[0:0].copy()  # retains columns, types, and headers if any
    empty_output_dataframe.loc[0] = [None] * len(imarina_dataframe.columns)
    return empty_output_dataframe


def upload_excel(excel_path):
    logger = setup_logger("Upload", "./logs/log.log", level=logging.DEBUG)

    logger.info('Connecting to FTP server.')
    ftp = None
    try:
        serv = paramiko.Transport((read_secret("FTP_HOST"), int(read_secret("FTP_PORT"))))
        serv.connect(username=read_secret("FTP_USER"), password=read_secret("FTP_PASSWORD"))
        ftp = paramiko.SFTPClient.from_transport(serv)
    except Exception as e:
        logger.exception(e)
    logger.info('Connected to FTP server.')

    #logger.info('Changing directory.')
    #try:
    #    ftp.chdir('carga_personal')
    #except Exception as e:
    #    logger.exception(e)
    #logger.info('Changed directory.')

    logger.info('Uploading file.')
    try:
        ftp.put(excel_path, 'icl_ag_personal_12539')
    except Exception as e:
        logger.exception(e)
    logger.info('Uploaded file.')

    logger.info('Closing connection.')
    try:
        ftp.close()
    except Exception as e:
        logger.exception(e)
    logger.info('Closed connection.')


# in process
def has_changed_jobs( researcher_a3, researcher_imarina, translator):
    # translate the job_description from A3 (researcher_a3.job_description)
    a3_job =  translator[A3_Field.JOB_DESCRIPTION].get(researcher_a3.job_description, researcher_a3.job_description)


    # if job_description  is changed
    if a3_job != researcher_imarina.job_description:
        print(f"[CAMBIO] El puesto cambió de : '{a3_job}' a '{researcher_imarina.job_description}'")
        return True

    # if ini_date or end_date have changed & dates are diferents
    if (researcher_a3.ini_date or researcher_a3.end_date) and (
            researcher_a3.ini_date != researcher_imarina.ini_date or
            researcher_a3.end_date != researcher_imarina.end_date
    ):
        print(
            f"[CAMBIO] Fechas diferentes:\n"
            f"  A3: inicio={researcher_a3.ini_date}, fin={researcher_a3.end_date}\n"
            f"  iMarina: inicio={researcher_imarina.ini_date}, fin={researcher_imarina.end_date}"
        )
        return True
    else:


    # si es igual tanto puesto(job_description) como fechas(ini_date & end_date) y no ha cambiado muestra por consola esto:
        print("[SIN CAMBIO] El puesto y las fechas son iguales y no han cambiado.")
    return False


def is_visitor(researcher_a3: Researcher,) -> bool:

  if researcher_a3.code_center == 4:
      start = researcher_a3.ini_date
      end = researcher_a3.end_date
      if start is None:
          return False
      if end is None:
         end = datetime.datetime.today()
      duration = (end - start).days
      return duration < 365
  return False


def build_upload_excel(input_dir, output_path, countries_path, jobs_path, imarina_path, a3_path,):
    logger = setup_logger("Excel build", "./logs/log.log", level=logging.DEBUG)

    today = date.today()

    # Get A3 data
    a3_data = pd.read_excel(a3_path, header=2)
    a3_data = a3_data.iloc[3:]

    # Get iMarina last upload data
    im_data = pd.read_excel(imarina_path, header=0)

    output_data = im_data[0:0]  # retains columns, types, and headers if any
    added_researchers = set()
    empty_row_output_data = build_empty_row(imarina_dataframe=im_data)

    personal_web_path = "input/Personal_web.xlsx"

    translator = build_translations(countries_path, jobs_path, personal_web_path)

    # Phase 1: Check if the researchers in iMarina are still in A3
    not_present = 0
    for index, row in im_data.iterrows():
        print("Processing data from: " + row.values[1] + " " + row.values[2])

        researcher_imarina = parse_imarina_row_data(row, translator,)
        researchers_matched_a3 = search_data(researcher_imarina, a3_data, parse_a3_row_data, translator)
        empty_row = empty_row_output_data.copy()
        if len(researchers_matched_a3) == 0:
            # The current researcher in last iMarina load is not present in A3 --> the researcher is no longer in ICIQ.
            if researcher_imarina.end_date is None:
                researcher_imarina.end_date = today  # Use end time already in iMarina if present, if not, set to today
            new_row = empty_row_output_data.copy()
            unparse_researcher_to_imarina_row(researcher_imarina, new_row)
            output_data = pd.concat([output_data, new_row], ignore_index=True)
            not_present += 1



        elif len(researchers_matched_a3) == 1:
            researcher_a3 = researchers_matched_a3[0]
            # The current researcher in iMarina is present in A3 --> Corresponds to a researcher still working in ICIQ
            if researcher_imarina.end_date is None:
                # if have changed add a new line
                if has_changed_jobs(researcher_a3, researcher_imarina, translator):
                    # El puesto cambió → añadir una nueva línea con los nuevos datos
                    # If end date not present check if a position change Add a new line  with same data with the new position and dates to determine to output.
                    new_row = empty_row_output_data.copy()
                    unparse_researcher_to_imarina_row(researcher_a3, new_row)
                    output_data = pd.concat([output_data, new_row], ignore_index=True)
                    print(f"[INFO] {researcher_a3.name}: cambio detectado, fila nueva añadida")
                else:
                    # No cambió entonces mantener la fila actual
                    # If it has not changed, add current iMarina row to output as is.
                    # (end date not present) it is a contract that could be still ongoing continue
                    new_row = empty_row_output_data.copy()
                    unparse_researcher_to_imarina_row(researcher_a3, new_row)
                    output_data = pd.concat([output_data, new_row], ignore_index=True)
                    print(f"[INFO] {researcher_a3.name}: sin cambio, se mantiene igual")
                continue


            # Contract has end date and is already present in ICIQ; it is a history line, so append to output as is
            unparse_researcher_to_imarina_row(researcher_imarina, empty_row)
            output_data = pd.concat([output_data, empty_row], ignore_index=True)
        else:
            raise ValueError("More than one value matched in A3 for researcher " + str(researcher_imarina.name))

    # Phase 2: Add researchers in A3 that are not present in iMarina
    for index, row in a3_data.iterrows():
        researcher_a3 = parse_a3_row_data(row, translator)
        researchers_matched_im = search_data(researcher_a3, im_data, parse_imarina_row_data, translator) #find researcher_a3 have exist in iMarina
        empty_row = empty_row_output_data.copy()  #prepare a empty row just in case i need dates

        print(
            f"{researcher_a3.name}: code_center={researcher_a3.code_center}, ini_date={researcher_a3.ini_date}, end_date={researcher_a3.end_date}")
        print(f"Visitante: {is_visitor(researcher_a3)}")

        if is_visitor(researcher_a3):
            continue

        if len(researchers_matched_im) == 0:     #the researcher_a3  is new and is not in iMarina
            logger.info(f"Present in A3 but not on iMarina, is a new researcher to add to iMarina")
            unparse_researcher_to_imarina_row(researcher_a3, empty_row)
            output_data = pd.concat([output_data, empty_row], ignore_index=True)
        else:
            logger.info(f"Present in A3 and also on iMarina - already processed in Phase 1")
            # No hacer nada, ya fue procesado en Phase 1


    # Si grupo  unidad = DIRECCIO, o grupo unidad = GESTIO, o grupo unidad = OUTREACH llavors eliminar del output ( no poner)

    # For each researcher in A3, check if they are not present in iMarina
    # If they are not present, it has a code 4, it begins and end date is outside a range
    # to determine from fields to determine, then the current row from A3 corresponds to ICREA researcher or predoc
    # with CSC, so its data from A3 needs to be added to the output.
    output_data.to_excel(output_path, index=False)

# new function TODO
#def upload_file_sharepoint(file_path: Path):
    """
    Uploads a file to Sharepoint Institutional Strengthening
    """


    #pass


def main():
    logger = setup_logger("Main process", "./logs/log.log", level=logging.DEBUG)
    args = process_parse_arguments()
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_dir = os.path.join(root_dir, 'input')
    excel_name = "iMarina_upload_" + datetime.datetime.today().__str__() + ".xlsx"
    output_path = os.path.join(root_dir, 'output', excel_name)

    #pass the args create in arguments.py
    if args.step == "build" or args.step == "all":
        build_upload_excel(input_dir, output_path, args.countries_dict, args.jobs_dict, args.imarina_input, args.a3_input)
    if args.step == "upload" or args.step == "all":
        if args.upload:
            upload_excel(args.upload)
        else:
            upload_excel(output_path)

    # Phase 3: Upload file to iMarina and make backup
    shutil.move(output_path, os.path.join(root_dir, "uploads", excel_name))
    #upload_file_sharepoint(os.path.join(root_dir, "uploads", excel_name)) #de momento silenciada hasta que termine lo cambio de posicion


if __name__ == "__main__":
    main()
