import pygame
import random
import math
from typing import List, Tuple, Dict
import time

# Initialize Pygame and font
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 14)

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
FPS = 30
VEHICLE_BASE_SPEED = 2
STOP_LINE_DISTANCE = 60  # Distance from junction center to stop line

# Green corridor configuration
TRAVEL_TIME_J1_TO_J2 = 175  # Time in frames for vehicles to travel from J1 to J2
TRAVEL_TIME_J2_TO_J3 = 175  # Time in frames for vehicles to travel from J2 to J3
GREEN_DURATION = 150       # Duration of green light in frames
RED_DURATION = 150         # Duration of red light in frames

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
ROAD_COLOR = (50, 50, 50)
TEXT_COLOR = (30, 30, 30)
GREEN_WAVE_COLOR = (0, 255, 0, 50)
TEXT_BACKGROUND = (255, 255, 255, 180)

class Vehicle:
    def __init__(self, x: float, y: float, direction: str):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = VEHICLE_BASE_SPEED
        self.width = 20
        self.height = 40 if direction in ['up', 'down'] else 40
        self.waiting = False
        self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        self.in_junction = False  # Track if vehicle is currently inside a junction

    def move(self):
        if not self.waiting:
            if self.direction == 'right':
                self.x += self.speed
            elif self.direction == 'left':
                self.x -= self.speed
            elif self.direction == 'up':
                self.y -= self.speed
            elif self.direction == 'down':
                self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, 
                        (self.x - self.width/2, 
                         self.y - self.height/2, 
                         self.width, 
                         self.height))

