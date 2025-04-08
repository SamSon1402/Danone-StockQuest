import streamlit as st

def add_custom_css():
    """Add retro gaming CSS styling to the app"""
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
    """Display a pixel-style divider"""
    st.markdown('<div class="pixel-divider"></div>', unsafe_allow_html=True)

def display_health_stats(value, label, max_value=None):
    """Display a health-stat style bar"""
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
    """Display a stat card with optional change indicator"""
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
    """Display a priority item card with badge"""
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
    """Display a horizontal progress bar with label and value"""
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
    """Display a dataframe with custom styling"""
    # Convert DataFrame to HTML
    table_html = df.to_html(classes='table', index=False)
    
    # Apply custom styling
    styled_html = f"""
    <div class="dataframe-container" style="height: {height}px; overflow-y: auto;" >
        {table_html}
    </div>
    """
    
    st.markdown(styled_html, unsafe_allow_html=True)