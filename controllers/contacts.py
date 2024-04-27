
import camelot
import os

from uuid import uuid4
from database import session_scope
from models.contacts import Contact
from models.custom_exceptions import ApplicationException
from repository.contacts import ContactsRepository
from sqlalchemy.exc import IntegrityError



def get_ping():
    data = {"message": "pong"}
    return data

def _process_and_upload_contacts(temp_file_name):
    tables = camelot.read_pdf(temp_file_name, flavor='stream')
    table = tables[0]
    df_table = table.df

    # Set the first row as column names
    df_table.columns = df_table.iloc[0]
    df_table = df_table[1:]
    formatted_list_rows = df_table.to_dict(orient='records')
    contacts = []
    for row in formatted_list_rows:
        contact = Contact(
            phone_number=row['Phone#'],
            first_name=row['Contact First Name'],
            last_name=row['Contact Last Name'],
            designation=row['Contact Designation'],
            email=row['Contact Email']
        )
        contacts.append(contact)

    try:
        with session_scope() as db:
            response = db.add_all(contacts)
        return True
    except IntegrityError as e:
        print("[ERROR]: IntegrityError ", e)
        return False


def _process_and_upload_interest(temp_file_name):
    return True

def create_contacts_from_file(file_content, file_type="pdf"):
    """
    file_content : 'bytes'
    """
    temp_file_name = f"temp_files/{uuid4().hex}.pdf"
    with open(temp_file_name, "wb") as temp_file:
        temp_file.write(file_content)

    if file_type == "pdf":
        status = _process_and_upload_contacts(temp_file_name)
    elif  file_type == "pdf" :
        status = _process_and_upload_interest(temp_file_name)
    else:
        status = True

    os.remove(temp_file_name)

    if not status:
        raise ApplicationException("Failed to upload bulk contacts data")

    response = {
        "message": "Successfully inserted data"
    }
    return response, 200




def read_all_contacts():
    contacts = []

    try:
        with session_scope() as db:
            contacts_resp = db.query(Contact).all()
            print("contacts_resp: ", contacts_resp)
            contacts = [contact.get_dict() for contact in contacts_resp]
    except IntegrityError as e:
        print("[ERROR]: IntegrityError ", e)
        raise ApplicationException("Failed to read data for contacts")

    return contacts, 200
