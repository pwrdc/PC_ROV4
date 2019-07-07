
# Version for ROV3.5 (1.07)
To run steering:
0) 'sudo pigpiod' on rpi
1) 'sh run_servers.sh' on rpi in RPi_ROV4/cmmunication/rpi_drivers
2) 'python3.6 main.py' on rpi in RPi_ROV4/
3) 'python3.6 zmq_engine_client.py' on rpi in KN_Robocik-Electronics-Rpi/
4) 'python3.6 depth.py' on rpi in KN_Robocik-Electronics-Rpi/
5) 'python3 main.py' here

Points 2-5 in separate threads
Every time program question for log option - choose A or o
For force killing evry thread use 'pkill python3.6'

# Version for ROV4 (1.07)
Same as in ROV3.5 without point 0)
