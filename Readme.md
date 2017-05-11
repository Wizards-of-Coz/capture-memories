# Cozmo Captures Memories

## Project Description

_Memory Capture_ is a simple demo where Cozmo takes a short video from his camera and uploads it to your preferred Instagram profile. Cozmo's camera view is mirrored on his face for players to see what is being shot. Whenever the user is ready, they may tap a cube to start recording. Cozmo would capture 60 images, create a video and upload the video to an Instagram account configured in the code. The script also generates a thumbnail and creates 14 different filters for the same.

## Video

[https://www.youtube.com/watch?v=kR9tWSeeHi8](https://www.youtube.com/watch?v=kR9tWSeeHi8)

## Implementation Details

This demo is primarily utilizing cube's tap detection as a trigger for Cozmo to start capturing the images. In order to trigger the command using voice, you could also say "cheese" whenever you are ready. We have used an InstagramAPI to upload the videos to Instagram and used Google Speech Recognition for voice commands. 

## Instructions

There are a few dependencies on other Python libraries: 
opencv3 is used to create a video from the images clicked by Cozmo
numpy is used for image manipulations
PIL is used for adding filters to the images
Wizards of Coz Common folder found [here](https://github.com/Wizards-of-Coz/Common)

To link your Instagram account with the script, change the INSTAGRAM_USER_NAME and INSTAGRAM_PASSWORD fields at the top of the CaptureImage Class. 

The game starts once Cozmo sees one cube in front of him. The cube will flash green once it is found by Cozmo. Cozmo will listen for taps on this cube to start clicking the images. 

In order to click and upload a picture instead of a video, view code from lines 227 - 234. 

## Thoughts for the Future
Cozmo having his own Instagram account is a great way for people all over the world to see what Cozmo is seeing. This can be used with a lot of games and experiences to capture fun moments along the way. 
