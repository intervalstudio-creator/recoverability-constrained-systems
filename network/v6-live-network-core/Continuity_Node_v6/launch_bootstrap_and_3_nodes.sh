#!/bin/sh
(cd ../Bootstrap_Service_v6 && python3 bootstrap_server.py --port 9000) &
sleep 2
python3 node.py --port 8080 --name node-1 --bootstrap http://127.0.0.1:9000 &
python3 node.py --port 8081 --name node-2 --bootstrap http://127.0.0.1:9000 &
python3 node.py --port 8082 --name node-3 --bootstrap http://127.0.0.1:9000 &
wait
