import os
import cv2
import numpy as np
from loguru import logger
import matplotlib.pyplot as plt
import pandas as pd
import re


def extract_frames(video_path, save_images_path=None, target_fps=5):
    """
    :param video_path: path to mp4-file or folder containing mp4-files
    :param save_images_path: if given, images will be saved to this folder
    :param target_fps: number of frames to extract from each video
    :return: List of length #num_videos of tuples: (video_name, np-array of shape (#num_frames, W, H, 3 channels))
    """
    if video_path.endswith('.mp4'):  # single mp4-file
        video_paths = [video_path]
    else:  # folder containing mp4-files
        video_paths = [os.path.join(video_path, video_name) for video_name in os.listdir(video_path) if video_name.endswith('.mp4')]
    video_frames = []
    for video_path in video_paths:
        video = cv2.VideoCapture(video_path)
        fps = int(video.get(cv2.CAP_PROP_FPS))  # Get the frame rate of the video
        # print(fps)
        if video_path.split("/")[-1].startswith("usr"):  # 5-second video where user is speaking
            # times = [1, 2.5, 4]  # Set the time points to extract frames
            times = np.arange(0, 5, 1 / target_fps)
            print(times)
        else:  # bea talking video of any duration
            duration = get_video_duration(video)
            print(duration)
            if duration == 0:
                logger.error(f"Video {video_path} has duration 0. No frames can be extracted.")
                return []
            # times = calculate_frame_times(duration)
            times = np.arange(0, duration, 1 / target_fps)
            print(times)
            print(len(times))

        # Convert the time points to frame indices
        frames = [int(time * fps) for time in times]
        frames_list = []

        for frame_idx, seconds in enumerate(frames):
            # Set the frame index to read from the video
            video.set(cv2.CAP_PROP_POS_FRAMES, seconds)
            # Read the frame from the video
            ret, frame = video.read()

            if not ret:  # Check if the frame was successfully read
                print(f'Error reading frame at {seconds} seconds')
                continue

            frames_list.append(frame)

            if save_images_path:
                if not os.path.exists(save_images_path):
                    os.makedirs(save_images_path)
                img_name = f'{video_path[10:-4]}_frame_{str(frame_idx).zfill(3)}.png'
                save_path = os.path.join(save_images_path, img_name)
                print(save_path)

                # plt.imshow(frame)
                # plt.imsave(save_path, frame)
                if not cv2.imwrite(save_path, frame):
                    raise Exception("Could not write image")

        video.release()
        video_frames.append((video_path, np.array(frames_list)))
    return video_frames


def calculate_frame_times(duration):
    times = [duration * 0.25,
             duration * 0.5,
             duration * 0.75]
    print(times)
    return times


def get_video_duration(video):
    fps = video.get(cv2.CAP_PROP_FPS)
    frames = 0
    while True:
        # Read a frame from the input video
        ret, frame = video.read()
        # If there are no more frames, break out of the loop
        if not ret:
            break
        # Append the frame to the list
        frames += 1
    return frames / fps


def frame_data_df_from_folder(folder_path):
    """
    :param folder_path: path to folder containing images named in format:
            "bea-301-14215-11126-Q1_1-Q2_1-Q3_2_frame_060.png"
    :return: DataFrame with columns: video_name, frame_num, file_name, q1, q2, q3
    """
    file_names = os.listdir(folder_path)
    file_names = [file_name for file_name in file_names if file_name.endswith(".png")]
    file_names = sorted(file_names)

    df = pd.DataFrame(columns=["video_name", "frame_num", "file_name", "q1", "q2", "q3"])

    for file_name in file_names:
        match = re.search(r"(bea|usr)-(\d{1,4})-(\d{1,5})-(\d{1,5})-Q1_(\d)-Q2_(\d)-Q3_(\d)_frame_(\d{1,3})", file_name)
        print(match)
        if match:
            category = match.group(1)
            move_id = int(match.group(2))
            performed_move_id = int(match.group(3))
            session_id = int(match.group(4))
            q1 = int(match.group(5))
            q2 = int(match.group(6))
            q3 = int(match.group(7))
            frame_number = int(match.group(8))

            new_row = {"video_name": file_name[:-14] + ".mp4",
                            "frame_num": frame_number,
                            "file_name": file_name,
                            "q1": q1,
                            "q2": q2,
                            "q3": q3}
            df = pd.concat([df, pd.DataFrame([new_row])],
                           ignore_index=True)
    print(df)
    return df



if __name__ == '__main__':
    vid_path = "009-11126/bea-301-14215-11126-Q1_1-Q2_1-Q3_2.mp4"
    vid_path = "009-11126/bea-302-14217-11126-Q1_2-Q2_2-Q3_2.mp4"
    frame_folder = "frames"
    # frames = extract_frames(vid_path, save_images_path=frame_folder)
    train_df = frame_data_df_from_folder(frame_folder)
    train_df.to_csv("train_df.csv", index=False)


