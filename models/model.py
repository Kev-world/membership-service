from databases.sqlDB import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
import uuid

class Members(Base):
    __tablename__ = 'members'
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    firstName = Column(String(25))
    lastName = Column(String(25))
    email = Column(String(50), unique=True)
    address = Column(String(100))
    dob = Column(Date)

class MemberShipDetails(Base):
    __tablename__ = 'membershipdetails'
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    type_code = Column(String(3), ForeignKey('membershiptypes.code'))
    valid_till = Column(Date)
    member_id = Column(String(36), ForeignKey('members.id'))
     # Relationship: Each MembershipDetails references one MembershipStatus
    membership_status = Column(String(3), ForeignKey('membershipstatus.code'))
    # Relationship: Each MembershipDetails references one MembershipType
    membership_type = relationship("MemberShipTypes", back_populates="membership_details")


class MemberShipTypes(Base):
    __tablename__ = 'membershiptypes'
    code = Column(String(3), primary_key=True, unique=True)
    name = Column(String(10), nullable=False, unique=True)
    # Relationship: One MembershipType can be referenced by many MemberShipDetails
    membership_details = relationship("MemberShipDetails", back_populates="membership_type")


class MemberShipStatus(Base):
    __tablename__ = 'membershipstatus'
    code = Column(String(3), primary_key=True, unique=True)
    status = Column(String(10), nullable=False, unique=True)
    # Relationship: One MembershipStatus can be referenced by many MemberShipDetails
    membership_status = relationship("MemberShipDetails", back_populates="membership_status")