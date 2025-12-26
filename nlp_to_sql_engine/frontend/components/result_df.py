import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import time
import matplotlib.pyplot as plt

def generate_ecommerce_visualizations(df, visualization_code=None):
    """
    Generate smart visualizations for e-commerce data
    Automatically detects query type and creates relevant charts
    """
    
    if df is None or len(df) == 0 or visualization_code is None:
        return
    
    # Get column names (lowercase for easier matching)
    cols = [col.lower() for col in df.columns]
    original_cols = df.columns.tolist()
    
    with st.expander("📊 View Visualizations", expanded=False):
        try:
            local_env = {
                "df": df,
                "pd": pd,
                "px": px,
                "go": go,
                "st": st,
                "plt": plt,
            }
            exec(visualization_code, {}, local_env)
        except Exception as e:
            st.error(f"❌ Error generating visualizations: {str(e)}")


def display_dataframe(df, visualization_code):
    """Display DataFrame with compact metrics and smart e-commerce visualizations"""
    
    # Compact one-line metrics
    st.markdown(
        f'<div style="display: flex; gap: 20px; margin-bottom: 12px; font-size: 0.9rem; color: #666;">'
        f'<span>📊 <strong>{len(df):,}</strong> rows</span>'
        f'<span>📋 <strong>{len(df.columns)}</strong> columns</span>'
        f'</div>',
        unsafe_allow_html=True)
    
    # Display DataFrame as-is
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=min(400, len(df) * 35 + 38)
    )
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="query_results.csv",
        mime="text/csv",
        key=f"download_{int(time.time() * 1000)}"
    )
    
    # Generate smart visualizations
    generate_ecommerce_visualizations(df, visualization_code)