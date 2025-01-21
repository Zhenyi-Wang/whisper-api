from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
import tempfile
import os
import torch
from typing import List, Dict
from pydantic import BaseModel
import uvicorn
from config import Config
import logging
from datetime import datetime
import time
from pydub import AudioSegment
from pydub.utils import mediainfo

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 加载配置
Config.load_from_env()

# API 模型
class TranscriptionResult(BaseModel):
    segments: List[Dict[str, float | str]]

# FastAPI 应用
app = FastAPI()

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Whisper 模型管理
class WhisperManager:
    _instance = None
    
    @classmethod
    def get_model(cls):
        if cls._instance is None:
            cls._instance = WhisperModel(
                model_size_or_path=Config.MODEL_PATH or Config.MODEL_SIZE,
                device=Config.DEVICE,
                compute_type=Config.COMPUTE_TYPE
            )
        return cls._instance

# 文件验证
async def validate_audio_file(file: UploadFile):
    if not file.content_type.startswith('audio/'):
        raise HTTPException(400, "文件类型必须是音频")

@app.post("/transcribe", response_model=TranscriptionResult)
async def transcribe_audio(file: UploadFile):
    start_time = time.time()
    logger.info(f"收到转写请求 - 文件名: {file.filename}, 类型: {file.content_type}, 大小: {len(await file.read())} bytes")
    await file.seek(0)  # 重置文件指针
    
    try:
        await validate_audio_file(file)
        logger.info("文件验证通过")
        
        # 保存文件到临时目录
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp:
            content = await file.read()
            temp.write(content)
            temp_path = temp.name
            logger.info(f"临时文件已保存: {temp_path}")
            
            # 获取音频信息
            audio_info = mediainfo(temp_path)
            duration = float(audio_info.get('duration', 0))
            logger.info(f"音频信息 - 时长: {duration:.2f}秒, 采样率: {audio_info.get('sample_rate', 'unknown')}Hz, 声道数: {audio_info.get('channels', 'unknown')}")
        
        try:
            # 直接处理音频
            logger.info("开始转写音频...")
            model = WhisperManager.get_model()
            segments, _ = model.transcribe(temp_path)
            
            result = TranscriptionResult(segments=[
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip()
                }
                for segment in segments
            ])
            
            end_time = time.time()
            process_time = end_time - start_time
            process_ratio = duration / process_time if process_time > 0 else 0
            
            logger.info(f"转写完成 - 共 {len(result.segments)} 个片段")
            logger.info(f"处理统计 - 音频时长: {duration:.2f}秒, 处理时间: {process_time:.2f}秒, 处理比: {process_ratio:.2f}x")
            
            return result
            
        except Exception as e:
            logger.error(f"转写过程发生错误: {str(e)}")
            raise HTTPException(500, "转写失败")
        finally:
            # 清理临时文件
            os.unlink(temp_path)
            logger.info("临时文件已清理")
            
    except HTTPException as e:
        logger.error(f"请求验证失败: {str(e.detail)}")
        raise
    except Exception as e:
        logger.error(f"处理请求时发生未知错误: {str(e)}")
        raise HTTPException(500, "服务器内部错误")

if __name__ == "__main__":
    uvicorn.run(app, host=Config.HOST, port=Config.PORT) 