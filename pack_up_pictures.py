import os
import shutil
from sklearn.model_selection import train_test_split

# 原始路径
jpg_base_dir = r"C:\Users\pc\Desktop\HANDS\SRTP\egohands_data\_LABELLED_SAMPLES"
png_base_dir = r"C:\Users\pc\Desktop\HANDS\SRTP\egohands_data\masks"
project_dir = r"C:\Users\pc\Desktop\HANDS\SRTP\HandSegmentationProject\data"

# 获取所有视频文件夹
video_dirs = [d for d in os.listdir(jpg_base_dir) if os.path.isdir(os.path.join(jpg_base_dir, d))]

# 收集所有帧
frame_pairs = []
for video_dir in video_dirs:
    jpg_dir = os.path.join(jpg_base_dir, video_dir)
    jpg_files = [f for f in os.listdir(jpg_dir) if f.endswith(".jpg")]
    for jpg_file in jpg_files:
        # 提取帧编号
        frame_num = jpg_file.split("frame_")[1].replace(".jpg", "")
        # 对应的掩码文件
        png_file = f"{video_dir}_frame_{frame_num}.png"
        if os.path.exists(os.path.join(png_base_dir, png_file)):
            frame_pairs.append((video_dir, jpg_file, png_file, frame_num))

# 划分数据集
train_pairs, test_val_pairs = train_test_split(frame_pairs, test_size=0.3, random_state=42)
val_pairs, test_pairs = train_test_split(test_val_pairs, test_size=0.5, random_state=42)

# 创建目标目录并移动文件
for split, pairs in [("train", train_pairs), ("val", val_pairs), ("test", test_pairs)]:
    img_dir = os.path.join(project_dir, split, "images")
    mask_dir = os.path.join(project_dir, split, "masks")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(mask_dir, exist_ok=True)
    
    for idx, (video_dir, jpg_file, png_file, frame_num) in enumerate(pairs):
        # 新文件名：frame_xxxx.jpg 和 frame_xxxx.png
        new_name = f"frame_{frame_num}"
        
        # 复制并重命名 .jpg 文件
        src_jpg = os.path.join(jpg_base_dir, video_dir, jpg_file)
        dst_jpg = os.path.join(img_dir, f"{new_name}.jpg")
        shutil.copy(src_jpg, dst_jpg)
        
        # 复制并重命名 .png 文件
        src_png = os.path.join(png_base_dir, png_file)
        dst_png = os.path.join(mask_dir, f"{new_name}.png")
        shutil.copy(src_png, dst_png)

print("数据集划分和重命名完成！")