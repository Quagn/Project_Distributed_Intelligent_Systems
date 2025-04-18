from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Khởi tạo cảm biến
sensor_names = ['ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7']
sensors = [robot.getDevice(name) for name in sensor_names]
for sensor in sensors:
    sensor.enable(timestep)

# Khởi tạo động cơ
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

MAX_SPEED = 6.28

# Vòng lặp chính
while robot.step(timestep) != -1:
    ps_values = [sensor.getValue() for sensor in sensors]
    
    threshold = 80

    # Cảm biến bên trái: ps5, ps6, ps7
    obstacle_left = ps_values[5] > threshold or ps_values[6] > threshold or ps_values[7] > threshold
    # Cảm biến bên phải: ps0, ps1, ps2
    obstacle_right = ps_values[0] > threshold or ps_values[1] > threshold or ps_values[2] > threshold
    # Cảm biến phía trước: ps3, ps4
    obstacle_front = ps_values[3] > threshold or ps_values[4] > threshold

    if obstacle_front:
        if obstacle_left and not obstacle_right:
            # Bên trái chặn, bên phải rảnh → rẽ phải
            left_speed = 0.5 * MAX_SPEED
            right_speed = -0.2 * MAX_SPEED
        elif obstacle_right and not obstacle_left:
            # Bên phải chặn, bên trái rảnh → rẽ trái
            left_speed = -0.2 * MAX_SPEED
            right_speed = 0.5 * MAX_SPEED
        elif obstacle_left and obstacle_right:
            # Bị chặn cả hai bên → lùi lại
            left_speed = -0.5 * MAX_SPEED
            right_speed = -0.5 * MAX_SPEED
        else:
            # Nếu chỉ có vật trước mà hai bên trống → rẽ ngẫu nhiên
            left_speed = 0.5 * MAX_SPEED
            right_speed = -0.5 * MAX_SPEED
    elif obstacle_left:
        left_speed = 0.5 * MAX_SPEED
        right_speed = 0.1 * MAX_SPEED
    elif obstacle_right:
        left_speed = 0.1 * MAX_SPEED
        right_speed = 0.5 * MAX_SPEED
    else:
        left_speed = 0.5 * MAX_SPEED
        right_speed = 0.5 * MAX_SPEED

    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
