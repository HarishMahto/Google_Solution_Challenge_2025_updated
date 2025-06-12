import pygame
import random
import math
import os
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

# Green corridor configuration - optimized for better synchronization
TRAVEL_TIME_J1_TO_J2 = 120  # Reduced for better sync
TRAVEL_TIME_J2_TO_J3 = 120  # Reduced for better sync
GREEN_DURATION = 180       # Longer green duration
RED_DURATION = 90          # Shorter red duration for main road

# Collision detection constants
MIN_FOLLOWING_DISTANCE = 45  # Minimum distance between vehicles
SAFE_STOPPING_DISTANCE = 35  # Distance to maintain when stopping

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
ROAD_COLOR = (50, 50, 50)
TEXT_COLOR = (30, 30, 30)
GREEN_WAVE_COLOR = (0, 255, 100)  # More visible green
TEXT_BACKGROUND = (255, 255, 255, 180)

# Scenery colors
GRASS_COLOR = (34, 139, 34)
TREE_TRUNK_COLOR = (101, 67, 33)
TREE_FOLIAGE_COLOR = (0, 100, 0)
TREE_FOLIAGE_LIGHT = (50, 150, 50)
SKY_COLOR = (135, 206, 235)

# Get the absolute path to the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(SCRIPT_DIR, 'images')

# Vehicle speeds (from second code)
speeds = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'rickshaw': 2, 'bike': 2.5}

class VehicleImageManager:
    def __init__(self):
        # Define vehicle classes like in your second simulation
        self.vehicle_classes = ['car', 'bus', 'truck', 'bike', 'rickshaw']
        self.images = {}
        self.original_images = {}  # Store original images for rotation
        self.load_images()
    
    def load_images(self):
        """Load vehicle images from the images folder structure like the second simulation"""
        try:
            # Initialize nested dictionaries
            for direction in ['up', 'down', 'left', 'right']:
                self.images[direction] = {}
                self.original_images[direction] = {}
                
                for vehicle_class in self.vehicle_classes:
                    # Follow the same path structure as your second simulation
                    image_path = os.path.join(IMAGE_DIR, direction, f'{vehicle_class}.png')
                    
                    if os.path.exists(image_path):
                        try:
                            # Load original image
                            original_image = pygame.image.load(image_path)
                            self.original_images[direction][vehicle_class] = original_image
                            self.images[direction][vehicle_class] = original_image.copy()
                            
                            print(f"Loaded image: {image_path}")
                        except pygame.error as e:
                            print(f"Error loading image {image_path}: {e}")
                            self.create_fallback_image(direction, vehicle_class)
                    else:
                        print(f"Image not found: {image_path}")
                        self.create_fallback_image(direction, vehicle_class)
        except Exception as e:
            print(f"Error in load_images: {e}")
            self.create_all_fallback_images()
    
    def create_fallback_image(self, direction, vehicle_class):
        """Create a fallback colored rectangle for a specific vehicle class"""
        # Different colors for different vehicle types
        colors = {
            'car': (255, 100, 100),      # Red
            'bus': (100, 255, 100),      # Green  
            'truck': (100, 100, 255),    # Blue
            'bike': (255, 255, 100),     # Yellow
            'rickshaw': (255, 100, 255)  # Magenta
        }
        
        color = colors.get(vehicle_class, (150, 150, 150))  # Default gray
        
        # Different sizes for different vehicle types
        sizes = {
            'car': (60, 30),
            'bus': (80, 35),
            'truck': (70, 35),
            'bike': (40, 25),
            'rickshaw': (50, 28)
        }
        
        width, height = sizes.get(vehicle_class, (60, 30))
        
        if direction in ['up', 'down']:
            surface = pygame.Surface((height, width))  # Swap dimensions for vertical
        else:
            surface = pygame.Surface((width, height))
        surface.fill(color)
        
        # Ensure the dictionaries exist
        if direction not in self.images:
            self.images[direction] = {}
        if direction not in self.original_images:
            self.original_images[direction] = {}
            
        self.images[direction][vehicle_class] = surface
        self.original_images[direction][vehicle_class] = surface.copy()
    
    def create_all_fallback_images(self):
        """Create fallback images for all directions and vehicle classes"""
        for direction in ['up', 'down', 'left', 'right']:
            for vehicle_class in self.vehicle_classes:
                self.create_fallback_image(direction, vehicle_class)
    
    def get_image(self, direction, vehicle_class=None):
        """Get a vehicle image for the specified direction and vehicle class"""
        if vehicle_class is None:
            # If no vehicle class specified, pick randomly
            vehicle_class = random.choice(self.vehicle_classes)
        
        if (direction in self.images and 
            vehicle_class in self.images[direction]):
            return self.images[direction][vehicle_class], vehicle_class
        else:
            # Fallback: create a colored rectangle
            self.create_fallback_image(direction, vehicle_class)
            return self.images[direction][vehicle_class], vehicle_class
    
    def get_original_image(self, direction, vehicle_class):
        """Get the original (unscaled) image for rotation purposes"""
        if (direction in self.original_images and 
            vehicle_class in self.original_images[direction]):
            return self.original_images[direction][vehicle_class]
        return None

