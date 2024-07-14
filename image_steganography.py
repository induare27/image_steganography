# %%
import cv2
import os
import hashlib


# %%
# Specify the path to the input image
original_image_path = r"E:\image steganography\code\cleanImage.jpg"

# Specify the path to the encrypted image
encrypted_image_path = r"E:\image steganography\code\encryptedImage.jpg"

# %%
def load_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    return img

def hash_password(password):
    return hashlib.sha256(password.encode()).digest()

def initialize_ascii_dictionaries():
    return {chr(i): i for i in range(256)}, {i: chr(i) for i in range(256)}

def encode_message_into_image(img, msg, hashed_password):
    height, width, channels = img.shape
    n = m = z = 0
    
    for i, char in enumerate(msg):
        img[n, m, z] = (int(img[n, m, z]) + d[char] + hashed_password[i % len(hashed_password)]) % 256
        
        m += 1
        if m >= width:
            m = 0
            n += 1
        
        if n >= height:
            raise ValueError("Image too small to hold the entire message.")
        
        z = (z + 1) % 3
    
    return img

def save_image(img,new_filename="encryptedImage.jpg"):
    new_image_path = os.path.join(os.path.dirname(original_image_path), new_filename)
    print(new_image_path)
    cv2.imwrite(new_image_path, img)
    return new_image_path

def decode_message_from_image(img, hashed_password, msg_length):
    height, width, channels = img.shape
    n = m = z = 0
    decoded_chars = []
    
    for i in range(msg_length):
        original_value = (int(img[n, m, z]) - hashed_password[i % len(hashed_password)]+256) % 256
      
        decoded_chars.append(c[original_value])

        
        m += 1
        if m >= width:
            m = 0
            n += 1
        
        if n >= height:
            raise ValueError("Image is too small or corrupted.")
        
        z = (z + 1) % 3
    
    return ''.join(decoded_chars)


# %%
# Prompt the user to input the secret message and password
msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Hash the password
hashed_password = hash_password(password)
print("Password hashed successfully.",hashed_password)
d, c = initialize_ascii_dictionaries()
print(d,c)

# %%
# Load the input image
try:
    img = load_image(original_image_path)
    print("Image loaded successfully.")
except FileNotFoundError as e:
    print(e)

# Encode the secret message into the image
try:
    img = encode_message_into_image(img, msg, hashed_password)
    print("Message encoded successfully.")
except ValueError as e:
    print(e)

# Save the modified image to a new file
try:
    encrypted_image_path = save_image(img)
    print(f"Message has been encoded into '{encrypted_image_path}'.")
except Exception as e:
    print(e)

# Open the newly saved encrypted image
#os.startfile(encrypted_image_path)

# %%
# Load the encrypted image
try:
    img = load_image(encrypted_image_path)
    print("Encrypted image loaded successfully.")
except FileNotFoundError as e:
    print(e)

# Decode the secret message from the image
message_length = len(msg)  # Using the length of the original message
print(message_length)
try:
    decoded_message = decode_message_from_image(img, hashed_password, message_length)
    print("Message decoded successfully.")
    print(f"The secret message is: {decoded_message}")
except ValueError as e:
    print(e)
