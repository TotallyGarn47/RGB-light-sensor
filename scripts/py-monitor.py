import serial, time, csv

ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)                                

with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['r-value', 'g-value', 'b-value', 'value'])
    try:
        while True:
            line = ser.readline().decode(errors='ignore').strip()
            if not line:
                continue
            
            try:
                # Convert split values to integers and ensure there are exactly 4 values
                row_data = [int(x) for x in line.split(',')]
                if len(row_data) == 4:
                    writer.writerow(row_data)
                    print(line)
            except ValueError:
                # Silently skip lines that contain non-integer text or errors
                continue
                
    except KeyboardInterrupt:
        pass

ser.close()