from datetime import datetime
from dateutil import parser
import pandas as pd
import os

speaking_time = 5000  # milliseconds

bea_starts = [None, "2022-10-10 23:51:23.824681",
              "2022-10-04 06:35:32.843005", "2022-10-04 07:45:58.232266", "2022-10-04 09:18:28.973795", "2022-10-04 10:25:24.978192", "2022-10-04 23:27:10.042475", "2022-10-05 00:24:49.157567", "2022-10-05 01:16:47.691087", "2022-10-05 02:21:28.423826", "2022-10-05 03:28:27.895830", "2022-10-05 04:21:10.907666", "2022-10-05 05:33:35.358305", "2022-10-05 06:31:59.495532", "2022-10-05 08:12:15.830985", "2022-10-05 09:17:37.133063", "2022-10-05 10:29:22.229236", "2022-10-05 16:19:31.533232", "2022-10-07 00:45:30.668801", "2022-10-07 02:10:18.395357", "2022-10-07 03:27:55.567441", "2022-10-10 00:35:46.342257", "2022-10-10 01:34:03.736986", "2022-10-10 02:26:47.844728", "2022-10-10 03:39:40.442071", "2022-10-10 05:37:07.554478", "2022-10-10 06:53:20.585964", "2022-10-10 09:01:22.154357", "2022-10-10 10:05:55.763743", "2022-10-11 00:38:41.759374", "2022-10-11 01:40:32.650789", "2022-10-11 02:38:03.898111", "2022-10-11 03:41:07.482956", "2022-10-11 04:32:49.545932", "2022-10-11 05:44:06.713840", "2022-10-11 06:31:27.573744", "2022-10-11 07:31:37.057089", "2022-10-11 09:41:09.777241", "2022-10-11 10:37:10.506577", "2022-10-11 12:04:47.958980", "2022-10-12 00:42:51.210933", "2022-10-12 02:37:15.547141", "2022-10-12 03:34:10.894606", "2022-10-12 04:33:11.570775", "2022-10-12 05:40:52.412136", "2022-10-12 06:57:11.360052", "2022-10-12 07:55:30.004257", "2022-10-12 08:46:58.662112", "2022-10-12 09:44:07.808020", "2022-10-13 03:36:06.006796", "2022-10-13 04:35:55.541963", "2022-10-13 05:39:30.418795", "2022-10-13 06:42:09.926166", "2022-10-13 07:45:26.698035", "2022-10-13 08:36:48.351403", "2022-10-13 09:39:10.355389", "2022-10-13 23:49:34.592801", "2022-10-14 01:41:43.715322", "2022-10-14 02:39:10.118379", "2022-10-14 03:29:06.409728", "2022-10-14 05:31:36.075277"]
