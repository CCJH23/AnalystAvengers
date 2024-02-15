# import pytest
# from main import app, drop_tables, initialize_databases
# from models.model import db
# from models.staff_model import Staff
# from models.role_model import Role


# # Set up the Flask app for testing
# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client


# # Test for successful creation of role listing
# def test_create_success(client):
#     initialize_databases()
#     client.get('/access/get_access')
#     new_staff = Staff(
#         id=130001,
#         staff_first_name="James",
#         staff_last_name="Re",
#         dept="Sales",
#         country="USA",
#         email="james.re@example.com",
#         role=1
#     )
#     new_role = Role(
#         role_name="Product Manager",
#         role_description="I call the manager's assistance"
#     )
#     application_data = {
#         "role_name": "Product Manager",
#         "country": "USA",
#         "dept": "Sales",
#         "is_open": True,
#         "opening_date": "2023-10-01",
#         "closing_date": "2023-10-15",
#         "reporting_manager": None
#     }
#     with app.app_context():
#         db.session.add(new_staff)
#         db.session.add(new_role)
#         db.session.commit()
#     response = client.post('/listing/create', json=application_data)
#     expected_message = {'message': 'Role Listing created successfully'}
#     assert response.json == expected_message
#     assert response.status_code == 201
#     drop_tables()


# # Test for creating a listing role with missing required fields
# def test_create_role_listing_with_missing_fields_failure(client):
#     initialize_databases()
#     client.get('/access/get_access')
#     new_staff = Staff(
#         id=130001,
#         staff_first_name="James",
#         staff_last_name="Re",
#         dept="Sales",
#         country="USA",
#         email="james.re@example.com",
#         role=1
#     )
#     application_data = {
#         "role_name": "Product Manager",
#         "country": "USA",
#         "dept": "Sales",
#         "is_open": True,
#         "opening_date": "",
#         "closing_date": "",
#         "reporting_manager": None
#     }
#     with app.app_context():
#         db.session.add(new_staff)
#         db.session.commit()
#     response = client.post('/listing/create', json=application_data)
#     expected_message = {'message': 'Missing required fields'}
#     assert response.json == expected_message
#     assert response.status_code == 400
#     drop_tables()


# # Test for creating a duplicate role listing
# def test_create_duplicate_role_listing_failure(client):
#     initialize_databases()
#     client.get('/access/get_access')
#     new_staff = Staff(
#         id=130001,
#         staff_first_name="James",
#         staff_last_name="Re",
#         dept="Sales",
#         country="USA",
#         email="james.re@example.com",
#         role=1
#     )
#     new_role = Role(
#         role_name="Product Manager",
#         role_description="I call the manager's assistance"
#     )
#     application_data = {
#         "role_name": "Product Manager",
#         "country": "USA",
#         "dept": "Sales",
#         "is_open": True,
#         "opening_date": "2023-10-01",
#         "closing_date": "2023-10-15",
#         "reporting_manager": None
#     }
#     duplicate_data = {
#         "role_name": "Product Manager",
#         "country": "USA",
#         "dept": "Sales",
#         "is_open": True,
#         "opening_date": "2023-10-01",
#         "closing_date": "2023-10-15",
#         "reporting_manager": None
#     }
#     with app.app_context():
#         db.session.add(new_role)
#         db.session.add(new_staff)
#         db.session.commit()
#     # Send the first POST request
#     response1 = client.post('/listing/create', json=application_data)
#     expected_message1 = {'message': 'Role Listing created successfully'}
#     assert response1.json == expected_message1
#     assert response1.status_code == 201

#     # Send the second POST request with duplicate data
#     response2 = client.post('/listing/create', json=duplicate_data)
#     expected_message2 = {'message': 'Role Listing already exists'}
#     assert response2.json == expected_message2
#     assert response2.status_code == 409
#     drop_tables()


# # Test for creating a role listing with non-existent manager
# def test_create_role_listing_with_nonexistent_reporting_manager(client):
#     initialize_databases()
#     client.get('/access/get_access')
#     new_staff = Staff(
#         id=130001,
#         staff_first_name="James",
#         staff_last_name="Re",
#         dept="Sales",
#         country="USA",
#         email="james.re@example.com",
#         role=1
#     )
#     application_data = {
#         "role_name": "Product Manager",
#         "country": "USA",
#         "dept": "Sales",
#         "is_open": True,
#         "opening_date": "2023-10-01",
#         "closing_date": "2023-10-15",
#         "reporting_manager": 2
#     }
#     with app.app_context():
#         db.session.add(new_staff)
#         db.session.commit()
#     # Send the first POST request
#     response = client.post('/listing/create', json=application_data)
#     expected_message = {'message': 'Reporting manager does not exist'}
#     assert response.json == expected_message
#     assert response.status_code == 404
#     drop_tables()