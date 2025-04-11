@echo off
echo Starting ngrok...
ngrok\ngrok.exe config add-authtoken %1
ngrok\ngrok.exe http 5000 