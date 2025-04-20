from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import relationship
Base = declarative_base()


# class Example(Base):
#     __tablename__ = "business"
#
#     id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
#     example_column = Column(String(100), nullable=False)
#     created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
#     created_by = Column(String(100), nullable=True)
#     updated_by = Column(String(100), nullable=True)


class Business(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)

    symptoms = relationship("BusinessSymptom", back_populates="business")


class Symptom(Base):
    __tablename__ = "symptom"

    code = Column(String(20), primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)

    business_symptoms = relationship("BusinessSymptom", back_populates="symptom")


class BusinessSymptom(Base):
    __tablename__ = "business_symptom"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(Integer, ForeignKey("business.id"), nullable=False)
    symptom_code = Column(String(20), ForeignKey("symptom.code"), nullable=False)
    diagnostic = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)

    business = relationship("Business", back_populates="symptoms")
    symptom = relationship("Symptom", back_populates="business_symptoms")