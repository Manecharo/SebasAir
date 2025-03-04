from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
import os

from ..config.db import get_db
from ..services import report_service

router = APIRouter(
    prefix="/api/reports",
    tags=["reports"],
    responses={404: {"description": "Not found"}},
)

@router.get("/daily")
def get_daily_report(
    db: Session = Depends(get_db),
    date: Optional[str] = None
):
    """
    Generate a daily report for a specific date.
    If no date is provided, generates a report for yesterday.
    """
    try:
        if date:
            report_date = datetime.strptime(date, "%Y-%m-%d").date()
        else:
            report_date = (datetime.utcnow() - timedelta(days=1)).date()
        
        report = report_service.generate_daily_report(db, report_date)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating daily report: {str(e)}")

@router.get("/weekly")
def get_weekly_report(
    db: Session = Depends(get_db),
    end_date: Optional[str] = None
):
    """
    Generate a weekly report ending on a specific date.
    If no date is provided, generates a report for the last week.
    """
    try:
        if end_date:
            report_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            report_end_date = (datetime.utcnow() - timedelta(days=1)).date()
        
        report = report_service.generate_weekly_report(db, report_end_date)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating weekly report: {str(e)}")

@router.get("/export/json")
def export_report_to_json(
    db: Session = Depends(get_db),
    report_type: str = Query(..., description="Type of report: 'daily' or 'weekly'"),
    date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Export a report to JSON format.
    """
    try:
        if report_type == "daily":
            if date:
                report_date = datetime.strptime(date, "%Y-%m-%d").date()
            else:
                report_date = (datetime.utcnow() - timedelta(days=1)).date()
            
            report = report_service.generate_daily_report(db, report_date)
        elif report_type == "weekly":
            if end_date:
                report_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            else:
                report_end_date = (datetime.utcnow() - timedelta(days=1)).date()
            
            report = report_service.generate_weekly_report(db, report_end_date)
        else:
            raise HTTPException(status_code=400, detail="Invalid report type. Must be 'daily' or 'weekly'")
        
        # Create reports directory if it doesn't exist
        os.makedirs("reports", exist_ok=True)
        
        # Generate filename
        if report_type == "daily":
            filename = f"reports/daily_report_{report['date']}.json"
        else:
            filename = f"reports/weekly_report_{report['start_date']}_to_{report['end_date']}.json"
        
        # Export report
        report_service.export_report_to_json(report, filename)
        
        return {"message": "Report exported successfully", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting report to JSON: {str(e)}")

@router.get("/export/csv")
def export_report_to_csv(
    db: Session = Depends(get_db),
    report_type: str = Query(..., description="Type of report: 'daily' or 'weekly'"),
    date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Export a report to CSV format.
    """
    try:
        if report_type == "daily":
            if date:
                report_date = datetime.strptime(date, "%Y-%m-%d").date()
            else:
                report_date = (datetime.utcnow() - timedelta(days=1)).date()
            
            report = report_service.generate_daily_report(db, report_date)
        elif report_type == "weekly":
            if end_date:
                report_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            else:
                report_end_date = (datetime.utcnow() - timedelta(days=1)).date()
            
            report = report_service.generate_weekly_report(db, report_end_date)
        else:
            raise HTTPException(status_code=400, detail="Invalid report type. Must be 'daily' or 'weekly'")
        
        # Create reports directory if it doesn't exist
        os.makedirs("reports", exist_ok=True)
        
        # Generate filename
        if report_type == "daily":
            filename = f"reports/daily_report_{report['date']}.csv"
        else:
            filename = f"reports/weekly_report_{report['start_date']}_to_{report['end_date']}.csv"
        
        # Export report
        report_service.export_report_to_csv(report, filename)
        
        return {"message": "Report exported successfully", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting report to CSV: {str(e)}") 