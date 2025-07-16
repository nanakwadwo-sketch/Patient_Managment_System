from fastapi import FastAPI
from routers import patients, doctors, appointments, medical_records
from middleware.log_request_time import log_request_time
from utils.exceptions import add_exception_handlers

app = FastAPI(title="Patient Medical Record Management System")

app.middleware("http")(log_request_time)

# Include routers for different functionalities
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(medical_records.router)

add_exception_handlers(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Patient Medical Record Management System"}