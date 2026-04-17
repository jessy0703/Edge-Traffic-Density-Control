import time
import logging
import numpy as np

class AccuracyMetrics:
    def __init__(self, output_file='outputs/accuracy_report.txt'):
        """Initialize accuracy metrics tracker"""
        self.output_file = output_file
        
        # Configure logging
        logging.basicConfig(
            filename=output_file,
            level=logging.INFO,
            format='%(message)s',
            filemode='a'
        )
        self.logger = logging.getLogger(__name__)
        
        # Metrics storage
        self.vehicle_counts = []
        self.frame_times = []
        self.detection_confidences = []
        self.start_time = None
        self.frame_count = 0

    def start_video(self, video_name):
        """Start tracking for a new video"""
        self.vehicle_counts = []
        self.frame_times = []
        self.detection_confidences = []
        self.start_time = time.time()
        self.frame_count = 0
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Video: {video_name}")
        self.logger.info(f"{'='*60}")

    def log_frame(self, vehicle_count, frame_time, confidences):
        """Log metrics for a single frame"""
        self.frame_count += 1
        self.vehicle_counts.append(vehicle_count)
        self.frame_times.append(frame_time)
        
        if confidences:
            self.detection_confidences.extend(confidences)

    def end_video(self):
        """Calculate and log final metrics for the video"""
        if self.start_time is None or self.frame_count == 0:
            return
        
        total_time = time.time() - self.start_time
        
        # Calculate metrics
        avg_vehicle_count = np.mean(self.vehicle_counts)
        max_vehicle_count = np.max(self.vehicle_counts)
        min_vehicle_count = np.min(self.vehicle_counts)
        avg_fps = self.frame_count / total_time
        avg_frame_time = np.mean(self.frame_times) * 1000  # Convert to ms
        avg_confidence = np.mean(self.detection_confidences) if self.detection_confidences else 0.0
        
        # Log final metrics
        self.logger.info(f"Total Frames: {self.frame_count}")
        self.logger.info(f"Total Processing Time: {total_time:.2f}s")
        self.logger.info(f"Average FPS: {avg_fps:.2f}")
        self.logger.info(f"Average Frame Processing Time: {avg_frame_time:.2f}ms")
        self.logger.info(f"Average Detection Confidence: {avg_confidence:.4f}")
        self.logger.info(f"Average Vehicle Count: {avg_vehicle_count:.2f}")
        self.logger.info(f"Max Vehicle Count: {max_vehicle_count}")
        self.logger.info(f"Min Vehicle Count: {min_vehicle_count}")
        self.logger.info(f"✅ Video processing complete\n")

    def log_summary(self):
        """Log final summary"""
        self.logger.info(f"{'='*60}")
        self.logger.info("✅ All videos processed!")
        self.logger.info(f"{'='*60}\n")