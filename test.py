import requests

# Base URL of your Flask API
BASE_URL = "http://127.0.0.1:5000"

# Assuming these are the student IDs for testing
STUDENT_ID_1 = 1  # Student who creates the report
STUDENT_ID_2 = 2  # Another student, for unauthorized access test

def test_create_report(student_id):
    print("Testing: Create Report")
    response = requests.post(f"{BASE_URL}/reports", json={"issue": "Test Issue", "description": "Test Description", "student_id": student_id})
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    return response.json()

def test_get_report(report_id):
    print("\nTesting: Get Report")
    response = requests.get(f"{BASE_URL}/reports/{report_id}")
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_update_report(report_id, student_id):
    print("\nTesting: Update Report")
    response = requests.put(f"{BASE_URL}/reports/{report_id}", json={"issue": "Updated Issue", "description": "Updated Description", "student_id": student_id})
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_delete_report(report_id, student_id):
    print("\nTesting: Delete Report")
    response = requests.delete(f"{BASE_URL}/reports/{report_id}", json={"issue": "", "description": "", "student_id": student_id})
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def main():
    # Create a new report with STUDENT_ID_1
    new_report = test_create_report(STUDENT_ID_1)
    report_id = new_report.get('id')

    # Test get, update, and delete operations
    if report_id:
        test_get_report(report_id)
        test_update_report(report_id, STUDENT_ID_1)  # Authorized update
        test_update_report(report_id, STUDENT_ID_2)  # Unauthorized update
        test_delete_report(report_id, STUDENT_ID_1)  # Authorized delete
        test_delete_report(report_id, STUDENT_ID_2)  # Unauthorized delete
    else:
        print("Failed to create a new report.")

if __name__ == "__main__":
    main()
