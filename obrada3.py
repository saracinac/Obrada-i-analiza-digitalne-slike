import numpy as np
import cv2

# Read and preprocess the image
slika = cv2.imread("koruny.jpg")
s_kopija = slika.copy()
slika = cv2.GaussianBlur(slika, (7, 7), 3)

# Convert the image to grayscale and threshold it
gray = cv2.cvtColor(slika, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 142, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Dictionary to store coins grouped by diameter
coin_groups = {}

# Group coins by diameter
for contour in contours:
    (x, y), radius = cv2.minEnclosingCircle(contour)
    diameter = radius * 2  # The diameter of the coin

    # Assigning coin value based on diameter range
    if 75 <= diameter <= 76:
        coin_value = 0.05
    elif 88 <= diameter <= 89:
        coin_value = 0.1
    elif 90 <= diameter <= 91:
        coin_value = 0.2
    elif 95 <= diameter <= 97.8:
        coin_value = 1
    elif 98 <= diameter <= 99:
        coin_value = 0.5
    elif 100 <= diameter <=120:
        coin_value = 5
    else:
        coin_value = None

    if coin_value is not None:
        coin_groups.setdefault(coin_value, []).append(contour)

# Define the coin values
coin_values = {
    5.00: "5 KM",
    1.00: "1 KM",
    0.50: "0.50 KM",
    0.20: "0.20 KM",
    0.10: "0.10 KM",
    0.05: "0.05 KM"
}

# Group coins by size difference
grouped_coins = {}
for coin_value, group in coin_groups.items():
    grouped_coins.setdefault(coin_values[coin_value], []).extend(group)

# Print the number of coins in each group
for group, coins in grouped_coins.items():
    print(f"Group: {group}, Count: {len(coins)}")

# Calculate total value
total_value = sum(coin_value * len(coins) for coin_value, coins in coin_groups.items())
print("Total value in KM:", total_value)

# Visualize grouped coins
for group, coins in grouped_coins.items():
    color = np.random.randint(0, 255, size=3).tolist()  # Random color for each group
    for contour in coins:
        s_kopija = cv2.drawContours(s_kopija, [contour], -1, color, 3)

cv2.imshow("Grouped Coins", s_kopija)
cv2.waitKey(0)
cv2.destroyAllWindows()
