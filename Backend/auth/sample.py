import cv2
import os

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #create a video capture object which is helpful to capture videos through webcam
cam.set(3, 640) # set video FrameWidth
cam.set(4, 480) # set video FrameHeight

# Dynamically get the path to the Haar Cascade file in the current directory
haar_path = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')
detector = cv2.CascadeClassifier(haar_path)


face_id = input("Enter a Numeric user ID  here:  ")
#Use integer ID for every new face (0,1,2,3,4,5,6,7,8,9........)

print("Taking samples, look at camera ....... ")
count = 0 # Initializing sampling face count

while True:

    ret, img = cam.read() #read the frames using the above created object
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #The function converts an input image from one color space to another
    faces = detector.detectMultiScale(converted_image, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2) #used to draw a rectangle on any image
        count += 1

        
        # Construct the path for saving the face sample image
        face_img_path = os.path.join('samples', f"face.{face_id}.{count}.jpg")
        cv2.imwrite(face_img_path, converted_image[y:y + h, x:x + w])
        # To capture & Save images into the datasets folder

        cv2.imshow('image', img) #Used to display an image in a window

    k = cv2.waitKey(100) & 0xff # Waits for a pressed key
    if k == 27: # Press 'ESC' to stop
        break
    elif count >= 100: # Take 50 sample (More sample --> More accuracy)
         break

print("Samples taken now closing the program....")
cam.release()
cv2.destroyAllWindows()