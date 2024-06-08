import numpy as np
import cv2

slika = cv2.imread("slika7.jpg")
slika = cv2.resize(slika, (640, 800))
s_kopija = slika.copy()
slika = cv2.GaussianBlur(slika, (7, 7), 3)

gray = cv2.cvtColor(slika, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 142, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
area = {}
for i in range(len(contours)):
    cnt = contours[i]
    ar = cv2.contourArea(cnt)
    area[i] = ar

srt = sorted(area.items(), key=lambda x: x[1], reverse=True)
rez = np.array(srt).astype("int")
num = np.argwhere(rez[:, 1] > 500).shape[0]

diameters = []

for i in range(1, num):
    s_kopija = cv2.drawContours(s_kopija, contours, rez[i, 0], (0, 255, 0), 3)
    (x, y), radius = cv2.minEnclosingCircle(contours[rez[i, 0]])
    diameter = radius * 2  
    diameters.append((diameter, rez[i, 0]))


diameters.sort(reverse=True, key=lambda x: x[0])

coin_values = [5.00, 0.50, 1.00, 0.20, 0.10, 0.05]  

total_value = 0

for idx, (diameter, contour_idx) in enumerate(diameters):
    coin_value = coin_values[idx % len(coin_values)]  
    total_value += coin_value
    
   
    print(f"Recognized coin {idx+1}: Diameter = {diameter:.2f} pixels, Value = {coin_value} KM")
    
  
    (x, y), radius = cv2.minEnclosingCircle(contours[contour_idx])
    center = (int(x), int(y))
    cv2.putText(s_kopija, f"{coin_value} KM", center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

print("Total value:", total_value, "KM")

cv2.imshow("rezultat", s_kopija)
cv2.waitKey(0)
cv2.destroyAllWindows()




