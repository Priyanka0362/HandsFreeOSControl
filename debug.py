import mediapipe as mp

print("MediaPipe Version:", mp.__version__)
print("MediaPipe File:", mp.__file__)

print("\nAvailable attributes:")
for item in dir(mp):
    print(item)