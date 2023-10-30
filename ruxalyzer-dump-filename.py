#!/usr/local/bin/python3

import struct
import PIL.Image

import sys
FILENAME = sys.argv[1]
#FILENAME = "Idle.bin"
print(sys.argv[1], FILENAME)

storyfile = open(FILENAME, "rb+")

SNXROM = {}

# check for magic bytes
SNXROM['SNXROM'] = storyfile.read(12).decode('utf-16')
if SNXROM['SNXROM'] != 'SNXROM':
    raise RuntimeError("Didn't find SNXROM magic bytes")

print(SNXROM['SNXROM'], "found")

# read and toss next 28 bytes all 0xFF
storyfile.read(28)
# find 0x400 bytes
if 0x400 != struct.unpack('I', storyfile.read(4))[0]:
    raise RuntimeError("Didn't find 0x400 magic bytes")

SNXROM['assetTableLengthWords'] = struct.unpack('I', storyfile.read(4))[0]
print("Asset table length (words):", SNXROM['assetTableLengthWords'], "& bytes:", SNXROM['assetTableLengthWords'] * 4)

# read and toss next 464 bytes all 0xFF

allff=storyfile.read(464) # This is all FF and that is what it should be
#print(allff)

# NOTE: the pointers are in byte offsets not words!
print("Looking for asset table pointers at", hex(storyfile.tell()))
assetTablePointers = [0] * SNXROM['assetTableLengthWords']
for i in range(SNXROM['assetTableLengthWords']):
    assetTablePointers[i] = struct.unpack('I', storyfile.read(4))[0]
print("Asset table pointers:", [hex(i) for i in assetTablePointers])



# Go to the metadata table
SNXROM['metaOffset'] = assetTablePointers[0]
storyfile.seek(SNXROM['metaOffset'])

if 0x0000 == struct.unpack('h', storyfile.read(2))[0]:
    SNXROM['storyId'] = struct.unpack('h', storyfile.read(2))[0]
    SNXROM['numberOfEyeAnimations'] = struct.unpack('h', storyfile.read(2))[0]
    SNXROM['numberOfEyeBitmaps'] = struct.unpack('h', storyfile.read(2))[0]
    SNXROM['numberOfVideoSequences'] = struct.unpack('h', storyfile.read(2))[0]
    SNXROM['numberOfAudioBlocks'] = struct.unpack('h', storyfile.read(2))[0]
    print("Story ID: ", SNXROM['storyId'])
    print("Eye animations:", SNXROM['numberOfEyeAnimations'])
    print("Eye bitmaps:", SNXROM['numberOfEyeBitmaps'])
    print("Video seqs:", SNXROM['numberOfVideoSequences'])
    print("Audio blocks:", SNXROM['numberOfAudioBlocks'])
    num_eyes=SNXROM['numberOfEyeBitmaps']
else:
    print("Didn't find 0x0000 magic bytes, skipping meta!")
    SNXROM['metaOffset'] = 0
    num_eyes=73     # This is for Idle

SNXROM['ROMfilesize'] = struct.unpack('i', storyfile.read(4))[0]
print("Filesize should be:", SNXROM['ROMfilesize'])

##############
# struct ROMMetadata {
    # uint16_t unknown; // always 0x0
    # /**
     # * 0 - Intro "Hi. My name is Teddy Ruxpin. Can you and I be friends?"
     # * 1 - All About Bears
     # * 2 - The Airship
     # * 3 - Captured by MudBlups
     # * 4 - Wooly and The Wizard
     # * 5 - The Missing Princess
     # * 6 - Grubby's Romance
     # * 7 - The Day Teddy Met Grubby
     # * 8 - Teddy Ruxpin's Birthday
     # * 9 - Teddy Ruxpin's Christmas
     # * 10 - Teddy Ruxpin Lullabies
     # * 11 - Double Grubby
     # * 12 - The Story of the Faded Fobs
     # * 14 - Teddy Ruxpin Summertime
     # * 15 - Grundo Springtime Singtime
     # */
    # uint16_t storyId;
    # uint16_t numberOfEyeAnimations;
    # uint16_t numberOfEyeBitmaps;
    # uint16_t numberOfVideoSequences;
    # uint16_t numberOfAudioBlocks;
    # /**
     # * ROM file size = (fileSizeUpper) << 16 + fileSizeLower;
     # * 
     # * In Stories 12, 13 & 15, this value is incorrectly copied from Story 11.
     # */ 
    # uint16_t fileSizeUpper;
    # uint16_t fileSizeLower;
    # uint8_t _unknown[16]; // all 0xFF    
    # /**
     # * In order, follows:
     # * - EyeAnimationMetadata
     # * - VideoAudioSequence
     # */ 
    # MetadataObject metadataObjects[];
# };
##############

SNXROM['audioOffset'] = assetTablePointers[-1]
SNXROM['marktable'] = []
    
