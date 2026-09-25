#importing python's built-in toolkit for making graphical interfaces
from datetime import datetime
import tkinter as tk
from urllib import response

#importing requests module to make HTTP requests to APIs
from matplotlib import image
from matplotlib.pyplot import box
from matplotlib.pyplot import box
import requests

#importing ttk module from tkinter for themed widgets
from tkinter import ttk

#importing random module to generate random choices
import random

#importing threading module to run tasks in the background without freezing the GUI
import threading

#importing Image and ImageTk from PIL (Python Imaging Library) to handle images
from PIL import Image, ImageTk

#importing BytesIO from io to handle image data in memory
from io import BytesIO

#function to get the center location of a geometry (point or polygon)
def get_location(geometry):
    coordinates = geometry[0].get("coordinates")

    #point: [longitude, latitude]
    if isinstance(coordinates[0], (int, float)):
        return coordinates

    #polygon: [[[longitude, latitude], ...]]
    points = coordinates[0]

    #extract longitudes and latitudes from the points
    longitudes = [point[0] for point in points]
    latitudes = [point[1] for point in points]

    #calculate the center of the bounding box
    center_longitude = (min(longitudes) + max(longitudes)) / 2
    center_latitude = (min(latitudes) + max(latitudes)) / 2

    return [center_longitude, center_latitude]

#function to get a GIBS image URL for a given metadata
def get_gibs_image(latitude, longitude, date):
    image_url = (
        "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi"
        f"?SERVICE=WMS"
        f"&REQUEST=GetMap"
        f"&LAYERS=MODIS_Terra_CorrectedReflectance_TrueColor"
        f"&FORMAT=image/jpeg"
        f"&TRANSPARENT=false"
        f"&VERSION=1.1.1"
        f"&WIDTH=800"
        f"&HEIGHT=500"
        f"&SRS=EPSG:4326"
        f"&BBOX={longitude-2},{latitude-2},{longitude+2},{latitude+2}"
        f"&TIME={date}"
    )

    return image_url

#function to display a GIBS image in a given label box
def show_gibs_image(image_url, box):

    #fetch the image from the URL with a timeout of 30 seconds
    response = requests.get(image_url, timeout=30)
    #check if the request was successful, raise an error if not
    response.raise_for_status()

    print("GIBS status:", response.status_code)
    print("GIBS content type:", response.headers.get("Content-Type"))

    #open the image from the response content and resize it to fit the label box
    image_data = Image.open(BytesIO(response.content))
    image_data = image_data.resize((350, 220))
    
    print("Image size:", image_data.size)

    #convert the image format to display in Tkinter
    image = ImageTk.PhotoImage(image_data)

    #update the label box with the image and clear any text
    box.config(image=image, text="", width=350, height=220)
    box.image = image
    box.update_idletasks()

#function to get a random event from NASA's EONET API, optionally filtered by category
def get_event(category=None):

    #first, try to get a currently active event
    response = requests.get(
        "https://eonet.gsfc.nasa.gov/api/v3/events",
        params={"category": category} if category else {},
        timeout=30
    )

    data = response.json()

    #if current events exist, choose one randomly
    if data["events"]:
        event = random.choice(data["events"])

    #if there are no current events, get previous events
    else:
        response = requests.get(
            "https://eonet.gsfc.nasa.gov/api/v3/events",
            params={
                "category": category,
                "status": "all"
            },
            timeout=30
        )

        data = response.json()

        #if there are still no events, return None
        if not data["events"]:
            return None

        #choose a previous/current event from the category
        event = random.choice(data["events"])

    print(event["title"])
    print(event["categories"][0]["title"])
    print(event["geometry"][0]["date"])

    #get the coordinates of the event's geometry
    coordinates = event["geometry"][0].get("coordinates")

    print("coordinates =", coordinates)

    return event

#using tk's function .Tk() to make window's object with name: main_window
main_window = tk.Tk()
main_window.title("gl@ncearth")
main_window.config(bg="#F5F0E6")  #setting background color of the window

#making a canvas for the scrollable area with background color and no border
canvas = tk.Canvas(main_window, bg="#F5F0E6", highlightthickness=0)

#making a scrollbar
scrollbar = ttk.Scrollbar(main_window, orient="vertical", command=canvas.yview)

#connecting the scrollbar to the canvas
canvas.configure(yscrollcommand=scrollbar.set)

#canvas takes the left side, fills horizontally and vertically and uses available window space 
canvas.pack(side="left", fill="both", expand=True)

#puts scrollbar on the right and fill = y makes it stretch vertically
scrollbar.pack(side="right", fill="y")

