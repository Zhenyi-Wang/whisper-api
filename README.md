# Whisper ASR 服务

这是一个基于 Faster-Whisper 的语音识别服务，提供简单的 REST API 接口进行音频转写。

## 功能特点

- 基于 Faster-Whisper 的高效语音识别
- 支持多种音频格式
- 简单的 REST API 接口
- 支持 GPU 加速
- 灵活的配置选项
- 详细的处理日志

## 快速开始

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置服务
```bash
# 复制配置文件模板
cp .env.example .env

# 编辑配置文件
vim .env
```

3. 运行服务
```bash
python main.py
```

服务将在 http://localhost:8000 启动

## API 使用

### 音频转写

**请求**:
- URL: `/transcribe`
- 方法: `POST`
- Content-Type: `multipart/form-data`
- 参数: `file` (音频文件)

**响应**:
```json
{
    "segments": [
        {
            "start": 0.0,
            "end": 2.5,
            "text": "转写的文本内容"
        }
    ]
}
```

## 日志输出

服务会记录详细的处理日志，包括：

1. 请求信息
   - 文件名、类型、大小
   - 请求时间

2. 音频信息
   - 音频时长
   - 采样率
   - 声道数

3. 处理统计
   - 音频总时长
   - 实际处理时间
   - 处理比（>1 表示快于实时）

示例日志：
```
2024-xx-xx HH:MM:SS - INFO - 收到转写请求 - 文件名: test.wav, 类型: audio/wav, 大小: 1234567 bytes
2024-xx-xx HH:MM:SS - INFO - 文件验证通过
2024-xx-xx HH:MM:SS - INFO - 音频信息 - 时长: 60.50秒, 采样率: 44100Hz, 声道数: 2
2024-xx-xx HH:MM:SS - INFO - 开始转写音频...
2024-xx-xx HH:MM:SS - INFO - 转写完成 - 共 15 个片段
2024-xx-xx HH:MM:SS - INFO - 处理统计 - 音频时长: 60.50秒, 处理时间: 15.20秒, 处理比: 3.98x
```

## 配置选项

服务配置支持两种方式：环境变量或 .env 文件。推荐使用 .env 文件进行配置。

### .env 配置文件

项目提供了配置文件模板 `.env.example`：

```bash
# 服务配置
WHISPER_HOST=0.0.0.0
WHISPER_PORT=8000

# 模型配置
WHISPER_MODEL_SIZE=base
#WHISPER_MODEL_PATH=/path/to/model  # 可选，自定义模型路径
WHISPER_DEVICE=cuda  # 或 cpu
WHISPER_COMPUTE_TYPE=float16  # 或 float32
```

### 配置项说明

#### 服务配置
- `WHISPER_HOST`: 服务监听地址
  - 默认值: "0.0.0.0"
  - 说明: 设置为 0.0.0.0 允许外部访问，设置为 127.0.0.1 仅允许本地访问

- `WHISPER_PORT`: 服务端口
  - 默认值: 8000
  - 说明: 可以根据需要修改，注意不要与其他服务冲突

#### 模型配置
- `WHISPER_MODEL_SIZE`: 模型大小
  - 默认值: "base"
  - 可选值: "tiny", "base", "small", "medium", "large"
  - 说明: 模型越大，准确率越高，但需要更多资源

- `WHISPER_MODEL_PATH`: 自定义模型路径
  - 默认值: 无
  - 说明: 可选配置，用于指定本地模型文件路径

- `WHISPER_DEVICE`: 运行设备
  - 默认值: 自动选择
  - 可选值: "cuda"（GPU）, "cpu"
  - 说明: 有 GPU 时建议使用 "cuda"

- `WHISPER_COMPUTE_TYPE`: 计算精度
  - 默认值: 自动选择
  - 可选值: "float16", "float32"
  - 说明: GPU 模式下建议使用 "float16"，CPU 模式使用 "float32"

### 使用环境变量

也可以直接使用环境变量进行配置，优先级高于 .env 文件：

```bash
export WHISPER_PORT=8080
export WHISPER_MODEL_SIZE=small
export WHISPER_DEVICE=cuda
python main.py
```

## 系统要求

- Python 3.8+
- CUDA 支持（可选，用于 GPU 加速）
