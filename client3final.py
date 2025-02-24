import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# Load client3's private key
with open('client3_private_key.pem', 'rb') as key_file:
    client3_private_key = serialization.load_pem_private_key(key_file.read(), password=None)

# Load public keys of other clients
with open('client1_public_key.pem', 'rb') as key_file:
    client1_public_key = serialization.load_pem_public_key(key_file.read())

with open('client2_public_key.pem', 'rb') as key_file:
    client2_public_key = serialization.load_pem_public_key(key_file.read())

public_keys = {
    "client1": client1_public_key,
    "client2": client2_public_key,
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Client 3 connected successfully")
        client.subscribe("topic/client3")  # Subscribe to receive messages
    else:
        print(f"Failed to connect with result code {rc}")

def on_message(client, userdata, msg):
    try:
        decrypted_message = client3_private_key.decrypt(
            msg.payload,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"Client 3 received message: {decrypted_message.decode()}")
    except Exception as e:
        print(f"Failed to decrypt message: {e}")

client3 = mqtt.Client("client3")
client3.on_connect = on_connect
client3.on_message = on_message

client3.connect("test.mosquitto.org", 1883, 60)
client3.loop_start()

try:
    while True:
        recipient = input("Client 3: Enter the recipient (client1, client2): ")
        if recipient not in public_keys:
            print("Invalid recipient. Try again.")
            continue

        message = input(f"Client 3: Enter message to send to {recipient}: ")
        encrypted_message = public_keys[recipient].encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        client3.publish(f"topic/{recipient}", encrypted_message)
except KeyboardInterrupt:
    print("\nClient 3 is shutting down...")

client3.loop_stop()
client3.disconnect()