
import cv2
import json
import os


def process_video(video_path, output_dir="outputs"):
    # Check whether the video file exists
    if not os.path.exists(video_path):
        print("Error: Video file not found.")
        return

    # Create the output folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the video
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Error: Could not open the video.")
        return

    # Read basic video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = total_frames / fps if fps > 0 else 0

    # Extract one frame approximately every second
    interval = max(1, round(fps)) if fps > 0 else 1
    extracted_frames = []
    frame_number = 0
    saved_count = 0

    while True:
        success, frame = video.read()

        if not success:
            break

        if frame_number % interval == 0:
            frame_path = os.path.join(
                output_dir, f"frame_{saved_count:04d}.jpg"
            )

            cv2.imwrite(frame_path, frame)
            extracted_frames.append(frame_path)
            saved_count += 1

        frame_number += 1

    # Release the video resource
    video.release()

    # Create a report
    report = {
        "video_path": video_path,
        "fps": fps,
        "total_frames": total_frames,
        "width": width,
        "height": height,
        "duration_seconds": round(duration, 2),
        "extracted_frames": len(extracted_frames),
        "frame_paths": extracted_frames
    }

    # Save the report as JSON
    report_path = os.path.join(output_dir, "video_report.json")

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("Video processing completed!")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Total frames: {total_frames}")
    print(f"Extracted frames: {saved_count}")
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    video_path = input("Enter the full path of your video: ").strip().strip('"')
    process_video(video_path)
