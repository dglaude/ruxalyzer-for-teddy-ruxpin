# ruxalyzer-for-teddy-ruxpin
Variation on ruxalyzer by LadyAda of Adafruit - replace images

This whole repo started with the file `ruxalyzer-by-ladyada.py` that as name imply is code written by LadyAda and demonstrated in Adafruit Live stream. The code was never really published but was waiting in a PR that was never really published but that I recovered.
So it is not a finished product and there is no support from Adafruit on it and it was not supposed to published.
I assumed that the LICENCE would be MIT like all the code Adafruit produce.

After hacking herself with the Teddy Ruxpin file format Lady Ada hacked herself into the file format and demontrated that in Live stream, she asked @jepler (Jeff Epler) to continue the work and he produced the following repo as a result of that colaboration: https://github.com/adafruit/snxrom

Using the code by Jepler, Erin St Blaine rebuilded a Teddy Ruxpin to a dragon speaking stories read by/for family member and documented the process in a learn guide: https://learn.adafruit.com/teddy-ruxpin-rebuild?view=all

The code in snxrom repo works great for changing the audio and can also dump images, but has some problems.
* Apparently only the right eyes
* It is inverting red and blue color
* It might dump things that are not image as image
* It cannot take a directory as input to rebuild an image

But there is no real plan to continue working on snxrom, PR for correction might be accepted but no new development, the learn guide seems to be the goal or end of that project.

I did try to fix and improve snxrom, but the code is a bit complex for me. So I decided to try to modify the original ruxalyzer. This repo is to try to share my progress.

`ruxalyzer-by-ladyada.py`:
Initial code that dump all of the image in the rom file.
It is hard coded for reading `Idle.bin` and by default it dump all eye images into file with format `eye{i}.png`.
By changing the code, you can overwrite the eye images by the content of the file `logo.png`.

`ruxalyzer-dump-filename.py`:
This is basically doing the same thing as LadyAda code, but you have to specify an input filename, like `Story01.bin`. Added value is that it skip the non image at the end of the file (based on number of image specified in the header).

`ruxalyzer-dump-redeye-filename.py`:
Exactly the same as dump filename, but I include a processing of the image data to create red eyes out of blue eyes before saving the image to file. The formula used is to check if a pixel has a value of zero in the red channel, if so, the blue channel value is used for the red channel and green and blue are set to zero. In most eye images from the Teddy Ruxpin, the blue part of the eye has zero red inside, so that formula has good result on most image... just by chance.

`ruxalyzer-inject-filename.py`:
If you created image files for a rom (like `Story01.bin`), and decide to modify them (or it is modified by the `-redeye-` version), you can then re-inject them into the rom file, ready to re-upload to the Teddy Ruxpin. Warning, you have to specify a romfile, and that romfile will be modified. Make sure you have a backup of the original files.

**Ideal workflow**
You could `-dump-` all the images from a rom file, then modify them either manually or with another program, then you can `-inject-` them back into a copy of the same rom file. Right now I only inject the red-eye version of the eye images, but ideally one could use a modified PiEye to generate realistic eye sequence.

**Here is side by side the original blue eye and modified red eye:**

![image](https://github.com/dglaude/ruxalyzer-for-teddy-ruxpin/assets/19435932/f729c832-4aff-48c1-9ba7-f2a4345ccca6)