# verify audio offset
print("Looking for audio at", hex(SNXROM['audioOffset']))
storyfile.seek(SNXROM['audioOffset'])

if b'AU' == storyfile.read(2):
    print("Found beginning of audio")
    (samplerate, bitrate, channels, frame_count, file_len, mark_flag, silence_flag, \
     mbf, pcs, rec, header_len) = \
     struct.unpack('<HHHIIHHHHHH', storyfile.read(26))
    
    print("Header Size (16b words):", hex(header_len))
    
    print("Samplerate:", samplerate)
    print("Bitrate:", bitrate)
    print("Channels:", channels)
    print("Frame count:", frame_count)
    print("File len (16b words):", file_len)
    if (file_len * 2) / 80 != frame_count:
        print("Should be %d frames * 80 bytes per frame = %d total size" % (frame_count, file_len*2))
    print("Mark flag:", mark_flag)
    print("Silence flag:", silence_flag)
    print("Header Size (16b words):", header_len)

    # toss 0xFFFFFFFF
    storyfile.read(4)

    table_size = struct.unpack('<H', storyfile.read(2))[0]
    #print(table_size * 2)
    mark_entries = header_len*2 - (storyfile.tell() - SNXROM['audioOffset']) - 4
    print("entries:", mark_entries)

    SNXROM['marktable'] = []
    for i in range(mark_entries // 2):
        SNXROM['marktable'].append(struct.unpack('<H', storyfile.read(2))[0])
    totaltime = 0;
    for i in range(len(SNXROM['marktable']) // 2):
        totaltime+= SNXROM['marktable'][2*i+0]
        print( SNXROM['marktable'][2*i+0], SNXROM['marktable'][2*i+1])
    print("total length of motion mark table (s):", totaltime / 1000.0)

    print("Actual audio data starts at", hex(SNXROM['audioOffset'] + header_len*2))
    print("and ends at ", hex(SNXROM['audioOffset'] + header_len*2 + file_len*2))

else:
    print("Didn't find AU at beginning of audio, no mark table!")

# The rest are eyeball frames, extract them!

for i,pointer in enumerate(assetTablePointers):
    if SNXROM['metaOffset'] and (i == 0):
        continue # skip metadata table if it exists
    if SNXROM['marktable'] and (i == len(assetTablePointers)-1):
        continue # skip audio table if it exists
    if i>num_eyes:
        print("skipping non image things")
        continue

### This code can be used to do a numbering identical for left and right eyes.
#    if i<=(num_eyes//2):
#        j=i
#    else:
#        j=i-(num_eyes//2)

    print(i,pointer)
    storyfile.seek(pointer)
    image_data = storyfile.read(128*128*2)

    print(len(image_data))
    img = PIL.Image.frombytes('RGB', (128,128), image_data, 'raw', 'BGR;16')
# Save the image as PNG
    img.save(f'eye{i}.png')

### Code to actually display one image to troubleshooting
#    if (i == 4):
#        img.show()

### Process the image to make red eyes based on blue eyes.
#    newimg=getCorrectedImage(img)
#    newimg.save(f'eye{i}.png')


#    if i!=j:
#        newimg.save(f'eye{j:04d}l{i:04d}.png')
#    else:
#        newimg.save(f'eye{j:04d}r{i:04d}.png')

#    continue
#    logobytes = bytearray(b'')
#    for pix in PIL.Image.open("logo.png").convert('RGB').getdata():
#        r = (pix[2] >> 3) & 0x1F
#        g = (pix[1] >> 2) & 0x3F
#        b = (pix[0] >> 3) & 0x1F
#        logobytes = logobytes + struct.pack('H', (r << 11) + (g << 5) + b)
    #print(len(logobytes))
#    storyfile.write(logobytes)


#print(storyfile.tell() - SNXROM['audioOffset'])

"""

seen.add(i)
                asset = (c_uint16 * (128*128)).from_buffer(content, assetTablePointers[i])
                PIL.Image.frombytes('RGB', (128,128), string_at(asset, 128*128*2), 'raw', 'RGB;16').save(f'eye{i}.png')

SNXROM['leftEyeOffset'] = struct.unpack('I', storyfile.read(4))[0]
SNXROM['rightEyeOffset'] = struct.unpack('I', storyfile.read(4))[0]


print("Metadata offset: %d bytes, address 0x%0X" % (SNXROM['metaOffset'], SNXROM['metaOffset']))

print("Left Eye offset: %d bytes, address 0x%0X" % (SNXROM['leftEyeOffset'], SNXROM['leftEyeOffset']))
print("Right Eye offset: %d bytes, address 0x%0X" % (SNXROM['rightEyeOffset'], SNXROM['rightEyeOffset']))
print("Audio data offset: %d bytes, address 0x%0X" % (SNXROM['audioOffset'], SNXROM['audioOffset']))

print(storyfile.tell())

"""

storyfile.close()
