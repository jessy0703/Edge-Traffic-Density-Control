import cv2
import os

# ===== CHANGE THESE PATHS IF NEEDED =====
dataset_paths = {
    "MVI_20011": "data/high.mp4",
    "MVI_20012": "data/medium.mp4"
}

def convert_images_to_video(image_folder, output_video):


    images = sorted([img for img in os.listdir(image_folder) if img.endswith(".jpg")])

    if not images:
        print(f"No images found in {image_folder}")
        return

    # Read first image
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, _ = frame.shape

    # Create video writer
    video = cv2.VideoWriter(output_video,
                            cv2.VideoWriter_fourcc(*'mp4v'),
                            10, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    video.release()
    print(f"Video saved: {output_video}")


# ===== MAIN =====
for folder, output in dataset_paths.items():
    print(f"\nProcessing folder: {folder}")
    convert_images_to_video(folder, output)

print("\n All videos created successfully!")