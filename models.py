from pydantic import BaseModel, EmailStr, Field, condecimal

class CustomerRequest(BaseModel):
    name: str
    dni: str
    email: EmailStr
    capital: float

class CustomerResponse(CustomerRequest):
    id: int

class SimulationRequest(BaseModel):
    tae: condecimal(gt=0) # type: ignore # greater than 0
    years: int

class SimulationResponse(BaseModel):
    monthly_payment: float
    total_amount: float
    dni: str


class Customer(BaseModel):
    id: int
    name: str
    dni: str
    email: str
    capital: float