#making a frame to hold all the content
content_frame = tk.Frame(canvas, bg="#F5F0E6")

#putting the frame inside the canvas
content_window = canvas.create_window((0, 0), window=content_frame, anchor="n")
#making the canvas responsive to window resizing
canvas.bind(

    "<Configure>",
    lambda event: canvas.itemconfig(content_window, width=event.width)
)

#function label() to display text an formatting it and function pack() to display it in window
title = tk.Label(content_frame, text="🌍 WHAT IS EARTH UP TO!?", font=("Times New Roman", 20), bg="#f5f0e6", fg="#26352B")
title.pack(pady=20)# tk's layout method

#another label and formatting its positioning in pack; 
#anchor="w" means left
#padx= 20 pixel space from left
#pady= 10 pixel space from top
question = tk.Label(content_frame, text="Pick an Earth event to explore:", font=("Times New Roman", 16),  bg="#f5f0e6", fg="#26352B")
question.pack(anchor="w", padx=20, pady=10)

#defining a label to display the result of the button click
result = tk.Label(content_frame, 
    text="",
    font=("Times New Roman", 14),
    fg="#26352B",
    bg="#F5F0E6"
    )

#positioning the result label
result.pack(anchor="w", padx=20, pady=10)

#making a frame to hold the before and after boxes
image_frame = tk.Frame(content_frame, bg="#F5F0E6")
image_frame.pack(pady=10)

#making a frame for the before image and caption
before_frame = tk.Frame(image_frame, bg="#F5F0E6")
before_frame.pack(side="left", padx=20)

#making 'before' box 
before_box = tk.Label(
    before_frame,
    width=25,
    height=10,
    relief="solid",
    bg="#C9D8C5",
    fg="#26352B",
    font=("Times New Roman", 14)
)
before_box.pack()

#making 'before' caption
before_caption = tk.Label(
    before_frame,
    text="BEFORE",
    bg="#F5F0E6",
    fg="#26352B",
    font=("Times New Roman", 12)
)
before_caption.pack(pady=(5, 0))

#making a frame for the after image and caption
after_frame = tk.Frame(image_frame, bg="#F5F0E6")
after_frame.pack(side="left", padx=20)

#making 'after' box
after_box = tk.Label(
    after_frame,
    width=25,
    height=10,
    relief="solid",
    bg="#C9D8C5",
    fg="#26352B",
    font=("Times New Roman", 14)
)
after_box.pack()

#making 'after' caption
after_caption = tk.Label(
    after_frame,
    text="AFTER",
    bg="#F5F0E6",
    fg="#26352B",
    font=("Times New Roman", 12)
)
after_caption.pack(pady=(5, 0))

#making a frame for buttons
choices_frame = tk.Frame(content_frame, bg="#F5F0E6")
choices_frame.pack(pady=10)

#function to display the selected Earth event
def show_event(name, location, description, before, after):
    result.config(
        text=f"you picked --> {name}\n\n{location}\n{description}"
    )
    before_box.config(text=before)
    after_box.config(text=after)

#b1
#function button() to make a button
floods_button = tk.Button(
    choices_frame,
    text="💧 Floods",
    command=lambda: load_event("floods"),
    font=("Times New Roman", 12),
    bg="#D8C6A3",
    fg="#26352B",
    width=15,
    height=2
)
floods_button.grid(row=0, column=0, padx=10, pady=5)

#b2 (using the same structure for making buttons)   
severestorms_button = tk.Button(
    choices_frame,
    text="⛈️ Severe Storms",
    command=lambda: load_event("severeStorms"),
    font=("Times New Roman", 12),
    bg="#D8C6A3",
    fg="#26352B",
    width=15,
    height=2
)
severestorms_button.grid(row=0, column=1, padx=10, pady=5)

#b3
volcanoes_button = tk.Button(
    choices_frame,
    text="🌋 Volcanoes",
    command=lambda: load_event("volcanoes"),
    font=("Times New Roman", 12),
    bg="#D8C6A3",
    fg="#26352B",
    width=15,
    height=2
)
volcanoes_button.grid(row=1, column=0, padx=10, pady=5)

#b4
wildfire_button = tk.Button(
    choices_frame,
    text="🔥 Wildfire",
    command=lambda: load_event("wildfires"),
    font=("Times New Roman", 12),
    bg="#D8C6A3",
    fg="#26352B",
    width=15,
    height=2
)
wildfire_button.grid(row=1, column=1, padx=10, pady=5)

