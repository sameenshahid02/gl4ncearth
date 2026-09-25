**gl4ncearth** is a Python Tkinter application that uses NASA APIs to retrieve real-world natural event data and visualize the affected locations through satellite imagery.

## About the Project

The application connects NASA Earth Observatory Natural Event Tracker (EONET) with NASA Global Imagery Browse Services (GIBS) to create an interactive Earth-events explorer.

Users can select an event category, retrieve a real event from NASA EONET, and view satellite imagery from the event location before and after the event date.

## Features

1. Select from an Earth event :

  * Floods
  * Severe Storms
  * Volcanoes
  * Wildfires
  * Earthquakes
  * Snow
  * Landslides
  * Drought
2. Retrieve real events dynamically from NASA EONET
3. Random event selection within the selected category
4. Fallback to historical EONET events when no current event is available
5. Handle both point and polygon event geometries
6. Extract event coordinates and calculate a center location for area-based events
7. Retrieve satellite imagery through NASA GIBS WMS (Web Map Service)
8. Generate BEFORE and AFTER imagery using the event date and a 3-day offset
9. Display event metadata including title, category, date, and location
10. Background threading for event retrieval
11. Scrollable Tkinter interface
12. Clear and reset displayed event data and imagery
13. Random event discovery through the SURPRISE!!! 

## Workflow

```text
User selects category
        ↓
NASA EONET API
        ↓
Retrieve matching events
        ↓
Random event selection
        ↓
Extract event metadata
        ↓
Normalize event geometry
(Point / Polygon → coordinates)
        ↓
NASA GIBS WMS
        ↓
Retrieve satellite imagery
        ↓
BEFORE + AFTER
        ↓
Display in Tkinter
```

For polygon-based events, the application calculates the center of the event's bounding box and uses that location for the GIBS imagery request.

## Tools & Technologies

* **Python**
* **Tkinter / ttk**: GUI
* **Requests**: HTTP/API requests
* **Pillow (PIL)**: image processing and Tkinter image rendering
* **Threading**: background API/event loading
* **NASA EONET API**: natural event data
* **NASA GIBS WMS**: satellite imagery
* **Git / GitHub**: version control

## NASA APIs

### EONET

Provides the event information used by the application:

* Event title
* Category
* Date
* Geometry
* Coordinates
* Current and historical events

### GIBS

Provides satellite imagery using the event's coordinates and date.

The application constructs a WMS `GetMap` request using:

* Event latitude and longitude
* Event date
* MODIS Terra Corrected Reflectance True Color imagery
* EPSG:4326 geographic coordinate system

```text
## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sameenshahid02/gl4ncearth.git
cd gl4ncearth

### 2. Install dependencies

```bash
pip install requests pillow

### 3. Run the application

```bash
python earth_observer.py

## Good to Know

The application retrieves event data and satellite imagery through external NASA APIs, so generating a result may take some time depending on the response from the services. If the application appears to be taking a while, please wait for it to process the request or check the terminal for any functional errors caused by your system. The code may still be processing the request and has not necessarily stopped or failed.
