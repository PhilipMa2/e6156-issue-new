from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# Database Configuration using SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ZLY0802kk.@35.193.93.151/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)

# Database Model
class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.String)
    description = db.Column(db.String)

# Ensure the table exists
with app.app_context():
    db.create_all()

# Request Parsing
parser = reqparse.RequestParser()
parser.add_argument('issue', type=str, required=True, help='Issue cannot be blank')
parser.add_argument('description', type=str, required=True, help='Description cannot be blank')

# API Resource Classes
class ReportResource(Resource):
    def get(self, report_id):
        report = Report.query.get(report_id)
        if report:
            return jsonify({'id': report.id, 'issue': report.issue, 'description': report.description})
        return {'message': 'Report not found'}, 404

    def delete(self, report_id):
        report = Report.query.get(report_id)
        if report:
            db.session.delete(report)
            db.session.commit()
            return {'message': 'Report deleted'}
        return {'message': 'Report not found'}, 404

    def put(self, report_id):
        args = parser.parse_args()
        report = Report.query.get(report_id)
        if report:
            report.issue = args['issue']
            report.description = args['description']
            db.session.commit()
            return {'message': 'Report updated'}
        return {'message': 'Report not found'}, 404

class ReportsResource(Resource):
    def get(self):
        reports = Report.query.all()
        return jsonify([{'id': report.id, 'issue': report.issue, 'description': report.description} for report in reports])

    def post(self):
        args = parser.parse_args()
        new_report = Report(issue=args['issue'], description=args['description'])
        db.session.add(new_report)
        db.session.commit()

        # Send email via AWS API after inserting the report
        api_url = "https://15fhhhmf86.execute-api.us-east-1.amazonaws.com/default/test_gcp"
        try:
            response = requests.post(api_url, json={})
            if response.status_code == 200:
                print("Email sent successfully")
            else:
                print("Failed to send email")
        except requests.exceptions.RequestException as e:
            print(f"Error sending email: {e}")

        return {'message': 'Report added', 'id': new_report.id}, 201

# API Endpoints
api.add_resource(ReportResource, '/reports/<int:report_id>')
api.add_resource(ReportsResource, '/reports')

# App Initialization
if __name__ == '__main__':
    app.run(debug=True)