#b5
earthquake_button = tk.Button(
    choices_frame,
    text="震 Earthquakes",
    command=lambda: load_event("earthquakes"),
    font=("Times New Roman", 12),
    bg="#D8C6A3",
    fg="#26352B",
    width=15,
    height=2
)
earthquake_button.grid(row=2, column=0, padx=10, pady=5)

#b6
snow_button = tk.Button(
    choices_frame,
    text="❄️ Snow",
    command=lambda: load_event("snow"),
    font=("Times New Roman", 12),
    bg="#D8C6A3",
    fg="#26352B",
    width=15,
    height=2
)
snow_button.grid(row=2, column=1, padx=10, pady=5)

#b7
landslide_button = tk.Button(
    choices_frame,
    text="🏔️ Landslides",
    command=lambda: load_event("landslides"),
    font=("Times New Roman", 12),
    bg="#D8C6A3",
    fg="#26352B",
    width=15,
    height=2
)
landslide_button.grid(row=3, column=0, padx=10, pady=5)

#b8
drought_button = tk.Button(
    choices_frame,
    text="🏜️ Drought",
    command=lambda: load_event("drought"),
    font=("Times New Roman", 12),
    bg="#D8C6A3",
    fg="#26352B",
    width=15,
    height=2
)
drought_button.grid(row=3, column=1, padx=10, pady=5)

#function to fetch a random event from NASA and update result label with event details
def load_event(category=None):
    event = get_event(category)

    if event is None:
        main_window.after(
            0,
            #lambda function enables us to update the GUI from a different thread
            lambda: result.config(text="No event found.")
        )
        return

    title = event.get("title", "Unknown event")
    category_name = event.get("categories", [{}])[0].get("title", "Unknown")
    geometry = event.get("geometry", [])

    #if geometry is not empty, extract the date and coordinates, then get the GIBS image URL
    if geometry:
        date = geometry[0].get("date", "Date unavailable")
        date = date[:10]

        #make an after date by adding 3 days
        from datetime import datetime, timedelta

        #convert the date string to a datetime object, add 3 days, and convert it back to a string
        event_date = datetime.strptime(date, "%Y-%m-%d")
        after_date = event_date + timedelta(days=3)
        after_date = after_date.strftime("%Y-%m-%d")

        #get the coordinates of the event's geometry
        coordinates = get_location(geometry)

        #get the GIBS image URL for the event's location and date
        gibs_url = get_gibs_image(
            coordinates[1],
            coordinates[0],
            date
        )

        #get the GIBS image URL for the event's location and after date
        after_gibs_url = get_gibs_image(
            coordinates[1],
            coordinates[0],
            after_date
        )

        try:
            main_window.after(
            0,
            lambda: show_gibs_image(gibs_url, before_box)
            )

            main_window.after(
            0,
            lambda: show_gibs_image(after_gibs_url, after_box)
            )

        except requests.RequestException:
            main_window.after(
            0,
            lambda: before_box.config(text="Satellite image unavailable")
            )

    else:
        date = "Date unavailable"
        coordinates = "Location unavailable"

    main_window.after(
        0,
        lambda: result.config(
            text=f"{title}\n"
                 f"Category: {category_name}\n"
                 f"Date: {date}\n"
                 f"Location: {coordinates}"
        )
    )

#b9
def surprise_clicked():
    result.config(text="Finding an event...")

    threading.Thread(
        target=load_event,
        daemon=True
    ).start()

surprise_button = tk.Button(
    choices_frame, text="  SURPRISE!!!  ", 
    command=surprise_clicked, 
    font=("Times New Roman", 12), 
    bg="#D8C6A3",
    fg="#26352B",
    width=15, 
    height=2)
surprise_button.grid(row=4, column=0, padx=10, pady=5)

#clear button
def clear_clicked():
    result.config(text="")
    before_box.config(
        image="",
        text="BEFORE",
        width=25,
        height=10
    )
    before_box.image = None

    after_box.config(
        image="",
        text="AFTER",
        width=25,
        height=10
    )
    after_box.image = None

clear_button = tk.Button(
    choices_frame,
    text="  CLEAR  ",
    command=clear_clicked,
    font=("Times New Roman", 12),
    bg="#D8C6A3",
    fg="#26352B",
    width=15,
    height=2
)
clear_button.grid(row=4, column=1, padx=10, pady=5)

# updating the scrollable area whenever the content changes
content_frame.bind(
    "<Configure>",
    #here lambda is updating the scrollregion of the canvas whenever the content_frame is resized
    lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
)

#using the mainloop w object to tell python keep it running and listen for things happening in
main_window.mainloop()