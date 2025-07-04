from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_run import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)

    # One-to-many: One contact can be linked to many chassis
    chassis = relationship("Chassis", back_populates="contact")


class Chassis(Base):
    __tablename__ = "chassis"

    id = Column(Integer, primary_key=True, index=True)
    chassis_number = Column(String, unique=True, index=True)
    model = Column(String)
    
    contact_id = Column(Integer, ForeignKey("contacts.id"))

    # Back-reference to contact
    contact = relationship("Contact", back_populates="chassis")
