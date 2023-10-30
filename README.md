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

`ruxalyzer-by-ladyada.py`
Initial code that dump all of the image in the rom file.
It is hard coded for reading `Idle.bin` and by default it dump all eye images into file with format `eye{i}.png`.
By changing the code, you can overwrite the eye images by the content of the file `logo.png`.

... to be continued ...


