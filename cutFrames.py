import cv2
import os, shutil


# code to delete all files from the directory
folder = 'frames/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



# Opens video to cut it into frames.
cap = cv2.VideoCapture("video/2021_11_05_12_08_54.h264")
i = 0

while (cap.isOpened()):
    ret, frame = cap.read()

    # This condition prevents from infinite looping
    # incase video ends.
    if ret == False:
        break

    # Save Frame by Frame into disk using imwrite method
    if (i % 10 == 0):
        cv2.imwrite('frames/Frame' + str(i) + '.jpg', frame)

    i += 1


cap.release()
cv2.destroyAllWindows()
