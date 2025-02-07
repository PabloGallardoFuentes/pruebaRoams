from decimal import Decimal
import sqlite3
from fastapi import HTTPException
from models import CustomerRequest, CustomerResponse

class CustomerService:
    @staticmethod
    def get_db_connection():
        """Return a connection to the database."""
        return sqlite3.connect("mortgage.db")
    

    @staticmethod
    def create_customer(customer: CustomerRequest):
        """Create a new customer."""
        if (not CustomerService.validate_dni(customer.dni)):
            raise HTTPException(status_code=400, detail="El DNI no es válido.")

        conn = CustomerService.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO customers (name, dni, email, capital)
                VALUES (?, ?, ?, ?)
                """,
                (customer.name, customer.dni, customer.email, customer.capital),
            )
            conn.commit()
            client_id = cursor.lastrowid
            return CustomerResponse(id=client_id, **customer.model_dump())
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="El DNI o el email ya están registrados.")
        finally:
            conn.close()

    @staticmethod
    def get_customer_by_dni(customer_dni: str):
        """Get a customer by DNI."""
        conn = CustomerService.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, dni, email, capital
            FROM customers
            WHERE dni = ?
            """,
            (customer_dni,),
        )
        customer = cursor.fetchone() 

        return customer

    @staticmethod
    def update_customer_by_dni(customer_dni: str, customer: CustomerRequest):
        """Update a customer by DNI."""
        selected_customer = CustomerService.get_customer_by_dni(customer_dni)
        if selected_customer is None:
            return selected_customer
        
        ## Check if the new DNI is valid
        if (not CustomerService.validate_dni(customer.dni)):
            raise HTTPException(status_code=400, detail="El DNI nuevo no es válido.")
        
        conn = CustomerService.get_db_connection()
        cursor = conn.cursor()
        try:
            # Update the customer data
            cursor.execute(
                """
                UPDATE customers
                SET name = ?, dni = ?, email = ?, capital = ?
                WHERE dni = ?
                """,
                (customer.name, customer.dni, customer.email, customer.capital, customer_dni),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            raise HTTPException(status_code=400, detail="El DNI o el email ya están registrados.")

        # Return the updated customer (check it was updated)
        cursor.execute(
            "SELECT * FROM customers WHERE dni = ?",
            (customer.dni,),
        )
        update_customer = cursor.fetchone()
        conn.close()

        return update_customer


    @staticmethod
    def delete_customer_by_dni(customer_dni: str):
        """Delete a customer by DNI."""
        # Check if the customer exists
        customer = CustomerService.get_customer_by_dni(customer_dni)

        if customer is None:
            return customer
    
        conn = CustomerService.get_db_connection()
        cursor = conn.cursor()
        # Delete the customer
        cursor.execute(
            "DELETE FROM customers WHERE dni = ?",
            (customer_dni,),
        )
        conn.commit()
        conn.close()

        return customer
    
    @staticmethod
    def validate_dni(dni: str):
        """Validate a DNI."""
        if len(dni) != 9:
            return False

        dni_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
        dni_number = int(dni[:-1])
        return dni[-1] == dni_letters[dni_number % 23]
    
    def emailExists(email: str):
        conn = CustomerService.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM customers WHERE email = ?
            """,
            (email,),
        )
        customer = cursor.fetchone()
        conn.close()
        return customer is not None

    @staticmethod
    def simulate_mortgage(dni: str, tae: float, years: int):
        """Simulate a mortgage."""
        conn = CustomerService.get_db_connection()
        cursor = conn.cursor()

        customer = CustomerService.get_customer_by_dni(dni)

        if customer is None:
            conn.close()
            raise HTTPException(status_code=404, detail="Cliente no encontrado.")
        
        capital = Decimal(customer[4])
        i = tae / 100 / 12
        n = years * 12
        #Calculate the monthly payment
        monthly_payment = (capital * i) / (1 - (1 + i) ** -n)
        #Calculate the total amount
        total_amount = monthly_payment * n

        cursor.execute(
            """
            INSERT INTO simulations (dni, tae, years, monthly_payment, total_amount)
            VALUES (?, ?, ?, ?, ?)
            """,
            (dni, float(tae), int(years), float(monthly_payment), float(total_amount)),
        )
        conn.commit()
        simulation_id = cursor.lastrowid
        return {
            "id": simulation_id,
            "dni": dni,
            "tae": tae,
            "years": years,
            "monthly_payment": monthly_payment,
            "total_amount": total_amount,
        }
    
    @staticmethod
    def get_customers():
        """Get all customers."""
        conn = CustomerService.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, dni, email, capital
            FROM customers
            """
        )
        customers = cursor.fetchall()
        conn.close()

        return customers