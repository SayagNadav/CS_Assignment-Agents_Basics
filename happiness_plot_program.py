import pandas as pd
import matplotlib.pyplot as plt

try:
    df = pd.read_csv('World-happiness-report-2024.csv')
except FileNotFoundError:
    print("The specified file was not found.")
    exit()

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Check for required columns
if 'country_name' not in df.columns or 'ladder_score' not in df.columns:
    print("Required columns are missing in the data.")
    exit()

# Handle any missing data
df = df[['country_name', 'ladder_score']].dropna()

# Calculate average happiness score
average_score = df['ladder_score'].mean()

# Get top 5 and lowest 5 countries by ladder score
top_5 = df.nlargest(5, 'ladder_score')
lowest_5 = df.nsmallest(5, 'ladder_score')

# Prepare data for plotting
countries = top_5['country_name'].tolist() + lowest_5['country_name'].tolist() + ['Average']
scores = top_5['ladder_score'].tolist() + lowest_5['ladder_score'].tolist() + [average_score]

# Create the plot
plt.figure(figsize=(12, 8))
plt.bar(countries, scores, color=['green']*5 + ['red']*5 + ['blue'], alpha=0.7)
plt.axhline(y=average_score, color='blue', linestyle='--', label='Average Happiness Score')
plt.title('Happiness Scores of Top 5 and Lowest 5 Countries (World Happiness Report 2024)')
plt.xlabel('Countries')
plt.ylabel('Happiness Score (Ladder Score)')
plt.xticks(rotation=15)
plt.legend()

# Save the plot
plt.savefig('happiness_plot.png', dpi=300, bbox_inches='tight')