#bea_ms = [None, None,
#          1664865332843.005, 1664869558232.2659, 1664875108973.795, 1664879124978.1921, 1664926030042.475, 1664929489157.5671, 1664932607691.087, 1664936488423.826, 1664940507895.8298, 1664943670907.666, 1664948015358.305, 1664951519495.532, 1664957535830.985, 1664961457133.063, 1664965762229.2358, 1664986771533.232, 1665103530668.801, 1665108618395.357, 1665113275567.441, 1665362146342.257, 1665365643736.9858, 1665368807844.728, 1665373180442.071, 1665380227554.478, 1665384800585.9639, 1665392482154.357, 1665396355763.743, 1665445883824.6812, 1665448721759.374, 1665452432650.789, 1665455883898.111, 1665459667482.956, 1665462769545.9321, 1665467046713.84, 1665469887573.7441, 1665473497057.089, 1665481269777.241, 1665484630506.577, 1665489887958.98, 1665535371210.9329, 1665542235547.141, 1665545650894.6062, 1665549191570.7751, 1665553252412.136, 1665557831360.052, 1665561330004.257, 1665564418662.112, 1665567847808.02, 1665632166006.796, 1665635755541.9631, 1665639570418.7952, 1665643329926.166, 1665647126698.035, 1665650208351.403, 1665653950355.3892, 1665704974592.801, 1665711703715.322, 1665715150118.3792, 1665718146409.728, 1665725496075.277]
bea_ms = [None, 1665445883824.6812, 1664865332843.005, 1664869558232.2659, 1664875108973.795, 1664879124978.1921, 1664926030042.475, 1664929489157.5671, 1664932607691.087, 1664936488423.826, 1664940507895.8298, 1664943670907.666, 1664948015358.305, 1664951519495.532, 1664957535830.985, 1664961457133.063, 1664965762229.2358, 1664986771533.232, 1665103530668.801, 1665108618395.357, 1665113275567.441, 1665362146342.257, 1665365643736.9858, 1665368807844.728, 1665373180442.071, 1665380227554.478, 1665384800585.9639, 1665392482154.357, 1665396355763.743, 1665448721759.374, 1665452432650.789, 1665455883898.111, 1665459667482.956, 1665462769545.9321, 1665467046713.84, 1665469887573.7441, 1665473497057.089, 1665481269777.241, 1665484630506.577, 1665489887958.98, 1665535371210.9329, 1665542235547.141, 1665545650894.6062, 1665549191570.7751, 1665553252412.136, 1665557831360.052, 1665561330004.257, 1665564418662.112, 1665567847808.02, 1665632166006.796, 1665635755541.9631, 1665639570418.7952, 1665643329926.166, 1665647126698.035, 1665650208351.403, 1665653950355.3892, 1665704974592.801, 1665711703715.322, 1665715150118.3792, 1665718146409.728, 1665725496075.277]
bea_ends = ["no user 0","2022-10-10 00:25:23.824681","no end given", "2022-10-04 08:23:25.000000", "2022-10-04 09:55:00.000000", "2022-10-04 10:53:00.000000", "2022-10-04 23:58:30.928841", "2022-10-05 00:56:52.349608", "2022-10-05 01:47:42.624921", "2022-10-05 03:06:01.950011", "2022-10-05 03:58:18.778674", "2022-10-05 05:03:18.720814", "2022-10-05 06:09:07.001398", "2022-10-05 07:10:06.516911", "2022-10-05 08:53:36.225464", "2022-10-05 09:46:36.509484", "2022-10-05 11:13:02.741246", "no end given", "2022-10-07 01:37:30.668801", "2022-10-07 03:07:29.258887", "2022-10-07 03:55:21.487856", "2022-10-10 01:10:21.544025", "2022-10-10 02:01:58.076573", "2022-10-10 02:52:40.167385", "2022-10-10 04:21:21.989462", "2022-10-10 06:11:00.554478", "2022-10-10 07:28:58.175085", "2022-10-10 09:44:04.977379", "2022-10-10 10:46:44.373412", "2022-10-11 01:01:48.205845", "2022-10-11 02:21:12.991316", "2022-10-11 03:03:07.801661", "2022-10-11 04:09:56.897019", "2022-10-11 05:00:29.891634", "2022-10-11 06:08:54.110032", "2022-10-11 07:01:47.029348", "2022-10-11 07:59:10.530348", "2022-10-11 10:11:08.772134", "2022-10-11 11:15:48.802482", "2022-10-11 12:35:50.743650", "2022-10-12 01:12:30.665067", "2022-10-12 03:15:16.055730", "2022-10-12 04:07:40.217815", "2022-10-12 05:19:01.353502", "2022-10-12 06:13:16.707111", "2022-10-12 07:36:50.722787", "2022-10-12 08:29:35.824111", "2022-10-12 09:20:24.126476", "2022-10-12 10:08:30.640615", "2022-10-13 04:11:17.182111", "2022-10-13 05:00:19.488850", "2022-10-13 06:10:35.384587", "2022-10-13 07:10:59.577066", "2022-10-13 08:20:49.919933", "2022-10-13 09:08:27.422810", "2022-10-13 10:09:10.355389", "2022-10-14 00:21:34.592801", "2022-10-14 02:10:51.052432", "2022-10-14 03:10:51.082473", "2022-10-14 04:05:27.766141", "2022-10-14 06:10:22.632437"]
bea_ends_ms = ["no user 0", 1665361523824.6812,"no end given", 1664871805000.0, 1664877300000.0, 1664880780000.0, 1664927910928.841, 1664931412349.608, 1664934462624.9211, 1664939161950.011, 1664942298778.6738, 1664946198720.814, 1664950147001.3982, 1664953806516.9111, 1664960016225.464, 1664963196509.4841, 1664968382741.246, "no end given", 1665106650668.801, 1665112049258.887, 1665114921487.856, 1665364221544.025, 1665367318076.573, 1665370360167.385, 1665375681989.462, 1665382260554.478, 1665386938175.085, 1665395044977.3792, 1665398804373.4119, 1665450108205.8452, 1665454872991.3162, 1665457387801.6611, 1665461396897.0188, 1665464429891.634, 1665468534110.032, 1665471707029.348, 1665475150530.3481, 1665483068772.134, 1665486948802.482, 1665491750743.65, 1665537150665.067, 1665544516055.7302, 1665547660217.815, 1665551941353.502, 1665555196707.1108, 1665560210722.7869, 1665563375824.111, 1665566424126.476, 1665569310640.615, 1665634277182.111, 1665637219488.85, 1665641435384.5872, 1665645059577.066, 1665649249919.933, 1665652107422.81, 1665655750355.3892, 1665706894592.801, 1665713451052.4321, 1665717051082.4731, 1665720327766.1409, 1665727822632.437]
users = {
    11055: 2,
    11058: 3,
    11065: 4,
    11074: 5,
    11110: 6,
    11115: 7,
    11120: 8,
    11126: 9,
    11127: 10,
    11133: 11,
    11139: 12,
    11147: 13,
    11150: 14,
    11159: 15,
    11163: 16,
    11187: 17,
    11341: 18,
    11363: 19,
    11365: 20,
    11376: 21,
    11384: 22,
    11388: 23,
    11392: 24,
    11402: 25,
    11409: 26,
    11426: 27,
    11439: 28,
    11491: 1,
    11496: 29,
    11506: 30,
    11510: 31,
    11515: 32,
    11521: 33,
    11530: 34,
    11536: 35,
    11539: 36,
    11546: 37,
    11551: 38,
    11562: 39,
    11609: 40,
    11613: 41,
    11620: 42,
    11628: 43,
    11637: 44,
    11646: 45,
    11654: 46,
    11658: 47,
    11664: 48,
    11781: 49,
    11793: 50,
    11794: 51,
    11799: 52,
    11804: 53,
    11810: 54,
    11813: 55,
    11857: 56,
    11864: 57,
    11870: 58,
    11874: 59,
    11881: 60
}
input_video_names = []
t1s = []
t2s = []
t3s = []



