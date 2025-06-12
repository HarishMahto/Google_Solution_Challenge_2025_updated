# Single Junction Traffic Simulation 🚦  

## Overview  
This simulation models a **single 4-way intersection** with dynamic traffic signal control. The system optimizes signal timings based on real-time vehicle density to improve traffic flow and reduce congestion.  

## Key Features  
✅ **Dynamic Signal Timing** → Adjusts green, yellow, and red lights based on vehicle density.  
✅ **Vehicle Detection & Tracking** → Simulates traffic movement with realistic behavior.  
✅ **Pygame-Based Visualization** → Displays real-time traffic flow and signal changes.  

## Workflow  
1. **Traffic Flow Simulation**  
   - Vehicles enter the junction and move based on signal timings.  
2. **Dynamic Signal Control**  
   - Traffic lights adjust based on vehicle count and road congestion levels.  
3. **Real-Time Visualization**  
   - Displays vehicle movement, lane switching, and signal transitions.  

## Files  
- `single_junction_simulation.mp4` → Video demo of the simulation.  
- `single_junction_code.py` → Python script for running the simulation using **Pygame**.  
- `README.md` → Documentation explaining the simulation approach.  

## How to Run  
1. Install dependencies:  
   ```bash
   pip install pygame
   ```
2. Run the simulation:
   ```bash
   python single_junction_code.py
   ```