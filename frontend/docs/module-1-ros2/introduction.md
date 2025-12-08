---
sidebar_position: 1
title: Introduction to ROS 2
---

# Module 1: ROS 2 Fundamentals

Welcome to Module 1! In this module, you'll learn the fundamentals of ROS 2 (Robot Operating System 2), the industry-standard framework for building robot applications.

## Learning Objectives

By the end of this module, you will be able to:

- Understand ROS 2 architecture and core concepts
- Create and manage ROS 2 nodes
- Communicate using topics, services, and actions
- Build a simple robot simulation
- Debug ROS 2 applications

## Module Overview

### Week 3: ROS 2 Basics
- What is ROS 2?
- Nodes and packages
- Topics and messages
- Publishers and subscribers

### Week 4: Advanced Communication
- Services and clients
- Actions and action servers
- Parameters and launch files

### Week 5: Simulation & Integration
- Gazebo integration
- URDF robot models
- TF2 transformations
- Building a complete robot

## What is ROS 2?

**ROS 2** (Robot Operating System 2) is an open-source robotics middleware suite. Despite its name, it's not an operating system but rather a flexible framework for writing robot software.

### Key Features

- **Distributed Architecture**: Run nodes across multiple machines
- **Real-time Capable**: Support for real-time systems
- **Cross-platform**: Works on Linux, Windows, macOS
- **Language Support**: Python, C++, and more
- **Rich Ecosystem**: Thousands of packages and tools

### ROS 1 vs ROS 2

| Feature | ROS 1 | ROS 2 |
|---------|-------|-------|
| Communication | TCPROS | DDS |
| Real-time | Limited | Full support |
| Security | Basic | Built-in |
| Multi-robot | Difficult | Native |
| Platforms | Linux only | Cross-platform |

## Core Concepts

### 1. Nodes

A **node** is a process that performs computation. Robots typically have many nodes:

- Camera driver node
- Motor controller node
- Path planning node
- Localization node

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('Node started!')

def main():
    rclpy.init()
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 2. Topics

**Topics** are named buses for message passing. Nodes can publish or subscribe to topics.

```python
from std_msgs.msg import String

class Publisher(Node):
    def __init__(self):
        super().__init__('publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
    
    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS 2!'
        self.publisher_.publish(msg)
```

### 3. Services

**Services** provide request/response communication for one-time operations.

```python
from example_interfaces.srv import AddTwoInts

class ServiceNode(Node):
    def __init__(self):
        super().__init__('service_node')
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_two_ints_callback
        )
    
    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        return response
```

### 4. Actions

**Actions** are for long-running tasks with feedback and cancellation.

## ROS 2 Architecture

```
┌─────────────────────────────────────────┐
│           Application Layer             │
│  (Your Robot Code - Nodes)              │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│          ROS 2 Client Libraries         │
│         (rclpy, rclcpp, etc.)           │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│              ROS 2 Core                 │
│         (rcl, rmw, rosidl)              │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│        DDS Implementation               │
│    (Fast DDS, Cyclone DDS, etc.)        │
└─────────────────────────────────────────┘
```

## Your First ROS 2 Package

Let's create a simple package:

```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Create package
ros2 pkg create --build-type ament_python my_robot_pkg

# Build
cd ~/ros2_ws
colcon build

# Source
source install/setup.bash
```

## Hands-On Exercise

Create a "Hello World" publisher and subscriber:

1. Create a publisher node that sends "Hello ROS 2!" every second
2. Create a subscriber node that receives and prints the message
3. Run both nodes and observe the communication

**Solution** is in the next chapter!

## Common Commands

```bash
# List nodes
ros2 node list

# List topics
ros2 topic list

# Echo topic
ros2 topic echo /topic_name

# Get node info
ros2 node info /node_name

# Run a node
ros2 run package_name node_name
```

## Resources

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS Answers](https://answers.ros.org/)

## Next Steps

Ready to dive deeper? Continue to [Creating Your First Node](/docs/module-1-ros2/first-node)!

---

**💡 Tip**: Use the chatbot to ask questions about any ROS 2 concept. Highlight confusing text and click "Ask AI"!