def date_to_ms(date):
    #t = datetime.astimezone(timezone.utc).strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    #t = datetime(*time.strptime(date, "%Y-%m-%d %H:%M:%S")[0:6])
    t=parser.parse(date+" GMT")
    return t.timestamp() * 1000


def time_from_start(startms, timems):
    return datetime.fromtimestamp((timems-startms)/1000)-datetime.fromtimestamp(0)


def print_mclick_times(user, video_start=None):
    """
    :param user: user number
    :param video_start: if given, timestamp in original video and cut video will be given
    :return: None
    """
    if user>60:
        user = users[user]
    timelist=t3s[user]
    bea_start_ms=bea_ms[user]
    print("=== Printing User Starts Talking Timestamps (Participant "+str(user).zfill(3)+") ===")
    if video_start:
        for t in timelist:
            tfs = time_from_start(bea_start_ms, t-speaking_time)
            print("old:", str((tfs+video_start).strftime("%H:%M:%S.%f")), "\t new:",str(tfs))
    else:
        for t in timelist:
            print(time_from_start(bea_start_ms, t-speaking_time))
    print("=================================================================")


def calc_vid_start(user, click_time, t3_millis, print_command=True, print_mclicks=True):
    """Calculates the bea start point in a video from an identified mouseclick in the video.

    Args:
        user (int): Accepts user number or session_id
        click_time (String): Video timestamp of the mouse click in the format "HH:MM:SS"
        t3_millis (int): Timestamp of the identified mouseclick from session data in UNIX time, e.g. 1664926163248
        print_command (bool): Whether the Video Start is to be printed
        print_mclicks (bool):
    """
    if user>60:
        user = users[user]
    bea_start = bea_ms[user]
    delta = time_from_start(bea_start, t3_millis - speaking_time)
    click_time = datetime.strptime(click_time, "%H:%M:%S")
    video_start = click_time-delta
    if print_command:
        print_trim_command(user, video_start)
    if print_mclicks:
        print_mclick_times(user, video_start)
    return video_start


def print_trim_command(user, video_start):
    if user>60:
        user = users[user]
    duration = time_from_start(bea_ms[user], bea_ends_ms[user])
    video_end = video_start+duration
    print(
        "ffmpeg -ss "+
        str(video_start.strftime("%H:%M:%S"))+
        " -to "+
        str(video_end.strftime("%H:%M:%S"))+
        " -i {} -c copy ".format(input_video_names[user-1] if len(input_video_names)==60 else "x.mp4")+
        str(user).zfill(3)+ "-"+ str(get_key_from_value(users, user))+
        ".mp4"
    )


