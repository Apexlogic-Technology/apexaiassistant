import frappe
from frappe.utils import add_days, today, getdate, add_months
import random

@frappe.whitelist()
def get_revenue_regression(chart_name=None, chart=None, filters=None):
    """
    Simulates or calculates a Revenue Regression Analysis (Predictive)
    Using basic dummy data that scales over the last 6 months + next 2 months predicted
    """
    labels = []
    historical = []
    predicted = []
    
    current = getdate(today())
    # 6 months back
    for i in range(-5, 1):
        month_date = add_months(current, i)
        labels.append(month_date.strftime("%b %y"))
        val = random.randint(50000, 150000)
        historical.append(val)
        predicted.append(None)
        
    last_val = historical[-1]
    
    # 2 months forward
    for i in range(1, 3):
        month_date = add_months(current, i)
        labels.append(month_date.strftime("%b %y (Predicted)"))
        historical.append(None)
        # Add 5-15% growth prediction
        val = int(last_val * (1 + random.uniform(0.05, 0.15)))
        predicted.append(val)
        last_val = val

    # Tie the historical line to prediction for seamless graph
    predicted[5] = historical[5]

    return {
        "labels": labels,
        "datasets": [
            {"name": "Actual Revenue", "values": historical},
            {"name": "Predicted Regression", "values": predicted}
        ]
    }

@frappe.whitelist()
def get_attrition_forecast(chart_name=None, chart=None, filters=None):
    """
    Simulates HR Attrition Forecasting based on recent departures
    """
    labels = ["Under 1 YR", "1-3 YRS", "3-5 YRS", "5+ YRS"]
    
    # Calculate base risk based on random logic to simulate AI processing
    risk_values = [
        random.randint(15, 30), # High risk for new hires
        random.randint(10, 20),
        random.randint(5, 15),
        random.randint(2, 8)    # Low risk for veterans
    ]

    return {
        "labels": labels,
        "datasets": [
            {"name": "Predicted Turnover Rate (%)", "values": risk_values}
        ]
    }

@frappe.whitelist()
def get_ai_token_usage(chart_name=None, chart=None, filters=None):
    """
    Actual analytics: Check the frappe error log or standard usage for AI Tokens
    For demonstration, we generate a smooth past-30-days curve
    """
    labels = []
    usage = []
    
    current = getdate(today())
    base_usage = random.randint(1000, 5000)
    
    for i in range(-14, 1):
        day_date = add_days(current, i)
        labels.append(day_date.strftime("%d %b"))
        
        # Add some random walk for realism
        change = random.randint(-500, 800)
        base_usage = max(0, base_usage + change)
        usage.append(base_usage)
        
    return {
        "labels": labels,
        "datasets": [
            {"name": "LLM Tokens Used", "values": usage}
        ]
    }
