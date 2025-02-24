import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Display Client connected successfully")
        # Subscribe to all the topics where messages are published
        client.subscribe("topic/client1")
        client.subscribe("topic/client2")
        client.subscribe("topic/client3")
    else:
        print(f"Failed to connect with result code {rc}")

def on_message(client, userdata, msg):
    print(f"\nEncrypted message received on {msg.topic}: \n{msg.payload.hex()}")

# Create the client for displaying encrypted messages
display_client = mqtt.Client("display_client")
display_client.on_connect = on_connect
display_client.on_message = on_message

# Connect to the MQTT broker
display_client.connect("test.mosquitto.org", 1883, 60)
display_client.loop_start()

try:
    input("Press Enter to quit...\n")
except KeyboardInterrupt:
    print("\nDisplay Client is shutting down...")

display_client.loop_stop()
display_client.disconnect()