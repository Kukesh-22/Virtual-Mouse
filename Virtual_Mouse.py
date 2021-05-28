import numpy as np
import cv2
import mediapipe as mp
from win32api import GetSystemMetrics
import win32api, win32con


class virtual_mouse:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mpf = mp.solutions.hands
        self.hand = self.mpf.Hands()
        self.mpdraw = mp.solutions.drawing_utils 
        self.screenwidth = GetSystemMetrics(0)
        self.screenheight = GetSystemMetrics(1)


    def cursor_move(self,x,y):
        win32api.SetCursorPos((x,y))

    
    def left_click(self,x,y):   
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        
        
    def right_click(self,x,y):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
 

    def cursor(self,handLms):
        index_location_x= handLms.landmark[8].x
        index_location_y= handLms.landmark[8].y
        thumb_tip_location_x= handLms.landmark[4].x
        thumb_tip_location_y = handLms.landmark[4].y
        pinky_mcp_location_x = handLms.landmark[17].x
        pinky_mcp_location_y = handLms.landmark[17].y
        index_win_loc_x = self.screenwidth*index_location_x
        index_win_loc_y = self.screenheight*index_location_y
        thumb_win_loc_x = self.screenwidth*thumb_tip_location_x
        thumb_win_loc_y = self.screenheight*thumb_tip_location_y
        self.cursor_move(int(index_win_loc_x),int(index_win_loc_y))
        if abs(pinky_mcp_location_x-thumb_tip_location_x) < 0.08:
            
            self.right_click(int(index_win_loc_x),int(index_win_loc_x))
        if abs(index_win_loc_x-thumb_win_loc_x)< 40 :
            
            self.left_click(int(index_win_loc_x),int(index_win_loc_y))
    
    
    def controller(self):
        count = 0
        while(True):
            ret, frame = self.cap.read()
            count +=1
            if count % 4 != 0:
                continue
            frame = cv2.flip(frame,1)
            hands = self.hand.process(frame)
            if hands.multi_hand_landmarks:
                for handLms in hands.multi_hand_landmarks:
                    # for finger in self.mpf.HandLandmark:
                    self.cursor(handLms)
                    self.mpdraw.draw_landmarks(frame,handLms)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        self.cv2.destroyAllWindows()


vm = virtual_mouse()
vm.controller()