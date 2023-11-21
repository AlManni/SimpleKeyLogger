import socket
import datetime
import threading
from Analisi import analisi

HOST = '127.0.0.1'
PORT = 25566

INACTIVITY_MINUTES = 5
# Initializing variables to print datetime if more than 10 minutes from last message
last_time = datetime.datetime(2023, 1, 1, 0, 0, 0)
# Returns empty string if not more than INACTIVITY_MINUTES minutes.
# Otherwise returns new datetime
def checkTime() -> str:
    global last_time
    current_time = datetime.datetime.now()
    time_difference_minutes = (current_time - last_time).total_seconds() / 60
    last_time = current_time
    if time_difference_minutes > INACTIVITY_MINUTES:
        return "\n\n--------------------------------------------------------\n" + current_time.strftime("%d/%m/%Y, %H:%M:%S") + "\n"
    else:
        return ""


file_lock = threading.Lock()
def logToFile(ip : str, resultSTR : str):
    filename = ip + '.txt'
    with file_lock:
        with open(filename,'a') as f:
            f.write(checkTime() + resultSTR)
        with open ('buffer.txt','w') as bufferfile:
            bufferfile.write(checkTime() + resultSTR)
    # Starting analisys thread
    print ("Starting detectionThread   " + filename)
    detectionThread = threading.Thread(target=analisi, args=('buffer.txt',))
    detectionThread.start()


def handleClient(conn, addr):
    print('Connesso: ', addr)
    try:
        data = conn.recv(8760)
        if not data:
            return
        ip, port = conn.getpeername()
        message = data.decode('utf-8')
        now = datetime.datetime.now().isoformat()
        resultSTR = message
        print(resultSTR)
        logToFile(ip, resultSTR)
    except Exception as e:
        print(f"Error handling client: {e}")




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((HOST, PORT))
    except OSError():
        print("Error: port already in use")
    s.listen()
    while True:
        conn, addr = s.accept()
        
        print ("Starting clientThread")
        clientThread = threading.Thread(target=handleClient, args=(conn, addr))
        clientThread.start()

        



