import websocket
from json import loads
from lametric import discover
from threading import Thread

# Lametric functions
key = "0e1db77a87d1e922f4e122a8ddd5bc7fb7d0133ef0ad9137304ce50cbf0f3413"
print("[+] Connecting to laMetric time")
t = discover(key)


moodTable = {
    1: "D:",
    2: ":(",
    3: ":I",
    4: ":)",
    5: ":D",
}


# def handle_message(message):


def on_message(ws, message):
    # Thread(target=handle_message, args=[message]).start()
    try:
        data = loads(message)
        print("[+] Data received:", data)
    except:
        print("[!] There was an error decoding the data: " + message)

    mood = moodTable[data["mood"]]
    t.notify(mood, data["text"])

    
    


def on_error(ws, error):
    print("[!] Websocket connection was closed because of an error: ")
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("[!] Websocket connection was closed")
    print("### closed ###")

def on_open(ws):
    print("[+] Succesfully connected to websocket")

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://127.0.0.1:1000/socket",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()