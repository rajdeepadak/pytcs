# Use this tool to trim video and/or save frames to folder path
# Set trimvideo and saveframes to True to obtain trimmed video and individual frames of the video. Set destination folder by giving valid path to dest.
# Set trimvideo to True and saveframes to False to obtain only trimmed video. Set destination folder by giving valid path to dest.
# Set trimvideo to False and saveframes to True to obtain only individual frames of the trimmed video. Set destination folder by giving valid path to dest.

from moviepy.editor import *
import os, cv2, shutil, numpy as np
from pathlib import Path
import moviepy.video.io.ImageSequenceClip

class pytcs:
    def __init__(self, vid, out):
        self.vid = vid
        self.out = out

    def recreate_video(self, img_fol):
        fps=1

        image_files = [os.path.join(img_fol, img)
                       for img in os.listdir(img_fol)
                       if img.endswith(".jpg")]
                    
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
        clip.write_videofile('crop_'+self.out)


    def cropframes(self, video, x1, y1, x2, y2):
        vidcap = cv2.VideoCapture(video)
        success, image = vidcap.read()
        count = 0
        while success:
            cv2.imwrite("frame%d.jpg" % count, image[y1:y2, x1:x2, :])     # save frame as JPEG file      
            success, image = vidcap.read()
            count += 1


    def writeframes(self, source):
        vidcap = cv2.VideoCapture(source)
        success, image = vidcap.read()
        count = 0
        while success:
            cv2.imwrite(os.getcwd() + "/frame%d.jpg" % count, image)     # save frame as JPG file      
            success, image = vidcap.read()
            if success == False:
                print("Finished. Open Destination to view all saved frames.")
            count += 1


    def videotrimmer(self, start, end, trimvideo:bool, saveframes:bool, crop=False, 
                     topleft_x=None, topleft_y=None, bottomright_x=None, bottomright_y=None, dest=None, FPS=None):

        # Save trimmed Video only.
        if trimvideo == True and saveframes == False:

            # If destination is None then save to current working directory.
            if dest is None:

                # Save clipped video to pwd
                video = VideoFileClip(self.vid).subclip(start, end)
                video.write_videofile(self.out, fps=FPS)

                # if crop is true 
                if crop is True:
                    # get path to clipped video
                    clv = os.getcwd() + "/" + self.out
                    clv = clv.replace(os.sep, '/')
                    
                    #create a temp directory and switch pwd to temp
                    os.mkdir('temp')
                    os.chdir('temp')

                    # save cropped frames of clipped video here and return back to 
                    # parent directory of temp
                    self.cropframes(clv, topleft_x, topleft_y, bottomright_x, bottomright_y)
                    os.chdir("..")

                    # recreate video from cropped frame.
                    self.recreate_video('temp')
                    
                    # remove temp and remove clipped video
                    os.remove(self.out)
                    shutil.rmtree("temp")

            # Save to valid destination
            else:
                if os.path.exists(dest):
                    video = VideoFileClip(self.vid).subclip(start, end)
                    os.chdir(dest)
                    video.write_videofile(self.out, fps=FPS)

                    # if crop is true 
                    if crop is True:
                        # get path to clipped video
                        clv = os.getcwd() + "/" + self.out
                        clv = clv.replace(os.sep, '/')
                        
                        #create a temp directory and switch pwd to temp
                        os.mkdir('temp')
                        os.chdir('temp')

                        # save cropped frames of clipped video here and return back to 
                        # parent directory of temp
                        self.cropframes(clv, topleft_x, topleft_y, bottomright_x, bottomright_y)
                        os.chdir("..")

                        # recreate video from cropped frame.
                        self.recreate_video('temp')
                        
                        # remove temp and remove clipped video
                        os.remove(self.out)
                        shutil.rmtree("temp")

                else:
                    print("Invalid Path. Enter valid path to save to destination.")

        # Save trimmed video and frames
        elif trimvideo == True and saveframes == True:
            video = VideoFileClip(self.vid).subclip(start, end) 
            new_path = os.getcwd() + "/" + os.path.splitext(self.out)[0]
            new_path = new_path.replace(os.sep, '/')
            new_fol = Path(new_path).stem

            # If destination is None then save to current working directory
            if dest is None:

                if not os.path.exists(new_path):
                    
                    # Make a folder named frames and save frames of trimmed video in it.
                    # Save trimmed video as out in pwd.
                    if crop is False:
                        video.write_videofile(self.out, fps=FPS)

                        os.makedirs("frames")
                        vid_file = os.getcwd() + "/" + self.out
                        os.chdir(os.getcwd() + "/frames")
                        
                        self.writeframes(vid_file)

                    else:
                        # if crop is true 
                        video.write_videofile(self.out, fps=FPS)
                        # get path to clipped video
                        clv = os.getcwd() + "/" + self.out
                        clv = clv.replace(os.sep, '/')
                        
                        #create a cropped_frames directory and switch pwd to cropped_frames
                        os.mkdir('cropped_frames')
                        os.chdir('cropped_frames')

                        # save cropped frames of clipped video here and return back to 
                        # parent directory of cropped_frames
                        self.cropframes(clv, topleft_x, topleft_y, bottomright_x, bottomright_y)
                        os.chdir("..")

                        # recreate video from cropped frame.
                        self.recreate_video('cropped_frames')
                        
                        # remove clipped video
                        os.remove(self.out)

                else:
                    print("Path already exists. Rename output filename to create a new folder or mention destination folder.")

            # Else save to valid destination.
            else:
                if os.path.exists(dest):
                    
                    if crop is True:
                        os.chdir(dest)
                        # if crop is true 
                        video.write_videofile(self.out, fps=FPS)
                        # get path to clipped video
                        clv = os.getcwd() + "/" + self.out
                        clv = clv.replace(os.sep, '/')
                        
                        #create a cropped_frames directory and switch pwd to cropped_frames
                        os.mkdir('cropped_frames')
                        os.chdir('cropped_frames')

                        # save cropped frames of clipped video here and return back to 
                        # parent directory of cropped_frames
                        self.cropframes(clv, topleft_x, topleft_y, bottomright_x, bottomright_y)
                        os.chdir("..")

                        # recreate video from cropped frame.
                        self.recreate_video('cropped_frames')
                        
                        # remove clipped video
                        os.remove(self.out)

                    else:
                        os.chdir(dest)
                        video.write_videofile(self.out, fps=FPS)

                        os.makedirs("frames")
                        vid_file = os.getcwd() + "/" + self.out
                        os.chdir(os.getcwd() + "/frames")
                        
                        self.writeframes(vid_file)

                else:
                    print("Path doesn't exist")

        # Save frames only
        elif trimvideo == False and saveframes == True:
            # clip video
            video = VideoFileClip(self.vid).subclip(start, end)
            
            # create a folder in the current working directory with the name "out" save frames inside the folder.
            if dest is None:
                
                # create a folder with cropped frames of trimmed video in pwd
                if crop is True:
                    # save video here
                    video.write_videofile(self.out, fps=FPS)

                    # get path to clipped video
                    clv = os.getcwd() + "/" + self.out
                    clv = clv.replace(os.sep, '/')
                    
                    #create a cropped_frames directory and switch pwd to cropped_frames
                    os.mkdir('cropped_frames')
                    os.chdir('cropped_frames')

                    # save cropped frames of clipped video here and return back to 
                    # parent directory of temp
                    self.cropframes(clv, topleft_x, topleft_y, bottomright_x, bottomright_y)
                    os.chdir("..")

                    # recreate video from cropped frame.
                    self.recreate_video('cropped_frames')
                    
                    # remove clipped video and cropped video
                    os.remove(self.out)
                    os.remove('crop_'+self.out)

                # create a folder with full frames of trimmed video in pwd 
                else:
                    # make a directory with name out and change pwd to out.
                    os.makedirs("cropped_frames")
                    x = os.getcwd() + "/" + "cropped_frames"
                    x = x.replace(os.sep, '/')
                    os.chdir(x)
                    
                    # save video here
                    video.write_videofile(self.out, fps=FPS)

                    # obtain video file path
                    vid_file = os.getcwd() + "/" + self.out

                    # save frames without creating any new folder
                    self.writeframes(vid_file)
                    
                    # delete the vid_file
                    os.remove(vid_file)   
   
            elif os.path.exists(dest):

                if crop is True:
                    # change to destination
                    os.chdir(dest)
                    # save video here
                    video.write_videofile(self.out, fps=FPS)

                    # get path to clipped video
                    clv = os.getcwd() + "/" + self.out
                    clv = clv.replace(os.sep, '/')
                    
                    # save cropped frames
                    self.cropframes(clv, topleft_x, topleft_y, bottomright_x, bottomright_y)
                    
                    # remove clipped video and cropped video
                    os.remove(self.out)

                else:
                    # change to destination
                    os.chdir(dest)

                    # save video file here
                    video.write_videofile(self.out, fps=FPS)

                    # obtain video file path
                    vid_file = os.getcwd() + "/" + self.out

                    # Save frames
                    self.writeframes(vid_file)

                    # delete the vid_file
                    os.remove(vid_file) 
                
            
            else:
                print("Invalid destination path")

        else:
            print("Enable trimvideo or saveframes option to see results")

A = pytcs("R5.mp4", "cut.mp4")


"""Tests"""
#A.videotrimmer("00:00:00", "00:00:10", trimvideo=True, saveframes=True, dest=r"C:/Users/indra/Desktop/Bubbles New/cut")
#A.videotrimmer("00:00:00", "00:10:00", trimvideo=False, saveframes=True, dest=r"C:/Users/indra/Desktop/Bubbles New/Yada", FPS=None)


"""Actual"""
# Save frames only within a period of time, here = 00:10:00 mins
# cropping: 
# In an image top left corner coordinates are x1, y1. bottom right are x2, y2
# (x1, y1) -----------------------------------------|
# |                                                 |  
# |                                                 |
# |                                                 |
# |                      Image                      |
# |                                                 |
# |                                                 |
# |                                                 |
# |-------------------------------------------(x2, y2)



A.videotrimmer("00:00:00", "00:10:00", trimvideo=False, saveframes=True, crop=True, 
                topleft_x = 0, 
                topleft_y = 200, 
                bottomright_x = 490, 
                bottomright_y = 370,
                dest = "all_frames",
                FPS=1)




