import os
import argparse
from sys import argv
import subprocess
import re
import math

parser = argparse.ArgumentParser()
parser.add_argument('-i','--image',
    help='the path of image and it must be with even hight and width also .jpg     ex: -i \"myImage.jpg\"',
    nargs='?',
    type=str,
    dest='img',
    required=True)

parser.add_argument('-a','--audio',
    help='the path of audio and it must be .mp3     ex: -a \"myaudio.mp3\"',
    nargs='?',
    type=str,
    dest='audio',
    required=True)

parser.add_argument('-t','--time',
    help='the maximum time length of the single clip in seconds. Default:24     ex: -t 24',
    type=int,
    default=24,
    dest='duration')


ARGS=parser.parse_args()
img         =ARGS.img
track       =ARGS.audio
duration    =ARGS.duration
SPLITDURATION = getTotalDuration(track)

def getTotalDuration(inputfile):
    filelengthOutput = subprocess.run(["ffprobe", "-i", inputfile, "-show_format",
                                       "-v", "quiet"], stdout=subprocess.PIPE).stdout.decode("UTF-8")
    match = re.search("duration=([0-9]*)", filelengthOutput)
    return int(match.group(1)) + 1


splitcount = math.ceil(getTotalDuration(track) / SPLITDURATION)
print(splitcount)

for i in range(splitcount):
    print(i)
    subprocess.run(["ffmpeg", "-i", track, "-ss", str(i * SPLITDURATION),
                    "-t", str(SPLITDURATION), "part" + str(i) + ".mp3"])

files=os.listdir(os.getcwd())
audios  = [xfile  for xfile in files if 'part' in xfile]

print()
print()
print()
print(audios)
print()
print()
print()
print()
total =len(audios)
count = 1
for audio in audios :
    out=audio.replace('.mp3','.mp4')
    os.system(f'ffmpeg -loop 1 -i {img} -i {audio} '
              f'-c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -t {duration} {out} -y')
    print(f"part {count} has been done from {total}")
    count+=1