class TrafficLight:
    def __init__(self, x: int, y: int, direction: str):
        self.x = x
        self.y = y
        self.direction = direction
        self.state = 'red'
        self.timer = 0
        self.wave_active = False
        self.vehicle_count = 0
        self.density = 0.0
        
    def update(self):
        self.timer += 1

    def set_state(self, new_state: str):
        if new_state != self.state:
            self.state = new_state
            self.timer = 0

    def draw(self, screen):
        # Draw traffic light
        color = {'red': RED, 'yellow': YELLOW, 'green': GREEN}[self.state]
        radius = 10 if not self.wave_active else 12
        pygame.draw.circle(screen, color, (self.x, self.y), radius)
        
        if self.wave_active and self.state == 'green':
            pulse = abs(math.sin(time.time() * 5)) * 3
            pygame.draw.circle(screen, GREEN, (self.x, self.y), radius + pulse, 2)

        # Draw traffic info with background
        info_text = f"V:{self.vehicle_count} D:{self.density:.1f}"
        text_surface = FONT.render(info_text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        
        # Position text based on direction
        if self.direction == 'up':
            text_rect.midtop = (self.x, self.y - 40)
        elif self.direction == 'down':
            text_rect.midbottom = (self.x, self.y + 40)
        elif self.direction == 'left':
            text_rect.midright = (self.x - 30, self.y)
        else:  # right
            text_rect.midleft = (self.x + 30, self.y)

        # Draw semi-transparent background
        background_rect = text_rect.inflate(10, 6)
        background_surface = pygame.Surface(background_rect.size, pygame.SRCALPHA)
        background_surface.fill(TEXT_BACKGROUND)
        screen.blit(background_surface, background_rect)
        screen.blit(text_surface, text_rect)

class Junction:
    def __init__(self, x: int, y: int, index: int):
        self.x = x
        self.y = y
        self.index = index
        self.size = 100
        
        offset = self.size // 2 + 10
        self.lights = {
            'right': TrafficLight(x + offset, y, 'right'),
            'left': TrafficLight(x - offset, y, 'left'),
            'up': TrafficLight(x, y - offset, 'up'),
            'down': TrafficLight(x, y + offset, 'down')
        }
        
        # Initialize the horizontal corridor (east-west) to be green on all junctions by default
        if True:  # Changed from index == 0 to always initialize horizontal roads to green
            self.lights['right'].state = 'green'
            self.lights['left'].state = 'green'
            self.lights['right'].wave_active = True
            self.lights['left'].wave_active = True
            self.lights['up'].state = 'red'
            self.lights['down'].state = 'red'

    def get_stop_line_position(self, direction: str) -> Tuple[int, int]:
        """Get the position of the stop line for a given direction"""
        if direction == 'right':
            return (self.x - STOP_LINE_DISTANCE, self.y - self.size//4)
        elif direction == 'left':
            return (self.x + STOP_LINE_DISTANCE, self.y + self.size//4)
        elif direction == 'up':
            return (self.x, self.y + STOP_LINE_DISTANCE)
        elif direction == 'down':
            return (self.x, self.y - STOP_LINE_DISTANCE)
        return (self.x, self.y)  # Default fallback

    def update(self, master_timer: int, vehicles: List[Vehicle]):
        # Update traffic density for each direction
        for direction, light in self.lights.items():
            # Count vehicles in the vicinity of this light
            nearby_vehicles = [v for v in vehicles if v.direction == direction and
                             abs(v.x - self.x) < 200 and abs(v.y - self.y) < 200]
            light.vehicle_count = len(nearby_vehicles)
            light.density = len(nearby_vehicles) / 10.0  # Normalize density
            light.update()

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, 
                        (self.x - self.size//2, 
                         self.y - self.size//2, 
                         self.size, 
                         self.size))
        
        # Draw stop lines
        for direction in ['right', 'left', 'up', 'down']:
            stop_x, stop_y = self.get_stop_line_position(direction)
            
            if direction == 'right':
                pygame.draw.line(screen, WHITE, (stop_x, stop_y - 20), (stop_x, stop_y + 20), 3)
            elif direction == 'left':
                pygame.draw.line(screen, WHITE, (stop_x, stop_y - 20), (stop_x, stop_y + 20), 3)
            elif direction == 'up':
                pygame.draw.line(screen, WHITE, (stop_x - 20, stop_y), (stop_x + 20, stop_y), 3)
            elif direction == 'down':
                pygame.draw.line(screen, WHITE, (stop_x - 20, stop_y), (stop_x + 20, stop_y), 3)
        
        for light in self.lights.values():
            light.draw(screen)

class TrafficSimulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Traffic Flow Optimization - Green Corridor")
        self.clock = pygame.time.Clock()
        
        # Distance between junctions (used for timing calculations)
        self.j1_j2_distance = 350  # Distance from J1 to J2
        self.j2_j3_distance = 350  # Distance from J2 to J3
        
        self.junctions = [
            Junction(350, WINDOW_HEIGHT//2, 0),   # J1
            Junction(700, WINDOW_HEIGHT//2, 1),   # J2
            Junction(1050, WINDOW_HEIGHT//2, 2)   # J3
        ]
        
        self.vehicles = []
        self.road_width = 60
        self.running = True
        self.master_timer = 0
        
        # Create surface for green wave visualization
        self.wave_surface = pygame.Surface((WINDOW_WIDTH, self.road_width), pygame.SRCALPHA)

    def draw_green_wave(self, screen):
        wave_x = (self.master_timer * VEHICLE_BASE_SPEED) % WINDOW_WIDTH
        self.wave_surface.fill((0, 0, 0, 0))
        
        # Draw animated green wave arrows
        arrow_spacing = 100
        arrow_length = 40
        arrow_width = 20
        
        for x in range(0, WINDOW_WIDTH + arrow_spacing, arrow_spacing):
            pos = (x + wave_x) % (WINDOW_WIDTH + arrow_spacing) - arrow_spacing
            
            # Draw right-moving arrows on top lane
            arrow_y = self.road_width // 4
            points = [
                (pos, arrow_y),
                (pos + arrow_length, arrow_y),
                (pos + arrow_length, arrow_y - arrow_width//2),
                (pos + arrow_length + arrow_width//2, arrow_y),
                (pos + arrow_length, arrow_y + arrow_width//2),
                (pos + arrow_length, arrow_y)
            ]
            pygame.draw.lines(self.wave_surface, GREEN_WAVE_COLOR, False, points, 3)
            
            # Draw left-moving arrows on bottom lane
            arrow_y = self.road_width * 3 // 4
            points = [
                (pos + arrow_length + arrow_width//2, arrow_y),
                (pos + arrow_length, arrow_y),
                (pos + arrow_length, arrow_y - arrow_width//2),
                (pos, arrow_y),
                (pos + arrow_length, arrow_y + arrow_width//2),
                (pos + arrow_length, arrow_y)
            ]
            pygame.draw.lines(self.wave_surface, GREEN_WAVE_COLOR, False, points, 3)
        
        screen.blit(self.wave_surface, (0, WINDOW_HEIGHT//2 - self.road_width//2))

    def spawn_vehicle(self):
        if random.random() < 0.03:
            direction = random.choice(['right', 'left'])
            if direction == 'right':
                x, y = 0, WINDOW_HEIGHT//2 - self.road_width//4
            else:
                x, y = WINDOW_WIDTH, WINDOW_HEIGHT//2 + self.road_width//4
            self.vehicles.append(Vehicle(x, y, direction))
            
        if random.random() < 0.01:
            junction = random.choice(self.junctions)
            direction = random.choice(['up', 'down'])
            if direction == 'up':
                x, y = junction.x, WINDOW_HEIGHT
            else:
                x, y = junction.x, 0
            self.vehicles.append(Vehicle(x, y, direction))

    def should_stop_at_light(self, vehicle: Vehicle) -> bool:
        for junction in self.junctions:
            # Check if vehicle is already in this junction
            in_junction_area = (abs(vehicle.x - junction.x) < junction.size/2 and 
                               abs(vehicle.y - junction.y) < junction.size/2)
            
            if in_junction_area:
                # If already in junction, mark it and don't stop
                vehicle.in_junction = True
                continue
            
            # Calculate distance to stop line based on direction
            stop_x, stop_y = junction.get_stop_line_position(vehicle.direction)
            
            # Check if approaching stop line based on direction
            approaching = False
            stop_line_distance = 0
            
            if vehicle.direction == 'right':
                if vehicle.x < stop_x and abs(vehicle.y - stop_y) < 20:
                    approaching = True
                    stop_line_distance = stop_x - vehicle.x
            elif vehicle.direction == 'left':
                if vehicle.x > stop_x and abs(vehicle.y - stop_y) < 20:
                    approaching = True
                    stop_line_distance = vehicle.x - stop_x
            elif vehicle.direction == 'up':
                if vehicle.y > stop_y and abs(vehicle.x - stop_x) < 20:
                    approaching = True
                    stop_line_distance = vehicle.y - stop_y
            elif vehicle.direction == 'down':
                if vehicle.y < stop_y and abs(vehicle.x - stop_x) < 20:
                    approaching = True
                    stop_line_distance = stop_y - vehicle.y
            
            # If approaching a stop line and close enough to consider
            if approaching and stop_line_distance < 30:
                light_state = junction.lights[vehicle.direction].state
                
                # Stop if the light is red or yellow and we're close to the stop line
                if light_state in ['red', 'yellow'] and stop_line_distance < 15:
                    return True
                    
            # Reset in_junction flag when vehicle has cleared the junction
            elif vehicle.in_junction and not in_junction_area:
                vehicle.in_junction = False
                
        return False

    def update_green_corridor(self):
        # Calculate cycle time (total duration of one complete signal cycle)
        cycle_time = GREEN_DURATION + RED_DURATION
        
        # Junction 1 (first junction) timing - base timing
        j1 = self.junctions[0]
        cycle_position = self.master_timer % cycle_time
        
        # East-West corridor (right-left) is green for the first half of the cycle
        if cycle_position < GREEN_DURATION:
            j1.lights['right'].set_state('green')
            j1.lights['left'].set_state('green')
            j1.lights['right'].wave_active = True
            j1.lights['left'].wave_active = True
            
            # Yellow transition period for north-south
            if cycle_position > GREEN_DURATION - 30:
                j1.lights['up'].set_state('yellow')
                j1.lights['down'].set_state('yellow')
            else:
                j1.lights['up'].set_state('red')
                j1.lights['down'].set_state('red')
        else:
            # North-South is green for the second half of the cycle
            j1.lights['up'].set_state('green')
            j1.lights['down'].set_state('green')
            
            # Yellow transition period for east-west
            if cycle_position > cycle_time - 30:
                j1.lights['right'].set_state('yellow')
                j1.lights['left'].set_state('yellow')
                j1.lights['right'].wave_active = False
                j1.lights['left'].wave_active = False
            else:
                j1.lights['right'].set_state('red')
                j1.lights['left'].set_state('red')
                j1.lights['right'].wave_active = False
                j1.lights['left'].wave_active = False
        
        # Junction 2 timing - offset by TRAVEL_TIME_J1_TO_J2
        j2 = self.junctions[1]
        cycle_position_j2 = (self.master_timer - TRAVEL_TIME_J1_TO_J2) % cycle_time
        
        if cycle_position_j2 < GREEN_DURATION:
            j2.lights['right'].set_state('green')
            j2.lights['left'].set_state('green')
            j2.lights['right'].wave_active = True
            j2.lights['left'].wave_active = True
            
            if cycle_position_j2 > GREEN_DURATION - 30:
                j2.lights['up'].set_state('yellow')
                j2.lights['down'].set_state('yellow')
            else:
                j2.lights['up'].set_state('red')
                j2.lights['down'].set_state('red')
        else:
            j2.lights['up'].set_state('green')
            j2.lights['down'].set_state('green')
            
            if cycle_position_j2 > cycle_time - 30:
                j2.lights['right'].set_state('yellow')
                j2.lights['left'].set_state('yellow')
                j2.lights['right'].wave_active = False
                j2.lights['left'].wave_active = False
            else:
                j2.lights['right'].set_state('red')
                j2.lights['left'].set_state('red')
                j2.lights['right'].wave_active = False
                j2.lights['left'].wave_active = False
        
        # Junction 3 timing - offset by TRAVEL_TIME_J1_TO_J2 + TRAVEL_TIME_J2_TO_J3
        j3 = self.junctions[2]
        cycle_position_j3 = (self.master_timer - (TRAVEL_TIME_J1_TO_J2 + TRAVEL_TIME_J2_TO_J3)) % cycle_time
        
        if cycle_position_j3 < GREEN_DURATION:
            j3.lights['right'].set_state('green')
            j3.lights['left'].set_state('green')
            j3.lights['right'].wave_active = True
            j3.lights['left'].wave_active = True
            
            if cycle_position_j3 > GREEN_DURATION - 30:
                j3.lights['up'].set_state('yellow')
                j3.lights['down'].set_state('yellow')
            else:
                j3.lights['up'].set_state('red')
                j3.lights['down'].set_state('red')
        else:
            j3.lights['up'].set_state('green')
            j3.lights['down'].set_state('green')
            
            if cycle_position_j3 > cycle_time - 30:
                j3.lights['right'].set_state('yellow')
                j3.lights['left'].set_state('yellow')
                j3.lights['right'].wave_active = False
                j3.lights['left'].wave_active = False
            else:
                j3.lights['right'].set_state('red')
                j3.lights['left'].set_state('red')
                j3.lights['right'].wave_active = False
                j3.lights['left'].wave_active = False

    def draw_roads(self):
        pygame.draw.rect(self.screen, ROAD_COLOR, 
                        (0, WINDOW_HEIGHT//2 - self.road_width//2, 
                         WINDOW_WIDTH, self.road_width))
        
        for junction in self.junctions:
            pygame.draw.rect(self.screen, ROAD_COLOR,
                           (junction.x - self.road_width//2, 0,
                            self.road_width, WINDOW_HEIGHT))
        
        dash_length = 30
        gap_length = 30
        for x in range(0, WINDOW_WIDTH, dash_length + gap_length):
            pygame.draw.rect(self.screen, WHITE,
                           (x, WINDOW_HEIGHT//2 - 2, dash_length, 4))
        
        for junction in self.junctions:
            for y in range(0, WINDOW_HEIGHT, dash_length + gap_length):
                pygame.draw.rect(self.screen, WHITE,
                               (junction.x - 2, y, 4, dash_length))

    def draw_corridor_info(self):
        # Draw visualization of green wave coordination
        time_j1_to_j2 = f"J1→J2: {TRAVEL_TIME_J1_TO_J2/FPS:.1f}s"
        time_j2_to_j3 = f"J2→J3: {TRAVEL_TIME_J2_TO_J3/FPS:.1f}s"
        
        text_j1_j2 = FONT.render(time_j1_to_j2, True, BLACK)
        text_j2_j3 = FONT.render(time_j2_to_j3, True, BLACK)
        
        # Position between junctions
        mid_x_j1_j2 = (self.junctions[0].x + self.junctions[1].x) // 2
        mid_x_j2_j3 = (self.junctions[1].x + self.junctions[2].x) // 2
        
        self.screen.blit(text_j1_j2, (mid_x_j1_j2 - 30, WINDOW_HEIGHT//2 - 40))
        self.screen.blit(text_j2_j3, (mid_x_j2_j3 - 30, WINDOW_HEIGHT//2 - 40))
        
        
        corridor_status = FONT.render("Green Corridor Active", True, BLACK)
        corridor_rect = corridor_status.get_rect(center=(WINDOW_WIDTH//2, 30))
        self.screen.blit(corridor_status, corridor_rect)

    def update(self):
        self.master_timer += 1
        self.spawn_vehicle()
        
        
        self.update_green_corridor()
        
        for junction in self.junctions:
            junction.update(self.master_timer, self.vehicles)
        
        for vehicle in self.vehicles[:]:
            
            if self.should_stop_at_light(vehicle):
                vehicle.waiting = True
            else:
                vehicle.waiting = False
                vehicle.move()
            
            if (vehicle.x < -50 or vehicle.x > WINDOW_WIDTH + 50 or
                vehicle.y < -50 or vehicle.y > WINDOW_HEIGHT + 50):
                self.vehicles.remove(vehicle)

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_roads()
        self.draw_green_wave(self.screen)
        
        for junction in self.junctions:
            junction.draw(self.screen)
        
        for vehicle in self.vehicles:
            vehicle.draw(self.screen)
            
        self.draw_corridor_info()
        
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    simulation = TrafficSimulation()
    simulation.run()