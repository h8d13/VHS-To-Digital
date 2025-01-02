# VHS-To-Digital

For the adpaters there are two ways you can go about it:

SCART to HDMI 
I recommend to google your VHS player: Mine was a slvd920bs from Sony.

[1901419.pdf](https://github.com/user-attachments/files/18293494/1901419.pdf)

Download their specification sheet (usually at the end of the user manual). 

From there you should know if yours is using PAL or NTSC or other. 

The advantage of having SCART is that you might be able to get 576i @ 25 FPS

This will also determine the color quality: SCART is RBG compatible making the images quite crisp! 
Your main issue would be tear:

You can combat it in a couple of ways:

Set the display to mode:
YUV 4:2:2

Right click your source again and select "deinterlacing" retro, blend or linear you can try different ones. 

Go back to OBS settings: 

Make sure to set common FPS value to 25 PAL
Also make sure you're on BICUBIC 16 Samples: This is what I found best for retro. 

### Video Input

```
sudo apt update
sudo apt install obs-studio

sudo apt install v4l2-utils
```

In OBS:
Go to the "Sources" box at the bottom and click the +.
Select Video Capture Device.
Name it (e.g., "VHS Capture") and click OK.

### Audio input

``` sudo apt install pavucontrol```
& run pavucontrol to run the program. 

There you can select your HMDI to USB to capture the sound (you might have to set both?). 

Go back to OBS > In the sound mixers make sure one of them is moving with the VHS audio and remove your MIC source.

---

###The results

https://github.com/user-attachments/assets/504c38ed-8b5c-4fb4-b4ce-798497cb6b11




