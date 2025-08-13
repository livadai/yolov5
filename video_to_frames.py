import cv2
import os
import argparse

def video_to_frames(video_path, output_dir, frame_interval=1, img_format='jpg', resize=None):
    """
    将视频抽帧保存为图像（文件名格式化为001.jpg, 002.jpg等）
    :param video_path: 视频文件路径
    :param output_dir: 输出目录
    :param frame_interval: 抽帧间隔（每隔几帧取一帧）
    :param img_format: 输出图像格式（jpg/png等）
    :param resize: 可选，调整尺寸 (width, height)
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: 无法打开视频文件 {video_path}")
        return
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps
    
    print(f"视频信息: {total_frames}帧, {fps:.2f}FPS, 时长: {duration:.2f}秒")
    print(f"开始抽帧，间隔: 每{frame_interval}帧抽取1帧...")
    
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            # 调整尺寸（如果指定）
            if resize is not None:
                frame = cv2.resize(frame, resize)
            
            # 保存图像（使用三位数编号）
            img_name = f"{saved_count+1:03d}.{img_format}"  # 001, 002,...格式
            img_path = os.path.join(output_dir, img_name)
            cv2.imwrite(img_path, frame)
            saved_count += 1
            
            # 打印进度
            if saved_count % 100 == 0:
                print(f"已保存 {saved_count} 张图像 (处理到第 {frame_count}/{total_frames} 帧)")
        
        frame_count += 1
    
    cap.release()
    print(f"抽帧完成！共保存 {saved_count} 张图像到 {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='视频抽帧工具（输出文件名格式化为001.jpg, 002.jpg等）')
    parser.add_argument('video_path', type=str, help='输入视频文件路径')
    parser.add_argument('output_dir', type=str, help='输出目录')
    parser.add_argument('--interval', type=int, default=1, help='抽帧间隔（默认每帧都取）')
    parser.add_argument('--format', type=str, default='jpg', choices=['jpg', 'png'], help='输出图像格式')
    parser.add_argument('--width', type=int, default=None, help='输出图像宽度')
    parser.add_argument('--height', type=int, default=None, help='输出图像高度')
    
    args = parser.parse_args()
    
    resize = None
    if args.width and args.height:
        resize = (args.width, args.height)
    
    video_to_frames(
        video_path=args.video_path,
        output_dir=args.output_dir,
        frame_interval=args.interval,
        img_format=args.format,
        resize=resize
    )