import cv2
import numpy
from sklearn.cluster import KMeans
import numpy as np

img_name = "Bloody Hands"
image_path = f"C:/Users/mowai/Documents/Raggle/Clients/Farhan (Sockatlantis atlanore.com)/Codes/Flask server/sock_images/{img_name}.jpg"

palette = [
    ("black", (0, 0, 0), "Black"),
    ("white", (255, 255, 255), "White"),
    ("red", (255, 0, 0), "Red"),
    ("green", (0, 255, 0), "Lime"),  # Lime → Green
    ("blue", (0, 0, 255), "Blue"),
    ("yellow", (255, 255, 0), "Yellow"),
    ("blue", (0, 255, 255), "Cyan / Aqua"),  # Closer to Blue
    ("red", (255, 0, 255), "Magenta / Fuchsia"),  # Closer to Red
    ("white", (192, 192, 192), "Silver"),  # Closer to White
    ("black", (128, 128, 128), "Gray"),  # Closer to Black
    ("red", (128, 0, 0), "Maroon"),  # Closer to Red
    ("green", (128, 128, 0), "Olive"),  # Closer to Yellow
    ("green", (0, 128, 0), "Green"),
    ("red", (128, 0, 128), "Purple"),  # Closer to Red
    ("blue", (0, 128, 128), "Teal"),  # Closer to Blue
    ("blue", (0, 0, 128), "Navy"),  # Closer to Blue

    ("black", (0, 0, 0), "Black"),
    ("white", (255, 255, 255), "White"),
    ("red", (255, 0, 0), "Red"),
    ("green", (0, 255, 0), "Lime"),  # Lime → Green
    ("blue", (0, 0, 255), "Blue"),
    ("yellow", (255, 255, 0), "Yellow"),
    ("blue", (0, 255, 255), "Cyan / Aqua"),  # Closer to Blue
    ("red", (255, 0, 255), "Magenta / Fuchsia"),  # Closer to Red
    ("white", (192, 192, 192), "Silver"),  # Closer to White
    ("black", (128, 128, 128), "Gray"),  # Closer to Black
    ("red", (128, 0, 0), "Maroon"),  # Closer to Red
    ("green", (128, 128, 0), "Olive"),  # Closer to Yellow
    ("green", (0, 128, 0), "Green"),
    ("red", (128, 0, 128), "Purple"),  # Closer to Red
    ("blue", (0, 128, 128), "Teal"),  # Closer to Blue
    ("blue", (0, 0, 128), "Navy")  # Closer to Blue
]



def get_dominant_color(image_path, n_colors=4):
    print("started")
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Reshape the image into a list of pixels
    pixels = img.reshape(-1, 3)
    
    # Apply KMeans to find dominant colors
    kmeans = KMeans(n_clusters=n_colors)
    kmeans.fit(pixels)
    
    # Get the RGB values of the clusters
    dominant_colors = kmeans.cluster_centers_.astype(int)

    return dominant_colors

def getColorByManhattan(color, palette):
    diffs = []
    for colorMapping in palette:
        mapping = np.array(colorMapping[1])
        color = np.array(color)

        diff = np.sum(np.abs(mapping-color))
        diffs.append([colorMapping[0],diff,colorMapping[2]])
    sorted_data = sorted(diffs, key=lambda x: x[1])
    return sorted_data[0][0]




# get_dominant_color = get_dominant_color(image_path)
# closest_color = getColorByManhattan(get_dominant_color, palette)
# print(closest_color)
color = get_dominant_color = get_dominant_color(image_path)
for c in color:
    print(getColorByManhattan(c,palette))
    print(c)