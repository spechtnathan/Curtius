from strain import STRAIN
import time

try:
    strain = STRAIN()
except:
    print("No Strain")

while True:
    try:
        raw_values = strain.get_values()
        values1, values2 = tuple(v / 65535.0 * 3.3 for v in raw_values)  # Convert each value to voltage
        print(f"{values1}\t{values2}")
    except Exception as e:
        print(f"Error reading strain values: {e}")
    time.sleep(1)
