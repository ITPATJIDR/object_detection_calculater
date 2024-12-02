import math

# พิกัด
lat1, lon1 = 14.040687327186905, 100.6103504594003
lat2, lon2 = 14.040712127593626, 100.610352695971741

# แปลงละติจูดและลองจิจูดจากองศาเป็นเรเดียน
lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

# คำนวณความแตกต่างของละติจูดและลองจิจูด
delta_lat = lat2_rad - lat1_rad
delta_lon = lon2_rad - lon1_rad

# ใช้สูตร Haversine
a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# รัศมีโลก
R = 6371  # กิโลเมตร
distance = R * c  # ระยะทาง

print(f"ระยะทางระหว่างพิกัดทั้งสองคือ {distance} กิโลเมตร")
