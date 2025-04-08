import streamlit as st
import pandas as pd
import numpy as np
import random
import datetime
import plotly.graph_objects as go
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Danone StockQuest",
    page_icon="📊",
    layout="wide",
)

# ---- UI COMPONENTS ----

def add_custom_css():
    # Define Danone-inspired colors based on the image
    danone_blue = "#0056a3"
    danone_red = "#e63329"
    danone_light_blue = "#E9F5FF"
    danone_yellow = "#FFD700"
    
    # Add a slightly different light blue for the background
    background_light_blue = "#DCF0FF"
    
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono&display=swap');
        
        /* Global background color */
        .stApp {{
            background-color: {background_light_blue};
        }}
        
        /* Main container styling */
        .main .block-container {{
            background-color: {danone_light_blue};
            padding: 2rem;
            border: 4px solid {danone_blue};
            box-shadow: 8px 8px 0px 0px rgba(0,0,0,0.75);
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'VT323', monospace !important;
            color: {danone_blue} !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 3px 3px 0px rgba(0,0,0,0.2);
        }}
        
        h1 {{
            font-size: 4rem !important;
            border-bottom: 4px solid {danone_red};
            padding-bottom: 10px;
        }}
        
        h2 {{
            font-size: 2.5rem !important;
            border-left: 8px solid {danone_red};
            padding-left: 10px;
            margin-top: 20px !important;
        }}
        
        /* Paragraphs and text */
        p, li, div {{
            font-family: 'Space Mono', monospace !important;
        }}
        
        /* Sidebar */
        .css-1d391kg {{
            background-color: {danone_blue};
        }}
        
        .sidebar .sidebar-content {{
            background-color: {danone_blue} !important;
            color: white !important;
            border-right: 4px solid {danone_red};
        }}
        
        /* Widget labels in sidebar */
        .sidebar label, .sidebar .stRadio > div:first-child > label {{
            font-family: 'VT323', monospace !important;
            font-size: 1.2rem !important;
            color: white !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* Button styling */
        .stButton>button {{
            font-family: 'VT323', monospace !important;
            background-color: {danone_red} !important;
            color: white !important;
            border: 3px solid black !important;
            box-shadow: 4px 4px 0px 0px black;
            transition: all 0.1s ease;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 1.2rem !important;
            margin-top: 10px;
        }}
        
        .stButton>button:hover {{
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0px 0px black;
        }}
        
        .stButton>button:active {{
            transform: translate(4px, 4px);
            box-shadow: 0px 0px 0px 0px black;
        }}
        
        /* Slider styling */
        .stSlider div[data-baseweb="slider"] {{
            padding-top: 1rem;
        }}
        
        /* Expander styling */
        .streamlit-expander {{
            border: 3px solid {danone_blue} !important;
            background-color: white !important;
            box-shadow: 5px 5px 0px 0px rgba(0,0,0,0.5);
        }}
        
        .streamlit-expander .streamlit-expanderHeader {{
            font-family: 'VT323', monospace !important;
            font-size: 1.5rem !important;
            background-color: {danone_blue} !important;
            color: white !important;
        }}
        
        /* Success/Info message styling */
        .stSuccess, .stInfo, .stWarning, .stError {{
            font-family: 'Space Mono', monospace !important;
            border: 3px solid black !important;
            box-shadow: 5px 5px 0px 0px rgba(0,0,0,0.5);
        }}
        
        /* Pixel-style divider */
        .pixel-divider {{
            height: 5px;
            background: repeating-linear-gradient(to right, {danone_red} 0px, {danone_red} 10px, {danone_blue} 10px, {danone_blue} 20px);
            margin: 20px 0;
        }}
        
        /* Stat card styling */
        .stat-card {{
            background-color: white;
            border: 3px solid {danone_blue};
            box-shadow: 5px 5px 0px 0px rgba(0,0,0,0.5);
            padding: 15px;
            margin-bottom: 15px;
            transition: all 0.2s ease;
            text-align: center;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 5px 10px 0px 0px rgba(0,0,0,0.5);
        }}
        
        .stat-card h3 {{
            font-family: 'VT323', monospace !important;
            color: {danone_blue} !important;
            font-size: 1.5rem !important;
            margin-top: 5px !important;
            margin-bottom: 5px !important;
        }}
        
        .stat-value {{
            font-family: 'VT323', monospace !important;
            font-size: 2.5rem !important;
            color: {danone_blue};
            margin: 10px 0;
        }}
        
        .stat-change-positive {{
            color: #00AA00;
            font-weight: bold;
        }}
        
        .stat-change-negative {{
            color: #AA0000;
            font-weight: bold;
        }}
        
        /* Health stats bar styling */
        .health-stat {{
            margin-bottom: 10px;
        }}
        
        .health-stat-label {{
            font-family: 'VT323', monospace !important;
            font-size: 1.2rem;
            margin-bottom: 5px;
            display: flex;
            justify-content: space-between;
        }}
        
        .health-stat-bar {{
            height: 25px;
            background-color: #ddd;
            border: 2px solid black;
        }}
        
        .health-stat-fill {{
            height: 100%;
            background: repeating-linear-gradient(
                45deg,
                {danone_blue},
                {danone_blue} 10px,
                {danone_yellow} 10px,
                {danone_yellow} 20px
            );
        }}
        
        /* Priority badge styling */
        .priority-badge {{
            display: inline-block;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            text-align: center;
            line-height: 35px;
            font-family: 'VT323', monospace !important;
            font-size: 1.3rem;
            color: white;
            margin-right: 10px;
            font-weight: bold;
        }}
        
        .priority-high {{
            background-color: #AA0000;
            border: 2px solid black;
            box-shadow: 2px 2px 0px 0px rgba(0,0,0,0.5);
        }}
        
        .priority-medium {{
            background-color: #FFAA00;
            border: 2px solid black;
            box-shadow: 2px 2px 0px 0px rgba(0,0,0,0.5);
        }}
        
        .priority-low {{
            background-color: #00AA00;
            border: 2px solid black;
            box-shadow: 2px 2px 0px 0px rgba(0,0,0,0.5);
        }}
        
        /* Progress bar column */
        .progress-col {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }}
        
        .progress-label {{
            width: 120px;
            font-family: 'VT323', monospace !important;
            font-size: 1.1rem;
        }}
        
        .progress-bar-container {{
            flex-grow: 1;
            height: 25px;
            background-color: #ddd;
            border: 2px solid black;
            margin: 0 10px;
            position: relative;
        }}
        
        .progress-bar-fill {{
            height: 100%;
            background: repeating-linear-gradient(
                45deg,
                {danone_blue},
                {danone_blue} 10px,
                {danone_yellow} 10px,
                {danone_yellow} 20px
            );
            position: absolute;
            left: 0;
            top: 0;
        }}
        
        .progress-value {{
            width: 60px;
            text-align: right;
            font-family: 'Space Mono', monospace !important;
            font-weight: bold;
        }}
        
        /* Make sure text is readable with enhanced contrast */
        .stMarkdown {{
            color: #000000 !important;
        }}
        
        /* Dataframe/table styling */
        .dataframe-container {{
            border: 3px solid {danone_blue};
            box-shadow: 5px 5px 0px 0px rgba(0,0,0,0.5);
            margin: 20px 0;
            overflow: hidden;
        }}
        
        .dataframe-container th {{
            background-color: {danone_blue};
            color: white;
            font-family: 'VT323', monospace !important;
            font-size: 1.2rem;
            text-transform: uppercase;
            padding: 8px;
            text-align: center;
        }}
        
        .dataframe-container td {{
            font-family: 'Space Mono', monospace !important;
            padding: 8px;
            border: 1px solid #ddd;
            text-align: center;
        }}
        
        .dataframe-container tr:nth-child(even) {{
            background-color: {danone_light_blue};
        }}
        
        .dataframe-container tr:hover {{
            background-color: #d3e9ff;
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def pixel_divider():
    st.markdown('<div class="pixel-divider"></div>', unsafe_allow_html=True)

def display_health_stats(value, label, max_value=None):
    if max_value:
        percentage = min(100, max(0, (value / max_value) * 100))
        right_label = f"{value}/{max_value}"
    else:
        percentage = min(100, max(0, value))
        right_label = f"{value}%"
    
    html = f"""
    <div class="health-stat">
        <div class="health-stat-label">
            <span>{label}</span>
            <span>{right_label}</span>
        </div>
        <div class="health-stat-bar">
            <div class="health-stat-fill" style="width: {percentage}%;"></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def display_stat_card(title, value, change=None, icon=None):
    if change is not None:
        if change >= 0:
            change_html = f'<span class="stat-change-positive">▲ {change}%</span>'
        else:
            change_html = f'<span class="stat-change-negative">▼ {abs(change)}%</span>'
    else:
        change_html = ""
    
    icon_html = f"{icon} " if icon else ""
    
    html = f"""
    <div class="stat-card">
        <h3>{icon_html}{title}</h3>
        <div class="stat-value">{value}</div>
        {change_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def display_priority_item(priority, country, request, score):
    priority_class = "priority-high" if priority == 1 else "priority-medium" if priority == 2 else "priority-low"
    
    html = f"""
    <div style="background-color: white; border: 3px solid #0056a3; padding: 15px; margin-bottom: 15px; box-shadow: 5px 5px 0px 0px rgba(0,0,0,0.5);">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span class="priority-badge {priority_class}">{priority}</span>
            <h3 style="margin: 0;">{country}</h3>
        </div>
        <p style="margin-bottom: 10px;">{request}</p>
        <div class="health-stat">
            <div class="health-stat-label">
                <span>Priority Score</span>
                <span>{score}/100</span>
            </div>
            <div class="health-stat-bar">
                <div class="health-stat-fill" style="width: {score}%;"></div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def display_progress_bar(label, value, max_value):
    percentage = (value / max_value) * 100
    
    html = f"""
    <div class="progress-col">
        <div class="progress-label">{label}</div>
        <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width: {percentage}%;"></div>
        </div>
        <div class="progress-value">{value}/{max_value}</div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def display_customized_dataframe(df, height=None):
    # Convert DataFrame to HTML
    table_html = df.to_html(classes='table', index=False)
    
    # Apply custom styling
    styled_html = f"""
    <div class="dataframe-container" style="height: {height}px; overflow-y: auto;" >
        {table_html}
    </div>
    """
    
    st.markdown(styled_html, unsafe_allow_html=True)

# ---- MOCK DATA FUNCTIONS ----

def create_mock_sales_data():
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

def create_score_breakdown(country, request_type):
    # Create a radar chart of the score dimensions
    categories = ['Market Size', 'Growth Potential', 'Technical Feasibility', 
                 'Strategic Alignment', 'Cost Efficiency']
    
    # Generate "realistic" but random values based on country and request
    values = [
        random.randint(5, 10),  # Market Size
        random.randint(6, 9),   # Growth Potential
        random.randint(4, 9),   # Technical Feasibility
        random.randint(5, 10),  # Strategic Alignment
        random.randint(3, 8)    # Cost Efficiency (higher is better)
    ]
    
    # Create plotly radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=f'{country} - {request_type}',
        line=dict(color='#0056a3'),
        fillcolor='rgba(0, 86, 163, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="VT323, monospace",
            size=14,
            color="#0056a3"
        )
    )
    
    return fig

def create_forecast_scenario(product, trend=None):
    # Create date range for future 12 months
    start_date = datetime.datetime.now().date()
    future_date = start_date + datetime.timedelta(days=365)
    date_range = pd.date_range(start=start_date, end=future_date, freq='MS')  # Monthly
    
    # Set baseline based on product
    if 'Water' in product:
        baseline = 15000
        seasonality = 'summer'
    elif 'Yogurt' in product or 'Greek' in product:
        baseline = 12000
        seasonality = 'winter'
    else:
        baseline = 10000
        seasonality = 'balanced'
    
    # Create three scenarios
    baseline_data = []
    optimistic_data = []
    pessimistic_data = []
    
    # Apply trends if specified
    trend_factor = 1.0
    if trend == 'increasing':
        trend_growth = 0.03  # 3% monthly growth
    elif trend == 'decreasing':
        trend_growth = -0.02  # 2% monthly decline
    else:
        trend_growth = 0.005  # 0.5% growth (slight growth)
    
    for i, date in enumerate(date_range):
        month = date.month
        
        # Apply seasonality
        if seasonality == 'summer':
            # Peak in summer (June-August)
            seasonal_factor = 1 + 0.3 * np.sin(np.pi * (month - 3) / 6)
        elif seasonality == 'winter':
            # Peak in winter (December-February)
            seasonal_factor = 1 + 0.3 * np.sin(np.pi * (month - 9) / 6)
        else:
            # Milder seasonality
            seasonal_factor = 1 + 0.15 * np.sin(np.pi * month / 6)
        
        # Apply trend
        trend_factor *= (1 + trend_growth)
        
        # Calculate values for each scenario
        baseline_value = int(baseline * seasonal_factor * trend_factor)
        optimistic_value = int(baseline_value * (1 + 0.1 + 0.01 * i))  # Increasingly optimistic
        pessimistic_value = int(baseline_value * (1 - 0.08 - 0.005 * i))  # Increasingly pessimistic
        
        # Add to data lists
        baseline_data.append(baseline_value)
        optimistic_data.append(optimistic_value)
        pessimistic_data.append(pessimistic_value)
    
    # Create plot
    fig = go.Figure()
    
    # Add trace for each scenario
    fig.add_trace(go.Scatter(
        x=date_range, 
        y=baseline_data,
        mode='lines+markers',
        name='Baseline Forecast',
        line=dict(color='#0056a3', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=date_range, 
        y=optimistic_data,
        mode='lines+markers',
        name='Optimistic Scenario',
        line=dict(color='#00AA00', width=2, dash='dot'),
        marker=dict(size=7)
    ))
    
    fig.add_trace(go.Scatter(
        x=date_range, 
        y=pessimistic_data,
        mode='lines+markers',
        name='Pessimistic Scenario',
        line=dict(color='#AA0000', width=2, dash='dot'),
        marker=dict(size=7)
    ))
    
    # Customize layout
    fig.update_layout(
        title=f"{product} - 12 Month Forecast",
        title_font=dict(family="VT323, monospace", size=24),
        xaxis_title="Month",
        yaxis_title="Projected Sales Units",
        legend=dict(
            font=dict(family="Space Mono, monospace", size=10),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400,
        margin=dict(l=20, r=20, t=70, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Space Mono, monospace",
            size=12,
            color="#000000"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        )
    )
    
    return fig

def create_waste_reduction_chart():
    # Create monthly data points for a year
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Baseline waste (without optimization)
    baseline_waste = [380, 410, 395, 420, 450, 430, 
                     470, 460, 440, 410, 390, 420]
    
    # Optimized waste (with AI predictions)
    optimized_waste = [380, 370, 330, 300, 280, 250, 
                      240, 230, 210, 200, 190, 180]
    
    # Calculate savings
    savings = [baseline_waste[i] - optimized_waste[i] for i in range(len(months))]
    
    # Cumulative savings
    cumulative_savings = [sum(savings[:i+1]) for i in range(len(savings))]
    
    # Create plot
    fig = go.Figure()
    
    # Add both waste lines
    fig.add_trace(go.Scatter(
        x=months, 
        y=baseline_waste,
        mode='lines+markers',
        name='Baseline Waste',
        line=dict(color='#AA0000', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, 
        y=optimized_waste,
        mode='lines+markers',
        name='Optimized Waste',
        line=dict(color='#00AA00', width=3),
        marker=dict(size=8)
    ))
    
    # Add savings bar chart
    fig.add_trace(go.Bar(
        x=months,
        y=savings,
        name='Monthly Savings',
        marker_color='#0056a3',
        opacity=0.7,
        yaxis='y2'
    ))
    
    # Configure layout with two y-axes
    fig.update_layout(
        title="Waste Reduction Simulation",
        title_font=dict(family="VT323, monospace", size=24),
        xaxis_title="Month",
        yaxis=dict(
            title="Waste Units",
            titlefont=dict(color="#AA0000"),
            tickfont=dict(color="#AA0000")
        ),
        yaxis2=dict(
            title="Units Saved",
            titlefont=dict(color="#0056a3"),
            tickfont=dict(color="#0056a3"),
            anchor="x",
            overlaying="y",
            side="right"
        ),
        legend=dict(
            font=dict(family="Space Mono, monospace", size=10),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400,
        margin=dict(l=20, r=80, t=70, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Space Mono, monospace",
            size=12,
            color="#000000"
        ),
        bargap=0.15,
        barmode='group'
    )
    
    return fig

def create_heatmap_data():
    # Create a sample heatmap of country x product demand
    countries = [
        'France', 'Germany', 'UK', 'Spain', 'Italy', 
        'Netherlands', 'Belgium', 'Poland', 'Sweden'
    ]
    
    products = [
        'Activia Yogurt', 'Alpro Soya', 'Danone Greek', 'Evian Water', 
        'Actimel Probiotic', 'Volvic Water', 'Oykos Yogurt', 'Danette Dessert'
    ]
    
    # Create a matrix of demand values
    demand_values = []
    for country in countries:
        country_values = []
        for product in products:
            # Generate realistic but random values
            # Some countries prefer certain products
            if 'Water' in product and country in ['France', 'Italy', 'Spain']:
                base_value = random.randint(70, 100)
            elif 'Yogurt' in product and country in ['Germany', 'Poland', 'Sweden']:
                base_value = random.randint(70, 100)
            elif 'Soya' in product and country in ['UK', 'Netherlands', 'Belgium']:
                base_value = random.randint(70, 100)
            else:
                base_value = random.randint(30, 70)
            
            country_values.append(base_value)
        demand_values.append(country_values)
    
    # Create heatmap using plotly
    fig = go.Figure(data=go.Heatmap(
        z=demand_values,
        x=products,
        y=countries,
        colorscale=[
            [0, '#E9F5FF'],  # Light blue for low values
            [0.5, '#0056a3'],  # Medium blue for mid values
            [1, '#00254d']  # Dark blue for high values
        ],
        showscale=True,
        colorbar=dict(
            title="Demand Index",
            titleside="right",
            titlefont=dict(family="VT323, monospace", size=16),
            tickfont=dict(family="Space Mono, monospace", size=12),
        )
    ))
    
    fig.update_layout(
        title="Product Demand by Country",
        title_font=dict(family="VT323, monospace", size=24),
        xaxis=dict(
            title="Product",
            tickfont=dict(family="VT323, monospace", size=12),
            titlefont=dict(family="VT323, monospace", size=16),
        ),
        yaxis=dict(
            title="Country",
            tickfont=dict(family="VT323, monospace", size=12),
            titlefont=dict(family="VT323, monospace", size=16),
        ),
        height=500,
        margin=dict(l=50, r=50, t=70, b=70),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    for i, country in enumerate(countries):
        for j, product in enumerate(products):
            fig.add_annotation(
                x=product,
                y=country,
                text=str(demand_values[i][j]),
                showarrow=False,
                font=dict(
                    family="Space Mono, monospace",
                    size=10,
                    color="white" if demand_values[i][j] > 50 else "black"
                )
            )
    
    return fig

# ---- MAIN APP FUNCTION ----

def main():
    # Add custom CSS
    add_custom_css()
    
    # App header with retro styling
    st.markdown("<h1>DANONE STOCKQUEST</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.5rem; margin-bottom: 30px;'>AI-Driven Demand Forecasting & Waste Reduction 📊</p>", unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs([
        "🎮 DASHBOARD", 
        "🏆 COUNTRY PRIORITIZATION", 
        "📈 FORECAST SIMULATOR"
    ])
    
    with tab1:
        # Main dashboard with key metrics
        st.markdown("<h2>SUPPLY CHAIN COMMAND CENTER</h2>", unsafe_allow_html=True)
        
        # Key performance indicators
        st.markdown("<p>Current supply chain performance metrics:</p>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            display_stat_card("Forecast Accuracy", "92.4%", 3.5, "🎯")
        
        with col2:
            display_stat_card("On-Shelf Availability", "97.8%", 1.2, "🛒")
        
        with col3:
            display_stat_card("Waste Reduction", "32%", 8.5, "♻️")
        
        with col4:
            display_stat_card("Stock Turnover", "14.3", -2.1, "🔄")
        
        pixel_divider()
        
        # Supply status
        st.markdown("<h3>INVENTORY STATUS</h3>", unsafe_allow_html=True)
        
        inventory_df = create_mock_inventory_data()
        
        # Calculate stock status distribution
        stock_status = inventory_df['status'].value_counts().reset_index()
        stock_status.columns = ['Status', 'Count']
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.markdown("<h4>Stock Status Overview</h4>", unsafe_allow_html=True)
            
            # Create a pie chart
            fig = px.pie(
                stock_status, 
                values='Count', 
                names='Status',
                color='Status',
                color_discrete_map={
                    'Optimal': '#00AA00',
                    'Overstocked': '#FFAA00',
                    'Low': '#AA0000'
                },
                hole=0.4
            )
            
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(
                    font=dict(family="Space Mono, monospace", size=12),
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                font=dict(
                    family="Space Mono, monospace",
                    size=12,
                    color="#000000"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate expiry risk
            expiry_risk = inventory_df[inventory_df['expiry_risk'] > 30]
            
            st.markdown(f"<h4>High Expiry Risk Items: {len(expiry_risk)}</h4>", unsafe_allow_html=True)
            
            if not expiry_risk.empty:
                # Show top 5 highest risk items
                top_risk = expiry_risk.sort_values('expiry_risk', ascending=False).head(5)
                
                for _, item in top_risk.iterrows():
                    display_health_stats(
                        item['expiry_risk'], 
                        f"{item['product']} ({item['warehouse']})",
                    )
        
        with col2:
            st.markdown("<h4>Stock Levels by Warehouse</h4>", unsafe_allow_html=True)
            
            # Create a grouped bar chart of stock levels by warehouse
            warehouse_summary = inventory_df.groupby('warehouse').agg({
                'current_stock': 'sum',
                'max_capacity': 'sum'
            }).reset_index()
            
            # Calculate utilization percentage
            warehouse_summary['utilization'] = (warehouse_summary['current_stock'] / 
                                               warehouse_summary['max_capacity'] * 100).round(1)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=warehouse_summary['warehouse'],
                y=warehouse_summary['current_stock'],
                name='Current Stock',
                marker_color='#0056a3'
            ))
            
            fig.add_trace(go.Bar(
                x=warehouse_summary['warehouse'],
                y=warehouse_summary['max_capacity'],
                name='Maximum Capacity',
                marker_color='rgba(0, 86, 163, 0.3)',
                marker_line=dict(color='#0056a3', width=1)
            ))
            
            # Add utilization percentage as a line
            fig.add_trace(go.Scatter(
                x=warehouse_summary['warehouse'],
                y=warehouse_summary['utilization'],
                mode='lines+markers+text',
                name='Utilization %',
                yaxis='y2',
                text=warehouse_summary['utilization'].apply(lambda x: f"{x}%"),
                textposition="top center",
                line=dict(color='#e63329', width=2),
                marker=dict(size=8, color='#e63329')
            ))
            
            fig.update_layout(
                barmode='group',
                yaxis=dict(
                    title="Units",
                    titlefont=dict(color="#0056a3"),
                    tickfont=dict(color="#0056a3")
                ),
                yaxis2=dict(
                    title="Utilization %",
                    titlefont=dict(color="#e63329"),
                    tickfont=dict(color="#e63329"),
                    anchor="x",
                    overlaying="y",
                    side="right",
                    range=[0, 100]
                ),
                legend=dict(
                    font=dict(family="Space Mono, monospace", size=10),
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=20, r=70, t=20, b=70),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(
                    family="Space Mono, monospace",
                    size=12,
                    color="#000000"
                ),
                xaxis=dict(
                    title="",
                    tickangle=45,
                    tickfont=dict(size=10)
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        pixel_divider()
        
        # Waste reduction simulation
        st.markdown("<h3>WASTE REDUCTION SIMULATION</h3>", unsafe_allow_html=True)
        
        waste_fig = create_waste_reduction_chart()
        st.plotly_chart(waste_fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            display_stat_card("Total Waste Reduction", "2,350 units", None, "♻️")
        
        with col2:
            display_stat_card("Cost Savings", "€38,450", None, "💰")
        
        with col3:
            display_stat_card("CO₂ Reduction", "18.2 tons", None, "🌿")
    
    with tab2:
        # Country prioritization
        st.markdown("<h2>COUNTRY REQUEST PRIORITIZATION</h2>", unsafe_allow_html=True)
        
        # Create mock country requests data
        requests_df = create_mock_country_requests()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("<h3>TOP PRIORITY REQUESTS</h3>", unsafe_allow_html=True)
            
            # Display top 5 priority requests
            top_requests = requests_df.head(5)
            
            for _, request in top_requests.iterrows():
                display_priority_item(
                    request['priority'],
                    request['country'],
                    request['request_type'],
                    request['priority_score']
                )
        
        with col2:
            st.markdown("<h3>REQUEST STATS</h3>", unsafe_allow_html=True)
            
            # Count by priority
            priority_counts = requests_df['priority'].value_counts().sort_index()
            
            # Create simple bar chart
            fig = px.bar(
                x=["High", "Medium", "Low"],
                y=priority_counts.values,
                color=["High", "Medium", "Low"],
                color_discrete_map={
                    "High": "#AA0000",
                    "Medium": "#FFAA00",
                    "Low": "#00AA00"
                },
                labels={"x": "Priority Level", "y": "Count"}
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(
                    family="Space Mono, monospace",
                    size=12,
                    color="#000000"
                ),
                height=200
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Count by status
            status_counts = requests_df['status'].value_counts()
            
            # Create horizontal bars for status
            statuses = status_counts.index.tolist()
            counts = status_counts.values.tolist()
            
            for i, status in enumerate(statuses):
                display_progress_bar(status, counts[i], sum(counts))
            
            # Select country for detailed analysis
            st.markdown("<h3>PRIORITY SCORE ANALYSIS</h3>", unsafe_allow_html=True)
            
            selected_request = st.selectbox(
                "Select request for detailed analysis:",
                [f"{row['country']} - {row['request_type']}" for _, row in top_requests.iterrows()]
            )
            
            if selected_request:
                country, request_type = selected_request.split(" - ", 1)
                
                # Display radar chart for score breakdown
                score_fig = create_score_breakdown(country, request_type)
                st.plotly_chart(score_fig, use_container_width=True)
        
        pixel_divider()
        
        # Country-product heatmap
        st.markdown("<h3>PRODUCT DEMAND BY COUNTRY</h3>", unsafe_allow_html=True)
        
        heatmap_fig = create_heatmap_data()
        st.plotly_chart(heatmap_fig, use_container_width=True)
        
        with st.expander("View All Country Requests"):
            # Display full table with request status
            display_df = requests_df[['country', 'request_type', 'priority_score', 
                                     'submission_date', 'status']]
            display_df.columns = ['Country', 'Request Type', 'Priority Score', 
                                 'Submission Date', 'Status']
            
            display_customized_dataframe(display_df, height=400)
    
    with tab3:
        # Forecast simulator
        st.markdown("<h2>DEMAND FORECAST SIMULATOR</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("<h3>Simulation Controls</h3>", unsafe_allow_html=True)
            
            selected_product = st.selectbox(
                "Select Product:",
                [
                    'Activia Yogurt', 'Alpro Soya', 'Danone Greek', 
                    'Evian Water', 'Actimel Probiotic', 'Volvic Water'
                ]
            )
            
            selected_trend = st.radio(
                "Market Trend:",
                ["increasing", "steady", "decreasing"]
            )
            
            promotion_impact = st.slider(
                "Promotion Impact (%)",
                min_value=0,
                max_value=50,
                value=20,
                step=5
            )
            
            seasonality_strength = st.slider(
                "Seasonality Strength",
                min_value=1,
                max_value=10,
                value=5,
                step=1
            )
            
            run_simulation = st.button("RUN SIMULATION")
        
        with col2:
            st.markdown("<h3>12-Month Forecast</h3>", unsafe_allow_html=True)
            
            if run_simulation or selected_product:
                # Display loading message
                with st.spinner("Generating AI forecast..."):
                    import time
                    time.sleep(1)  # Simulate processing time
                
                # Create and display forecast
                forecast_fig = create_forecast_scenario(selected_product, selected_trend)
                st.plotly_chart(forecast_fig, use_container_width=True)
                
                # Summary of forecast
                if selected_trend == "increasing":
                    trend_text = "significant growth"
                    risk_level = "Low"
                    risk_color = "#00AA00"
                elif selected_trend == "decreasing":
                    trend_text = "declining demand"
                    risk_level = "High"
                    risk_color = "#AA0000"
                else:
                    trend_text = "steady demand"
                    risk_level = "Medium"
                    risk_color = "#FFAA00"
                
                st.markdown(f"""
                <div style="background-color: white; border: 3px solid #0056a3; padding: 15px; margin: 15px 0; box-shadow: 5px 5px 0px 0px rgba(0,0,0,0.5);">
                    <h4 style="margin-top: 0; font-family: 'VT323', monospace; color: #0056a3;">FORECAST SUMMARY</h4>
                    <p>The AI forecasting model predicts <strong>{trend_text}</strong> for {selected_product} over the next 12 months.</p>
                    <p>Risk of stockout: <span style="color: {risk_color}; font-weight: bold;">{risk_level}</span></p>
                    <p>Recommended safety stock: <strong>{random.randint(500, 2000)} units</strong></p>
                    <p>With optimized ordering based on this forecast, estimated waste reduction: <strong>{random.randint(15, 35)}%</strong></p>
                </div>
                """, unsafe_allow_html=True)
        
        pixel_divider()
        
        st.markdown("<h3>SCENARIO COMPARISON</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h4>Key Metrics</h4>", unsafe_allow_html=True)
            
            data = {
                'Metric': ['Total Sales Forecast', 'Peak Demand Month', 'Lowest Demand Month', 
                          'Stock Turnover Ratio', 'Required Storage Capacity'],
                'Baseline': ['142,500 units', 'July', 'January', '14.2', '12,000 units'],
                'Optimized': ['156,700 units', 'July', 'January', '15.7', '10,500 units']
            }
            
            metrics_df = pd.DataFrame(data)
            
            display_customized_dataframe(metrics_df)
            
            st.markdown("""
            <div style="background-color: white; border: 3px solid #0056a3; padding: 15px; margin-top: 15px; box-shadow: 5px 5px 0px 0px rgba(0,0,0,0.5);">
                <h4 style="margin-top: 0; font-family: 'VT323', monospace; color: #0056a3;">AI RECOMMENDATIONS</h4>
                <ul>
                    <li>Increase production capacity for summer months (May-August)</li>
                    <li>Implement dynamic pricing during peak demand periods</li>
                    <li>Reduce safety stock during low-demand months</li>
                    <li>Consider cross-regional inventory sharing to balance stock levels</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h4>Financial Impact</h4>", unsafe_allow_html=True)
            
            # Create financial impact chart
            categories = ['Revenue Impact', 'Waste Reduction', 'Inventory Holding', 
                         'Production Efficiency', 'Transportation']
            
            baseline = [0, 0, 0, 0, 0]  # Baseline is 0
            optimized = [9.5, 12.5, 8.0, 5.5, 3.0]  # Percentage improvements
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=categories,
                y=optimized,
                name='Optimized Scenario',
                marker_color='#0056a3'
            ))
            
            fig.update_layout(
                yaxis=dict(
                    title="Improvement (%)",
                    titlefont=dict(family="Space Mono, monospace", size=12),
                    tickfont=dict(family="Space Mono, monospace", size=10)
                ),
                xaxis=dict(
                    titlefont=dict(family="Space Mono, monospace", size=12),
                    tickfont=dict(family="Space Mono, monospace", size=10),
                    tickangle=45
                ),
                margin=dict(l=20, r=20, t=20, b=70),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(
                    family="Space Mono, monospace",
                    size=12,
                    color="#000000"
                ),
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div style="background-color: white; border: 3px solid #00AA00; padding: 15px; margin-top: 15px; box-shadow: 5px 5px 0px 0px rgba(0,0,0,0.5);">
                <h4 style="margin-top: 0; font-family: 'VT323', monospace; color: #00AA00;">TOTAL FINANCIAL BENEFIT</h4>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="margin: 5px 0;">Annual Cost Savings:</p>
                        <p style="margin: 5px 0;">Revenue Increase:</p>
                        <p style="margin: 5px 0;">Waste Reduction Value:</p>
                        <p style="margin: 5px 0;">CO₂ Reduction:</p>
                    </div>
                    <div style="text-align: right; font-weight: bold;">
                        <p style="margin: 5px 0;">€152,000</p>
                        <p style="margin: 5px 0;">€243,500</p>
                        <p style="margin: 5px 0;">€76,800</p>
                        <p style="margin: 5px 0;">24.5 tons</p>
                    </div>
                </div>
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #00AA00;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; font-family: 'VT323', monospace;">TOTAL VALUE:</h4>
                        <h4 style="margin: 0; font-family: 'VT323', monospace;">€472,300</h4>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer with simulation info
    st.markdown("""
    <div style="background-color: #0056a3; color: white; padding: 10px; border-radius: 5px; margin-top: 20px; font-family: 'Space Mono', monospace; font-size: 0.8rem; text-align: center;">
        DANONE STOCKQUEST v1.0 - AI Forecasting & Optimization Simulator | Data last updated: April 8, 2025
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()