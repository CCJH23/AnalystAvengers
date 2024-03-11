from models.serviceGroupModel import ServiceGroup
from flask import jsonify

class ServiceGroupClass():
    # Get all records from ServiceGroupClass table
    def get_service_group():
        # retrieve all records from ServiceGroupClass table
        records = ServiceGroup.query.all()
        # Store retrieved records in array format
        mapped_records = [{"ServiceId": record.ServiceId, "ServiceName": record.ServiceName} for record in records]
        # List to store mappings
        return mapped_records