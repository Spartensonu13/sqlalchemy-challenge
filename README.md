# This challenge includes Jupyter Notebook and Flask api app.

As part of assignment connected to existing sqlite using SQLAlchemy and published following apis

## http://localhost:5000/
Start at the homepage.
List all the available routes.

## http://localhost:5000/api/v1.0/precipitation
Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
Return the JSON representation of your dictionary.

## http://localhost:5000/api/v1.0/stations
Return a JSON list of stations from the dataset.

## http://localhost:5000/api/v1.0/tobs
Query the dates and temperature observations of the most-active station for the previous year of data.
Return a JSON list of temperature observations for the previous year.

## http://localhost:5000/api/v1.0/<start> and http://localhost:5000/api/v1.0/<start>/<end>
Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
