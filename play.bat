for /f "delims=" %%x in (config.txt) do (set "%%x")
set PATH=%PATH%;%mpvpath%

taskkill /F /IM mpv.exe /T
start "" /MIN bash.exe %streamplayer%\play.sh http://www.namava.ir/play/%1 %2 \\.\pipe\mpv-pipe
