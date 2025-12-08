import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import time

def generate_ecommerce_visualizations(df):
    """
    Generate smart visualizations for e-commerce data
    Automatically detects query type and creates relevant charts
    """
    
    if df is None or len(df) == 0:
        return
    
    # Get column names (lowercase for easier matching)
    cols = [col.lower() for col in df.columns]
    original_cols = df.columns.tolist()
    
    with st.expander("📊 View Visualizations", expanded=False):
        charts_created = 0
        
        # ============================================
        # 1. GEOGRAPHIC ANALYSIS (State/City Distribution)
        # ============================================
        state_cols = [c for c in original_cols if 'state' in c.lower()]
        city_cols = [c for c in original_cols if 'city' in c.lower()]
        
        if state_cols:
            state_col = state_cols[0]
            # Check if we have a count/numeric column
            numeric_cols = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
            
            if len(numeric_cols) > 0:
                # State with aggregated metric (e.g., total sales by state)
                num_col = numeric_cols[0]
                st.markdown(f"#### 🗺️ {num_col.replace('_', ' ').title()} by State")
                
                # Aggregate data by state
                state_data = df.groupby(state_col)[num_col].sum().reset_index()
                state_data = state_data.sort_values(num_col, ascending=False).head(15)
                
                fig = px.bar(
                    state_data,
                    x=state_col,
                    y=num_col,
                    color=num_col,
                    color_continuous_scale='Viridis',
                    text=num_col
                )
                fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                fig.update_layout(
                    xaxis_title='State',
                    yaxis_title=num_col.replace('_', ' ').title(),
                    showlegend=False,
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
                charts_created += 1
            else:
                # Just state distribution (count)
                st.markdown(f"#### 🗺️ Distribution by State")
                state_counts = df[state_col].value_counts().head(15)
                
                fig = px.bar(
                    x=state_counts.index,
                    y=state_counts.values,
                    labels={'x': 'State', 'y': 'Count'},
                    color=state_counts.values,
                    color_continuous_scale='Blues'
                )
                fig.update_traces(text=state_counts.values, textposition='outside')
                fig.update_layout(showlegend=False, height=450)
                st.plotly_chart(fig, use_container_width=True)
                charts_created += 1
        
        # ============================================
        # 2. PRICE/VALUE ANALYSIS
        # ============================================
        price_cols = [c for c in original_cols if any(x in c.lower() for x in ['price', 'value', 'payment', 'freight'])]
        
        if price_cols and len(df) <= 100:
            price_col = price_cols[0]
            
            # Price distribution histogram
            st.markdown(f"#### 💰 {price_col.replace('_', ' ').title()} Distribution")
            
            # Convert to numeric if needed
            try:
                df_price = pd.to_numeric(df[price_col], errors='coerce')
                df_price = df_price.dropna()
                
                fig = px.histogram(
                    df_price,
                    nbins=30,
                    labels={'value': price_col.replace('_', ' ').title(), 'count': 'Frequency'},
                    color_discrete_sequence=['#00CC96']
                )
                fig.update_layout(
                    xaxis_title=price_col.replace('_', ' ').title(),
                    yaxis_title='Count',
                    showlegend=False,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                charts_created += 1
                
                # Box plot for price outliers
                if len(df_price) > 10:
                    st.markdown(f"#### 📦 {price_col.replace('_', ' ').title()} Range & Outliers")
                    fig = px.box(
                        df_price,
                        y=df_price.values,
                        labels={'y': price_col.replace('_', ' ').title()},
                        color_discrete_sequence=['#AB63FA']
                    )
                    fig.update_layout(showlegend=False, height=350)
                    st.plotly_chart(fig, use_container_width=True)
                    charts_created += 1
            except:
                pass
        
        # ============================================
        # 3. PRODUCT CATEGORY ANALYSIS
        # ============================================
        category_cols = [c for c in original_cols if 'category' in c.lower()]
        
        if category_cols:
            cat_col = category_cols[0]
            cat_counts = df[cat_col].value_counts().head(10)
            
            if len(cat_counts) > 1:
                st.markdown(f"#### 📦 Top Product Categories")
                
                fig = px.pie(
                    values=cat_counts.values,
                    names=cat_counts.index,
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}'
                )
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
                charts_created += 1
        
        # ============================================
        # 4. REVIEW SCORE ANALYSIS
        # ============================================
        review_cols = [c for c in original_cols if 'review' in c.lower() and 'score' in c.lower()]
        
        if review_cols:
            review_col = review_cols[0]
            
            try:
                df_review = pd.to_numeric(df[review_col], errors='coerce')
                df_review = df_review.dropna()
                review_counts = df_review.value_counts().sort_index()
                
                st.markdown(f"#### ⭐ Review Score Distribution")
                
                colors = ['#FF6B6B', '#FFA07A', '#FFD93D', '#6BCB77', '#4D96FF']
                fig = go.Figure(data=[
                    go.Bar(
                        x=review_counts.index,
                        y=review_counts.values,
                        marker_color=colors[:len(review_counts)],
                        text=review_counts.values,
                        textposition='outside'
                    )
                ])
                fig.update_layout(
                    xaxis_title='Review Score',
                    yaxis_title='Count',
                    showlegend=False,
                    height=400,
                    xaxis=dict(tickmode='linear')
                )
                st.plotly_chart(fig, use_container_width=True)
                charts_created += 1
                
                # Average review score metric
                avg_score = df_review.mean()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("⭐ Average Score", f"{avg_score:.2f}")
                with col2:
                    st.metric("🔢 Total Reviews", len(df_review))
                with col3:
                    good_reviews = len(df_review[df_review >= 4])
                    st.metric("👍 Good Reviews (4-5)", f"{good_reviews} ({good_reviews/len(df_review)*100:.1f}%)")
                    
            except:
                pass
        
        # ============================================
        # 5. ORDER STATUS ANALYSIS
        # ============================================
        status_cols = [c for c in original_cols if 'status' in c.lower()]
        
        if status_cols:
            status_col = status_cols[0]
            status_counts = df[status_col].value_counts()
            
            st.markdown(f"#### 📊 Order Status Breakdown")
            
            fig = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                labels={'x': 'Status', 'y': 'Count'},
                color=status_counts.values,
                color_continuous_scale='Teal',
                text=status_counts.values
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
            charts_created += 1
        
        # ============================================
        # 6. PAYMENT TYPE ANALYSIS
        # ============================================
        payment_cols = [c for c in original_cols if 'payment' in c.lower() and 'type' in c.lower()]
        
        if payment_cols:
            payment_col = payment_cols[0]
            payment_counts = df[payment_col].value_counts()
            
            st.markdown(f"#### 💳 Payment Method Distribution")
            
            fig = px.pie(
                values=payment_counts.values,
                names=payment_counts.index,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            charts_created += 1
        
        # ============================================
        # 7. TIME-BASED ANALYSIS
        # ============================================
        date_cols = [c for c in original_cols if any(x in c.lower() for x in ['date', 'timestamp']) 
                     and 'last_processed' not in c.lower()]
        
        if date_cols and len(df) > 5:
            date_col = date_cols[0]
            
            try:
                df_copy = df.copy()
                df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
                df_copy = df_copy.dropna(subset=[date_col])
                
                if len(df_copy) > 0:
                    # Time series of order volume
                    df_copy['date_only'] = df_copy[date_col].dt.date
                    daily_counts = df_copy.groupby('date_only').size().reset_index(name='count')
                    
                    st.markdown(f"#### 📅 Trend Over Time")
                    
                    fig = px.line(
                        daily_counts,
                        x='date_only',
                        y='count',
                        markers=True,
                        labels={'date_only': 'Date', 'count': 'Count'}
                    )
                    fig.update_traces(line_color='#636EFA', line_width=3)
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    charts_created += 1
            except:
                pass
        
        # ============================================
        # 8. TOP N ANALYSIS (Products, Sellers, Customers)
        # ============================================
        id_cols = [c for c in original_cols if 'id' in c.lower()]
        numeric_cols = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
        
        if len(id_cols) > 0 and len(numeric_cols) > 0 and len(df) <= 50:
            id_col = id_cols[0]
            num_col = numeric_cols[0]
            
            # Top performers
            entity_name = id_col.replace('_id', '').replace('_', ' ').title()
            st.markdown(f"#### 🏆 Top {entity_name}s")
            
            top_data = df.nlargest(10, num_col)
            
            fig = px.bar(
                top_data,
                x=id_col,
                y=num_col,
                color=num_col,
                color_continuous_scale='Sunset',
                text=num_col
            )
            fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            fig.update_layout(
                xaxis_title=entity_name,
                yaxis_title=num_col.replace('_', ' ').title(),
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            charts_created += 1
        
        # ============================================
        # 9. CORRELATION ANALYSIS (Multiple Numeric Columns)
        # ============================================
        numeric_cols = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
        
        if len(numeric_cols) >= 3:
            st.markdown("#### 🔥 Correlation Between Numeric Variables")
            
            corr_matrix = df[numeric_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdBu_r',
                aspect='auto',
                labels=dict(color="Correlation")
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            charts_created += 1
        
        # Show message if no charts were created
        if charts_created == 0:
            st.info("💡 No suitable visualizations available for this specific query result. Try queries with categories, states, prices, or dates for better visualizations.")


def display_dataframe(df):
    """Display DataFrame with compact metrics and smart e-commerce visualizations"""
    
    # Compact one-line metrics
    st.markdown(
        f'<div style="display: flex; gap: 20px; margin-bottom: 12px; font-size: 0.9rem; color: #666;">'
        f'<span>📊 <strong>{len(df):,}</strong> rows</span>'
        f'<span>📋 <strong>{len(df.columns)}</strong> columns</span>'
        f'</div>',
        unsafe_allow_html=True
    )
    
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
    generate_ecommerce_visualizations(df)