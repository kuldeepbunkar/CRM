from flask import Blueprint, render_template, request, redirect, url_for
from src.crm import CRM
import logging

web = Blueprint('web', __name__)
crm = CRM()

@web.route('/')
def dashboard():
    properties = crm.get_active_properties()
    recent_leads = crm.get_recent_leads()
    pending_tasks = crm.get_pending_tasks()
    return render_template('dashboard.html', 
                         properties=properties,
                         leads=recent_leads,
                         tasks=pending_tasks)

@web.route('/properties')
def properties():
    try:
        properties = crm.get_active_properties()
        return render_template('properties/index.html', properties=properties)
    except Exception as e:
        logging.error(f"Error fetching properties: {str(e)}")
        return render_template('errors/500.html'), 500

@web.route('/leads')
def leads():
    leads = crm.get_all_leads()
    return render_template('leads/index.html', leads=leads)

@web.route('/about')
def about():
    return render_template('about.html') 