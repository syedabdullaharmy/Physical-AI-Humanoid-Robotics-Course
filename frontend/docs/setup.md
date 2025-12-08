---
sidebar_position: 2
title: Setup Guide
---

# Environment Setup

This guide will help you set up your development environment for the Physical AI & Humanoid Robotics course.

## Choose Your Hardware Path

Select one of three configurations based on your needs and resources.

## Path 1: Digital Twin Workstation

### Requirements
- **GPU**: NVIDIA RTX 3060 or better (12GB+ VRAM recommended)
- **OS**: Ubuntu 22.04 LTS
- **RAM**: 16GB minimum, 32GB recommended
- **Storage**: 100GB+ free space
- **CPU**: 8+ cores recommended

### Installation Steps

#### 1. Install Ubuntu 22.04

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y build-essential git curl wget vim
```

#### 2. Install NVIDIA Drivers

```bash
# Add NVIDIA PPA
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# Install latest driver
sudo apt install -y nvidia-driver-535

# Reboot
sudo reboot

# Verify installation
nvidia-smi
```

#### 3. Install ROS 2 Humble

```bash
# Set locale
sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS 2 repository
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 Humble
sudo apt update
sudo apt install -y ros-humble-desktop

# Source ROS 2
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

#### 4. Install Gazebo

```bash
# Install Gazebo Garden
sudo apt install -y ros-humble-gazebo-ros-pkgs
```

#### 5. Install Python Dependencies

```bash
# Install Python 3.10
sudo apt install -y python3-pip python3-venv

# Create virtual environment
python3 -m venv ~/robotics_env
source ~/robotics_env/bin/activate

# Install packages
pip install numpy scipy matplotlib jupyter
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Verification

```bash
# Test ROS 2
ros2 run demo_nodes_cpp talker

# In another terminal
ros2 run demo_nodes_py listener

# Test Gazebo
gazebo --verbose
```

## Path 2: NVIDIA Jetson Orin Nano

### Requirements
- NVIDIA Jetson Orin Nano Developer Kit
- 64GB+ microSD card
- 5V/4A power supply
- USB keyboard, mouse, HDMI monitor

### Installation Steps

#### 1. Flash JetPack

1. Download NVIDIA SDK Manager on host PC
2. Flash JetPack 5.1.2 to Jetson
3. Complete initial setup

#### 2. Install ROS 2

```bash
# Follow same ROS 2 installation as Ubuntu path
# JetPack includes Ubuntu 20.04, use ROS 2 Foxy instead
```

#### 3. Optimize for Edge

```bash
# Set power mode
sudo nvpmodel -m 0
sudo jetson_clocks

# Monitor resources
sudo tegrastats
```

## Path 3: Cloud-Native (AWS)

### Requirements
- AWS account
- Basic cloud knowledge
- Credit card for billing

### Setup Steps

#### 1. Launch EC2 Instance

```bash
# Instance type: g4dn.xlarge or better
# AMI: Deep Learning AMI (Ubuntu 22.04)
# Storage: 100GB+ EBS
```

#### 2. Connect and Configure

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install ROS 2 (same as Ubuntu path)
```

#### 3. Cost Optimization

- Use Spot Instances for training
- Stop instances when not in use
- Use S3 for data storage

## Common Tools

### VS Code with ROS Extension

```bash
# Install VS Code
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code

# Install ROS extension
code --install-extension ms-iot.vscode-ros
```

### Git Configuration

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Troubleshooting

### GPU Not Detected

```bash
# Check NVIDIA driver
nvidia-smi

# Reinstall if needed
sudo apt purge nvidia-*
sudo apt install nvidia-driver-535
```

### ROS 2 Not Found

```bash
# Ensure sourced
source /opt/ros/humble/setup.bash

# Add to bashrc permanently
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

### Permission Denied

```bash
# Add user to dialout group (for serial devices)
sudo usermod -a -G dialout $USER
```

## Next Steps

Once your environment is set up, proceed to [Module 1: ROS 2 Fundamentals](/docs/module-1-ros2/introduction)!

## Need Help?

- Use the AI chatbot (bottom-right corner)
- Check the [Troubleshooting Guide](/docs/references/troubleshooting)
- Visit [Panaversity Community](https://panaversity.org)
