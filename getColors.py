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
    color_intervals = {
        "red": ((200, 0, 0), (255, 50, 50)),
        "orange": ((200, 100, 0), (255, 165, 50)),
        "yellow": ((200, 200, 0), (255, 255, 50)),
        "green": ((0, 200, 0), (50, 255, 50)),
        "cyan": ((0, 200, 200), (50, 255, 255)),
        "blue": ((0, 0, 200), (50, 50, 255)),
        "white": ((200, 200, 200), (255, 255, 255)),
        "black": ((0, 0, 0), (50, 50, 50))
    }

    def is_within_interval(color, lower_bound, upper_bound):
        return all(lower <= c <= upper for c, lower, upper in zip(color, lower_bound, upper_bound))

    for color_name, (lower_bound, upper_bound) in color_intervals.items():
        if is_within_interval(rgb, lower_bound, upper_bound):
            return color_name

    # If no match is found, return the closest color
    closest_color = min(color_intervals, key=lambda color: np.linalg.norm(np.array(rgb) - np.array(color_intervals[color][0])))
    return closest_color


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
