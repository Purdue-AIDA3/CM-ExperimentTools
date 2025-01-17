import os

def extract_last_frame_ffmpeg(video_path, output_image_path):
    command = f"ffmpeg -sseof -1 -i {video_path} -update 1 -q:v 1 {output_image_path}"
    os.system(command)

# Loop through the range of values for i and j
for i in range(1, 11):
    for j in (1, 3, 5):
        video_path = f"./Task_1/Task_1_{j}_{i}.mp4"
        output_image_path = f"./Task_1/Images/Task_1_{j}_{i}.png"
        if os.path.exists(video_path):
            extract_last_frame_ffmpeg(video_path, output_image_path)
        else:
            print(f"File {video_path} does not exist.")

print("Last frames extracted and saved as images for all videos.")
