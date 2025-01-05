import cv2
import numpy as np

def play_videos_side_by_side(video1_path, video2_path):
    cap1 = cv2.VideoCapture(video1_path)
    cap2 = cv2.VideoCapture(video2_path)
    
    if not cap1.isOpened() or not cap2.isOpened():
        print("Error opening one or both videos")
        return

    # Get original frame rates and dimensions
    fps = cap1.get(cv2.CAP_PROP_FPS)
    frame_time = int((1/fps) * 1000)
    
    width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
    height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Smaller target height
    target_height = 480
    scale = target_height / height1
    
    # Calculate dimensions maintaining aspect ratio
    new_width1 = int(width1 * scale)
    new_height1 = int(height1 * scale)
    new_width2 = int(width2 * scale)
    new_height2 = int(height2 * scale)
    
    window_name = 'Video Comparison'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    combined_width = new_width1 + new_width2
    max_height = max(new_height1, new_height2)
    cv2.resizeWindow(window_name, combined_width, max_height)
    
    paused = False
    while True:
        if not paused:
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()
            
            if not ret1 or not ret2:
                break
            
            frame1 = cv2.resize(frame1, (new_width1, new_height1), interpolation=cv2.INTER_LANCZOS4)
            frame2 = cv2.resize(frame2, (new_width2, new_height2), interpolation=cv2.INTER_LANCZOS4)
            
            combined_frame = np.zeros((max_height, combined_width, 3), dtype=np.uint8)
            combined_frame[:new_height1, :new_width1] = frame1
            combined_frame[:new_height2, new_width1:new_width1+new_width2] = frame2
            
            # Adjusted font scale for smaller window
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
            
            cv2.imshow(window_name, combined_frame)
        
        key = cv2.waitKey(frame_time) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            paused = not paused
            print("Video paused" if paused else "Video playing")
        elif key == ord('s'):
            cv2.imwrite('comparison_frame.png', combined_frame)
            print("Frame saved as comparison_frame.png")
        
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

def main():
    video1_path = "test.mkv"
    video2_path = "output_video.mkv"
    
    print("\nVideo Comparison Controls:")
    print("- Space: Pause/Play")
    print("- Q: Quit")
    print("- S: Save current frame")
    print("\nStarting comparison...")
    
    play_videos_side_by_side(video1_path, video2_path)

if __name__ == "__main__":
    main()