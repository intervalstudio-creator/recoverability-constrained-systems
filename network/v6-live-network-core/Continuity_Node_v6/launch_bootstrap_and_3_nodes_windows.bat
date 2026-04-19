@echo off
start powershell -NoExit -Command "cd %~dp0..\Bootstrap_Service_v6; python bootstrap_server.py --port 9000"
timeout /t 2 >nul
start powershell -NoExit -Command "cd %~dp0; python node.py --port 8080 --name node-1 --bootstrap http://127.0.0.1:9000"
start powershell -NoExit -Command "cd %~dp0; python node.py --port 8081 --name node-2 --bootstrap http://127.0.0.1:9000"
start powershell -NoExit -Command "cd %~dp0; python node.py --port 8082 --name node-3 --bootstrap http://127.0.0.1:9000"
