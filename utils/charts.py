import plotly.graph_objects as go
import plotly.express as px
import datetime
import random
import numpy as np

def create_waste_reduction_chart():
    """Create a waste reduction simulation chart"""
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

def create_score_breakdown(country, request_type):
    """Create a radar chart of the priority score dimensions"""
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
    """Create a forecast scenario chart with multiple scenarios"""
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

def create_heatmap_data():
    """Create a heatmap of country x product demand"""
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