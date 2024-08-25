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

chart1.properties(width='container')


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

loan_status_distribution.properties(width='container')


# If earlier charts are defined, combine all charts into a dashboard
dashboard = chart1 | loan_status_distribution 

# Display or save the dashboard
dashboard.save("chart1.json")



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



alt.data_transformers.disable_max_rows()

df = df[df['dti'] < 100]

# Rounding and capping annual income
df['rounded_annual_inc'] = df['annual_inc'].apply(lambda x: int(min(max(40000, round(x / 10000) * 10000), 200000)))

# Rounding installment to nearest 100, capping at 1500
df['rounded_installment'] = df['installment'].apply(lambda x: int(min(round(x / 100) * 100, 1500)))

# 1. Bar Chart for DTI vs Loan Status
bar_chart = alt.Chart(df).mark_bar().encode(
    x='loan_status:N',
    y=alt.Y('mean(dti):Q', scale=alt.Scale(domain=(0, 25))),
    color='loan_status:N',
    tooltip=['mean(dti)', 'loan_status']
).properties(
    title="Average DTI by Loan Status",
    width=600,
    height=400
)

bar_chart.properties(width='container')


# 2. Line Plot with Points for DTI vs Rounded Annual Income
line_plot_income = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('rounded_annual_inc:Q', title='Annual Income', scale=alt.Scale(domain=(40000, 200000))),
    y=alt.Y('mean(dti):Q', scale=alt.Scale(domain=(0, 25))),
    color='loan_status:N',
    tooltip=[alt.Tooltip('rounded_annual_inc:Q', title='Annual Income'), 'mean(dti):Q', 'loan_status:N']
).properties(
    title="Average DTI vs Annual Income by Loan Status",
    width=600,
    height=400)
line_plot_income.properties(width='container')


df = df[df['rounded_installment']<=1200]

# 3. Line Plot with Points for DTI vs Rounded Installment
line_plot_installment = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('rounded_installment:Q', title='Installment', scale=alt.Scale(domain=(0, 1200))),
    y=alt.Y('mean(dti):Q', scale=alt.Scale(domain=(0, 25))),
    color='loan_status:N',
    tooltip=[alt.Tooltip('rounded_installment:Q', title='Installment'), 'mean(dti):Q', 'loan_status:N']
).properties(
    title="Average DTI vs Installment by Loan Status",
    width=200
)

line_plot_installment.properties(width='container')


# Combine all three charts horizontally
combined_chart = alt.hconcat(bar_chart, line_plot_income, line_plot_installment, spacing=30)  # Adjust spacing as needed

# Display the combined chart
combined_chart.save("chart3.json")

