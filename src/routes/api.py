from flask import Blueprint, jsonify, request
from src.crm import CRM
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

api = Blueprint('api', __name__)
crm = CRM()

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@api.route('/properties', methods=['GET'])
@limiter.limit("30 per minute")
def get_properties():
    properties = crm.get_active_properties()
    return jsonify(properties)

@api.route('/leads', methods=['POST'])
def create_lead():
    data = request.json
    lead = crm.add_lead(
        name=data['name'],
        email=data['email'],
        source=data['source']
    )
    return jsonify(lead), 201 

@api.route('/properties/<int:id>', methods=['PUT'])
def update_property(id):
    data = request.json
    property = crm.update_property(id, data)
    return jsonify(property)

@api.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = crm.get_pending_tasks()
    return jsonify(tasks)

@api.route('/analytics/sales', methods=['GET'])
def sales_analytics():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    analytics = crm.get_sales_metrics(start_date, end_date)
    return jsonify(analytics) 