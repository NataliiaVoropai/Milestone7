import requests
import sys

valid_months = ["january", "february", "march", "april", "may", "june", "july",
                "august", "september", "october", "november", "december"]
valid_departments = ["engineering", "hr", "finance", "r&d", "marketing",
                     "management", "tech support"]


def normalize_validate_args(month, department):
    month_ = month.lower()
    department_ = department.lower()
    if month_ not in valid_months:
        print(f'Error: "{month}" is not a valid month. Please enter '
              'a correct month.')
        sys.exit(1)
    if department_ not in valid_departments:
        print(f'Error: "{department}" is not a valid department. Please check '
              'spelling')
        sys.exit(1)
    return month_, department_
        

def fetch_report(month, department):
    base_url = 'http://127.0.0.1:5000'
    endpoints = ['/birthdays', '/anniversaries']
    for endpoint in endpoints:
        url = f'{base_url}{endpoint}?month={month}&department={department}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print_report(data, department, month, endpoint.strip('/'))
        else:
            print(f'Failed to fetch data from {endpoint}. Status code: {response.status_code}')


def print_report(data, department, month, report_type):
    print(f'{report_type.title()} report for {department} for {month} fetched')
    print(f'Total: {data['total']}')
    if int(data['total']) > 0:
        print('Employees:')
        for employee in data['employees']:
            date = employee['birthday'] if report_type == 'birthdays' else employee['anniversary']
            print(f" --{date} - {employee['name']}")
    else:
        return None


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python fetch_report.py <month> <department>")
        sys.exit(1)
    month, department = normalize_validate_args(sys.argv[1], sys.argv[2])
    fetch_report(month, department)