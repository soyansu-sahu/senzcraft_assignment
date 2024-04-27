from sqlalchemy import Column, String, Integer  
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint

from database import engine


Base = declarative_base()


class Interest(Base):
    __tablename__ = "sports"
    name = Column(String, primary_key=True)

class Contact(Base):  
    __tablename__ = "contact_details" 
    id = Column(Integer, primary_key=True)
    phone_number = Column(String, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    designation = Column(String)
    email = Column(String)

    interests = relationship("Interest", secondary="contact_interests")

    def get_dict(self):
        interests = [interest.name for interest in self.interests]
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "designation": self.designation,
            "email": self.designation,
            "interests": interests
        }

class ContactInterest(Base):
    __tablename__ = "contact_interests"
    contact_id = Column(Integer, ForeignKey('contact_details.id'), primary_key=True)
    interest_name = Column(String, ForeignKey('sports.name'), primary_key=True)

    contact = relationship("Contact", backref="contact_interests")
    interest = relationship("Interest", backref="contact_interests")

    # Define a unique constraint on the combination of contact_id and interest_name
    __table_args__ = (
        UniqueConstraint('contact_id', 'interest_name', name='uq_contact_interest'),
    )


Base.metadata.create_all(engine)
