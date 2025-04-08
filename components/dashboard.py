import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.styling import display_stat_card, display_health_stats, pixel_divider
from utils.charts import create_waste_reduction_chart

def render_dashboard_tab():
    """Render the Supply Chain Command Center dashboard tab"""
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
    
    # Get inventory data
    from data.sample_data import create_mock_inventory_data
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