# Multi-Junction Traffic Simulation   

## Overview  
This simulation models a **three-junction synchronized traffic system** to create a **Green Corridor (Green Wave)** using the **Zero Red Time Algorithm**. The goal is to optimize traffic flow by ensuring continuous vehicle movement across multiple intersections.  

## Key Features  
 **Three-Junction Synchronization** → Coordinates traffic lights across three 4-way intersections.  
 **Green Corridor (Green Wave)** → Minimizes vehicle stoppage by synchronizing green signals.  
 **Zero Red Time Algorithm** → Ensures at least one lane remains open at all times.  
 **Pygame-Based Simulation** → Visualizes real-time traffic movement and signal changes.  

## Workflow  
1. **Traffic Signal Synchronization**  
   - Traffic signals are dynamically adjusted to maintain a **continuous green wave**.  
2. **Zero Red Time Algorithm**  
   - Ensures no complete stoppage at any junction, reducing congestion.  
3. **Vehicle Movement Simulation**  
   - Vehicles follow realistic movement patterns based on signal timings.  

## Files  
- `multi_junction_simulation.mp4` → Video demonstrating the simulation.  
- `multi_junction_code.py` → Python script implementing the simulation using **Pygame**.  
- `README.md` → This document explaining the simulation approach.  

## How to Run  
1. Install dependencies:  
   ```bash
   pip install pygame
   ```
2. Run the simulation:
  ```bash
  python multi_junction_code.py
  ```
