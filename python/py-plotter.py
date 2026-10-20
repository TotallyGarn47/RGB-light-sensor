import sys
print(sys.executable)

import pandas as pd 
import matplotlib.pyplot as plt

def plot_led_strength(filename='data.csv'):
    try:
        # Load the CSV file
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: '{filename}' not found. Make sure your data collection script has run and generated the file.")
        return

    # Check if the expected 'value' column exists
    if 'value' not in df.columns:
        print("Error: 'value' column not found in the CSV headers.")
        return

    # Convert the column to numeric, forcing any non-integer or corrupted text to NaN (Not a Number)
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    # Drop rows where the value couldn't be converted to an integer (ignoring non-integers)
    df = df.dropna(subset=['value'])
    
    # Convert the clean values to integers
    df['value'] = df['value'].astype(int)

    # Set up X-axis (line number / sample index) and Y-axis (led strength)
    x = range(1, len(df) + 1)
    y = df['value']

    if len(df) == 0:
        print("No valid integer data found to plot.")
        return

    # Create the plot
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker='o', linestyle='-', color='royalblue', linewidth=1.5, markersize=4, alpha=0.8)
    
    # Customize the graph labels and appearance
    plt.title('Arduino LED Strength Monitor', fontsize=14, fontweight='bold')
    plt.xlabel('Line Number (Sample Index)', fontsize=12)
    plt.ylabel('LED Strength (0-1023)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Display the graph window
    plt.show()

if __name__ == '__main__':
    plot_led_strength()