def create_millis_arrays():
    df = pd.read_csv("dialogue_feedback_with_session.csv", skipinitialspace=True,
                     usecols=['t1_millis','t2_millis','t3_millis', 'session_id'])
    df = df.sort_values('t3_millis')
    arr1 = []
    arr2 = []
    arr3 = []
    for i in range(61):
        arr1.append([])
        arr2.append([])
        arr3.append([])
    for session, user in users.items():
        arr1[user] = df.loc[df['session_id'] == session]['t1_millis'].to_list()
        arr2[user] = df.loc[df['session_id'] == session]['t2_millis'].to_list()
        arr3[user] = df.loc[df['session_id'] == session]['t3_millis'].to_list()
    return arr1, arr2, arr3


def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None

def split_video(user):
    if user>60:
        user = users[user]
    folder_name = str(user).zfill(3) + "-" + str(get_key_from_value(users, user))
    vid_name = folder_name + ".mp4"
    vid_dir = "/Users/jonas/Movies/BEA-Videos/cut"
    vid_path = vid_dir + "/" + vid_name
    if not os.path.exists(vid_path):
        print("Video not found")
        return None
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        user_input = input('Folder already exists. Do you want to overwrite? (y/n): ')
        if user_input.lower() != 'y':
            return None
    print("doing stuff")
    df = pd.read_csv("dialogue_feedback_with_session.csv", skipinitialspace=True)
    df = df.loc[df['session_id'] == get_key_from_value(users, user)]
    df = df.sort_values('t1_millis')  # actually shouldn't matter if sort by id, or any timestamp column
    bea_start = bea_ms[user]
    df['t1_millis'] = df['t1_millis'] - bea_start
    df['t2_millis'] = df['t2_millis'] - bea_start
    df['t3_millis'] = df['t3_millis'] - bea_start
    commands = []
    for index, row in df.iterrows():
        bea_part_start = str(datetime.utcfromtimestamp(row['t1_millis'] / 1000).strftime("%H:%M:%S"))
        bea_part_end = str(datetime.utcfromtimestamp(row['t2_millis'] / 1000).strftime("%H:%M:%S"))
        user_part_start = str(datetime.utcfromtimestamp(row['t3_millis'] / 1000 - 5).strftime("%H:%M:%S"))
        user_part_end = str(datetime.utcfromtimestamp(row['t3_millis'] / 1000).strftime("%H:%M:%S"))
        # bea speaking
        commands.append("ffmpeg -ss " +
                        bea_part_start +
                        " -to " +
                        user_part_start +  # includes time user thinks/processing beas argument until clicking to answer
                        " -i " + vid_path +
                        " -c copy " + folder_name + "/" + "bea-" +
                        str(int(row['id'])) + "-" + str(int(row['performed_move_id'])) + "-" + str(int(row['session_id']))+
                        "-Q1_" + str(int(row['question_one'])) +
                        "-Q2_" + str(int(row['question_two'])) +
                        "-Q3_" + str(int(row['question_three'])) +
                        ".mp4")
        # user speaking
        commands.append("ffmpeg -ss " +
                        user_part_start +
                        " -to " +
                        user_part_end +
                        " -i " + vid_path +
                        " -c copy " + folder_name + "/" + "usr-" +
                        str(int(row['id'])) + "-" + str(int(row['performed_move_id'])) + "-" + str(int(row['session_id']))+
                        "-Q1_" + str(int(row['question_one'])) +
                        "-Q2_" + str(int(row['question_two'])) +
                        "-Q3_" + str(int(row['question_three'])) +
                        ".mp4")
    for command in commands:
        os.system(command)


