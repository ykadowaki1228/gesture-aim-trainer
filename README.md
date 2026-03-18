# Gesture-Controlled Aim Trainer

A real-time aim training system that enables controller-free interaction using computer vision–based hand tracking.

## Overview

This project explores free-space human–computer interaction for rehabilitation and accessibility.  
Users interact with virtual targets using hand gestures detected through a webcam, while performance data such as reaction time is recorded and visualized.

## Features

- Real-time hand tracking using MediaPipe and OpenCV  
- Gesture-based interaction (hover, click, drag) without physical controllers  
- Coordinate mapping from camera space to screen space  
- Interactive UI with animations, audio feedback, and scoring system  
- Reaction-time measurement and performance visualization  
- Multiple difficulty levels inspired by aim training systems  

## System Design

- Hand Tracking Module: Extracts hand landmarks and gesture states from webcam input  
- Interface Layer: Converts hand motion into interaction events  
- Game Module (Pygame): Manages targets, scoring logic, feedback, and difficulty control  
- Data Module: Logs performance data for analysis and visualization  

## Technologies

- Python  
- OpenCV  
- MediaPipe  
- Pygame  
- PyAutoGUI  

## Motivation

The system aims to support motor-skill training and rehabilitation by providing an accessible and portable interaction environment that does not require traditional input devices.

## Future Improvements

- Adaptive difficulty based on user performance  
- Additional gesture support  
- Clinically validated rehabilitation protocols  
- Accessibility customization options  
