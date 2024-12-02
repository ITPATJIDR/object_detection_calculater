import math

def latlng_to_meters(lat1, lng1, lat2, lng2):
    """
    คำนวณระยะทางระหว่างพิกัดละติจูดและลองจิจูดเป็นเมตร

    :param lat1: ละติจูดจุดที่ 1
    :param lng1: ลองจิจูดจุดที่ 1
    :param lat2: ละติจูดจุดที่ 2
    :param lng2: ลองจิจูดจุดที่ 2
    :return: ระยะทางเป็นเมตร
    """
    # ค่าคงที่
    EARTH_RADIUS_METERS = 6371000  # รัศมีโลกในหน่วยเมตร
    
    # แปลงละติจูดและลองจิจูดเป็นเรเดียน
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)

    # คำนวณความต่างในเรเดียน
    delta_lat = lat2_rad - lat1_rad
    delta_lng = lng2_rad - lng1_rad

    # ใช้สูตร Haversine
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS_METERS * c  # ระยะทางเป็นเมตร
    
    return distance

# ตัวอย่างการใช้งาน
lat1, lng1 = 14.041428, 100.616263
lat2, lng2 = 14.040410, 100.616203
distance = latlng_to_meters(lat1, lng1, lat2, lng2)
print(f"ระยะทางระหว่างพิกัดทั้งสอง: {distance:.2f} เมตร")
