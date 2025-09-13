import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(21)

data = []
drivers = [f"driver_{i}" for i in range(1, 50)]

for i in drivers:
    trips = np.random.randint(5, 15)
    for _ in range(trips):
        start = datetime(2025, 9, np.random.randint(1,5), np.random.randint(0, 24), np.random.randint(0, 60))
        duration = np.random.randint(5,60)
        avg_speed = np.random.uniform(20, 80)
        extreme_brakes = np.random.randint(0, 5)
        extreme_accels = np.random.randint(0, 5)
        late_driving = np.random.choice([0, 1], p=[0.7, 0.3])
        weather_conditions = np.random.choice(['clear', 'rainy', 'foggy', 'snowy'], p=[0.6, 0.2, 0.1, 0.1])
        traffic_conditions = np.random.choice(['light', 'moderate', 'heavy'], p=[0.5, 0.3, 0.2])
        mileage = (avg_speed * duration) / 60 
        data.append([i, start, duration, avg_speed, extreme_brakes, extreme_accels, late_driving, weather_conditions, traffic_conditions, mileage])
        
        
        
df = pd.DataFrame(data, columns=['driver_id', 'start', 'duration', 'avg_speed', 
                                 'extreme_brakes', 'extreme_accels', 'late_driving', 
                                 'weather_conditions', 'traffic_conditions', 'mileage'])


df.to_csv('data/simulated_drivers.csv', index=False)
