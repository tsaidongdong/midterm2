"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm

def ml_loop(side: str):
    """
    The main loop for the machine learning process
    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```
    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    def move_to(player, pred) : #move platform to predicted position to catch ball 
        if player == '1P':
            if scene_info["platform_1P"][0]+20  > (pred-10) and scene_info["platform_1P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_1P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left
        else :
            if scene_info["platform_2P"][0]+20  > (pred-10) and scene_info["platform_2P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_2P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left
    def blocker_predict(frame_gap,blocker_now_position,dbr):
        distance=frame_gap*dbr
        if distance>0:
            while distance>=340:
                distance=distance-340
            if blocker_now_position+distance>170:
                if (blocker_now_position+distance-170)>170:
                    predict_position=blocker_now_position-340
                else:
                    predict_position=170-(blocker_now_position+distance-170)
            else:
                predict_position=blocker_now_position+distance
        else:
            while distance<=-340:
                distance=distance+340
            if blocker_now_position+distance<0:
                if (-(blocker_now_position+distance))>170:
                    predict_position=170-((-blocker_now_position+distance)-170)
                else:
                    predict_position=-(blocker_now_position+distance)
            else:
                predict_position=blocker_now_position+distance
        return predict_position
    def blocker_direction(now_position,old_position):
        if abs(now_position-old_position)<3:
            if now_position>100:
                return -3
            else:
                return 3
        else:
            return (now_position-old_position)
    def ml_loop_for_1P(): 
        dblocker = 0  
        if scene_info["ball_speed"][1] > 0 and scene_info["ball"][1]>260: # 球正在向下 # ball goes down #而且不可能敲到block
            x = ( scene_info["platform_1P"][1]-scene_info["ball"][1] ) //scene_info["ball_speed"][1] # 幾個frame以後會需要接  # x means how many frames before catch the ball
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x)  # 預測最終位置 # pred means predict ball landing site 
            bound = pred //200 # Determine if it is beyond the boundary
            if (bound > 0): # pred > 200 # fix landing position
                if (bound%2 == 0) : 
                    pred = pred - bound*200                    
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) : # pred < 0
                if (bound%2 ==1) :
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            return move_to(player = '1P',pred = pred)
        elif scene_info["ball_speed"][1] > 0 and scene_info["ball"][1]<260:# 球正在向下 # ball goes down #但可能敲到block

            #檢查敲到BLOCK
            #敲到上面預測位置
            
            #最後預測            
            x = ( scene_info["platform_1P"][1]-scene_info["ball"][1] ) //scene_info["ball_speed"][1] # 幾個frame以後會需要接  # x means how many frames before catch the ball
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x)  # 預測最終位置 # pred means predict ball landing site 
            bound = pred // 200 # Determine if it is beyond the boundary
            if (bound > 0): # pred > 200 # fix landing position
                if (bound%2 == 0) : 
                    pred = pred - bound*200                    
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) : # pred < 0
                if (bound%2 ==1) :
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            #敲到上
                return move_to(player = '1P',pred = pred)

        elif scene_info["ball"][1]>260 and scene_info["ball"][1]<420:#球向上 但在下板子跟BLOCK中間
            if len(blocker_position_history)<2:
                dblocker=0
            else:
                dblocker = blocker_direction(blocker_position_history[-1],blocker_position_history[-2])
            t=(scene_info["blocker"][1]+20-scene_info["ball"][1])// -(scene_info["ball_speed"][1])#幾個frame會接合
            down_predict=scene_info["ball"][0]+(scene_info["ball_speed"][0]*t)#the place that maybe hit the block
            blocker_position_predict=blocker_predict(t,blocker_position_history[-1],dblocker)
            down_pred=2*down_predict-scene_info["ball"][0]
            bound = down_predict // 200 # Determine if it is beyond the boundary
            if (bound > 0): # pred > 200 # fix landing position
                if (bound%2 == 0) : 
                    down_predict = down_predict - bound*200                    
                else :
                    down_predict = 200 - (down_predict - 200*bound)
            elif (bound < 0) : # pred < 0
                if (bound%2 ==1) :
                    down_predict = abs(down_predict - (bound+1) *200)
                else :
                    down_predict = down_predict + (abs(bound)*200)
            if down_predict+5>=blocker_position_predict and down_predict<=blocker_position_predict+30:
              
                return move_to(player = '1P',pred = down_predict)
            else:
                return move_to(player = '1P',pred = 100)
        else: # 球正在向上 # ball goes up #但不會敲到板子
            return move_to(player = '1P',pred = 100)



    def ml_loop_for_2P():  # as same as 1P
        if scene_info["ball_speed"][1] > 0 : 
            return move_to(player = '2P',pred = 100)
        else : 
            x = ( scene_info["platform_2P"][1]+30-scene_info["ball"][1] ) // scene_info["ball_speed"][1] 
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x) 
            bound = pred // 200 
            if (bound > 0):
                if (bound%2 == 0):
                    pred = pred - bound*200 
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) :
                if bound%2 ==1:
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            return move_to(player = '2P',pred = pred)

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:  #main code 
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()
        blocker_position_history=[]

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False
            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue
        
        # 3.3 Put the code here to handle the scene information

        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        else:
            blocker_position_history.append(scene_info["blocker"][0])
            if side == "1P":
                command = ml_loop_for_1P()
            else:
                command = ml_loop_for_2P()

            if command == 0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif command == 1:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
