ref = db.reference("machines/motor_1/readings")

ref.child(str(int(time.time()*1000))).set({
    "vibration_x": x,
    "vibration_y": y,
    "vibration_z": z,
    "gyro_x": gx,
    "gyro_y": gy,
    "gyro_z": gz,
    "current_ma": current,
    "voltage_v": voltage,
    "power_mw": power,
    "timestamp": int(time.time()*1000)
})