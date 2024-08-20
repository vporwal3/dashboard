import pandas as pd
import altair as alt

# Load your data
df = pd.read_csv("output.csv")

df['default'] = df['loan_status'].apply(lambda x: 1 if x == 'Default' else 0)
state_defaults = df.groupby('addr_state')['default'].mean().reset_index()
state_defaults['default'] = state_defaults['default']*100
# Create a brush for linking the visualizations
brush = alt.selection_interval(encodings=['x'])

# First Plot: Histogram of State vs Loan Default Rate
chart1 = alt.Chart(state_defaults).mark_bar().encode(
    x='addr_state:N',
    y='default:Q',
    tooltip=['addr_state', 'default']
).properties(
    title="State vs Loan Default Rate"
).add_selection(brush)

#chart1.properties(width='container')


# Second Plot: Pie Chart of Loan Status
loan_status_distribution = alt.Chart(df).mark_arc().encode(
    theta=alt.Theta('count()', title='Number of Loans'),
    color=alt.Color('loan_status:N', legend=alt.Legend(title="Loan Status")),
    tooltip=['loan_status', 'count()']
).transform_filter(
    brush
).properties(
    title="Loan Status Distribution"
)



#loan_status_distribution.properties(width='container')

combined_chart = alt.hconcat(chart1, loan_status_distribution,spacing=100)  # Combine charts horizontally

# Display or save the combined chart
combined_chart.save('chart1.json')  # Saving to JSON file

# # If earlier charts are defined, combine all charts into a dashboard
# dashboard = chart1 | loan_status_distribution 

# # Display or save the dashboard
# dashboard.save("chart1.json")
# dashboard.save("chart1.html")



# Load your data
df = pd.read_csv("output.csv")

# Calculate the default rate per state
df['default'] = df['loan_status'].apply(lambda x: 1 if x == 'Default' else 0)
# Convert FICO score to a string if it isn't already

df['mean_fico_score'] = df['mean_fico_score'].astype(float).astype(int).astype(str)

# Calculate delinquency rate
df['is_delinquent'] = df['delinq_2yrs'].apply(lambda x: 1 if x > 0 else 0)
avg_delinquency_rate = df.groupby(['mean_fico_score', 'loan_status'])['is_delinquent'].mean().reset_index()

# Create a dropdown selection for loan status 
input_dropdown = alt.binding_select(options=sorted(df['loan_status'].unique()), name='Loan Status')
selection = alt.selection_point(fields=['loan_status'], bind=input_dropdown, value='Current')

# Creating the line chart with a dropdown filter
line_chart = alt.Chart(avg_delinquency_rate).mark_line(point=True).encode(
    x=alt.X('mean_fico_score:O', title='FICO Score'),
    y=alt.Y('is_delinquent:Q', title='Delinquency Rate', scale=alt.Scale(domain=(-0.05, 0.5))),
    tooltip=['mean_fico_score', 'is_delinquent']
).transform_filter(
    selection
).properties(
    title="Delinquency Rate by FICO Score",
    width=600,
    height=400
).add_params(selection)

line_chart.properties(width='container')

# Display or save the chart
line_chart.save('chart2.json')  # Saving to HTML file

