import streamlit as st
import pandas as pd

from utils.styling import display_priority_item, pixel_divider, display_progress_bar, display_customized_dataframe
from utils.charts import create_score_breakdown, create_heatmap_data
from data.sample_data import create_mock_country_requests

def render_prioritization_tab():
    """Render the Country Request Prioritization tab"""
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
        import plotly.express as px
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