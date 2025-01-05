import cv2
import numpy as np
import os
from multiprocessing import Pool
from tqdm import tqdm
import subprocess

class VideoProcessor:
    def __init__(self, input_path, output_path, percentile_clip=2, chunk_size=100, n_processes=4):
        self.input_path = input_path
        self.output_path = output_path
        self.percentile_clip = percentile_clip
        self.chunk_size = chunk_size
        self.n_processes = n_processes
        self.temp_dir = "temp_frames"
        self.ffmpeg_path = r"C:\Users\hade\Downloads\ffmpeg.exe"
        
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
    
    def get_video_properties(self):
        cap = cv2.VideoCapture(self.input_path)
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

    def process_frame(self, frame):
        processed_frame = np.zeros_like(frame)
        for i in range(3):  # BGR channels
            channel = frame[:,:,i]
            
            # Calculate percentile values
            lower_bound = np.percentile(channel, self.percentile_clip)
            upper_bound = np.percentile(channel, 100 - self.percentile_clip)
            
            # Clip the channel values
            processed_channel = np.clip(channel, lower_bound, upper_bound)
            
            # Normalize to full range
            processed_channel = ((processed_channel - lower_bound) * 255 / 
                               (upper_bound - lower_bound)).astype(np.uint8)
            
            processed_frame[:,:,i] = processed_channel
        
        return processed_frame

    def process_chunk(self, chunk_info):
        start_frame, end_frame = chunk_info
        
        cap = cv2.VideoCapture(self.input_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        processed_frames = []
        for _ in range(end_frame - start_frame):
            ret, frame = cap.read()
            if not ret:
                break
            processed_frame = self.process_frame(frame)
            processed_frames.append(processed_frame)
        
        cap.release()
        return processed_frames

    def save_processed_video(self, processed_frames):
        temp_output = "temp_output.mkv"
        
        # First save video without audio - using exactly the same settings as before
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output, fourcc, self.fps, 
                            (self.width, self.height))
        
        for frame in tqdm(processed_frames, desc="Saving video"):
            out.write(frame)
        
        out.release()

        # Now copy the audio
        try:
            print("Copying audio stream...")
            command = [
                self.ffmpeg_path,
                '-i', temp_output,
                '-i', self.input_path,
                '-c:v', 'copy',
                '-c:a', 'copy',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-y',
                self.output_path
            ]
            subprocess.run(command, check=True)
            os.remove(temp_output)
            
        except subprocess.CalledProcessError as e:
            print(f"Error copying audio: {e}")
            os.rename(temp_output, self.output_path)

    def process_video(self):
        print("Starting video processing...")
        self.get_video_properties()
        
        chunks = []
        for start_frame in range(0, self.total_frames, self.chunk_size):
            end_frame = min(start_frame + self.chunk_size, self.total_frames)
            chunks.append((start_frame, end_frame))
        
        processed_frames = []
        with Pool(self.n_processes) as pool:
            chunk_results = list(tqdm(pool.imap(self.process_chunk, chunks), 
                                    total=len(chunks),
                                    desc="Processing chunks"))
            
            for chunk_result in chunk_results:
                processed_frames.extend(chunk_result)
        
        print("Saving processed video...")
        self.save_processed_video(processed_frames)
        print("Processing complete!")

    def cleanup(self):
        if os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)

def main():
    input_file = "test.mkv"
    output_file = "output_video.mkv"
    
    processor = VideoProcessor(
        input_path=input_file,
        output_path=output_file,
        percentile_clip=2,
        chunk_size=100,
        n_processes=4
    )
    
    try:
        processor.process_video()
    finally:
        processor.cleanup()

if __name__ == "__main__":
    main()