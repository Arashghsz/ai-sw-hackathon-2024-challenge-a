import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
import os

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Transform the nested structure into flat dictionary
    flat_data = []
    for entry in data:
        flat_entry = {'date': entry['date']}
        # Extract only the values from nested dictionaries
        for key in entry:
            if key != 'date':
                try:
                    flat_entry[key] = float(entry[key]['value'])
                except (TypeError, KeyError):
                    print(f"Warning: Could not process {key} in entry")
                    continue
        flat_data.append(flat_entry)
    
    df = pd.DataFrame(flat_data)
    df['date'] = pd.to_datetime(df['date'])
    return df

# Dictionary to store units for each variable
UNITS = {
    'rainfall': 'mm/day',
    'temperature': '°C',
    'fuel_price': '€/L',
    'fertilizer_price': '€/ton',
    'soil_moisture': '%',
    'exchange_rate': '€/USD',
    'wheat_price': '€/ton'
}

def plot_time_series(df):
    plt.figure(figsize=(15, 20))
    variables = df.columns.drop('date')
    
    for i, var in enumerate(variables, 1):
        plt.subplot(len(variables), 1, i)
        plt.plot(df['date'], df[var])
        unit = UNITS.get(var, '')
        plt.title(f'{var.replace("_", " ").title()} Over Time ({unit})')
        plt.xlabel('Date')
        plt.ylabel(f'{var.replace("_", " ").title()} ({unit})')
        plt.xticks(rotation=45)
        plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(df):
    plt.figure(figsize=(10, 8))
    correlation_matrix = df.drop('date', axis=1).corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap between Variables')
    plt.tight_layout()
    plt.show()

def plot_distributions(df):
    variables = df.columns.drop('date')
    plt.figure(figsize=(15, 10))
    
    for i, var in enumerate(variables, 1):
        plt.subplot(3, 3, i)
        sns.histplot(df[var], kde=True)
        unit = UNITS.get(var, '')
        plt.title(f'{var.replace("_", " ").title()} Distribution ({unit})')
        plt.xlabel(f'{var.replace("_", " ").title()} ({unit})')
        plt.ylabel('Frequency')
    
    plt.tight_layout()
    plt.show()

def main():
    try:
        # Get the current script's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct path to dataset.json
        file_path = os.path.join(current_dir, '..', 'data', 'dataset.json')
        
        print(f"Looking for data file at: {file_path}")
        print("Loading data...")
        df = load_data(file_path)
        
        print("Generating visualizations...")
        # Generate and show visualizations
        plot_time_series(df)
        plot_correlation_heatmap(df)
        plot_distributions(df)
        
        # Print statistics
        print("\nBasic Statistics:")
        print(df.describe())
        
        print("\nCorrelations with wheat price:")
        correlations = df.corr()['wheat_price'].sort_values(ascending=False)
        print(correlations)
        
    except FileNotFoundError:
        print("Error: dataset.json file not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
