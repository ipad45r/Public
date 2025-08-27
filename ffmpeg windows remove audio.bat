@echo off
REM Remove audio from video using ffmpeg
REM Usage: remove_audio.bat input.mp4 output.mp4

if "%~1"=="" (
    echo Usage: %~nx0 inputfile outputfile
    exit /b
)

if "%~2"=="" (
    echo Please specify output file name.
    exit /b
)

ffmpeg -i "%~1" -c copy -an "%~2"
echo Done! Audio removed from "%~1" -> "%~2"
