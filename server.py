from flask import Flask, request, jsonify
import csv
from datetime import datetime

app = Flask(__name__)


def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        return None


def get_employees(database_filename, month, department, date_type):
    month_num = datetime.strptime(month, '%B').month
    employees = []
    with open(database_filename, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for record in reader:
            if parse_date(record[date_type]).month == month_num and record['Department'].lower() == department.lower():
                employees.append({
                    'id': record.get('id', len(employees) + 1),
                    'name': record['Name'],
                    'birthday': datetime.strptime(record[date_type], '%Y-%m-%d').strftime('%b %d') if date_type == 'Birthdate' else None,
                    'anniversary': datetime.strptime(record[date_type], '%Y-%m-%d').strftime('%b %d') if date_type == 'Hiring Date' else None
                    })
    return employees


@app.route('/birthdays')
def birthdays():
    month = request.args.get('month')
    department = request.args.get('department')
    employees = get_employees('database.csv', month, department, 'Birthdate')
    return jsonify({"total": len(employees), "employees": employees})


@app.route('/anniversaries')
def anniversaries():
    month = request.args.get('month')
    department = request.args.get('department')
    employees = get_employees('database.csv', month, department, 'Hiring Date')
    return jsonify({"total": len(employees), "employees": employees})


if __name__ == '__main__':
    app.run(debug=True)