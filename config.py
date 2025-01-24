import os
from typing import Optional
import torch
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Config:
    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Whisper 配置
    MODEL_SIZE: str = "base"  # tiny, base, small, medium, large
    MODEL_PATH: Optional[str] = None  # 如果为 None，则使用默认下载路径
    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"
    COMPUTE_TYPE: str = "float16" if torch.cuda.is_available() else "float32"
    
    # 繁简转换配置
    CONVERT_TO_SIMPLIFIED: bool = True  # 是否将繁体转换为简体
    
    # 从环境变量加载配置
    @classmethod
    def load_from_env(cls):
        cls.HOST = os.getenv("WHISPER_HOST", cls.HOST)
        cls.PORT = int(os.getenv("WHISPER_PORT", cls.PORT))
        cls.MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", cls.MODEL_SIZE)
        cls.MODEL_PATH = os.getenv("WHISPER_MODEL_PATH", cls.MODEL_PATH)
        cls.DEVICE = os.getenv("WHISPER_DEVICE", cls.DEVICE)
        cls.COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", cls.COMPUTE_TYPE)
        cls.CONVERT_TO_SIMPLIFIED = os.getenv("WHISPER_CONVERT_TO_SIMPLIFIED", "true").lower() == "true" 