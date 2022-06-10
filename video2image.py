import argparse
import cv2
import os
import shutil as st

st.rmtree("run/image")
os.mkdir("run/image")

parser = argparse.ArgumentParser(description='video to image')
parser.add_argument('video', type= str, help = 'input video')
args = parser.parse_args()



def video2image(source: str):
    input_video = None
    if source == "0":
        input_video = 0        
    else:
        try:
            with open(source, mode = 'r') as f:
                pass
        except:
            print("Đường dẫn ko đúng")
            return
        finally:
            source.replace('\\','/')
            input_video = source
    num_frame = 0
    video = cv2.VideoCapture(input_video)

    while video.isOpened():
        _, frame = video.read()
        if _ == True:
            cv2.imwrite("run/image/" + str(num_frame) + ".jpg", frame)
            num_frame+=1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()
    print("Done")
    with open("run/log.txt", mode = 'w') as f:
        f.write(str(num_frame))

if __name__ == "__main__":
    video2image(args.video)