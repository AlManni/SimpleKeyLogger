# SimpleKeyLogger

## Overview

This is a GO/Python script designed to capture, send, analyze and log characters sent from the client. It provides a simple server that listens for incoming connections, processes the received messages, and logs the data to individual files for each client. Additionally, it performs a basic analysis on the logged data using a separate analysis module.

## Features

- **Client Handling**: The script can handle multiple client connections concurrently using multithreading.

- **Logging**: Messages received from clients are logged to individual files named by their respective IP addresses.

- **Timestamps**: Each log entry includes a timestamp with the date and time of the received message.

- **Inactivity Alert**: If no messages are received from a client for a specified period (default is 5 minutes), a timestamped alert is logged to indicate the inactivity.

- **Analysis Module**: An analysis module (`Analisi.py`) is used to perform additional analysis on the logged data. This is executed in a separate thread for each client.

## Usage

1. **Configuration**: Update the script with the desired configuration parameters, such as the host, port, and inactivity threshold.

```python
HOST = '127.0.0.1'
PORT = 25566
INACTIVITY_MINUTES = 5
```

2. **Run the server**: In order to start the server program, you need to run server.py.


```
python server.py
```

2a. **Client connections**: Clients will connect to the server by specifying the remote host and port. The server is able to handle multiple clients.

2b. **Logs**: Each client data is logged to the respective file named after the client remote ip.

## File Structure
- `server.py`
- `analisi.py`
- `buffer.txt`
- `client_ip.txt`
