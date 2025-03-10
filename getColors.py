import time
import cv2
import numpy as np
from sklearn.cluster import KMeans
import webcolors
import os
import json

def get_dominant_color(image_name, n_colors=2):
    # Load image

    original_name = image_name
    temp_name = "temp.jpg"
    os.rename(f"sock_images/{original_name}", f"sock_images/{temp_name}")
    img = cv2.imread(f"sock_images/{temp_name}")
    print(f"renamed image {original_name} and extracted it, shape={img.shape}")
    os.rename(f"sock_images/{temp_name}", f"sock_images/{original_name}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Reshape the image into a list of pixels
    pixels = img.reshape(-1, 3)
    
    # Apply KMeans to find dominant colors
    kmeans = KMeans(n_clusters=n_colors)
    kmeans.fit(pixels)
    
    # Get the RGB values of the clusters
    dominant_colors = kmeans.cluster_centers_.astype(int)
    
    # Classify colors to general categories
    color_names = [classify_color(rgb) for rgb in dominant_colors]
    
    return color_names
def classify_color(rgb):
    # Define RGB intervals for each color
    palette = [
        #("black", (0, 0, 0), "Black"),
        #("white", (255, 255, 255), "White"),
        ("red", (255, 0, 0), "Red"),
        ("green", (0, 255, 0), "Lime"),  # Lime → Green
        ("blue", (0, 0, 255), "Blue"),
        ("yellow", (255, 255, 0), "Yellow"),
        ("blue", (0, 255, 255), "Cyan / Aqua"),  # Closer to Blue
        ("red", (255, 0, 255), "Magenta / Fuchsia"),  # Closer to Red
        #("white", (192, 192, 192), "Silver"),  # Closer to White
        #("black", (128, 128, 128), "Gray"),  # Closer to Black
        ("red", (128, 0, 0), "Maroon"),  # Closer to Red
        ("green", (128, 128, 0), "Olive"),  # Closer to Yellow
        ("green", (0, 128, 0), "Green"),
        ("red", (128, 0, 128), "Purple"),  # Closer to Red
        ("blue", (0, 128, 128), "Teal"),  # Closer to Blue
        ("blue", (0, 0, 128), "Navy"),  # Closer to Blue

        #("black", (0, 0, 0), "Black"),
        #("white", (255, 255, 255), "White"),
        ("red", (255, 0, 0), "Red"),
        ("green", (0, 255, 0), "Lime"),  # Lime → Green
        ("blue", (0, 0, 255), "Blue"),
        ("yellow", (255, 255, 0), "Yellow"),
        ("blue", (0, 255, 255), "Cyan / Aqua"),  # Closer to Blue
        ("red", (255, 0, 255), "Magenta / Fuchsia"),  # Closer to Red
        #("white", (192, 192, 192), "Silver"),  # Closer to White
        #("black", (128, 128, 128), "Gray"),  # Closer to Black
        ("red", (128, 0, 0), "Maroon"),  # Closer to Red
        ("green", (128, 128, 0), "Olive"),  # Closer to Yellow
        ("green", (0, 128, 0), "Green"),
        ("red", (128, 0, 128), "Purple"),  # Closer to Red
        ("blue", (0, 128, 128), "Teal"),  # Closer to Blue
        ("blue", (0, 0, 128), "Navy")  # Closer to Blue
    ]

    # manhattan diff
    diffs = []
    for colorMapping in palette:
        mapping = np.array(colorMapping[1])
        color = np.array(rgb)

        diff = np.sum(np.abs(mapping-color))
        diffs.append([colorMapping[0],diff,colorMapping[2]])
    sorted_data = sorted(diffs, key=lambda x: x[1])
    return sorted_data[0][0]



def getColors():
    # get existing image colors
    try:
        with open("data/color.json","r",encoding="UTF-8") as file:
            data = json.load(file)
            colors = [color["name"] for color in data]
    except:
        file = open("data/color.json","w",encoding="UTF-8")
        data = []
        colors = []


    output = []
    for i, name in enumerate(os.listdir("sock_images")):


        if name not in colors:
            print(f"Processing {name}...")
            try:
                image_path = f"{name}"
                dominant_colors = get_dominant_color(image_path)
                output.append({
                    "name":name,
                    "colors":dominant_colors
                })
                # output.append(f"{name} == ['{dominant_colors[0]}', '{dominant_colors[1]}']")
            except Exception as e:
                print("test",e)

    print(output)

    # get current file contents
    with open("data/color.json", "r", encoding="UTF-8") as file:
        data = json.load(file)

    # Update colors for each entry
    data+=output

    print(f"Added {len(data)} colors to colors.json (again)")

    today = time.strftime("%Y-%m-%d")
    with open(f"logs/{today}.log","a",encoding="UTF-8") as file:
        file.write(f"Added {len(data)} colors to colors.json")
        file.write("\n\n\n")

    # Save the updated JSON data
    with open("data/color.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4,ensure_ascii=False)

getColors()