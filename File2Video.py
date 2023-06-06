import argparse
import numpy as np
import math
import cv2

def get_frames(filename, frame_width, frame_height):
    with open(filename, 'rb') as file_obj:
        raw_bytes = file_obj.read()
        base_10 = list(raw_bytes)

        total_bytes = len(base_10)
        frame_size = frame_width * frame_height

        total_frames = math.ceil(total_bytes/frame_size)
        rounded_3_frames = total_frames + ((-1) * total_frames % 3)

        images = np.zeros((rounded_3_frames, frame_size), dtype='uint8')
        current_frame_index = 0

        while current_frame_index < total_frames:
            print(f'Parsing frame {current_frame_index + 1} / {total_frames}', end='\r')
            current_frame = \
                np.array(base_10[current_frame_index * frame_size:(current_frame_index + 1) * frame_size])
            current_frame_len = len(current_frame)
            images[current_frame_index, 0:current_frame_len] = current_frame
            current_frame_index += 1

        images = images.reshape((rounded_3_frames//3, frame_height, frame_width, 3))
        return images


def get_fake_frames(frame_width, frame_height):
    total_frames = 5
    frame_size = frame_width * frame_height
    rounded_3_frames = total_frames + ((-1) * total_frames % 3)
    images = np.zeros((rounded_3_frames, frame_size), dtype='uint8')

    images[0,0] = 255

    images = images.reshape((rounded_3_frames // 3, frame_height, frame_width, 3))
    return images


def write_video(video_frames, video_width, video_height, video_name, fps=10):
    # fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(video_name, 0, fps, (video_width, video_height))

    for frame in video_frames:
        video.write(frame)

    cv2.destroyAllWindows()
    video.release()


def write_frames(video_frames):
    count = 0
    total = len(video_frames)
    for frame in video_frames:
        print(f'Writing frame {count+1} / {total}', end='\r')
        cv2.imwrite(f'frames/frame_{count}.png', frame)
        count += 1


def decode_video(video_filename):
    video_capture = cv2.VideoCapture(video_filename)
    success, image = video_capture.read()
    raw_bytes = []
    while success:
        #raw_bytes = np.append(raw_bytes, image)
        raw_bytes.append(image)
        success, image = video_capture.read()

    return np.array(raw_bytes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='File2Video',
                                     description="Parsing binary file data into colour video.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("src", help="Source file location")
    parser.add_argument('-x', '--width', type=int, default=1920)
    parser.add_argument('-y', '--height', type=int, default=1080)
    args = parser.parse_args()
    config = vars(args)

    print("Source file:", args.src)
    print("Output dimensions:", args.width, "x", args.height)

    frames = get_frames(args.src, args.width, args.height)
    write_frames(frames)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
