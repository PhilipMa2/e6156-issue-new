import requests

# Base URL of your Flask API
BASE_URL = "http://127.0.0.1:5000"

def test_create_report():
    print("Testing: Create Report")
    response = requests.post(f"{BASE_URL}/reports", json={"issue": "Test Issue", "description": "Test Description"})
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    return response.json()

def test_get_report(report_id):
    print("\nTesting: Get Report")
    response = requests.get(f"{BASE_URL}/reports/{report_id}")
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_update_report(report_id):
    print("\nTesting: Update Report")
    response = requests.put(f"{BASE_URL}/reports/{report_id}", json={"issue": "Updated Issue", "description": "Updated Description"})
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_delete_report(report_id):
    print("\nTesting: Delete Report")
    response = requests.delete(f"{BASE_URL}/reports/{report_id}")
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def main():
    # Create a new report and get its ID
    new_report = test_create_report()
    report_id = new_report.get('id')

    # Test get, update, and delete operations
    if report_id:
        test_get_report(report_id)
        test_update_report(report_id)
        test_delete_report(report_id)
    else:
        print("Failed to create a new report.")

if __name__ == "__main__":
    main()
