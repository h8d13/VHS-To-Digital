# VHS-To-Digital

For the adpaters there are a couple of ways you can go about it:

SCART to HDMI or S-audio or RAC 
And a HMDI to USB also.

-----

I recommend to google your VHS player: Mine was a **slvd920bs from Sony.**

[1901419.pdf](https://github.com/user-attachments/files/18293494/1901419.pdf)

Download their specification sheet (usually at the end of the user manual). 

From there you should know if yours is using PAL or NTSC or other. 

The advantage of having SCART is that you might be able to get 576i @ 25 FPS

Here is what my adapter looks like:

![Adapter](/sc.png)

If you have mini cassettes (VHS-C) you can also buy this:

![51CZxvAMGyL _AC_SL1200_](https://github.com/user-attachments/assets/05471ee0-eb78-4cec-968c-aa8499628a15)

## This will determine the color quality + res: SCART is RBG compatible making the images quite crisp! 
----
Download OBS (open source and free)

> **_NOTE:_** Your main issue would be tear:

> You can combat it in a couple of ways:
> Set the display to mode: YUV 4:2:2

> Right click your source again and select "deinterlacing" retro, blend or linear you can try different ones. 

Go back to OBS settings: 

Make sure to set common FPS value to 25 PAL and output to 576px.
Also make sure you're on BICUBIC 16 Samples: This is what I found best for retro. 

----
## Linux 

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

----
### Audio input

``` sudo apt install pavucontrol```
& run pavucontrol to run the program. 

There you can select your HMDI to USB to capture the sound (you might have to set both?). 

Go back to OBS > In the sound mixers make sure one of them is moving with the VHS audio and remove your MIC source.

---

## For Windows the process is the same but Plug and play!

### The results

https://github.com/user-attachments/assets/504c38ed-8b5c-4fb4-b4ce-798497cb6b11

It's not perfect and the sound could definetly be improved. The image is quite okay tho, even a bad setting like this interview. Also GitHub has compression...

Why is this cool? 

First of all this interview isn't anywhere on the internet. That's the cool part: obsoclescence. 

----

This part of the code needs FFMPEG.exe to conserve audio!

Using some post processing techniques we can also try to regain colors that were lost using some maths: 

![Comparison](/comparison_frame.png)

![comparison_frame](https://github.com/user-attachments/assets/c76e357f-eabb-4ce1-9f48-839a57e2afdc)

![comparison_frame](https://github.com/user-attachments/assets/f6b0b0cb-7037-4bc5-aa22-ef40cad85cf9)

We simply clip the lowest 2% and higest 2% values of RGB graphs (or at least I thought).

----

### But that created another issue which was that sometimes it would be too "Warm".

![comparison_frame](https://github.com/user-attachments/assets/81f373de-4d07-4cec-a29d-965b47fd6eec)


----

So to combat this: LAB colors spaces which preserves colors but let's us play around with L (Luminance, so light/dark)

![comparison_frame](https://github.com/user-attachments/assets/c3e7435d-0918-4c83-9018-d643b83be114)



---


I'm happy with colors. Let's move on to denoising, sharpen and contrast. We will try to use subtle values to not destroy the original feel. 

![comparison_frame](https://github.com/user-attachments/assets/e59a74e5-403e-4f25-8809-17965c4a04ec)

All the code is available in the /scripts folder :)

![temp_comparison-ezgif com-optimize](https://github.com/user-attachments/assets/11c46a2d-0ac8-4a42-9231-709062ed90c6)

