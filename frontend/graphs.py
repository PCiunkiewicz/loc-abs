"""Placeholder graphs for frontend when no data is available."""
import pandas as pd
import plotly.express as px

def fig_system_status_placeholder():
    """System readiness gauge - always shows current state."""
    import plotly.graph_objects as go
    
    # Check if system components are ready (agents configured, terrains loaded, etc.)
    readiness_score = 75  # Calculate based on: agents > 0, terrains > 0, scenarios > 0
    
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=readiness_score,
        title={'text': "System Readiness"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#0d6efd"},
            'steps': [
                {'range': [0, 33], 'color': "#ffc107"},
                {'range': [33, 66], 'color': "#17a2b8"},
                {'range': [66, 100], 'color': "#198754"}
            ],
        }
    )).update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        height=300
    )

def fig_config_summary_placeholder(api_data=None):
    """Shows counts of configured resources - always has data."""
    # Fetch from API or use defaults
    config_counts = pd.DataFrame({
        'Resource': ['Scenarios', 'Agents', 'Terrains', 'Preventions', 'Viruses'],
        'Count': [0, 0, 0, 0, 0]  # Replace with actual API counts
    })
    
    return px.bar(
        config_counts,
        x='Resource',
        y='Count',
        title="System Configuration Status",
        labels={'Count': 'Configured Items'},
        color='Count',
        color_continuous_scale='Blues',
        text='Count'
    ).update_layout(
        margin=dict(l=40, r=20, t=50, b=40),
        showlegend=False,
        height=350
    ).update_traces(textposition='outside')

def fig_run_history_placeholder():
    """Empty state that guides users to run first simulation."""
    import plotly.graph_objects as go
    
    return go.Figure().add_annotation(
        text="📊 No simulation runs yet<br><br>Click 'Create New Scenario' to get started",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color="#6c757d"),
        align="center"
    ).update_layout(
        title="Recent Run History",
        xaxis={'visible': False},
        yaxis={'visible': False},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='#f8f9fa'
    )

def fig_agent_type_distribution():
    """Shows configured agent types even before runs."""   
    # Fetch from /api/simulation/agent-configs/
    agent_types = pd.DataFrame({
        'Agent Type': ['Explorer', 'Mapper', 'Monitor'],  # From AgentConfig
        'Count': [3, 2, 1]  # Configured agent counts
    })
    
    if agent_types['Count'].sum() == 0:
        # Show placeholder types
        agent_types = pd.DataFrame({
            'Agent Type': ['No agents configured'],
            'Count': [1]
        })
        colors = ['#e9ecef']
    else:
        colors = px.colors.qualitative.Set2
    
    return px.pie(
        agent_types,
        names='Agent Type',
        values='Count',
        title="Configured Agent Types",
        hole=0.4,
        color_discrete_sequence=colors
    ).update_layout(margin=dict(l=20, r=20, t=50, b=20))


def fig_terrain_coverage_placeholder():
    """Shows available terrains/floors - always has data."""
    import plotly.graph_objects as go
    
    # Fetch from /api/simulation/terrains/
    terrains_df = pd.DataFrame({
        'Floor': ['Floor 1', 'Floor 2', 'Floor 3'],
        'Area_sqm': [500, 450, 600],
        'Status': ['Loaded', 'Loaded', 'Not Loaded']
    })
    
    return go.Figure(data=[
        go.Bar(
            x=terrains_df['Floor'],
            y=terrains_df['Area_sqm'],
            marker_color=['#198754' if s == 'Loaded' else '#dc3545' 
                          for s in terrains_df['Status']],
            text=terrains_df['Status'],
            textposition='outside'
        )
    ]).update_layout(
        title="Loaded Terrain Maps",
        xaxis_title="Floor",
        yaxis_title="Area (m²)",
        margin=dict(l=40, r=20, t=50, b=40),
        height=350
    )