if __name__ == '__main__':

    bea_video_path = '/Users/jonas/Movies/BEA-Videos'
    file_names = [f for f in os.listdir(bea_video_path) if f.endswith('２０２２.mp4')]
    file_names.sort()
    print(len(file_names), "mp4-files in folder")  #, file_names)
    input_video_names=file_names

    t1s, t2s, t3s = create_millis_arrays()
    # calc_vid_start(6, "00:13:03", 1664926163248, True)
    # calc_vid_start(7, "00:12:13", 1664929671091, True)  # 1s late
    # calc_vid_start(7, "00:12:14", 1664929671091, True)
    # calc_vid_start(8, "00:05:28", 1664932948069, True)
    # calc_vid_start(9, "00:27:44", 1664937293817, True) # 2s late
    # calc_vid_start(9, "00:27:46", 1664937293817, True)
    # calc_vid_start(10, "00:04:37", 1664940776603, True) #1s late
    # calc_vid_start(10, "00:04:38", 1664940776603, True)
    # calc_vid_start(11, "00:09:41", 1664944065813, True) # 1s late
    # calc_vid_start(11, "00:09:42", 1664944065813, True)
    # calc_vid_start(15, "00:17:12", 1664961815381, True) # 2s late
    # calc_vid_start(15, "00:17:14", 1664961815381, True)
    # calc_vid_start(16, "00:14:29", 1664966044062, True)
    # calc_vid_start(20, "00:10:19", 1665113477027, True)
    # calc_vid_start(21, "00:15:30", 1665362317978, True)
    # calc_vid_start(22, "00:05:00", 1665365764399)
    # calc_vid_start(23, "00:08:30", 1665369048496)
    # calc_vid_start(24, "00:23:23", 1665373310384)
    # calc_vid_start(27, "00:09:07", 1665392621583)
    # calc_vid_start(28, "00:09:01", 1665396729110)
    # calc_vid_start(1, "00:12:47", 1665446215966)
    # calc_vid_start(29, "00:06:49", 1665448915367)
    # calc_vid_start(30, "00:20:19", 1665452638896)
    # calc_vid_start(31, "00:03:58", 1665455991577)
    # calc_vid_start(32, "00:30:55", 1665459812274)
    # calc_vid_start(33, "00:05:10", 1665462968357)
    # calc_vid_start(34, "00:07:20", 1665467364585)
    # calc_vid_start(35, "00:08:32", 1665470184176)
    # calc_vid_start(36, "00:19:15", 1665473863481)
    # calc_vid_start(37, "00:24:31", 1665481524958) # a bit too early like this
    # calc_vid_start(37, "00:25:07", 1665481509648)
    # calc_vid_start(38, "00:08:20", 1665484832856, True)
    # calc_vid_start(39, "00:15:36", 1665490325197, True)  # a bit late
    # calc_vid_start(40, "00:24:12", 1665535499710, True)
    # calc_vid_start(41, "00:34:22", 1665543229014, True)
    # calc_vid_start(42, "00:20:41", 1665546977602, True)
    # calc_vid_start(43, "00:06:52", 1665550514316, True)
    # calc_vid_start(44, "00:06:52", 1665553388592, True)
    # calc_vid_start(45, "00:14:10", 1665558028545, True)
    # calc_vid_start(45, "00:13:28", 1665557985901, True)
    # calc_vid_start(46, "00:11:49", 1665561726574, True)  # below is better
    # calc_vid_start(46, "00:11:12", 1665561689516, True)
    # calc_vid_start(47, "00:10:29", 1665564825962, True)
    # calc_vid_start(47, "00:15:12", 1665565108640, True)  # bit too early
    # calc_vid_start(47, "00:21:19", 1665565476424, True)
    # calc_vid_start(48, "00:16:51", 1665568339555, True)
    # calc_vid_start(49, "00:21:00", 1665632570727, True)
    # calc_vid_start(50, "00:18:25", 1665635874663, True)
    # calc_vid_start(50, "00:18:57", 1665635906433, True)
    # calc_vid_start(51, "00:24:28", 1665639815906, True)
    # calc_vid_start(51, "00:30:03", 1665640149772, True)
    # calc_vid_start(52, "00:15:36", 1665644083545, True)
    # calc_vid_start(52, "00:14:50", 1665644036396, True)
    # calc_vid_start(53, "00:34:34", 1665648303534, True)
    # calc_vid_start(54, "00:26:37", 1665651569534, True)
    # calc_vid_start(55, "00:22:07", 1665654187084, True)
    # calc_vid_start(56, "00:21:27", 1665705250641, True)
    # calc_vid_start(57, "00:42:33", 1665712122486, True)
    # calc_vid_start(58, "00:19:32", 1665715999040, True)
    # calc_vid_start(59, "00:19:35", 1665718907344, True)
    calc_vid_start(60, "00:28:48", 1665726204449, True)


    # split_video(10)
