import cv2
import numpy as np

def create_comparison_video(video1_path, video2_path, output_path, target_height=360):  # Reduced height
    cap1 = cv2.VideoCapture(video1_path)
    cap2 = cv2.VideoCapture(video2_path)
    
    if not cap1.isOpened() or not cap2.isOpened():
        print("Error opening one or both videos")
        return

    # Force 25 fps
    fps = 25
    width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
    height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    scale = target_height / height1
    new_width1 = int(width1 * scale)
    new_height1 = int(height1 * scale)
    new_width2 = int(width2 * scale)
    new_height2 = int(height2 * scale)
    
    combined_width = new_width1 + new_width2
    max_height = max(new_height1, new_height2)

    # Create temporary video with lower quality
    temp_output = "temp_comparison.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_output, fourcc, fps, (combined_width, max_height))
    
    window_name = 'Video Comparison (Recording)'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, combined_width, max_height)
    
    total_frames = min(int(cap1.get(cv2.CAP_PROP_FRAME_COUNT)), 
                      int(cap2.get(cv2.CAP_PROP_FRAME_COUNT)))
    
    print(f"\nProcessing {total_frames} frames at 25 FPS...")
    for frame_count in range(total_frames):
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        
        if not ret1 or not ret2:
            break
            
        frame1 = cv2.resize(frame1, (new_width1, new_height1), interpolation=cv2.INTER_LANCZOS4)
        frame2 = cv2.resize(frame2, (new_width2, new_height2), interpolation=cv2.INTER_LANCZOS4)
        
        combined_frame = np.zeros((max_height, combined_width, 3), dtype=np.uint8)
        combined_frame[:new_height1, :new_width1] = frame1
        combined_frame[:new_height2, new_width1:new_width1+new_width2] = frame2
        
        font_scale = scale * 0.8
        thickness = max(1, int(1.5 * scale))
        cv2.putText(combined_frame, 'Original', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        cv2.putText(combined_frame, 'Processed', (new_width1 + 10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        
        cv2.line(combined_frame, 
                (new_width1, 0), 
                (new_width1, max_height), 
                (255, 255, 255), 
                thickness)
        
        out.write(combined_frame)
        cv2.imshow(window_name, combined_frame)
        
        if frame_count % 30 == 0:
            progress = (frame_count + 1) / total_frames * 100
            print(f"Progress: {progress:.1f}%", end='\r')
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    print("\nCompressing final video...")
    
    # Cleanup initial write
    out.release()
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

    # Compress using FFmpeg
    import subprocess
    try:
        command = [
            'ffmpeg',
            '-i', temp_output,
            '-c:v', 'libx264',
            '-crf', '28',  # Higher compression
            '-preset', 'slower',  # Better compression
            '-r', '25',  # Force 25 fps
            '-y',
            output_path
        ]
        subprocess.run(command, check=True)
        import os
        os.remove(temp_output)
    except subprocess.CalledProcessError as e:
        print(f"Error compressing video: {e}")
        os.rename(temp_output, output_path)

    print("Processing complete!")

def main():
    input_file = "test.mkv"
    processed_file = "output_video.mkv"
    comparison_output = "comparison.mp4"
    
    print("\nCreating comparison video...")
    print("Press 'Q' to stop early")
    
    create_comparison_video(
        input_file,
        processed_file,
        comparison_output,
        target_height=360  # Reduced height for smaller file
    )

if __name__ == "__main__":
    main()