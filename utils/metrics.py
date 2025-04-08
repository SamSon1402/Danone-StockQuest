import pandas as pd
import numpy as np
import random

def calculate_forecast_accuracy(predicted_values, actual_values):
    """Calculate forecast accuracy metrics"""
    if len(predicted_values) != len(actual_values):
        raise ValueError("Predicted and actual values must have the same length")
    
    # Mean Absolute Percentage Error (MAPE)
    mape = np.mean(np.abs((np.array(actual_values) - np.array(predicted_values)) / np.array(actual_values))) * 100
    
    # Accuracy is the inverse of MAPE
    accuracy = max(0, 100 - mape)
    
    # Calculate other metrics
    bias = np.mean(np.array(predicted_values) - np.array(actual_values))
    rmse = np.sqrt(np.mean((np.array(predicted_values) - np.array(actual_values))**2))
    
    return {
        'accuracy': round(accuracy, 1),
        'mape': round(mape, 1),
        'bias': round(bias, 1),
        'rmse': round(rmse, 1)
    }

def calculate_on_shelf_availability(inventory_df):
    """Calculate on-shelf availability from inventory data"""
    # In a real implementation, this would use actual inventory and demand data
    # For demo purposes, we'll simulate it
    
    # Count items with low stock
    low_stock_count = len(inventory_df[inventory_df['status'] == 'Low'])
    total_items = len(inventory_df)
    
    # Calculate OSA - formula is simplified for demo
    osa = 100 * (1 - (low_stock_count / total_items) * random.uniform(0.3, 0.7))
    
    return round(osa, 1)

def calculate_waste_reduction(baseline_df, optimized_df):
    """Calculate waste reduction percentage between baseline and optimized"""
    # In a real implementation, this would use actual waste data
    # For demo purposes, we'll generate random but realistic values
    
    # Simulated baseline and optimized waste
    baseline_waste = random.randint(1800, 2200)
    optimized_waste = random.randint(1100, 1500)
    
    # Calculate reduction
    waste_reduction = 100 * (baseline_waste - optimized_waste) / baseline_waste
    
    # Calculate financial impact (average cost per unit)
    unit_cost = random.uniform(15, 25)
    savings = (baseline_waste - optimized_waste) * unit_cost
    
    # Calculate environmental impact
    co2_per_unit = random.uniform(5, 15)
    co2_reduction = (baseline_waste - optimized_waste) * co2_per_unit / 1000  # in tons
    
    return {
        'percentage': round(waste_reduction, 1),
        'units_saved': baseline_waste - optimized_waste,
        'financial_savings': int(savings),
        'co2_reduction': round(co2_reduction, 1)
    }

def calculate_stock_turnover(sales_df, inventory_df):
    """Calculate stock turnover ratio"""
    # In a real implementation, this would use actual sales and inventory data
    # For demo purposes, we'll simulate it
    
    # Calculate average inventory
    avg_inventory = inventory_df['current_stock'].mean()
    
    # Calculate annual sales (simplified)
    annual_sales = sales_df['sales'].sum()
    
    # Stock turnover = Annual sales / Average inventory
    turnover = annual_sales / avg_inventory
    
    # Simulate change from previous period
    previous_turnover = turnover * random.uniform(0.9, 1.1)
    change_pct = 100 * (turnover - previous_turnover) / previous_turnover
    
    return {
        'turnover': round(turnover, 1),
        'change_pct': round(change_pct, 1)
    }

def calculate_priority_score(request_data):
    """Calculate priority score for country requests"""
    # Extract criteria values
    market_size = request_data.get('market_size', 5)
    growth_potential = request_data.get('growth_potential', 5)
    technical_feasibility = request_data.get('technical_feasibility', 5)
    strategic_alignment = request_data.get('strategic_alignment', 5)
    cost_estimate = request_data.get('cost_estimate', 5)
    
    # Calculate weighted score
    priority_score = (market_size * 2 + 
                      growth_potential * 3 + 
                      technical_feasibility * 1.5 + 
                      strategic_alignment * 2.5 - 
                      cost_estimate * 1.5)
    
    # Normalize to 0-100 scale
    priority_score = max(0, min(100, int(priority_score / 0.19)))
    
    # Determine priority level
    if priority_score >= 70:
        priority_level = 1  # High
    elif priority_score >= 40:
        priority_level = 2  # Medium
    else:
        priority_level = 3  # Low
    
    return {
        'score': priority_score,
        'level': priority_level
    }