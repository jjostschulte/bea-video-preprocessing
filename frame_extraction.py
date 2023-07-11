import os
import cv2
import numpy as np
from loguru import logger
import matplotlib.pyplot as plt
import pandas as pd
import re
import datetime
from split_data import train_dev_test_split


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
        logger.info(f"Extracting frames from {video_path}")
        video = cv2.VideoCapture(video_path)
        fps = int(video.get(cv2.CAP_PROP_FPS))  # Get the frame rate of the video
        # print(fps)
        if video_path.split("/")[-1].startswith("usr"):  # 5-second video where user is speaking
            # times = [1, 2.5, 4]  # Set the time points to extract frames
            times = np.arange(0, 5, 1 / target_fps)
        else:  # bea talking video of any duration
            duration = get_video_duration(video)
            if duration == 0:
                logger.error(f"Video {video_path} has duration 0. No frames can be extracted.")
                return []
            # times = calculate_frame_times(duration)
            times = np.arange(0, duration, 1 / target_fps)

        # Convert the time points to frame indices
        frames = [int(time * fps) for time in times]
        frames_list = []

        for frame_idx, seconds in enumerate(frames):
            # Set the frame index to read from the video
            video.set(cv2.CAP_PROP_POS_FRAMES, seconds)
            # Read the frame from the video
            ret, frame = video.read()

            if not ret:  # Check if the frame was successfully read
                logger.error(f'Error reading frame at {seconds} seconds')
                continue

            frames_list.append(frame)

            if save_images_path:
                if not os.path.exists(save_images_path):
                    os.makedirs(save_images_path)
                img_name = f'{video_path[23:-4]}_frame_{str(frame_idx).zfill(3)}.png'
                save_path = os.path.join(save_images_path, img_name)
                # print(save_path)

                # plt.imshow(frame)
                # plt.imsave(save_path, frame)
                if not cv2.imwrite(save_path, frame):
                    raise Exception(f"Could not write image to {save_path}")

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
    return df


def get_all_user_folders(root_folder="."):
    """
    :return: list of all user folders in the dataset
    """
    all_folders = os.listdir(root_folder)
    user_folders = [root_folder + "/" + folder for folder in all_folders if folder.startswith("0")]
    return sorted(user_folders)


def extract_all_frames(frame_target_folder, video_folder=".", exclude_videos=None, user_folders=None):
    """
    Create all frames for all videos in the dataset
    :return: void
    """
    if user_folders is None:
        user_folders = get_all_user_folders(video_folder)
    else:
        user_folders = [video_folder + "/" + folder for folder in user_folders]
    logger.info(f"Processing folders: {user_folders}")
    for user_folder in user_folders:
        logger.info(f"Processing user folder {user_folder}")
        video_paths = [os.path.join(user_folder, video_name) for video_name in os.listdir(user_folder) if video_name.endswith('.mp4')]
        for video_path in sorted(video_paths):
            if video_path in exclude_videos:
                logger.info(f"Skipping video {video_path}")
                continue
            # save frames to folder
            extract_frames(video_path, save_images_path=frame_target_folder)


if __name__ == '__main__':
    vid_path = "009-11126/bea-301-14215-11126-Q1_1-Q2_1-Q3_2.mp4"
    vid_path = "009-11126/bea-302-14217-11126-Q1_2-Q2_2-Q3_2.mp4"
    frame_folder = "frames" + datetime.datetime.now().strftime("%m%d-%H%M")
    # frames = extract_frames(vid_path, save_images_path=frame_folder)

    videos_to_exclude = pd.read_csv("ignore-videos.txt", header=None)[0].tolist()

    # print(get_all_user_folders("preprocessed"))

    frame_folder = "/Volumes/Crucial X6/denis/train2"
    train_users, dev_users, test_users = train_dev_test_split()

    # extract train frames
    #extract_all_frames(frame_folder, video_folder="preprocessed", exclude_videos=videos_to_exclude,
    #                   user_folders=train_users)

    #train_df = frame_data_df_from_folder(frame_folder)
    #train_df.to_csv(os.path.join(frame_folder, f"train.csv"), index=False)

    # extract dev frames
    dev_folder = "/Volumes/Crucial X6/denis/dev"
    logger.info(f"Extracting dev frames to {dev_folder}")
    extract_all_frames(dev_folder, video_folder="preprocessed", exclude_videos=videos_to_exclude,
                       user_folders=dev_users)
    dev_df = frame_data_df_from_folder(dev_folder)
    dev_df.to_csv(os.path.join(dev_folder, f"dev.csv"), index=False)

    # extract test frames
    test_folder = "/Volumes/Crucial X6/denis/test"
    logger.info(f"Extracting test frames to {test_folder}")
    extract_all_frames(test_folder, video_folder="preprocessed", exclude_videos=videos_to_exclude,
                       user_folders=test_users)
    test_df = frame_data_df_from_folder(test_folder)
    test_df.to_csv(os.path.join(test_folder, f"test.csv"), index=False)

    # frame_folder = "frames0707-1517"
    # extract_all_frames(frame_folder)
