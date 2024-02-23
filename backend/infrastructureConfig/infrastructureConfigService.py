from models.infrastructureConfigModel import InfrastructureConfig
from flask import jsonify

class infrastructureConfigClass():
    # Get all records from the InfrastructureConfig table
    def get_infrastructure_config():
        # Retrieve all records from the InfrastructureConfig table
        records = InfrastructureConfig.query.all()
        
        # List to store server configurations
        server_configurations = []
        
        # Iterate through each record
        for record in records:
            # Convert record to a dictionary
            config_data = record.__dict__
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            config_data.pop('_sa_instance_state', None)
            # Append server configuration data to the list
            server_configurations.append(config_data)
            
        if server_configurations:  # Check if server configurations are available
            # Return JSON response with server configurations
            return jsonify({"code": 200, "data": {"server_configurations": server_configurations}}), 200
        else:
            # Return JSON response indicating no server configurations are available
            return jsonify({"code": 404, "message": "There are no server configurations available."}), 404
    
    # Query data from infrastructure_config table by infrastructure name and type
    def get_infrastructure_config_by_infra_name_and_type(infrastructure_name, infrastructure_type):
        try:
            # Query to fetch the server configuration by infrastructure name and type
            config = InfrastructureConfig.query.filter_by(InfrastructureName=infrastructure_name, InfrastructureType=infrastructure_type).first()

            if config:
                # Convert record to a dictionary
                config_data = config.__dict__
                # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
                config_data.pop('_sa_instance_state', None)
                # Return JSON response with the server configuration
                return jsonify({"code": 200, "data": {"server_configuration": config_data}}), 200
            else:
                # Return JSON response indicating no server configuration is available
                return jsonify({"code": 404, "message": "There is no server configuration available for the specified infrastructure name and type."}), 404
        except Exception as e:
            # Handle any exceptions and return an error response
            return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

