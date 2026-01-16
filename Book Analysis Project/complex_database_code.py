# Step by Step process of code for Contact Managment System with MySQL

# Step 1: Import necessary libraries
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Step 2: Create a base class for declarative models
Base = declarative_base()

# Step 3: Define the Contact model
class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
    email = Column(String(100), nullable=True)

# Step 4: Set up the database
# Replace 'username', 'password', 'host', and 'database_name' with your MySQL credentials
DATABASE_URL = 'mysql+pymysql://root:paswrd@localhost/userdb'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Step 5: Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Step 6: Define CRUD operations
def add_contact(name, phone_number, email):
    new_contact = Contact(name=name, phone_number=phone_number, email=email)
    session.add(new_contact)
    session.commit()

def get_all_contacts():
    return session.query(Contact).all()

def update_contact(contact_id, name=None, phone_number=None, email=None):
    contact = session.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        if name:
            contact.name = name
        if phone_number:
            contact.phone_number = phone_number
        if email:
            contact.email = email
        session.commit()

def delete_contact(contact_id):
    contact = session.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        session.delete(contact)
        session.commit()

# Step 7: Example usage
if __name__ == "__main__":
    # Adding contacts
    add_contact("Alice Smith", "123-456-7890", "alice@example.com")
    add_contact("Bob Johnson", "987-654-3210", "bob@example.com")

    # Fetching all contacts
    contacts = get_all_contacts()
    print("Contacts List:")
    for contact in contacts:
        print(f"ID: {contact.id}, Name: {contact.name}, Phone: {contact.phone_number}, Email: {contact.email}")

    # Updating a contact
    update_contact(1, phone_number="111-222-3333")

    # Deleting a contact
    delete_contact(2)
    print("Contact with ID 2 has been deleted.")
