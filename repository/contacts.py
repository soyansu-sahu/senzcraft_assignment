from models.contacts import Contact
from database import get_db


class ContactsRepository:
    def __init__(self, connection):
        self.connection = connection
    def insert_contact(self, contact: Contact):
        try:
            connection = next(get_db())  # Get connection from session maker
            connection.add(contact)  # Add contact object to session
            connection.commit()  # Commit changes to database
        except Exception as e:
            raise e  # Re-raise the exception for proper error handling


    # def get_all_contacts_with_interests(self) -> List[Dict]:
    #     cursor = self.connection.cursor(cursor_factory=DictCursor)
    #     cursor.execute("""
    #         SELECT cd."Sl NO" AS "Sl_NO", cd."Phone#", cd."Contact First Name", cd."Contact Last Name",
    #                cd."Contact Designation", cd."Contact eMail", i.Interest
    #         FROM Contact_Details cd
    #         LEFT JOIN Interest i ON cd."Sl NO" = i.Contact_Serial_No
    #         ORDER BY cd."Sl NO";
    #     """)
    #     data = cursor.fetchall()
    #     response = []
    #     for row in data:
    #         response.append(dict(row))
    #     cursor.close()
    #     return response
