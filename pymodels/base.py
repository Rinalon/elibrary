from sqlalchemy.orm import  DeclarativeBase
from enum import Enum as PyEnum

class Base(DeclarativeBase): pass

class AgeRating(PyEnum):
    ALL = "0+"
    SIX = "6+"
    TWELVE = "12+"
    SIXTEEN = "16+"
    EIGHTEEN = "18+"