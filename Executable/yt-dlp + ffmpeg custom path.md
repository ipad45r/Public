
# using custom path for yt-dlp?
## in this case the the executable is set at HOME/bin 
## included ffmpeg path as well, 
## -a is the url save in a txt file
## -P is the path where you save the video file

/home/user/bin/yt-dlp --ffmpeg-location "/home/user/bin/ffmpeg" --restrict-filenames -a /home/user/ncc/ncclink.txt   -P /home/user/ytlive
