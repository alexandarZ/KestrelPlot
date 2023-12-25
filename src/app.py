import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from windrose import WindroseAxes
import sys

class WeatherDataVisualizer:
    def __init__(self, data_file):
        self.df = pd.read_csv(data_file)
        self.date_time = pd.to_datetime(self.df['FORMATTED DATE_TIME'])

    def createTemperaturePlot(self, ax):
        # Temperature and Dew Point
        ax.plot(self.date_time, self.df['Temperature'], label='Temperature (°C)', color='tab:red')
        ax.plot(self.date_time, self.df['Dew Point'], label='Dew Point (°C)', color='tab:green')
        ax.set_ylabel('Temperature / Dew Point')
        ax.legend(loc='upper left')

        # Humidity
        ax2 = ax.twinx()
        ax2.plot(self.date_time, self.df['Relative Humidity'], color='tab:blue', label='Humidity (%)')
        ax2.set_ylabel('Humidity', color='tab:blue')
        ax2.legend(loc='upper right')

        ax.grid(True)
        ax.set_title('Temperature and Humidity')

    def createBarometricPressurePlot(self, ax):
        # Barometric Pressure
        ax.plot(self.date_time, self.df['Barometric Pressure'],color='tab:orange', label='Barometric Pressure (mbar)')
        ax.set_ylabel('Barometric Pressure')
        ax.legend(loc='upper left')

        # Altitude
        ax2 = ax.twinx()
        ax2.plot(self.date_time, self.df['Altitude'], color='tab:purple', label='Altitude (m)')
        ax2.set_ylabel('Altitude', color='tab:purple')
        ax2.legend(loc='upper right')

        ax.grid(True)
        ax.set_title('Barometric Pressure and Altitude')

    def createWindPlot(self, compassName, windParamName):
       # Wind speed 
       ax = WindroseAxes.from_ax()
       ax.bar(self.df[compassName], self.df[windParamName], normed=True, opening=1.0, edgecolor='white')
       ax.set_legend()
       ax.grid(True)
       ax.set_title(windParamName+' Plot')

    def createFogProbabilityPlot(self, ax):
        # Parameters for fog probability (Adjust based on your dataset)
        humidity_parameter = 'Relative Humidity'
        temperature_parameter = 'Temperature'
        dew_point_parameter = 'Dew Point'
        pressure_parameter = 'Barometric Pressure'
        wind_speed_parameter = 'Wind Speed'

        # Set threshold values for fog conditions (Adjust based on your observations)
        humidity_threshold = 90
        temperature_threshold = 15
        dew_point_threshold = 10
        pressure_threshold = 1010
        wind_speed_threshold = 5

        # Calculate fog probability based on the number of parameters above their thresholds
        fog_probability = np.mean(
            (self.df[humidity_parameter] > humidity_threshold,
             self.df[temperature_parameter] < temperature_threshold,
             self.df[dew_point_parameter] < dew_point_threshold,
             self.df[pressure_parameter] < pressure_threshold,
             self.df[wind_speed_parameter] < wind_speed_threshold),
            axis=0
        ) * 100

        # Plotting humidity
        ax.plot(self.date_time, self.df[humidity_parameter], label='Humidity (%)', color='blue')

        # Fill the area above the fog probability threshold with different colors
        ax.fill_between(self.date_time, self.df[humidity_parameter], where=(fog_probability > 90),
                        interpolate=True, color='red', alpha=0.3, label='High Fog Probability')
        ax.fill_between(self.date_time, self.df[humidity_parameter], where=(fog_probability > 10) & (fog_probability <= 90),
                        interpolate=True, color='orange', alpha=0.3, label='Medium Fog Probability')
        ax.fill_between(self.date_time, self.df[humidity_parameter], where=(fog_probability <= 10),
                        interpolate=True, color='lightgreen', alpha=0.3, label='Low Fog Probability')

        # Customize the chart
        ax.set_title('Fog Probability')
        ax.set_xlabel('Time')
        ax.set_ylabel('Humidity (%)')
        ax.axhline(y=humidity_threshold, color='gray', linestyle='--', label='Humidity Threshold')
        ax.legend()
        ax.grid(True)

        # Create secondary y-axes for other parameters
        ax2 = ax.twinx()
        ax2.plot(self.date_time, self.df[temperature_parameter], label='Temperature (°C)', color='green')
        ax2.plot(self.date_time, self.df[dew_point_parameter], label='Dew Point (°C)', color='orange')
        ax2.plot(self.date_time, self.df[pressure_parameter], label='Pressure (hPa)', color='purple')
        ax2.plot(self.date_time, self.df[wind_speed_parameter], label='Wind Speed (m/s)', color='brown')

        ax2.set_ylabel('Other Parameters')
        ax2.legend()

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python3 app.py <file.csv>")
        sys.exit(1)

    # Get the file path from the command-line arguments
    file_path = sys.argv[1]

    # Create figures with subplots
    fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 18))
    fig1.suptitle('Weather Data')

    fig3, ax3 = plt.subplots(figsize=(10, 6))

    weather_visualizer = WeatherDataVisualizer(file_path)
    weather_visualizer.createTemperaturePlot(ax1)
    weather_visualizer.createBarometricPressurePlot(ax2)
    weather_visualizer.createWindPlot('Compass True Direction', 'Wind Speed')
    weather_visualizer.createFogProbabilityPlot(ax3)

    plt.show()  # Display the figures with subplots

if __name__ == "__main__":
    main()
