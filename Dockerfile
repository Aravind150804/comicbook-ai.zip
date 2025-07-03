FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    git python3 python3-pip ffmpeg libgl1 unzip wget curl nano && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN git clone https://github.com/comfyanonymous/ComfyUI.git comfyui
WORKDIR /workspace/comfyui
RUN pip3 install -r requirements.txt

WORKDIR /workspace

COPY app app/
COPY requirements.txt .
COPY startup.sh .

RUN pip3 install -r requirements.txt

EXPOSE 7860

CMD ["/bin/bash", "startup.sh"]
