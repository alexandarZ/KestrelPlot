# Weather Meter Plotter
Simple Python script for plotting Kestrel Instruments 5500 weather meter data using matplotlib.

![Screenshot](./assets/Plot.png)

### Requirements

* Matplotlib
* Numpy
* Windrose

### How to plot data

**Step 1: Prepare CSV file for plotting**
```
1) Remove first 3 lines that contains Device Name, Device Mode and Serial Number.

2) For some reason CSV file will contain following lines:

FORMATTED DATE_TIME,Temperature,Wet Bulb Temp,Relative Humidity,Barometric Pressure,Altitude,Station Pressure,Wind Speed,Heat Index,Dew Point,Density Altitude,Crosswind,Headwind,Compass Magnetic Direction,Compass True Direction,Wind Chill


First line is ok, but if our CSV data does not contain Data Type, Record name, Start time, Duration (H:M:S), Location description, Location address, Location coordinates, Notes, Python will not load empty columns correctly and charts will
show invalid data. To fix that problem we need to remove from CSV following data:

1. Line that contains following data: yyyy-MM-dd hh:mm:ss a,°C,°C,%,mb,m,mb,km/h,°C,°C,m,km/h,km/h,Deg,Deg,°C,Data Type,Record name,Start time,Duration (H:M:S),Location description,Location address,Location coordinates,Notes
2. From each data point ,point value, so that our point looks like this:

2023-12-16 12:00:00 AM,22.1,15.0,47.5,998.7,119,998.7,0.0,21.5,10.4,452,0.0,0.0,305,306,22.0

and now, our charts will show correct values.
```

**Step 2: Start Python script**

```
python3 app.py <path_to_csv_file>
```
