import os

from gym.wrappers.monitoring import video_recorder
from gym import logger
from .vec_env import VecEnvWrapper


class VecVideoRecorder(VecEnvWrapper):
    """
    Wrap VecEnv to record rendered image as mp4 video.
    """

    def __init__(
        self,
        venv,
        directory,
        record_video_trigger,
        file_prefix="vecenv",
        video_length=200,
    ):
        """
        # Arguments
            venv: VecEnv to wrap
            directory: Where to save videos
            record_video_trigger:
                Function that defines when to start recording.
                The function takes the current number of step,
                and returns whether we should start recording or not.
            video_length: Length of recorded video
        """
        
        VecEnvWrapper.__init__(self, venv)
        self.record_video_trigger = record_video_trigger
        self.video_recorder = None

        self.directory = os.path.abspath(directory)
        os.makedirs(self.directory, exist_ok=True)

        self.file_prefix = file_prefix
        self.file_infix = "{}".format(os.getpid())
        self.step_id = 0
        self.video_length = video_length

        self.recording = False
        self.recorded_frames = 0

    def reset(self):
        # print(f"In VecVideoRecorder::reset before venv.reset()")
        obs = self.venv.reset()

        print(f"In VecVideoRecorder::reset before start_video_recorder()")
        self.start_video_recorder()
        print(f"In VecVideoRecorder::reset after start_video_recorder()")

        return obs

    def start_video_recorder(self):
        self.close_video_recorder()
        # print(f"In VecVideoRecorder::start_video_recorder after close_video_recorder()")

        base_path = os.path.join(
            self.directory, "{}_video".format(self.file_prefix)
        )
        self.video_recorder = video_recorder.VideoRecorder(
            env=self.venv, base_path=base_path, metadata={"step_id": self.step_id}
        )
        print(f"In VecVideoRecorder::start_video_recorder before video_recorder.capture_frame()")
        self.video_recorder.capture_frame()
        print(f"In VecVideoRecorder::start_video_recorder after video_recorder.capture_frame()")
        self.recorded_frames = 1
        self.recording = True

    def _video_enabled(self):
        return self.record_video_trigger(self.step_id)

    def step_wait(self):
        obs, rews, dones, infos = self.venv.step_wait()

        self.step_id += 1
        if self.recording:
            self.video_recorder.capture_frame()
            self.recorded_frames += 1
            if self.recorded_frames > self.video_length:
                self.close_video_recorder()
        elif self._video_enabled():
            self.start_video_recorder()

        return obs, rews, dones, infos

    def close_video_recorder(self):
        if self.recording:
            self.video_recorder.close()
        self.recording = False
        self.recorded_frames = 0

    def close(self):
        VecEnvWrapper.close(self)
        self.close_video_recorder()

    def __del__(self):
        self.close()
