from models.metricThresholdModel import MetricThreshold
from serverLogs.serverLogsController import get_latest_server_logs
from flask import jsonify

class metricThresholdClass():
    # Check the health status of the servers for server_logs table
    def get_health_status():
        try:
            # Fetch the latest server logs
            latest_server_logs_response = get_latest_server_logs()
            response, status_code = get_latest_server_logs()

            # Check if the response is successful
            if status_code == 200:
                # Extract the data from the response
                json_data = response.json

                latest_server_logs = json_data['data']['latest_server_logs']

                # Fetch health status thresholds from the database
                thresholds = MetricThreshold.query.all()
                threshold_dict = {threshold.Metric: (threshold.CriticalThreshold, threshold.BadThreshold, threshold.WarningThreshold) for threshold in thresholds}

                # List to store health status data
                health_status_data = []

                # Iterate through each server log
                for log in latest_server_logs:
                    infrastructure_name = log['InfrastructureName']
                    health_status = {}

                    # Determine health status for each metric
                    for metric in log.keys():
                        if metric in threshold_dict:
                            value = log[metric]
                            critical_threshold, bad_threshold, warning_threshold = threshold_dict[metric]

                            if metric == 'ServerAvailability' or metric == 'ServerNetworkAvailability':
                                if value == 0:
                                    health_status[metric] = 'Critical'
                                else:
                                    health_status[metric] = 'Healthy'
                            else:
                                if value >= critical_threshold:
                                    health_status[metric] = 'Critical'
                                elif value >= bad_threshold:
                                    health_status[metric] = 'Bad'
                                elif value >= warning_threshold:
                                    health_status[metric] = 'Warning'
                                else:
                                    health_status[metric] = 'Healthy'

                    # Append infrastructure name and its health status to the list
                    health_status_data.append({'InfrastructureName': infrastructure_name, 'HealthStatus': health_status})

                if health_status_data:
                    return jsonify({"code": 200, "data": health_status_data}), 200
                else:
                    return jsonify({"code": 404, "message": "No server logs available."}), 404
            else:
                # Return the response from get_latest_server_logs() directly
                return latest_server_logs_response[0]
        except Exception as e:
            # Handle any exceptions and return an error response
            return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

