import streamlit as st
import pandas as pd
import time

from utils.styling import pixel_divider
from utils.charts import create_forecast_scenario

def render_forecasting_tab():
    """Render the Demand Forecast Simulator tab"""
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
            
            import random
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
        
        from utils.styling import display_customized_dataframe
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
        import plotly.graph_objects as go
        
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