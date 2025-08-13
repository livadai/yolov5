import cv2
import os
import argparse

def resize_and_pad(img, target_size=640):
    """Resize image to target_size x target_size, keeping aspect ratio and padding if needed."""
    h, w = img.shape[:2]
    scale = min(target_size / h, target_size / w)
    new_h, new_w = int(h * scale), int(w * scale)
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # Pad to [target_size, target_size]
    top = (target_size - new_h) // 2
    bottom = target_size - new_h - top
    left = (target_size - new_w) // 2
    right = target_size - new_w - left
    padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)
    return padded

def main(input_dir, output_dir, target_size=640):
    os.makedirs(output_dir, exist_ok=True)
    img_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    for img_file in img_files:
        img_path = os.path.join(input_dir, img_file)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Warning: Could not read {img_path}, skipping...")
            continue

        # Resize + pad
        processed_img = resize_and_pad(img, target_size)
        
        # Save
        output_path = os.path.join(output_dir, img_file)
        cv2.imwrite(output_path, processed_img)
        print(f"Processed: {img_file} -> {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize images to 640x640 for calibration")
    parser.add_argument("--input-dir", required=True, help="Directory containing input images")
    parser.add_argument("--output-dir", required=True, help="Directory to save resized images")
    parser.add_argument("--target-size", type=int, default=640, help="Target width/height (default: 640)")
    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.target_size)