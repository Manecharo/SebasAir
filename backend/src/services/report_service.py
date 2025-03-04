from datetime import datetime, timedelta
from typing import Dict
from sqlalchemy.orm import Session
import pandas as pd
import json

from ..models.flight import Flight
from ..models.schedule import Schedule
from ..models.competitor import CompetitorFlight
from ..models.alert import Alert


def generate_daily_report(db: Session, date: datetime = None):
    """
    Generate a daily report for a specific date.
    If no date is provided, generates a report for yesterday.
    """
    if date is None:
        # Default to yesterday
        date = (datetime.utcnow() - timedelta(days=1)).date()
    
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())
    
    # Get all flights for the day
    flights = db.query(Flight).filter(
        Flight.scheduled_departure >= start_of_day,
        Flight.scheduled_departure <= end_of_day
    ).all()
    
    # Get all scheduled flights for the day
    scheduled = db.query(Schedule).filter(
        Schedule.scheduled_departure >= start_of_day,
        Schedule.scheduled_departure <= end_of_day
    ).all()
    
    # Get all competitor flights for the day
    competitor_flights = db.query(CompetitorFlight).filter(
        CompetitorFlight.departure_time >= start_of_day,
        CompetitorFlight.departure_time <= end_of_day
    ).all()
    
    # Get all alerts for the day
    alerts = db.query(Alert).filter(
        Alert.created_at >= start_of_day,
        Alert.created_at <= end_of_day
    ).all()
    
    # Calculate statistics
    total_flights = len(flights)
    completed_flights = sum(1 for f in flights if f.status == 'arrived')
    delayed_flights = sum(1 for f in flights if f.actual_departure and f.scheduled_departure and 
                         (f.actual_departure - f.scheduled_departure).total_seconds() > 15 * 60)  # > 15 minutes
    
    on_time_percentage = (completed_flights - delayed_flights) / completed_flights * 100 if completed_flights > 0 else 0
    
    # Calculate average delay
    total_delay_minutes = 0
    delay_count = 0
    for flight in flights:
        if flight.actual_departure and flight.scheduled_departure:
            delay_minutes = (flight.actual_departure - flight.scheduled_departure).total_seconds() / 60
            if delay_minutes > 0:
                total_delay_minutes += delay_minutes
                delay_count += 1
    
    avg_delay = total_delay_minutes / delay_count if delay_count > 0 else 0
    
    # Competitor statistics
    competitor_stats = {}
    for flight in competitor_flights:
        if flight.operator not in competitor_stats:
            competitor_stats[flight.operator] = {
                'total': 0,
                'completed': 0
            }
        
        competitor_stats[flight.operator]['total'] += 1
        if flight.status.lower() == 'completed':
            competitor_stats[flight.operator]['completed'] += 1
    
    # Compile the report
    report = {
        'date': date.strftime('%Y-%m-%d'),
        'total_flights': total_flights,
        'completed_flights': completed_flights,
        'delayed_flights': delayed_flights,
        'on_time_percentage': round(on_time_percentage, 2),
        'average_delay_minutes': round(avg_delay, 2),
        'total_alerts': len(alerts),
        'competitor_stats': competitor_stats
    }
    
    return report

def generate_weekly_report(db: Session, end_date: datetime = None):
    """
    Generate a weekly report ending on a specific date.
    If no date is provided, generates a report for the last week.
    """
    if end_date is None:
        # Default to yesterday
        end_date = (datetime.utcnow() - timedelta(days=1)).date()
    
    start_date = end_date - timedelta(days=6)  # 7 days including end_date
    
    # Generate daily reports for each day in the week
    daily_reports = []
    current_date = start_date
    while current_date <= end_date:
        daily_report = generate_daily_report(db, current_date)
        daily_reports.append(daily_report)
        current_date += timedelta(days=1)
    
    # Compile weekly statistics
    total_flights = sum(report['total_flights'] for report in daily_reports)
    completed_flights = sum(report['completed_flights'] for report in daily_reports)
    delayed_flights = sum(report['delayed_flights'] for report in daily_reports)
    
    on_time_percentage = (completed_flights - delayed_flights) / completed_flights * 100 if completed_flights > 0 else 0
    
    # Calculate average delay across all days
    total_delay_minutes = sum(report['average_delay_minutes'] * report['delayed_flights'] 
                             for report in daily_reports if report['delayed_flights'] > 0)
    total_delayed = sum(report['delayed_flights'] for report in daily_reports)
    avg_delay = total_delay_minutes / total_delayed if total_delayed > 0 else 0
    
    # Compile the weekly report
    weekly_report = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'total_flights': total_flights,
        'completed_flights': completed_flights,
        'delayed_flights': delayed_flights,
        'on_time_percentage': round(on_time_percentage, 2),
        'average_delay_minutes': round(avg_delay, 2),
        'daily_reports': daily_reports
    }
    
    return weekly_report

def export_report_to_json(report, filename=None):
    """
    Export a report to a JSON file.
    If no filename is provided, generates a default filename based on the report type and date.
    """
    if filename is None:
        if 'date' in report:
            # Daily report
            filename = f"daily_report_{report['date']}.json"
        else:
            # Weekly report
            filename = f"weekly_report_{report['start_date']}_to_{report['end_date']}.json"
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=4)
    
    return filename

def export_report_to_csv(report, filename=None):
    """
    Export a report to a CSV file.
    If no filename is provided, generates a default filename based on the report type and date.
    """
    if filename is None:
        if 'date' in report:
            # Daily report
            filename = f"daily_report_{report['date']}.csv"
        else:
            # Weekly report
            filename = f"weekly_report_{report['start_date']}_to_{report['end_date']}.csv"
    
    # Convert the report to a pandas DataFrame
    if 'daily_reports' in report:
        # Weekly report - flatten the daily reports
        df = pd.DataFrame(report['daily_reports'])
    else:
        # Daily report
        df = pd.DataFrame([report])
    
    # Export to CSV
    df.to_csv(filename, index=False)
    
    return filename
