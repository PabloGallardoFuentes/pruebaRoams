from typing import List
from fastapi import FastAPI, HTTPException
from database import get_db_connection
from models import Customer, CustomerRequest, CustomerResponse, SimulationRequest, SimulationResponse
from services.customer_service import CustomerService

app = FastAPI(
    title="API de gestión de hipotecas",
    description="API para la gestión de hipotecas",
    version="1.0.0",
)

@app.post("/clientes/", response_model=CustomerResponse)
def create_customer(customer: CustomerRequest):
    """Create a new customer."""
    return CustomerService.create_customer(customer)

@app.get("/clientes/{customer_dni}", response_model=CustomerResponse)
def get_customer(customer_dni: str):
    """Get a customer by DNI."""
    customer = CustomerService.get_customer_by_dni(customer_dni)

    if customer is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")

    return CustomerResponse(
        id=customer[0], 
        name=customer[1], 
        dni=customer[2], 
        email=customer[3], 
        capital=customer[4]
    )

@app.put("/clientes/{customer_dni}", response_model=CustomerResponse)
def update_customer(customer_dni: str, customer: CustomerRequest):
    """Update a customer by DNI."""
    customer = CustomerService.update_customer_by_dni(customer_dni, customer)

    if customer is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    
    return CustomerResponse(
        id=customer[0], 
        name=customer[1], 
        dni=customer[2], 
        email=customer[3], 
        capital=customer[4]
    )



@app.delete("/clientes/{customer_dni}", response_model=CustomerResponse)
def delete_customer(customer_dni: str):
    """Delete a customer by DNI."""
    customer = CustomerService.delete_customer_by_dni(customer_dni)

    if customer is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    
    return CustomerResponse(
        id=customer[0], 
        name=customer[1], 
        dni=customer[2], 
        email=customer[3], 
        capital=customer[4]
    )
    
@app.get("/clientes/", response_model=List[CustomerResponse])
def get_customers():
    """Get all customers."""
    customers = CustomerService.get_customers()

    return [CustomerResponse(name=customer[1], dni=customer[2], email=customer[3], capital=customer[4], id=customer[0]) for customer in customers]



# Mortgages
@app.post("/clientes/{customer_dni}/simulacion/", response_model=SimulationResponse)
def simulate_mortgage(customer_dni: str, simulation: SimulationRequest):
    """Simulate a mortgage."""
    savedSimulation = CustomerService.simulate_mortgage(customer_dni, simulation.tae, simulation.years)
    return SimulationResponse(
        monthly_payment=savedSimulation["monthly_payment"], 
        total_amount=savedSimulation["total_amount"], 
        dni=savedSimulation["dni"]
        )