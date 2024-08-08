def reward_function(params):
    reward=1
    DIRECTION_THRESHOLD = 3.0
    SPEED_THRESHOLD_1 = 1.8
    SPEED_THRESHOLD_2 =1.3
    waypoints = params['waypoints']
    heading = params['heading']
    speed = params['speed']
    steps = params['steps']
    progress= params['progress']
    benchmark_steps=173
    x = params['x']
    y = params['y']
    
    #Get reward if completes the lap and more reward if it is faster than benchmark_time    
    # if progress == 100:
    #     if round(steps/15,1)<benchmark_time:
    #         reward+=100*round(steps/15,1)/benchmark_time
    #     else:
    #         reward += 100
    if is_offtrack:
        reward-=50   
    
    # Calculate the direction of the center line based on the closest waypoints

    next_point = waypoints[closest_waypoints[1]] 
    prev_point = waypoints[closest_waypoints[0]] 



    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians

    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction_current_point = math.atan2(next_point[1] - y, next_point[0] - x) 

    # Convert to degree

    track_direction = math.degrees(track_direction)
    track_direction_current_point = math.degree(track_direction_current_point)

    # Calculate the difference between the track direction and the heading direction of the car

    direction_diff = abs(track_direction - heading)
    direction_diff_current= abs(track_direction_current_point-heading)


    # Penalize the reward if the difference is too large
   
    direction_bonus=1
  
    if direction_diff > DIRECTION_THRESHOLD or not all_wheels_on_track:

        direction_bonus=1-(direction_diff/15)
        if direction_bonus<0 or direction_bonus>1:
            direction_bonus = 0
        reward *= direction_bonus
    else:
        if direction_diff_current == 45 :
            if speed>=SPEED_THRESHOLD_1:
                reward+=max(speed,SPEED_THRESHOLD_1)
            else:
                reward+=1e-3
        else:
            if speed<=SPEED_THRESHOLD_2:
                reward+=max(speed,SPEED_THRESHOLD_2)
            else:
                reward+=1e-3
    
    # Give additional reward if the car pass every 50 steps faster than expected
    if (steps % 50) == 0 and progress >= (steps / benchmark_steps) * 100 :
        reward += 10.0
    # Penalize if the car cannot finish the track in less than benchmark_steps
    elif (steps % 50) == 0 and progress < (steps / benchmark_steps) * 100 :
        reward-=5.0
    return reward