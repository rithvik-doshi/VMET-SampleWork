#Copyright Rithvik Doshi 2021 rithvik@bu.edu

from moviepy.editor import * #import moviepy, library for video editing and creation
import os #organizing files
import shutil #resetting Videos folder

confirm = input(f"Before you continue, make sure that all the files you wish to include "
				f"are in the file format '.mp4' and are in the current directory, {os.getcwd()}.\n"
				f"In addition, please allow a good amount of time for the script to run, "
				f"especially if you intend to synchronize multiple videos. (y/n) ")

# In the future, we can write a script to automatically convert videos using the shell
# command: ffmpeg -i my-video.mov -vcodec h264 -acodec mp2 my-video.mp4

if confirm == 'n': #If the user ain't ready
	quit()

if os.path.exists("temp_videos"): #Resets Videos Folder
    shutil.rmtree("temp_videos")
os.mkdir("temp_videos")

if not(os.path.exists("Results")): #Creates a folder with all renders, if it doesn't already exist
	os.mkdir("Results")

cliplist = {}
n = 1
for file in os.listdir(): #Copies the first 9 .mp4 files. Largely to prevent corruption of original files if something goes awry
    if file.endswith(".mp4"):
        shutil.copy(file, f"temp_videos/{file}")
        cliplist[n] = VideoFileClip(f"temp_videos/{file}").fx(afx.audio_normalize).resize(height=180, width=320)
        # Not sure what dimensions to use, tried to keep it small in 180p but not sure if this changes actual pixels stored in memory
        n+=1 #create clip vars, store in dictionary, normalize audio and resize. Doesn't always resize though, need to look into that.
    if len(os.listdir("temp_videos")) >= 9: #Future functionality: Ability to add all videos and automatically arrange
        break

while n < 10: #Code to create extra black screens
    cliplist[n] = ColorClip(size = (180, 320), color = [0, 0, 0], duration = 1)
    n +=1

finalclip = clips_array([[cliplist[1], cliplist[2], cliplist[3]], #Arrangement of screens.
                         [cliplist[4], cliplist[5], cliplist[6]], #Need to research auto arrangement based on number of inputs
                         [cliplist[7], cliplist[8], cliplist[9]]]) #Goal: Zoom video arrangement.

# Future ideas for arrangement: Show preview using Pygame, ask user to confirm or to
# change arrangement of videos, add/delete videos, etc. Might need to use
# CompositeVideoClip instead of clips_array method.

outfile = input("Enter the title of the video (no extension .mp4): ") + ".mp4"

while outfile in os.listdir("Results"): #File creation and error checking
	outfile = input("This title has been taken. Enter another title with extension (example.mp4): ") + ".mp4"

finalclip.resize(width=1280, height=720)
print("Now rendering...")
finalclip.write_videofile(f"Results/{outfile}", codec = 'libx264', #Write file to Results folder
                                               audio_codec='aac',
                                               temp_audiofile = 'Results/temp_audio.m4a', 
                                               remove_temp = True
                                               )

print(f"The composite video {outfile} can now be found in the 'Results' folder.") #Confirmation messaage

shutil.rmtree("temp_videos") #Remove unnecessary folder

# Comments & Questions:

# When an individual video finishes playing, it disappears from the composite video. Is the
# intention to get it to freeze until the last video finishes playing, or trim each video
# to the shortest clip/last natural break in audio?

# I've done a little extra work with the I/O to update the user through the process of
# creating their video. Should this be expanded upon or should the script work silently
# with predetermined parameters?

# The dimensions of each video are arbitrary, however, the videos don't seem to take up
# an equal amount of space in the output video, nor does the output video show up in the 
# specified dimensions. Maybe we need to use a CompositeVideoClip type data structure in
# order to better manage and arrange these clips. More research will be needed.

#