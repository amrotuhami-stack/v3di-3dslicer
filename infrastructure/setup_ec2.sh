#!/bin/bash
# V3Di 3D Slicer Backend - AWS EC2 Setup Script
# Recommended Instance: g4dn.xlarge (4 vCPU, 16GB RAM, T4 GPU)
# AMI: Ubuntu 22.04 LTS (Deep Learning AMI recommended)

set -e

echo "=========================================="
echo "V3Di 3D Slicer Backend Installation"
echo "=========================================="

# Update system
echo "[1/8] Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install essential packages
echo "[2/8] Installing essential packages..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    unzip \
    libgl1-mesa-glx \
    libxrender1 \
    libxcursor1 \
    libxft2 \
    libxinerama1 \
    xvfb \
    mesa-utils \
    libglu1-mesa

# Install AWS CLI
echo "[3/8] Installing AWS CLI..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -q awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip

# Create work directory
echo "[4/8] Creating work directories..."
sudo mkdir -p /opt/v3di-backend
sudo chown ubuntu:ubuntu /opt/v3di-backend
cd /opt/v3di-backend

# Download and install 3D Slicer (headless)
echo "[5/8] Downloading 3D Slicer..."
SLICER_VERSION="5.6.2"
wget -q "https://download.slicer.org/bitstream/6756ded9bc8d3ab66ca3b88b" -O slicer.tar.gz
tar -xzf slicer.tar.gz
rm slicer.tar.gz
mv Slicer* Slicer
export SLICER_HOME=/opt/v3di-backend/Slicer

# Create Python virtual environment
echo "[6/8] Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install \
    fastapi \
    uvicorn \
    python-multipart \
    boto3 \
    numpy \
    SimpleITK \
    nibabel \
    scipy \
    scikit-image \
    trimesh \
    numpy-stl \
    pydantic

# Install PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install nnU-Net
pip install nnunetv2

# Create backend structure
echo "[7/8] Creating backend structure..."
mkdir -p api slicer_modules models uploads outputs

# Download DentalSegmentator model weights (placeholder)
echo "[8/8] Setting up model directory..."
mkdir -p models/nnUNet_results/Dataset111_453CT

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Configure AWS credentials: aws configure"
echo "2. Download model weights to models/nnUNet_results/"
echo "3. Start the backend: ./start_server.sh"
echo ""
echo "Slicer installed at: $SLICER_HOME"
echo "Backend directory: /opt/v3di-backend"
