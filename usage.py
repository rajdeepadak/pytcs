from pytcs import pytcstools

tcs = pytcstools("R5.mp4", "cut.mp4")

tcs.videotrimmer("00:00:00", "00:10:00", trimvideo=False, saveframes=True, crop=True, 
                topleft_x = 0, 
                topleft_y = 200, 
                bottomright_x = 490, 
                bottomright_y = 370,
                dest = "all_frames",
                FPS=1)
