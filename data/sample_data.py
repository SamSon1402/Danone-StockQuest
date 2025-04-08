import pandas as pd
import numpy as np
import random
import datetime

def create_mock_sales_data():
    """Generate mock sales data for demonstration purposes"""
    # Create date range for the past year
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=365)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Products
    products = [
        'Activia Yogurt', 'Alpro Soya', 'Danone Greek', 'Evian Water', 
        'Actimel Probiotic', 'Volvic Water', 'Oykos Yogurt', 'Danette Dessert'
    ]
    
    # Countries
    countries = [
        'France', 'Germany', 'UK', 'Spain', 'Italy', 
        'Netherlands', 'Belgium', 'Poland', 'Sweden'
    ]
    
    # Create dataframe structure
    data = []
    
    # Add seasonal patterns and trends
    for date in date_range:
        day_of_year = date.dayofyear
        month = date.month
        
        # Weekend effect
        weekend_factor = 0.8 if date.dayofweek >= 5 else 1.0
        
        # Seasonal factor (higher in summer for water, higher in winter for yogurt)
        season_factor = {}
        for product in products:
            if 'Water' in product:
                # Water sales peak in summer
                seasonal_component = np.sin(np.pi * day_of_year / 183) * 0.3 + 1
            elif 'Yogurt' in product or 'Greek' in product:
                # Yogurt sales higher in winter
                seasonal_component = -np.sin(np.pi * day_of_year / 183) * 0.25 + 1
            else:
                # Other products have milder seasonality
                seasonal_component = np.sin(np.pi * day_of_year / 183) * 0.15 + 1
            
            season_factor[product] = max(0.7, seasonal_component)
        
        # Special events/promotions (random spikes)
        for country in countries:
            for product in products:
                # Base sales (different by country and product)
                country_factor = 0.8 + 0.4 * (countries.index(country) / len(countries))
                product_popularity = 0.7 + 0.6 * (products.index(product) / len(products))
                
                base_sales = int(np.random.normal(500, 50) * country_factor * product_popularity)
                
                # Apply seasonal and weekend factors
                adjusted_sales = int(base_sales * season_factor[product] * weekend_factor)
                
                # Random promotions (sales spikes)
                if np.random.random() < 0.02:  # 2% chance of promotion
                    promotion_factor = np.random.uniform(1.5, 2.5)
                    adjusted_sales = int(adjusted_sales * promotion_factor)
                
                # Add some random noise
                final_sales = max(0, int(adjusted_sales * np.random.normal(1, 0.1)))
                
                # Add row to data
                data.append({
                    'date': date,
                    'country': country,
                    'product': product,
                    'sales': final_sales,
                    'year': date.year,
                    'month': date.month,
                    'day': date.day,
                    'dayofweek': date.dayofweek
                })
    
    # Convert to dataframe
    df = pd.DataFrame(data)
    
    return df

def create_mock_inventory_data():
    """Generate mock inventory data for demonstration purposes"""
    # Products
    products = [
        'Activia Yogurt', 'Alpro Soya', 'Danone Greek', 'Evian Water', 
        'Actimel Probiotic', 'Volvic Water', 'Oykos Yogurt', 'Danette Dessert'
    ]
    
    # Warehouses
    warehouses = [
        'Paris-North', 'Berlin-Central', 'London-East', 'Madrid-South', 
        'Rome-Central', 'Amsterdam-West', 'Brussels-Central', 'Warsaw-East'
    ]
    
    # Create dataframe structure
    data = []
    
    for warehouse in warehouses:
        for product in products:
            # Randomize inventory levels and capacities
            current_stock = random.randint(500, 10000)
            max_capacity = random.randint(max(current_stock, 8000), 15000)
            min_required = random.randint(300, 1000)
            
            # Determine stock status
            if current_stock < min_required:
                status = "Low"
            elif current_stock > 0.9 * max_capacity:
                status = "Overstocked"
            else:
                status = "Optimal"
            
            # Shelf life - different by product type
            if 'Yogurt' in product or 'Greek' in product:
                shelf_life_days = random.randint(14, 28)
            elif 'Water' in product:
                shelf_life_days = random.randint(180, 365)
            else:
                shelf_life_days = random.randint(30, 90)
            
            # Calculate expiry risk based on stock and shelf life
            expiry_risk = random.randint(0, 100) if shelf_life_days < 30 else random.randint(0, 20)
            
            data.append({
                'warehouse': warehouse,
                'product': product,
                'current_stock': current_stock,
                'max_capacity': max_capacity,
                'min_required': min_required,
                'status': status,
                'shelf_life_days': shelf_life_days,
                'expiry_risk': expiry_risk,
                'restock_days': random.randint(1, 7),
                'demand_trend': random.choice(["Increasing", "Steady", "Decreasing"])
            })
    
    # Convert to dataframe
    df = pd.DataFrame(data)
    
    return df

def create_mock_country_requests():
    """Generate mock country request data for prioritization"""
    countries = [
        'France', 'Germany', 'UK', 'Spain', 'Italy', 
        'Netherlands', 'Belgium', 'Poland', 'Sweden', 
        'Denmark', 'Finland', 'Greece', 'Portugal', 'Ireland'
    ]
    
    request_types = [
        "New product development for local market",
        "Packaging redesign for sustainability",
        "Increased production capacity",
        "Marketing campaign support",
        "Supply chain optimization",
        "Local sourcing initiative",
        "Flavor adaptation for local taste",
        "Reduced sugar reformulation",
        "Plant-based product line expansion",
        "Seasonal promotional SKUs",
        "On-the-go format development",
        "Family pack size introduction",
        "Organic certification process",
        "Distribution channel expansion"
    ]
    
    data = []
    
    # Create sample country requests with priority scores
    for i in range(30):  # 30 sample requests
        country = random.choice(countries)
        request = random.choice(request_types)
        
        # Calculate mock scores
        market_size = random.randint(1, 10)
        growth_potential = random.randint(1, 10)
        technical_feasibility = random.randint(1, 10)
        strategic_alignment = random.randint(1, 10)
        cost_estimate = random.randint(1, 10)
        
        # Calculate priority score (higher is higher priority)
        priority_score = (market_size * 2 + growth_potential * 3 + 
                         technical_feasibility * 1.5 + strategic_alignment * 2.5 - 
                         cost_estimate * 1.5)
        
        # Normalize to 0-100 scale
        priority_score = max(0, min(100, int(priority_score / 0.19)))
        
        # Assign priority level based on score
        if priority_score >= 70:
            priority = 1  # High
        elif priority_score >= 40:
            priority = 2  # Medium
        else:
            priority = 3  # Low
        
        # Add submission date (random date in past 3 months)
        days_ago = random.randint(1, 90)
        submission_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        
        data.append({
            'country': country,
            'request_type': request,
            'priority_score': priority_score,
            'priority': priority,
            'market_size': market_size,
            'growth_potential': growth_potential,
            'technical_feasibility': technical_feasibility,
            'strategic_alignment': strategic_alignment,
            'cost_estimate': cost_estimate,
            'submission_date': submission_date.strftime('%Y-%m-%d'),
            'status': random.choice(['New', 'In Review', 'Approved', 'In Progress', 'Completed', 'On Hold'])
        })
    
    return pd.DataFrame(data).sort_values(by='priority_score', ascending=False)