class Vehicle:
    def __init__(self, x: float, y: float, direction: str, image_manager: VehicleImageManager, vehicle_class: str = None):
        self.x = x
        self.y = y
        self.direction = direction
        
        # Get image and vehicle class
        self.image, self.vehicle_class = image_manager.get_image(direction, vehicle_class)
        self.original_image = image_manager.get_original_image(direction, self.vehicle_class)
        self.current_image = self.image  # For rotation handling
        
        # Set speed based on vehicle class
        self.speed = speeds.get(self.vehicle_class, VEHICLE_BASE_SPEED)
        self.max_speed = self.speed + random.uniform(-0.5, 0.5)
        self.current_speed = self.max_speed
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.waiting = False
        self.in_junction = False
        self.collision_detected = False
        self.will_turn = random.choice([True, False])  # Random turning decision
        self.turned = False
        self.rotate_angle = 0
        self.crossed = 0  # Add this from second code
        
        # For collision detection
        self.prev_x = x
        self.prev_y = y

    def get_rect(self):
        """Get the collision rectangle for this vehicle"""
        return pygame.Rect(self.x - self.width/2, self.y - self.height/2, 
                          self.width, self.height)

    def get_front_position(self):
        """Get the front position of the vehicle based on direction"""
        if self.direction == 'right':
            return (self.x + self.width/2, self.y)
        elif self.direction == 'left':
            return (self.x - self.width/2, self.y)
        elif self.direction == 'up':
            return (self.x, self.y - self.height/2)
        elif self.direction == 'down':
            return (self.x, self.y + self.height/2)
        return (self.x, self.y)

    def distance_to_vehicle(self, other_vehicle):
        """Calculate distance to another vehicle in the same direction"""
        if self.direction != other_vehicle.direction:
            return float('inf')
        
        front_x, front_y = self.get_front_position()
        other_x, other_y = other_vehicle.x, other_vehicle.y
        
        if self.direction == 'right':
            if other_x > self.x:
                return other_x - front_x
        elif self.direction == 'left':
            if other_x < self.x:
                return front_x - other_x
        elif self.direction == 'up':
            if other_y < self.y:
                return front_y - other_y
        elif self.direction == 'down':
            if other_y > self.y:
                return other_y - front_y
        
        return float('inf')

    def check_collision_ahead(self, vehicles):
        """Check if there's a vehicle too close ahead"""
        min_distance = float('inf')
        
        for other in vehicles:
            if other == self:
                continue
                
            same_lane = False
            if self.direction in ['left', 'right']:
                same_lane = abs(self.y - other.y) < 30
            else:
                same_lane = abs(self.x - other.x) < 30
            
            if same_lane:
                distance = self.distance_to_vehicle(other)
                if distance < min_distance:
                    min_distance = distance
        
        return min_distance < MIN_FOLLOWING_DISTANCE

    def update_speed(self, vehicles):
        """Update vehicle speed based on traffic conditions"""
        if self.waiting:
            self.current_speed = 0
            return
        
        if self.check_collision_ahead(vehicles):
            self.collision_detected = True
            self.current_speed = max(0, self.current_speed - 0.3)
        else:
            self.collision_detected = False
            if self.current_speed < self.max_speed:
                self.current_speed = min(self.max_speed, self.current_speed + 0.2)

    def move(self):
        if not self.waiting and self.current_speed > 0:
            self.prev_x, self.prev_y = self.x, self.y
            
            if self.direction == 'right':
                self.x += self.current_speed
            elif self.direction == 'left':
                self.x -= self.current_speed
            elif self.direction == 'up':
                self.y -= self.current_speed
            elif self.direction == 'down':
                self.y += self.current_speed

    def draw(self, screen):
        # Draw the vehicle image (removed collision detection indicator)
        image_rect = self.current_image.get_rect(center=(self.x, self.y))
        screen.blit(self.current_image, image_rect)

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
        return (self.x, self.y)

    def update(self, master_timer: int, vehicles: List[Vehicle]):
        # Update traffic density for each direction
        for direction, light in self.lights.items():
            nearby_vehicles = [v for v in vehicles if v.direction == direction and
                             abs(v.x - self.x) < 200 and abs(v.y - self.y) < 200]
            light.vehicle_count = len(nearby_vehicles)
            light.density = len(nearby_vehicles) / 10.0
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
        pygame.display.set_caption("Traffic Flow Optimization - Green Corridor with Enhanced Scenery")
        self.clock = pygame.time.Clock()
        
        # Initialize image manager
        self.image_manager = VehicleImageManager()
        
        # Distance between junctions
        self.j1_j2_distance = 350
        self.j2_j3_distance = 350
        
        self.junctions = [
            Junction(350, WINDOW_HEIGHT//2, 0),
            Junction(700, WINDOW_HEIGHT//2, 1),
            Junction(1050, WINDOW_HEIGHT//2, 2)
        ]
        
        self.vehicles = []
        self.road_width = 60
        self.running = True
        self.master_timer = 0
        
        # Generate trees for scenery
        self.trees = self.generate_trees()
        
        # Create surface for green wave visualization
        self.wave_surface = pygame.Surface((WINDOW_WIDTH, self.road_width), pygame.SRCALPHA)

    def generate_trees(self):
        """Generate random trees for scenery"""
        trees = []
        
        # Trees above the main road
        for i in range(25):
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = random.randint(50, WINDOW_HEIGHT//2 - self.road_width//2 - 60)
            
            # Avoid placing trees too close to vertical roads
            too_close = False
            for junction in self.junctions:
                if abs(x - junction.x) < 80:
                    too_close = True
                    break
            
            if not too_close:
                size = random.randint(15, 35)
                trees.append({'x': x, 'y': y, 'size': size})
        
        # Trees below the main road
        for i in range(25):
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = random.randint(WINDOW_HEIGHT//2 + self.road_width//2 + 60, WINDOW_HEIGHT - 50)
            
            # Avoid placing trees too close to vertical roads
            too_close = False
            for junction in self.junctions:
                if abs(x - junction.x) < 80:
                    too_close = True
                    break
            
            if not too_close:
                size = random.randint(15, 35)
                trees.append({'x': x, 'y': y, 'size': size})
        
        return trees

    def draw_scenery(self):
        """Draw background scenery"""
        # Draw sky gradient
        for y in range(WINDOW_HEIGHT):
            alpha = y / WINDOW_HEIGHT
            color = (
                int(SKY_COLOR[0] * (1 - alpha) + GRASS_COLOR[0] * alpha * 0.3),
                int(SKY_COLOR[1] * (1 - alpha) + GRASS_COLOR[1] * alpha * 0.3),
                int(SKY_COLOR[2] * (1 - alpha) + GRASS_COLOR[2] * alpha * 0.3)
            )
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
        
        # Draw grass areas
        grass_rects = [
            # Above main road
            pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT//2 - self.road_width//2),
            # Below main road
            pygame.Rect(0, WINDOW_HEIGHT//2 + self.road_width//2, WINDOW_WIDTH, WINDOW_HEIGHT//2 - self.road_width//2)
        ]
        
        for rect in grass_rects:
            pygame.draw.rect(self.screen, GRASS_COLOR, rect)
            
            # Add grass texture with small dots
            for _ in range(rect.width * rect.height // 1000):
                x = random.randint(rect.left, rect.right - 1)
                y = random.randint(rect.top, rect.bottom - 1)
                darker_grass = (
                    max(0, GRASS_COLOR[0] - random.randint(0, 20)),
                    max(0, GRASS_COLOR[1] - random.randint(0, 20)),
                    max(0, GRASS_COLOR[2] - random.randint(0, 20))
                )
                pygame.draw.circle(self.screen, darker_grass, (x, y), 1)
        
        # Draw trees
        for tree in self.trees:
            # Tree trunk
            trunk_height = tree['size'] // 2
            trunk_width = tree['size'] // 6
            trunk_rect = pygame.Rect(
                tree['x'] - trunk_width//2, 
                tree['y'] - trunk_height//2, 
                trunk_width, 
                trunk_height
            )
            pygame.draw.rect(self.screen, TREE_TRUNK_COLOR, trunk_rect)
            
            # Tree foliage (multiple circles for natural look)
            foliage_radius = tree['size'] // 2
            
            # Main foliage
            pygame.draw.circle(self.screen, TREE_FOLIAGE_COLOR, 
                             (tree['x'], tree['y'] - tree['size']//3), foliage_radius)
            
            # Lighter highlights
            pygame.draw.circle(self.screen, TREE_FOLIAGE_LIGHT, 
                             (tree['x'] - foliage_radius//3, tree['y'] - tree['size']//3 - foliage_radius//3), 
                             foliage_radius//2)
            
            # Additional smaller foliage clusters
            for _ in range(2):
                offset_x = random.randint(-foliage_radius//2, foliage_radius//2)
                offset_y = random.randint(-foliage_radius//2, foliage_radius//2)
                small_radius = random.randint(foliage_radius//3, foliage_radius//2)
                pygame.draw.circle(self.screen, TREE_FOLIAGE_COLOR,
                                 (tree['x'] + offset_x, tree['y'] - tree['size']//3 + offset_y),
                                 small_radius)

    def draw_green_wave(self, screen):
        """Draw enhanced green wave visualization"""
        wave_x = (self.master_timer * VEHICLE_BASE_SPEED) % WINDOW_WIDTH
        self.wave_surface.fill((0, 0, 0, 0))
        
        # Draw animated green wave arrows - more visible
        arrow_spacing = 80
        arrow_length = 50
        arrow_width = 25
        
        for x in range(0, WINDOW_WIDTH + arrow_spacing, arrow_spacing):
            pos = (x + wave_x) % (WINDOW_WIDTH + arrow_spacing) - arrow_spacing
            
            # Draw right-moving arrows on top lane with glow effect
            arrow_y = self.road_width // 4
            points = [
                (pos, arrow_y),
                (pos + arrow_length, arrow_y),
                (pos + arrow_length, arrow_y - arrow_width//2),
                (pos + arrow_length + arrow_width//2, arrow_y),
                (pos + arrow_length, arrow_y + arrow_width//2),
                (pos + arrow_length, arrow_y)
            ]
            
            # Glow effect
            for i in range(3):
                width = 6 - i * 2
                alpha = 100 - i * 30
                glow_color = (*GREEN_WAVE_COLOR, alpha)
                if len(points) > 2:
                    pygame.draw.lines(self.wave_surface, GREEN_WAVE_COLOR, False, points, width)
            
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
            
            # Glow effect
            for i in range(3):
                width = 6 - i * 2
                if len(points) > 2:
                    pygame.draw.lines(self.wave_surface, GREEN_WAVE_COLOR, False, points, width)
        
        # Add pulsing background to make green wave more visible
        pulse = abs(math.sin(time.time() * 3)) * 30 + 20
        wave_bg = pygame.Surface((WINDOW_WIDTH, self.road_width), pygame.SRCALPHA)
        wave_bg.fill((*GREEN_WAVE_COLOR, pulse))
        screen.blit(wave_bg, (0, WINDOW_HEIGHT//2 - self.road_width//2))
        
        screen.blit(self.wave_surface, (0, WINDOW_HEIGHT//2 - self.road_width//2))

    def spawn_vehicle(self):
        # Spawn vehicles less frequently to reduce congestion
        if random.random() < 0.025:  # Reduced from 0.03
            direction = random.choice(['right', 'left'])
            vehicle_class = random.choice(self.image_manager.vehicle_classes)
            
            if direction == 'right':
                x, y = 0, WINDOW_HEIGHT//2 - self.road_width//4
            else:
                x, y = WINDOW_WIDTH, WINDOW_HEIGHT//2 + self.road_width//4
            
            # Check if spawn position is clear
            spawn_clear = True
            for vehicle in self.vehicles:
                if (abs(vehicle.x - x) < MIN_FOLLOWING_DISTANCE and 
                    abs(vehicle.y - y) < 30):
                    spawn_clear = False
                    break
            
            if spawn_clear:
                self.vehicles.append(Vehicle(x, y, direction, self.image_manager, vehicle_class))
            
        if random.random() < 0.008:  # Reduced from 0.01
            junction = random.choice(self.junctions)
            direction = random.choice(['up', 'down'])
            vehicle_class = random.choice(self.image_manager.vehicle_classes)
            
            if direction == 'up':
                x, y = junction.x, WINDOW_HEIGHT
            else:
                x, y = junction.x, 0
            
            # Check if spawn position is clear
            spawn_clear = True
            for vehicle in self.vehicles:
                if (abs(vehicle.x - x) < MIN_FOLLOWING_DISTANCE and 
                    abs(vehicle.y - y) < MIN_FOLLOWING_DISTANCE):
                    spawn_clear = False
                    break
            
            if spawn_clear:
                self.vehicles.append(Vehicle(x, y, direction, self.image_manager, vehicle_class))

    def should_stop_at_light(self, vehicle: Vehicle) -> bool:
        for junction in self.junctions:
            # Check if vehicle is already in this junction
            in_junction_area = (abs(vehicle.x - junction.x) < junction.size/2 and 
                               abs(vehicle.y - junction.y) < junction.size/2)
            
            if in_junction_area:
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
            if approaching and stop_line_distance < SAFE_STOPPING_DISTANCE + 10:
                light_state = junction.lights[vehicle.direction].state
                
                # Stop if the light is red or yellow and we're close to the stop line
                if light_state in ['red', 'yellow'] and stop_line_distance < SAFE_STOPPING_DISTANCE:
                    return True
                    
            # Reset in_junction flag when vehicle has cleared the junction
            elif vehicle.in_junction and not in_junction_area:
                vehicle.in_junction = False
                
        return False

    def update_green_corridor(self):
        # Improved cycle time for better synchronization - reduced red duration
        cycle_time = GREEN_DURATION + 90  # Reduced red duration from 150 to 90
        
        # Junction 1 timing
        j1 = self.junctions[0]
        cycle_position = self.master_timer % cycle_time
        
        if cycle_position < GREEN_DURATION:
            j1.lights['right'].set_state('green')
            j1.lights['left'].set_state('green')
            j1.lights['right'].wave_active = True
            j1.lights['left'].wave_active = True
            
            if cycle_position > GREEN_DURATION - 20:  # Reduced yellow time
                j1.lights['up'].set_state('yellow')
                j1.lights['down'].set_state('yellow')
            else:
                j1.lights['up'].set_state('red')
                j1.lights['down'].set_state('red')
        else:
            j1.lights['up'].set_state('green')
            j1.lights['down'].set_state('green')
            
            if cycle_position > cycle_time - 20:  # Reduced yellow time
                j1.lights['right'].set_state('yellow')
                j1.lights['left'].set_state('yellow')
                j1.lights['right'].wave_active = False
                j1.lights['left'].wave_active = False
            else:
                j1.lights['right'].set_state('red')
                j1.lights['left'].set_state('red')
                j1.lights['right'].wave_active = False
                j1.lights['left'].wave_active = False
        
        # Junction 2 timing - improved offset calculation
        j2 = self.junctions[1]
        # Calculate precise travel time based on actual distance and average speed
        distance_j1_j2 = abs(self.junctions[1].x - self.junctions[0].x)
        travel_time_j1_j2 = int(distance_j1_j2 / (VEHICLE_BASE_SPEED * 1.1))  # Slightly faster sync
        cycle_position_j2 = (self.master_timer - travel_time_j1_j2) % cycle_time
        
        if cycle_position_j2 < GREEN_DURATION:
            j2.lights['right'].set_state('green')
            j2.lights['left'].set_state('green')
            j2.lights['right'].wave_active = True
            j2.lights['left'].wave_active = True
            
            if cycle_position_j2 > GREEN_DURATION - 20:
                j2.lights['up'].set_state('yellow')
                j2.lights['down'].set_state('yellow')
            else:
                j2.lights['up'].set_state('red')
                j2.lights['down'].set_state('red')
        else:
            j2.lights['up'].set_state('green')
            j2.lights['down'].set_state('green')
            
            if cycle_position_j2 > cycle_time - 20:
                j2.lights['right'].set_state('yellow')
                j2.lights['left'].set_state('yellow')
                j2.lights['right'].wave_active = False
                j2.lights['left'].wave_active = False
            else:
                j2.lights['right'].set_state('red')
                j2.lights['left'].set_state('red')
                j2.lights['right'].wave_active = False
                j2.lights['left'].wave_active = False
        
        # Junction 3 timing - improved offset calculation
        j3 = self.junctions[2]
        distance_j2_j3 = abs(self.junctions[2].x - self.junctions[1].x)
        travel_time_j2_j3 = int(distance_j2_j3 / (VEHICLE_BASE_SPEED * 1.1))
        cycle_position_j3 = (self.master_timer - (travel_time_j1_j2 + travel_time_j2_j3)) % cycle_time
        
        if cycle_position_j3 < GREEN_DURATION:
            j3.lights['right'].set_state('green')
            j3.lights['left'].set_state('green')
            j3.lights['right'].wave_active = True
            j3.lights['left'].wave_active = True
            
            if cycle_position_j3 > GREEN_DURATION - 20:
                j3.lights['up'].set_state('yellow')
                j3.lights['down'].set_state('yellow')
            else:
                j3.lights['up'].set_state('red')
                j3.lights['down'].set_state('red')
        else:
            j3.lights['up'].set_state('green')
            j3.lights['down'].set_state('green')
            
            if cycle_position_j3 > cycle_time - 20:
                j3.lights['right'].set_state('yellow')
                j3.lights['left'].set_state('yellow')
                j3.lights['right'].wave_active = False
                j3.lights['left'].wave_active = False
            else:
                j3.lights['right'].set_state('red')
                j3.lights['left'].set_state('red')
                j3.lights['right'].wave_active = False
                j3.lights['left'].wave_active = False

    def draw_scenery(self):
        """Draw background scenery - trees, grass, etc."""
        # Draw grass areas
        grass_color = (34, 139, 34)  # Forest green
        
        # Top grass area
        pygame.draw.rect(self.screen, grass_color, 
                        (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT//2 - self.road_width//2 - 30))
        
        # Bottom grass area  
        pygame.draw.rect(self.screen, grass_color,
                        (0, WINDOW_HEIGHT//2 + self.road_width//2 + 30, 
                         WINDOW_WIDTH, WINDOW_HEIGHT//2 - self.road_width//2 - 30))
        
        # Draw trees randomly but consistently
        random.seed(42)  # Fixed seed for consistent tree placement
        tree_positions = []
        
        # Generate tree positions avoiding roads and junctions
        for _ in range(25):  # Number of trees
            attempts = 0
            while attempts < 50:
                x = random.randint(50, WINDOW_WIDTH - 50)
                y = random.randint(50, WINDOW_HEIGHT - 50)
                
                # Avoid road areas
                if (WINDOW_HEIGHT//2 - self.road_width//2 - 50 < y < WINDOW_HEIGHT//2 + self.road_width//2 + 50):
                    attempts += 1
                    continue
                
                # Avoid junction areas
                too_close_to_junction = False
                for junction in self.junctions:
                    if (abs(x - junction.x) < 80 and abs(y - junction.y) < 80):
                        too_close_to_junction = True
                        break
                
                if not too_close_to_junction:
                    tree_positions.append((x, y))
                    break
                attempts += 1
        
        # Draw trees
        for x, y in tree_positions:
            # Tree trunk
            trunk_color = (101, 67, 33)  # Brown
            pygame.draw.rect(self.screen, trunk_color, (x-3, y-5, 6, 15))
            
            # Tree crown
            crown_color = (0, 100, 0)  # Dark green
            pygame.draw.circle(self.screen, crown_color, (x, y-8), 12)
            # Lighter green highlight
            pygame.draw.circle(self.screen, (0, 128, 0), (x-3, y-10), 6)
        
        # Reset random seed
        random.seed()
        
        # Draw some bushes along the roadside
        bush_color = (0, 100, 0)
        for i in range(0, WINDOW_WIDTH, 150):
            # Top side bushes
            bush_y = WINDOW_HEIGHT//2 - self.road_width//2 - 15
            pygame.draw.ellipse(self.screen, bush_color, (i + 20, bush_y - 8, 25, 16))
            
            # Bottom side bushes
            bush_y = WINDOW_HEIGHT//2 + self.road_width//2 + 5
            pygame.draw.ellipse(self.screen, bush_color, (i + 80, bush_y, 25, 16))

    def draw_roads(self):
        pygame.draw.rect(self.screen, ROAD_COLOR, 
                        (0, WINDOW_HEIGHT//2 - self.road_width//2, 
                         WINDOW_WIDTH, self.road_width))
        
        for junction in self.junctions:
            pygame.draw.rect(self.screen, ROAD_COLOR,
                           (junction.x - self.road_width//2, 0,
                            self.road_width, WINDOW_HEIGHT))
        
        # Draw road markings
        dash_length = 30
        gap_length = 30
        for x in range(0, WINDOW_WIDTH, dash_length + gap_length):
            pygame.draw.rect(self.screen, WHITE,
                           (x, WINDOW_HEIGHT//2 - 2, dash_length, 4))
        
        for junction in self.junctions:
            for y in range(0, WINDOW_HEIGHT, dash_length + gap_length):
                pygame.draw.rect(self.screen, WHITE,
                               (junction.x - 2, y, 4, dash_length))

    def draw_green_wave(self, screen):
        """Enhanced green wave visualization"""
        wave_x = (self.master_timer * VEHICLE_BASE_SPEED) % WINDOW_WIDTH
        
        # Create a more visible wave surface
        wave_surface = pygame.Surface((WINDOW_WIDTH, self.road_width), pygame.SRCALPHA)
        
        # Draw animated green wave with better visibility
        arrow_spacing = 80
        arrow_length = 30
        arrow_width = 12
        
        # Make the wave more prominent with multiple layers
        for layer in range(3):
            alpha = 100 - (layer * 20)  # Decreasing opacity for layers
            wave_color = (*GREEN_WAVE_COLOR[:3], alpha)
            
            for x in range(0, WINDOW_WIDTH + arrow_spacing, arrow_spacing):
                pos = (x + wave_x + layer * 10) % (WINDOW_WIDTH + arrow_spacing) - arrow_spacing
                
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
                if len(points) > 2:
                    pygame.draw.polygon(wave_surface, wave_color, points)
                
                # Draw left-moving arrows on bottom lane
                arrow_y = self.road_width * 3 // 4
                points = [
                    (pos + arrow_length + arrow_width//2, arrow_y),
                    (pos + arrow_length, arrow_y - arrow_width//2),
                    (pos, arrow_y),
                    (pos + arrow_length, arrow_y + arrow_width//2)
                ]
                if len(points) > 2:
                    pygame.draw.polygon(wave_surface, wave_color, points)
        
        # Add pulsing effect
        pulse = abs(math.sin(self.master_timer * 0.1)) * 30 + 70
        wave_glow = pygame.Surface((WINDOW_WIDTH, self.road_width), pygame.SRCALPHA)
        pygame.draw.rect(wave_glow, (0, 255, 0, int(pulse)), 
                        (0, 0, WINDOW_WIDTH, self.road_width))
        
        # Blend the surfaces
        screen.blit(wave_glow, (0, WINDOW_HEIGHT//2 - self.road_width//2))
        screen.blit(wave_surface, (0, WINDOW_HEIGHT//2 - self.road_width//2))

    def draw_corridor_info(self):
        # Calculate actual travel times
        distance_j1_j2 = abs(self.junctions[1].x - self.junctions[0].x)
        distance_j2_j3 = abs(self.junctions[2].x - self.junctions[1].x)
        travel_time_j1_j2 = distance_j1_j2 / (VEHICLE_BASE_SPEED * FPS)
        travel_time_j2_j3 = distance_j2_j3 / (VEHICLE_BASE_SPEED * FPS)
        
        time_j1_to_j2 = f"J1→J2: {travel_time_j1_j2:.1f}s"
        time_j2_to_j3 = f"J2→J3: {travel_time_j2_j3:.1f}s"
        
        text_j1_j2 = FONT.render(time_j1_to_j2, True, WHITE)
        text_j2_j3 = FONT.render(time_j2_to_j3, True, WHITE)
        
        mid_x_j1_j2 = (self.junctions[0].x + self.junctions[1].x) // 2
        mid_x_j2_j3 = (self.junctions[1].x + self.junctions[2].x) // 2
        
        # Move text higher up and add background for better visibility
        text_y = WINDOW_HEIGHT//2 - 80
        
        # Draw background rectangles for text
        bg_rect_1 = pygame.Rect(mid_x_j1_j2 - 40, text_y - 5, 80, 20)
        bg_rect_2 = pygame.Rect(mid_x_j2_j3 - 40, text_y - 5, 80, 20)
        
        pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect_1)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect_2)
        
        self.screen.blit(text_j1_j2, (mid_x_j1_j2 - 35, text_y))
        self.screen.blit(text_j2_j3, (mid_x_j2_j3 - 35, text_y))
        
        # Enhanced corridor status
        corridor_status = FONT.render("🟢 Smart Green Corridor - Optimized Synchronization", True, (0, 100, 0))
        corridor_rect = corridor_status.get_rect(center=(WINDOW_WIDTH//2, 25))
        
        # Background for main title
        bg_main = pygame.Rect(corridor_rect.x - 10, corridor_rect.y - 5, 
                             corridor_rect.width + 20, corridor_rect.height + 10)
        pygame.draw.rect(self.screen, (255, 255, 255, 200), bg_main)
        self.screen.blit(corridor_status, corridor_rect)
        
        # Display vehicle count with better styling
        vehicle_count_text = FONT.render(f"🚗 Active Vehicles: {len(self.vehicles)}", True, (0, 0, 100))
        count_rect = pygame.Rect(10, 10, 150, 20)
        pygame.draw.rect(self.screen, (255, 255, 255, 180), count_rect)
        self.screen.blit(vehicle_count_text, (15, 13))

    def update(self):
        self.master_timer += 1
        self.spawn_vehicle()
        
        self.update_green_corridor()
        
        for junction in self.junctions:
            junction.update(self.master_timer, self.vehicles)
        
        # Update vehicles with collision detection
        for vehicle in self.vehicles[:]:
            # Update speed based on traffic conditions (includes collision detection)
            vehicle.update_speed(self.vehicles)
            
            # Check traffic light conditions
            if self.should_stop_at_light(vehicle):
                vehicle.waiting = True
            else:
                vehicle.waiting = False
                vehicle.move()
            
            # Remove vehicles that have left the screen
            if (vehicle.x < -50 or vehicle.x > WINDOW_WIDTH + 50 or
                vehicle.y < -50 or vehicle.y > WINDOW_HEIGHT + 50):
                self.vehicles.remove(vehicle)

    def draw(self):
        self.screen.fill((135, 206, 235))  # Sky blue background
        self.draw_scenery()  # Draw scenery first (background)
        self.draw_roads()
        self.draw_green_wave(self.screen)  # Enhanced green wave
        
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