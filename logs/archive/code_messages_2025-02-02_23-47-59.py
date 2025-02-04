C:\mygit\BLazy\repo\scad\utils.scad
Language detected: openscad
// Common constants for 3D printing tolerances
$fn = 50; // Set the number of fragments for cylinders and circles
PRINT_TOLERANCE = 0.1; // Tolerance for 3D printing in mm

// Utility functions for creating rounded corners
module round_corner(size, radius) {
    // Create a quarter cylinder to form a rounded corner
    difference() {
        cylinder(h=size, d=2*radius, $fn=$fn); // Cylinder
        translate([0, 0, size]) cube([radius*2, radius*2, size]); // Cut out the corner
    }
}

module chamfer_cube(size, chamfer_size) {
    // Create a cube with chamfered edges
    union() {
        cube(size - [chamfer_size*2, chamfer_size*2, 0]);
        translate([0, 0, size[2] - chamfer_size]) round_corner(size[0], chamfer_size);
        translate([size[0] - chamfer_size, 0, 0]) rotate([0, 0, 90]) round_corner(size[1], chamfer_size);
        translate([0, size[1] - chamfer_size, 0]) rotate([0, 0, 270]) round_corner(size[0], chamfer_size);
        translate([size[0] - chamfer_size, size[1] - chamfer_size, 0]) rotate([0, 0, 180]) round_corner(size[1], chamfer_size);
        translate([(size[0] - chamfer_size) / 2, (size[1] - chamfer_size) / 2, size[2] - chamfer_size]) 
            rotate([90, 0, 0]) round_corner(size[1], chamfer_size);
        translate([(size[0] - chamfer_size) / 2, (size[1] - chamfer_size) / 2, size[2] - chamfer_size])
            rotate([270, 0, 0]) round_corner(size[1], chamfer_size);
        translate([(size[0] - chamfer_size) / 2, (size[1] - chamfer_size) / 2, size[2] - chamfer_size])
            rotate([0, 90, 0]) round_corner(size[0], chamfer_size);
        translate([(size[0] - chamfer_size) / 2, (size[1] - chamfer_size) / 2, size[2] - chamfer_size])
            rotate([0, 270, 0]) round_corner(size[0], chamfer_size);
    }
}

// Basic geometric helper functions
module offset_polygon(points, offset_distance) {
    // Offset a polygon by a given distance
    hull() {
        for (p = points) {
            translate(p) circle(d=offset_distance * 2, $fn=$fn);
        }
    }
}

// Example usage
cube_size = [50, 50, 20];
chamfer_size = 5;
chamfer_cube(cube_size, chamfer_size);
C:\mygit\BLazy\repo\scad\bearing.scad
Language detected: openscad
// Include the utils.scad file
include <utils.scad>

// Define parameters for the bearing
outer_diameter = 30; // Outer diameter of the bearing
inner_diameter = 20; // Inner diameter of the bearing
height = 10;        // Height of the bearing
num_balls = 6;      // Number of balls
ball_diameter = 5;  // Diameter of each ball
clearance = 0.2;    // Clearance between inner diameter and balls
retention_wall_height = 1; // Height of the retention wall
chamfer_size = 1;   // Chamfer size at the edges for easier printing

// Calculate effective diameters and positions
ball_position_radius = (inner_diameter / 2) + (ball_diameter / 2) + clearance;
ball_retention_radius = (inner_diameter / 2) + clearance;

// Define points for a hexagon pattern for ball positions (for even number of balls)
points = [];
angle_offset = 360 / num_balls;
for (i = [0 : num_balls-1]) {
    angle = i * angle_offset;
    x = ball_position_radius * cos(angle);
    y = ball_position_radius * sin(angle);
    points = points + [[x, y]];
}

// Module for a single ball
module ball() {
    sphere(d=ball_diameter);
}

// Module for a ball cage with retention walls
module ball_cage() {
    difference() {
        cylinder(h=height, d=inner_diameter, $fn=$fn);
        translate([0, 0, height-retention_wall_height]) 
            cylinder(h=retention_wall_height, d=inner_diameter + 2*clearance, $fn=$fn);
    }
}

// Module for ball retainer walls
module ball_retainer() {
    translate([0, 0, retention_wall_height]) 
        offset_polygon(points, ball_diameter / 2 + clearance);
}

// Main bearing module
module in_place_bearing() {
    union() {
        translate([0, 0, height/2]) ball_cage();
        for (ball_pos : points) {
            translate(ball_pos) ball();
        }
        ball_retainer();
    }
}

// Add chamfer to the edges for easier printing
translate([0, 0, -chamfer_size]) 
    cuboid([outer_diameter, outer_diameter, height + chamfer_size * 2], chamfer_size);

// Render the bearing
in_place_bearing();
C:\mygit\BLazy\repo\scad\hinge.scad
Language detected: scad
// Include the utils.scad file
include <utils.scad>

// Define parameters for the hinge
hinge_length = 50;           // Length of the hinge
hinge_width = 10;            // Width of the hinge
pin_diameter = 4;            // Diameter of the pin
num_knuckles = 5;            // Number of knuckles on the hinge
knuckle_spacing = 5;         // Spacing between knuckles
rotation_limit = 90;         // Rotation limit in degrees
chamfer_size = 1;            // Chamfer size at the edges for easier printing
print_tolerance = 0.2;       // Tolerance for 3D printing in mm

// Calculate effective dimensions and positions
knuckle_height = pin_diameter + 2 * print_tolerance;
knuckle_length = (hinge_length - (num_knuckles - 1) * knuckle_spacing) / num_knuckles;

// Define points for the knuckles
knuckle_positions = [];
for (i = [0 : num_knuckles - 1]) {
    position = i * (knuckle_length + knuckle_spacing) + knuckle_length / 2;
    knuckle_positions = knuckle_positions + [[position, hinge_width / 2]];
}

// Module for a single knuckle
module knuckle() {
    translate([0, 0, -knuckle_height / 2]) cube([hinge_width, pin_diameter, knuckle_height]);
}

// Module for the knuckle with chamfer
module chamfered_knuckle() {
    translate([0, 0, -knuckle_height / 2]) 
        chamfer_cube([hinge_width, pin_diameter, knuckle_height], chamfer_size);
}

// Module for the hinge pin
module hinge_pin() {
    union() {
        translate([-pin_diameter / 2, 0, 0]) cube([pin_diameter, hinge_width, hinge_length]);
        for (pos : knuckle_positions) {
            translate(pos) knuckle();
        }
    }
}

// Optional stop mechanism
module hinge_stop() {
    translate([hinge_length / 2 - pin_diameter / 2, 0, 0]) cube([pin_diameter, hinge_width, hinge_length / 2]);
}

// Module for the complete hinge
module in_place_hinge() {
    union() {
        translate([0, 0, hinge_length / 2]) hinge_pin();
        for (pos : knuckle_positions) {
            translate(pos) chamfered_knuckle();
        }
        if (rotation_limit < 360) {
            translate([0, 0, -hinge_length / 2]) hinge_stop();
        }
    }
}

// Add chamfer to the edges for easier printing
translate([0, 0, -chamfer_size]) 
    cuboid([hinge_length, hinge_width, hinge_length + chamfer_size * 2], chamfer_size);

// Render the hinge
in_place_hinge();
C:\mygit\BLazy\repo\scad\gear.scad
Language detected: openscad
// Include the utils.scad file
include <utils.scad>

// Define parameters for the gear
gear_diameter = 50;             // Diameter of the gear
number_of_teeth = 20;           // Number of teeth on the gear
tooth_profile = "involute";     // Tooth profile can be "involute" or "triangular"
gear_thickness = 10;            // Thickness of the gear
module_ratio = 1.25;            // Module ratio for gear design
pressure_angle = 20;            // Pressure angle in degrees
helical_angle = 0;              // Helical angle in degrees (0 for spur gears)
center_bore = 10;               // Diameter of the center bore
spokes = 4;                     // Number of spokes for hub
spoke_width = 2;                // Width of each spoke
helix_direction = "right";      // Direction of helical gear, can be "left" or "right"

// Internal function to calculate the pitch diameter
pitch_diameter = gear_diameter - 2 * module_ratio;

// Calculated values
module_value = gear_diameter / number_of_teeth;
tooth_height = 2.25 * module_value; // Approximation for tooth height
tooth_depth = tooth_height - 1.25 * module_value; // Calculated tooth depth
tooth_clearance = module_value * 0.15; // Clearance for 3D printing
backlash = 0.05; // Backlash for smooth operation

// Calculate tooth profile
function involute_to_radius(phi) = (module_value * phi) / 2 + sqrt((module_value * phi / 2) ^ 2 + (module_value / 2) ^ 2);
function involute_to_angle(r) = 2 * atan(module_value / (2 * (r - module_value / 2)));

module involute_tooth() {
    rotate(a=-90) linear_extrude(height=gear_thickness)
        polygon(points=[
            [involute_to_radius(pressure_angle), pressure_angle],
            [0, 180],
            [-involute_to_radius(pressure_angle), pressure_angle]
        ]);
}

module triangular_tooth() {
    rotate(a=-90) linear_extrude(height=gear_thickness)
        polygon(points=[
            [module_value / 2, 0],
            [module_value / 2, 180],
            [-module_value / 2, 180],
            [-module_value / 2, 0],
            [module_value / 2, 0]
        ]);
}

module tooth() {
    if (tooth_profile == "involute") {
        involute_tooth();
    } else {
        triangular_tooth();
    }
}

module gear() {
    union() {
        for (i = [0 : number_of_teeth - 1]) {
            rotate(i * (360 / number_of_teeth)) translate([pitch_diameter / 2, 0, 0]) tooth();
        }
    }
    difference() {
        translate([0, 0, -chamfer_size]) cuboid([gear_diameter, gear_diameter, gear_thickness + chamfer_size * 2], chamfer_size);
        // Add center bore
        translate([0, 0, gear_thickness / 2]) rotate([0, 0, center_bore / 2]) cylinder(d=center_bore, h=gear_thickness + chamfer_size * 2, $fn=$fn);
    }
    // Add spokes for the hub
    for (i = [0 : spokes - 1]) {
        rotate(i * (360 / spokes)) translate([pitch_diameter / 2, 0, 0]) cube([spoke_width, gear_thickness, pitch_diameter / 2]);
    }
}

// Render the gear
gear();
C:\mygit\BLazy\repo\scad\spring.scad
Language detected: openscad
C:\mygit\BLazy\repo\scad\ratchet.scad
Language detected: openscad
// Include the utils.scad file
include <utils.scad>

// Define parameters for the ratchet wheel
wheel_diameter = 50;            // Diameter of the ratchet wheel
number_of_teeth = 12;           // Number of teeth on the wheel
tooth_height = 2;               // Height of each tooth
tooth_angle = 30;               // Angle of each tooth (e.g., 30 degrees)
print_tolerance = 0.2;          // Tolerance for 3D printing in mm

// Define parameters for the pawl
pawl_length = 10;               // Length of the pawl
pawl_width = 2;                 // Width of the pawl
spring_arm_length = 15;         // Length of the pawl's spring arm
spring_arm_thickness = 1;       // Thickness of the spring arm
mounting_point = [0, 0, 0];     // Mounting point of the pawl relative to the wheel

// Function to calculate the arc length for tooth generation
function tooth_arc_length(radius, angle_degrees) = (angle_degrees * PI / 180) * radius;

// Define a module for a single tooth
module tooth() {
    translate([wheel_diameter / 2 - tooth_height, 0, 0])
    rotate([90, 0, 90 - tooth_angle / 2]) 
    linear_extrude(height=tooth_height)
    polygon(points=[
        [0, 0],
        [0, tooth_height],
        [tooth_arc_length(wheel_diameter / 2 - tooth_height / 2, tooth_angle), tooth_height / 2]
    ]);
}

// Define a module for the ratchet wheel
module ratchet_wheel() {
    union() {
        for (i = [0 : number_of_teeth - 1]) {
            rotate(i * (360 / number_of_teeth))
            translate([wheel_diameter / 2, 0, 0])
            tooth();
        }
        translate([0, 0, -print_tolerance]) cylinder(h=wheel_diameter + 2 * print_tolerance, r=wheel_diameter / 2, $fn=$fn);
    }
}

// Define a module for the pawl
module pawl() {
    translate(mounting_point)
    linear_extrude(height=pawl_length)
    polygon(points=[[0, 0], [pawl_width, 0], [pawl_width, -spring_arm_length], [0, -spring_arm_length]]);
    
    translate([0, -spring_arm_length, 0])
    cylinder(d=spring_arm_thickness, h=spring_arm_length * 2);
}

module spring_arm() {
    translate([pawl_length, 0, -spring_arm_length])
    cylinder(d=spring_arm_thickness, h=spring_arm_length);
}

// Render the full ratchet mechanism (with both linear and rotational options)
linear_extrude(height=ratchet_wheel().$children[0].size[2])
    ratchet_wheel();
union() {
    translate(mounting_point)
    pawl();
    spring_arm();
}

// Ensure that the pawl is within the wheel and clearances are set appropriately
if (pawl_length > wheel_diameter / 2 || pawl_width > wheel_diameter / 2) {
    echo("Pawl dimensions exceed the size of the ratchet wheel!");
} else {
    // Render the full mechanism
    ratchet_wheel();
    translate(mounting_point)
    union() {
        pawl();
        spring_arm();
    }
}
C:\mygit\BLazy\repo\scad\snap_fit.scad
Language detected: OpenSCAD
// Include the utils.scad file
include <utils.scad>

// Define parameters for the snap-fit connections
snap_size = 10;            // Size of the snap-fit connection
engagement_angle = 30;     // Angle at which the snap starts to engage
clearance = 0.2;           // Clearance for assembly
wall_thickness = 2;        // Wall thickness of the part
material_flex = 0.1;       // Material flex considerations
chamfer_size = 1;          // Chamfer size for easier printing

// Function to calculate engagement arc length based on the engagement angle
function engagement_arc_length(diameter, angle_degrees) = (angle_degrees * PI / 180) * (diameter / 2);

// Module for a hook-style snap
module hook_snap() {
    union() {
        translate([0, 0, snap_size / 2 + clearance]) 
            chamfer_cube([snap_size, snap_size, snap_size], chamfer_size);
        translate([0, 0, snap_size / 2]) 
            translate([snap_size / 2, snap_size / 2, 0])
            offset_polygon([
                [-engagement_arc_length(snap_size / 2, engagement_angle), 0], 
                [0, snap_size / 2], 
                [snap_size / 2, 0]
            ], snap_size / 5);
    }
}

// Module for a ball-and-socket joint
module ball_socket_joint() {
    union() {
        translate([0, 0, snap_size / 2 + clearance]) 
            sphere(d=snap_size);
        translate([0, 0, snap_size / 2]) 
            offset_polygon([
                [-engagement_arc_length(snap_size / 2, engagement_angle), 0], 
                [0, snap_size / 2], 
                [snap_size / 2, 0]
            ], snap_size / 5);
    }
}

// Module for a cantilever snap
module cantilever_snap() {
    union() {
        translate([0, 0, snap_size / 2 + clearance]) 
            cube([snap_size, snap_size, snap_size]);
        translate([0, 0, snap_size / 2]) 
            translate([snap_size / 2, snap_size / 2, 0])
            rotate([0, 0, engagement_angle])
            cube([snap_size, snap_size / 5, snap_size]);
    }
}

// Module for a living hinge
module living_hinge() {
    union() {
        translate([0, -snap_size / 2, snap_size / 2]) 
            cube([snap_size, snap_size / 5, snap_size]);
        translate([snap_size / 2, 0, snap_size / 2]) 
            rotate([0, 0, engagement_angle])
            translate([0, snap_size / 2, 0])
            cube([snap_size / 2, snap_size, snap_size]);
    }
}

// Example of snap-fit connections
hook_snap();
translate([0, snap_size + clearance, 0]) ball_socket_joint();
translate([0, 2 * (snap_size + clearance), 0]) cantilever_snap();
translate([0, 3 * (snap_size + clearance), 0]) living_hinge();
C:\mygit\BLazy\repo\scad\track_system.scad
Language detected: openscad
// Include the utils.scad file
include <utils.scad>

// Define parameters for the track system
track_width = 10;            // Width of the track
track_depth = 5;             // Depth of the track
guide_rail_dim = 1;          // Dimension of the guide rail
detent_spacing = 5;          // Spacing between detents
detent_depth = 1;            // Depth of the detents
clearance = 0.2;             // Clearance for smooth movement
stop_positions = [];         // List of stop positions
stop_types = [];             // Types of stops (e.g., "pin", "tab")
slider_width = track_width - 2 * guide_rail_dim; // Width of the slider
slider_depth = track_depth - guide_rail_dim;    // Depth of the slider
chamfer_size = 1;            // Chamfer size for easier printing

// Function to calculate detents positions
function calc_detent_positions() = [for (i = [0 : detent_spacing / slider_width - 1]) i * slider_width];

// Module for a detent
module detent() {
    translate([0, 0, -detent_depth / 2])
    cube([slider_width, guide_rail_dim, detent_depth]);
}

// Module for guide rails
module guide_rails() {
    translate([0, track_depth / 2 - guide_rail_dim / 2, 0])
    cube([track_width, guide_rail_dim, track_depth]);
    
    translate([0, -track_depth / 2 + guide_rail_dim / 2, 0])
    cube([track_width, guide_rail_dim, track_depth]);
}

// Module for a track section
module track_section() {
    union() {
        translate([0, 0, -track_depth / 2])
        cube([track_width, track_depth, track_depth]);
        
        for (position : calc_detent_positions()) {
            translate([position, 0, track_depth / 2])
            detent();
        }

        guide_rails();
    }
}

// Module for a slider
module slider() {
    union() {
        translate([0, 0, track_depth / 2])
        cube([slider_width, slider_depth, track_depth - 2 * guide_rail_dim]);

        translate([0, slider_depth / 2 - guide_rail_dim / 2, 0])
        cube([slider_width, guide_rail_dim, slider_depth]);
        
        translate([0, -slider_depth / 2 + guide_rail_dim / 2, 0])
        cube([slider_width, guide_rail_dim, slider_depth]);
    }
}

// Function for anti-binding features
function anti_binding_features() = [
    translate([0, 0, track_depth / 2]) chamfer_cube([slider_width, slider_depth, track_depth - 2 * guide_rail_dim], chamfer_size),
    translate([0, slider_depth / 2 - guide_rail_dim / 2, 0]) chamfer_cube([slider_width, guide_rail_dim, slider_depth], chamfer_size),
    translate([0, -slider_depth / 2 + guide_rail_dim / 2, 0]) chamfer_cube([slider_width, guide_rail_dim, slider_depth], chamfer_size)
];

// Render the track system
track_section();
slider();

// Example of slider and track
translate([0, 0, slider_depth / 2])
slider();
C:\mygit\BLazy\repo\scad\fidget_toy.scad
Language detected: openscad
// Include the necessary modules
include <utils.scad>
include <bearing.scad>
include <hinge.scad>
include <gear.scad>
include <ratchet.scad>
include <spring.scad>
include <snap_fit.scad>
include <track_system.scad>

// Define parameters for the main assembly
hub_diameter = 60;              // Overall diameter of the central hub
hub_thickness = 15;             // Thickness of the central hub
hub_clearance = 0.2;            // Clearance for the hub
chamfer_size = 1;               // Chamfer size for ease of printing

// Main assembly structure
module fidget_toy_assembly() {
    union() {
        // Central hub to hold all the components
        translate([0, 0, hub_thickness / 2])
        chamfer_cube([hub_diameter, hub_diameter, hub_thickness], chamfer_size);

        // Place the gear
        translate([0, -hub_diameter / 2 + gear.gear_diameter / 2, 2])
        gear();

        // Place the spring
        translate([0, hub_diameter / 2 - spring.spring_spring_diameter / 2 - 5, 2])
        spring();

        // Place the bearing
        translate([hub_diameter / 2 - bearing.outer_diameter / 2, 0, 2])
        bearing();

        // Place the hinge
        translate([-hub_diameter / 2 + hinge.hinge_length / 2, 0, 2])
        hinge();

        // Place the ratchet wheel
        translate([0, hub_diameter / 2 - ratchet.wheel_diameter / 2, 2])
        ratchet();

        // Track system for sliding elements
        translate([-hub_diameter, hub_diameter / 2 - track_system.track_depth / 2, 2])
        track_system();
    }
}

// Render the main fidget toy assembly
fidget_toy_assembly();

// Documentation and Notes:
// The assembly includes a central hub with various components placed around it.
// Each component has its own dedicated space and proper clearances.
// The fidget toy can be customized by adjusting the parameters such as overall size and configuration.
// Ensure all components are designed to be printed in place without supports.
C:\mygit\BLazy\repo\scad\fidget_toy_v2.scad
Language detected: openscad
// Include the necessary modules
include <utils.scad>
include <bearing.scad>
include <hinge.scad>
include <gear.scad>
include <ratchet.scad>
include <spring.scad>
include <snap_fit.scad>
include <track_system.scad>

// Define parameters to enable/disable specific components
enable_bearing = true;
enable_gear = true;
enable_hinge = true;
enable_ratchet = true;
enable_spring = true;
enable_track_system = true;

// Define color schemes
colors = ["Red", "Green", "Blue"];
default_color = colors[0];

// Define size presets
size_presets = ["Small", "Medium", "Large"];
preset_size = size_presets[1];

// Define default sizes and configurations
hub_diameter = 60; // Overall diameter of the central hub
hub_thickness = 15; // Thickness of the central hub
chamfer_size = 1; // Chamfer size for ease of printing

// Configure parameters dynamically based on size preset
if (preset_size == "Small") {
    hub_diameter = 30;
    hub_thickness = 7.5;
}
else if (preset_size == "Large") {
    hub_diameter = 90;
    hub_thickness = 22.5;
}

// Main assembly structure
module fidget_toy_assembly() {
    union() {
        // Central hub to hold all the components
        translate([0, 0, hub_thickness / 2])
        chamfer_cube([hub_diameter, hub_diameter, hub_thickness], chamfer_size);
        
        // Gear Assembly
        if (enable_gear) {
            translate([0, -hub_diameter / 2 + gear.gear_diameter / 2, 2])
            color(default_color) gear();
        }
        
        // Spring Assembly
        if (enable_spring) {
            translate([0, hub_diameter / 2 - spring.coil_spring_diameter / 2 - 5, 2])
            color(default_color) spring();
        }
        
        // Bearing Assembly
        if (enable_bearing) {
            translate([hub_diameter / 2 - bearing.outer_diameter / 2, 0, 2])
            color(default_color) bearing();
        }
        
        // Hinge Assembly
        if (enable_hinge) {
            translate([-hub_diameter / 2 + hinge.hinge_length / 2, 0, 2])
            color(default_color) hinge();
        }
        
        // Ratchet Assembly
        if (enable_ratchet) {
            translate([0, hub_diameter / 2 - ratchet.wheel_diameter / 2, 2])
            color(default_color) ratchet();
        }
        
        // Track System
        if (enable_track_system) {
            translate([-hub_diameter, hub_diameter / 2 - track_system.track_depth / 2, 2])
            color(default_color) track_system();
        }
    }
}

// Render the main fidget toy assembly
fidget_toy_assembly();

// Documentation and Notes:
// The assembly includes a central hub with various components placed around it.
// Each component has its own dedicated space and proper clearances.
// The fidget toy can be customized by:
// - Enabling or disabling specific components using enable_* variables.
// - Selecting color schemes from the default options.
// - Choosing size presets: small, medium, large, and custom sizes.
// Ensure all components are designed to be printed in place without additional support structures.
C:\mygit\BLazy\repo\scad\config.scad
Language detected: openscad
// OpenSCAD configuration file for the fidget toy settings

// 1. Global Settings
$fn = 50; // set the number of fragments for cylinders and circles
PRINT_TOLERANCE = 0.2; // Tolerance for 3D printing in mm
DEFAULT_CLEARANCE = 0.2; // Default clearance between parts for smooth movement
LAYER_HEIGHT = 0.2; // Suggested layer height for 3D printing

// 2. Size Configurations
SIZE_PRESETS = ["Small", "Medium", "Large"];
preset_size = SIZE_PRESETS[1];

if (preset_size == "Small") {
    HUB_DIAMETER = 30;
    HUB_THICKNESS = 7.5;
    CHAMFER_SIZE = 0.5;
} else if (preset_size == "Large") {
    HUB_DIAMETER = 90;
    HUB_THICKNESS = 22.5;
    CHAMFER_SIZE = 1.5;
} else {
    HUB_DIAMETER = 60;
    HUB_THICKNESS = 15;
    CHAMFER_SIZE = 1;
}

// 3. Component-specific Parameters
// Bearing configurations
BEARING_OUTER_DIAMETER = 30;
BEARING_INNER_DIAMETER = 20;
BEARING_HEIGHT = 10;
BALL_DIAMETER = 5;
NUM_BALLS = 6;

// Gear ratios and sizes
GEAR_DIAMETER = 50;
NUMBER_OF_TEETH = 20;
TOOTH_PROFILE = "involute";
GEAR_THICKNESS = 10;

// Spring constants
LEAF_SPRING_WIDTH = 2;
LEAF_SPRING_THICKNESS = 1;
LEAF_SPRING_LENGTH = 50;
LEAF_SPRING_COUNT = 5;

COIL_SPRING_DIAMETER = 20;
COIL_SPRING_WIRE_DIAMETER = 2;
COIL_SPRING_COILS = 5;
COIL_SPRING_HEIGHT = 30;

TORSION_SPRING_DIAMETER = 20;
TORSION_SPRING_WIRE_DIAMETER = 2;
TORSION_SPRING_COILS = 5;
TORSION_SPRING_ARM_LENGTH = 50;

// Track system dimensions
TRACK_WIDTH = 10;
TRACK_DEPTH = 5;
GUIDE_RAIL_DIM = 1;
DETENT_SPACING = 5;
DETENT_DEPTH = 1;

// Ratchet settings
WHEEL_DIAMETER = 50;
NUMBER_OF_TEETH = 12;
TOOTH_HEIGHT = 2;
TOOTH_ANGLE = 30;

// Hinge parameters
HINGE_LENGTH = 50;
HINGE_WIDTH = 10;
PIN_DIAMETER = 4;
KNUCKLE_SPACING = 5;

// Snap-fit tolerances
SNAP_SIZE = 10;
ENGAGEMENT_ANGLE = 30;
CLEARANCE = 0.2;
WALL_THICKNESS = 2;

// 4. Aesthetic Options
COLOR_SCHEMES = ["Red", "Green", "Blue"];
default_color = COLOR_SCHEMES[0];

// Function to set color based on the selected scheme
function select_color(color_name) = {
    if (color_name == "Red") {
        return "red";
    } else if (color_name == "Green") {
        return "green";
    } else if (color_name == "Blue") {
        return "blue";
    } else {
        return "grey";
    }
};

// Usage of color function
selected_color = select_color(default_color);

// Module for the fidget toy assembly
module fidget_toy_assembly() {
    union() {
        // Central hub to hold all the components
        translate([0, 0, HUB_THICKNESS / 2])
        chamfer_cube([HUB_DIAMETER, HUB_DIAMETER, HUB_THICKNESS], CHAMFER_SIZE);

        // Components
        if (enable_gear) {
            translate([0, -HUB_DIAMETER / 2 + GEAR_DIAMETER / 2, 2])
            color(selected_color) gear(gear_diameter = GEAR_DIAMETER,
                                       number_of_teeth = NUMBER_OF_TEETH,
                                       tooth_profile = TOOTH_PROFILE,
                                       gear_thickness = GEAR_THICKNESS);
        }
        
        if (enable_spring) {
            translate([0, HUB_DIAMETER / 2 - COIL_SPRING_DIAMETER / 2 - 5, 2])
            color(selected_color) spring(leaf_spring_width = LEAF_SPRING_WIDTH,
                                          leaf_spring_thickness = LEAF_SPRING_THICKNESS,
                                          leaf_spring_length = LEAF_SPRING_LENGTH,
                                          leaf_spring_count = LEAF_SPRING_COUNT,
                                          coil_spring_diameter = COIL_SPRING_DIAMETER,
                                          coil_spring_wire_diameter = COIL_SPRING_WIRE_DIAMETER,
                                          coil_spring_coils = COIL_SPRING_COILS,
                                          coil_spring_height = COIL_SPRING_HEIGHT);
        }
        
        if (enable_bearing) {
            translate([HUB_DIAMETER / 2 - BEARING_OUTER_DIAMETER / 2, 0, 2])
            color(selected_color) bearing(outer_diameter = BEARING_OUTER_DIAMETER,
                                           inner_diameter = BEARING_INNER_DIAMETER,
                                           height = BEARING_HEIGHT,
                                           num_balls = NUM_BALLS,
                                           ball_diameter = BALL_DIAMETER);
        }
        
        if (enable_hinge) {
            translate([-HUB_DIAMETER / 2 + HINGE_LENGTH / 2, 0, 2])
            color(selected_color) hinge(hinge_length = HINGE_LENGTH,
                                         hinge_width = HINGE_WIDTH,
                                         pin_diameter = PIN_DIAMETER,
                                         num_knuckles = 5,
                                         knuckle_spacing = KNUCKLE_SPACING);
        }
        
        if (enable_ratchet) {
            translate([0, HUB_DIAMETER / 2 - WHEEL_DIAMETER / 2, 2])
            color(selected_color) ratchet(wheel_diameter = WHEEL_DIAMETER,
                                           number_of_teeth = NUMBER_OF_TEETH,
                                           tooth_height = TOOTH_HEIGHT,
                                           tooth_angle = TOOTH_ANGLE);
        }
        
        if (enable_track_system) {
            translate([-HUB_DIAMETER, HUB_DIAMETER / 2 - TRACK_DEPTH / 2, 2])
            color(selected_color) track_system(track_width = TRACK_WIDTH,
                                                track_depth = TRACK_DEPTH,
                                                guide_rail_dim = GUIDE_RAIL_DIM,
                                                detent_spacing = DETENT_SPACING,
                                                detent_depth = DETENT_DEPTH);
        }
    }
}

// Render the main fidget toy assembly
fidget_toy_assembly();
C:\mygit\BLazy\repo\scad\test_prints.scad
Language detected: openscad
// Comprehensive test suite for fidget toy components in OpenSCAD

include <config.scad>
include <bearing.scad>
include <hinge.scad>
include <gear.scad>
include <ratchet.scad>
include <spring.scad>
include <snap_fit.scad>
include <track_system.scad>

// Tolerance Tests
module tolerance_test() {
    // Test various clearances and gaps
    difference() {
        // Base cube
        cube([10, 10, 10]);
        // Smaller cube with clearance
        translate([1, 1, 1])
        cube([8, 8, 8]);
    }
}

// Feature Size Tests
module feature_size_test() {
    // Test small and large features
    union() {
        // Small feature
        translate([0, 0, 0])
        cube([5, 5, 5]);
        // Large feature
        translate([10, 0, 0])
        cube([10, 10, 10]);
    }
}

// Component-Specific Tests
module bearing_test() {
    // Test bearing components
    bearing(outer_diameter = 30, inner_diameter = 20, height = 10, num_balls = 6, ball_diameter = 5);
}

module hinge_test() {
    // Test hinge components
    hinge(hinge_length = 50, hinge_width = 10, pin_diameter = 4, num_knuckles = 5, knuckle_spacing = 5);
}

module gear_test() {
    // Test gear components
    gear(gear_diameter = 50, number_of_teeth = 20, tooth_profile = "involute", gear_thickness = 10);
}

module ratchet_test() {
    // Test ratchet wheel components
    ratchet(wheel_diameter = 50, number_of_teeth = 12, tooth_height = 2, tooth_angle = 30);
}

module spring_test() {
    // Test spring components
    spring(leaf_spring_width = 2, leaf_spring_thickness = 1, leaf_spring_length = 50, leaf_spring_count = 5, coil_spring_diameter = 20, coil_spring_wire_diameter = 2, coil_spring_coils = 5, coil_spring_height = 30);
}

module snap_fit_test() {
    // Test snap-fit components
    hook_snap();
    ball_socket_joint();
    cantilever_snap();
    living_hinge();
}

module track_system_test() {
    // Test track system components
    track_system(track_width = 10, track_depth = 5, guide_rail_dim = 1, detent_spacing = 5, detent_depth = 1);
}

// Assembly Verification Tests
module assembly_verification_test() {
    // Test overall assembly of the fidget toy
    fidget_toy_assembly();
}

// Print Orientation Guides
module print_orientation_guides() {
    // Example guides
    intersection() {
        cube([10, 10, 1]);
        linear_extrude(height=10)
          text("Z", size=5);
    }
}

// Documentation for interpreting results
echo("This test suite is designed to validate the printability and functionality of each component of the fidget toy.");
echo("Each module contains features specifically aimed at testing clearances, feature sizes, and overall assembly.");
echo("Ensure that each component prints correctly and all parts fit together seamlessly.");

// Call test modules
tolerance_test();
feature_size_test();
bearing_test();
hinge_test();
gear_test();
ratchet_test();
spring_test();
snap_fit_test();
track_system_test();
assembly_verification_test();
print_orientation_guides();
C:\mygit\BLazy\repo\scad\README.md
Language detected: markdown
# Fidget Toy Project Documentation

## 1. Project Overview
The Fidget Toy project is a modular design that combines various mechanical mechanisms into a single interlocking toy. The toy includes elements such as bearings, gears, springs, hinges, ratchets, and snap fits. The design allows for customization through parameter adjustments, enabling users to tailor the toy's size and components.

## 2. File Structure
C:\mygit\BLazy\repo\scad\README.md
Language detected: markdown
# Fidget Toy Project Documentation

## 1. Project Overview
The Fidget Toy project is a modular design that combines various mechanical mechanisms into a single interlocking toy. The project aims to create a multifunctional fidget toy by integrating different mechanical components such as bearings, gears, springs, hinges, ratchets, and snap fits. This documentation guide provides a thorough understanding of the design, usage, customization, and build instructions for the toy.

## 2. File Structure
C:\mygit\BLazy\repo\scad\README.md
Language detected: markdown
# Print-in-Place Fidget Toy

## Project Overview
This project provides OpenSCAD files for creating a customizable, print-in-place fidget toy. The design features various mechanical elements including bearings, gears, springs, and hinges that can be printed as a single piece without requiring assembly.

## File Structure
- `config.scad`: Configuration parameters and settings
- `utils.scad`: Utility functions and common operations
- `bearing.scad`: Parametric bearing module
- `hinge.scad`: Print-in-place hinge module
- `gear.scad`: Customizable gear system
- `ratchet.scad`: Ratchet mechanism module
- `spring.scad`: Various spring type modules
- `snap_fit.scad`: Snap-fit connection system
- `track_system.scad`: Linear and curved track system
- `test_prints.scad`: Test prints for verification
- `fidget_toy.scad`: Main assembly file

## Installation
1. Install OpenSCAD from https://openscad.org/
2. Clone this repository
3. Open fidget_toy.scad in OpenSCAD

## Usage
1. Customize parameters in config.scad
2. Preview in OpenSCAD
3. Export STL and print

## Print Settings
- Layer Height: 0.2mm
- Infill: 15-20%
- No supports needed
- Build plate adhesion: Brim recommended
- Print speed: 40-50mm/s

## Testing
Use test_prints.scad to verify:
- Tolerances
- Feature sizes
- Component functionality
- Print settings

## Assembly Instructions
This is a print-in-place design - no assembly required! After printing:
1. Allow print to cool completely
2. Carefully break in moving parts
3. Clean any stringing or artifacts

## Customization Options
Edit config.scad to customize:
- Overall size
- Component placement
- Colors and aesthetics
- Individual component parameters

## Troubleshooting
Common issues and solutions:
1. Parts fused together:
   - Check printer calibration
   - Adjust clearance values
   
2. Poor movement:
   - Clean thoroughly
   - Break in gently
   - Check clearances

## Contributing
Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
This project is released under the MIT License.
C:\mygit\BLazy\repo\scad\build.py
Language detected: python
import os
import sys
import argparse
import subprocess
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REQUIRED_FILES = ['config.scad', 'utils.scad', 'bearing.scad', 'hinge.scad', 'gear.scad', 'ratchet.scad', 'spring.scad', 'snap_fit.scad', 'track_system.scad', 'fidget_toy.scad']
TEST_PRINT_FILE = 'test_prints.scad'

def validate_files():
    """Verify the presence of required SCAD files."""
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            logging.error(f"Missing required SCAD file: {file}")
            sys.exit(1)

def generate_stl(output_dir, size_preset="Medium"):
    """Generate STL files for the fidget toy assembly."""
    try:
        preset_arg = f"-D preset_size=\"{size_preset}\""
        stl_file = os.path.join(output_dir, f"fidget_toy_{size_preset}.stl")
        command = f"openscad -o {stl_file} {preset_arg} fidget_toy.scad"
        subprocess.run(command, check=True, shell=True)
        logging.info(f"STL file generated: {stl_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to generate STL: {str(e)}")
        sys.exit(1)

def create_test_prints(output_dir):
    """Create test prints for functional verification."""
    try:
        test_print_file = os.path.join(output_dir, TEST_PRINT_FILE)
        command = f"openscad -o {test_print_file} fidget_toy.scad"
        subprocess.run(command, check=True, shell=True)
        logging.info(f"Test prints generated: {test_print_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to generate test prints: {str(e)}")
        sys.exit(1)

def parse_arguments():
    """Parse command-line arguments for customization options."""
    parser = argparse.ArgumentParser(description='Automate OpenSCAD builds for fidget toy.')
    parser.add_argument('--output-dir', required=True, help='Output directory for STLs and test prints.')
    parser.add_argument('--size', choices=['Small', 'Medium', 'Large'], default="Medium", help='Size preset for the fidget toy.')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    validate_files()
    generate_stl(args.output_dir, args.size)
    create_test_prints(args.output_dir)

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\scad\build.py
Language detected: python
import os
import sys
import argparse
import subprocess
import logging
from pathlib import Path
from shutil import copy

# Custom exceptions
class OpenSCADValidationError(Exception):
    """Exception raised when OpenSCAD is not properly configured."""
    pass

class FeatureControlError(Exception):
    """Exception raised when there is an issue with enabling/disabling features."""
    pass

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REQUIRED_FILES = ['config.scad', 'utils.scad', 'bearing.scad', 'hinge.scad', 'gear.scad', 
                  'ratchet.scad', 'spring.scad', 'snap_fit.scad', 'track_system.scad', 'fidget_toy.scad']
TEST_PRINT_FILE = 'test_prints.scad'
OPENSCAD_COMMAND = "openscad"
OPENSCAD_VERSION_REQUIRED = "2020.01"

def validate_openscad_version():
    """Verify the OpenSCAD version."""
    try:
        result = subprocess.run([OPENSCAD_COMMAND, "--version"], capture_output=True, text=True)
        output = result.stdout.strip()
        version = output.split()[1]
        if version >= OPENSCAD_VERSION_REQUIRED:
            logging.info(f"OpenSCAD version {version} is valid.")
        else:
            raise OpenSCADValidationError(f"OpenSCAD version must be {OPENSCAD_VERSION_REQUIRED} or later.")
    except Exception as e:
        raise OpenSCADValidationError(f"Could not verify OpenSCAD version: {str(e)}")

def check_required_files():
    """Check for the presence of required SCAD files."""
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Required file missing: {file}")

def validate_directory(directory):
    """Validate if the output directory exists or create it."""
    path = Path(directory)
    if path.is_dir():
        logging.info(f"Directory {directory} exists.")
    else:
        logging.info(f"Creating directory {directory}.")
        path.mkdir(parents=True, exist_ok=True)

def generate_stl(output_dir, size_preset="Medium", features=None):
    """Generate STL files for the fidget toy assembly."""
    try:
        preset_arg = f"-D preset_size=\"{size_preset}\""
        stl_file = os.path.join(output_dir, f"fidget_toy_{size_preset}.stl")
        command = f"{OPENSCAD_COMMAND} -D \"{features}\" -o {stl_file} fidget_toy.scad"
        subprocess.run(command, check=True, shell=True)
        logging.info(f"STL file generated: {stl_file}")
    except subprocess.CalledProcessError as e:
        raise FeatureControlError(f"Failed to generate STL: {str(e)}")

def create_test_prints(output_dir):
    """Create test prints for functional verification."""
    try:
        test_print_file = os.path.join(output_dir, TEST_PRINT_FILE)
        command = f"{OPENSCAD_COMMAND} -o {test_print_file} fidget_toy.scad"
        subprocess.run(command, check=True, shell=True)
        logging.info(f"Test prints generated: {test_print_file}")
    except subprocess.CalledProcessError as e:
        raise FeatureControlError(f"Failed to generate test prints: {str(e)}")

def parse_arguments():
    """Parse command-line arguments for customization options."""
    parser = argparse.ArgumentParser(description='Automate OpenSCAD builds for fidget toy.')
    parser.add_argument('--output-dir', required=True, help='Output directory for STLs and test prints.')
    parser.add_argument('--size', choices=['Small', 'Medium', 'Large'], default="Medium", help='Size preset for the fidget toy.')
    parser.add_argument('--enable', nargs='+', choices=['bearing', 'gear', 'hinge', 'ratchet', 'spring', 'track'], help='Enable specific components.')
    parser.add_argument('--component-tests', action='store_true', help='Generate individual component test prints.')
    parser.add_argument('--progress', action='store_true', help='Display progress information.')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    validate_directory(args.output_dir)
    validate_openscad_version()
    check_required_files()
    
    component_flags = []
    if args.enable:
        component_flags = [f"enable_{comp}={comp in args.enable}" for comp in ['bearing', 'gear', 'hinge', 'ratchet', 'spring', 'track']]
    
    if args.progress:
        logging.info("Generating STL file...")
    
    for flag in component_flags:
        generate_stl(args.output_dir, args.size, flag)
    
    if args.component_tests:
        for file in [f"{module}.scad" for module in ['bearing', 'hinge', 'gear', 'ratchet', 'spring', 'snap_fit', 'track_system']]:
            generate_stl(args.output_dir, args.size, f'enable_{Path(file).stem}=True')
    
    if args.progress:
        logging.info("Generating test prints...")
    
    create_test_prints(args.output_dir)

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\scad\build.py
Language detected: python
import os
import sys
import argparse
import subprocess
import logging
from pathlib import Path
from shutil import copy
from tqdm import tqdm
import concurrent.futures
from datetime import datetime
from collections import defaultdict

# Custom exceptions
class OpenSCADValidationError(Exception):
    """Exception raised when OpenSCAD is not properly configured."""
    pass

class FeatureControlError(Exception):
    """Exception raised when there is an issue with enabling/disabling features."""
    pass

class DependencyError(Exception):
    """Exception raised when there is a dependency issue."""
    pass

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REQUIRED_FILES = ['config.scad', 'utils.scad', 'bearing.scad', 'hinge.scad', 'gear.scad',
                  'ratchet.scad', 'spring.scad', 'snap_fit.scad', 'track_system.scad', 'fidget_toy.scad']
TEST_PRINT_FILE = 'test_prints.scad'
OPENSCAD_COMMAND = "openscad"
OPENSCAD_VERSION_REQUIRED = "2020.01"
BUILD_MANIFEST_FILE = "build_manifest.txt"
SYSTEM_REQUIREMENTS = {"min_memory": 1<<30, "required_space": 1<<30}  # Minimum memory & space in bytes

def validate_openscad_version():
    """Verify the OpenSCAD version."""
    try:
        result = subprocess.run([OPENSCAD_COMMAND, "--version"], capture_output=True, text=True)
        output = result.stdout.strip()
        version = output.split()[1]
        if version >= OPENSCAD_VERSION_REQUIRED:
            logging.info(f"OpenSCAD version {version} is valid.")
        else:
            raise OpenSCADValidationError(f"OpenSCAD version must be {OPENSCAD_VERSION_REQUIRED} or later.")
    except Exception as e:
        raise OpenSCADValidationError(f"Could not verify OpenSCAD version: {str(e)}")

def validate_system_requirements():
    """Check if system meets the minimum requirement."""
    memory = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    disk_space_free = shutil.disk_usage("/").free
    
    if memory < SYSTEM_REQUIREMENTS["min_memory"]:
        raise DependencyError(f"Insufficient memory. Required: {SYSTEM_REQUIREMENTS['min_memory']} bytes, Actual: {memory} bytes")
    
    if disk_space_free < SYSTEM_REQUIREMENTS["required_space"]:
        raise DependencyError(f"Insufficient disk space. Required: {SYSTEM_REQUIREMENTS['required_space']} bytes, Actual: {disk_space_free} bytes")

def check_required_files():
    """Check for the presence of required SCAD files."""
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Required file missing: {file}")

def validate_directory(directory):
    """Validate if the output directory exists or create it."""
    path = Path(directory)
    if path.is_dir():
        logging.info(f"Directory {directory} exists.")
    else:
        logging.info(f"Creating directory {directory}.")
        path.mkdir(parents=True, exist_ok=True)

def generate_stl(output_dir, size_preset="Medium", feature=None):
    """Generate STL files for the fidget toy assembly."""
    try:
        preset_arg = f"-D preset_size=\"{size_preset}\""
        if feature:
            cmd = f"{OPENSCAD_COMMAND} -D \"{feature}\" -o {os.path.join(output_dir, f'fidget_toy_{size_preset}.stl')} fidget_toy.scad"
        else:
            cmd = f"{OPENSCAD_COMMAND} -o {os.path.join(output_dir, f'fidget_toy_{size_preset}.stl')} fidget_toy.scad"
        
        subprocess.run(cmd, check=True, shell=True)
        logging.info(f"STL file generated: {cmd}")
    except subprocess.CalledProcessError as e:
        raise FeatureControlError(f"Failed to generate STL: {str(e)}")

def create_test_prints(output_dir):
    """Create test prints for functional verification."""
    test_print_dir = os.path.join(output_dir, 'test_prints')
    os.makedirs(test_print_dir, exist_ok=True)

    scad_modules = ['bearing', 'hinge', 'gear', 'ratchet', 'spring', 'snap_fit', 'track_system']
    tasks = [os.path.join(output_dir, f'{module}.stl') for module in scad_modules]

    logging.info("Generating test prints in parallel...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(lambda module: generate_stl(test_print_dir, 'Medium', f'enable_{module.stem}=True'), tasks), total=len(tasks)))

def parse_arguments():
    """Parse command-line arguments for customization options."""
    parser = argparse.ArgumentParser(description='Automate OpenSCAD builds for fidget toy.')
    parser.add_argument('--output-dir', required=True, help='Output directory for STLs and test prints.')
    parser.add_argument('--size', choices=['Small', 'Medium', 'Large'], default="Medium", help='Size preset for the fidget toy.')
    parser.add_argument('--enable', nargs='+', choices=['bearing', 'gear', 'hinge', 'ratchet', 'spring', 'track'], help='Enable specific components.')
    parser.add_argument('--component-tests', action='store_true', help='Generate individual component test prints.')
    parser.add_argument('--progress', action='store_true', help='Display progress information.')
    parser.add_argument('--clean', action='store_true', help='Clean previous build before starting new one.')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    validate_directory(args.output_dir)
    validate_openscad_version()
    validate_system_requirements()
    check_required_files()
    
    if args.clean:
        for filename in os.listdir(args.output_dir):
            file_path = os.path.join(args.output_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error(f"Failed to delete {file_path}: {str(e)}")
    
    component_flags = []
    if args.enable:
        component_flags = [f"enable_{comp}={comp in args.enable}" for comp in ['bearing', 'gear', 'hinge', 'ratchet', 'spring', 'track']]
    
    manifest_data = defaultdict(dict)
    
    def save_manifest(feature, result_status):
        with open(os.path.join(args.output_dir, BUILD_MANIFEST_FILE), 'a') as manifest:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            manifest.write(f"{timestamp}, {feature}, {'success' if result_status else 'failed'}\n")
    
    with open(os.path.join(args.output_dir, BUILD_MANIFEST_FILE), 'w') as manifest:
        manifest.write("Timestamp,Component,Status\n")
    
    if args.progress:
        logging.info("Generating STL file...")
    
    try:
        for feature in tqdm(component_flags, desc="Generating STL files"):
            generate_stl(args.output_dir, args.size, feature)
            success = True
    except FeatureControlError as e:
        logging.error(f"Feature control error: {str(e)}")
        success = False
    finally:
        save_manifest(feature, success)
    
    if args.component_tests:
        create_test_prints(args.output_dir)
        success = True
    else:
        success = False
        
    save_manifest("test_prints", success)

if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\scad\build.py
Language detected: python
import os
import sys
import argparse
import subprocess
import logging
import json
import time
from pathlib import Path
from shutil import copy, rmtree
from tqdm import tqdm
import concurrent.futures
from datetime import datetime
import networkx as nx
import random
import pickle

# Custom exceptions
class OpenSCADValidationError(Exception):
    """Exception raised when OpenSCAD is not properly configured."""
    pass

class FeatureControlError(Exception):
    """Exception raised when there is an issue with enabling/disabling features."""
    pass

class DependencyError(Exception):
    """Exception raised when there is a dependency issue."""
    pass

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REQUIRED_FILES = ['config.scad', 'utils.scad', 'bearing.scad', 'hinge.scad', 'gear.scad',
                  'ratchet.scad', 'spring.scad', 'snap_fit.scad', 'track_system.scad', 'fidget_toy.scad']
TEST_PRINT_FILE = 'test_prints.scad'
OPENSCAD_COMMAND = "openscad"
OPENSCAD_VERSION_REQUIRED = "2020.01"
BUILD_MANIFEST_FILE = "build_manifest.json"
SYSTEM_REQUIREMENTS = {"min_memory": 1<<30, "required_space": 1<<30}  # Minimum memory & space in bytes

DEPENDENCIES = {
    'bearing': [],
    'gear': [],
    'hinge': [],
    'ratchet': [],
    'spring': [],
    'track_system': []
}

def load_state(output_dir):
    """Load build state from disk."""
    state_file = Path(output_dir) / 'build_state.pickle'
    if state_file.exists():
        with open(state_file, 'rb') as f:
            return pickle.load(f)
    return {}

def save_state(state, output_dir):
    """Save build state to disk."""
    state_file = Path(output_dir) / 'build_state.pickle'
    with open(state_file, 'wb') as f:
        pickle.dump(state, f)

def validate_openscad_version():
    """Verify the OpenSCAD version."""
    try:
        result = subprocess.run([OPENSCAD_COMMAND, "--version"], capture_output=True, text=True)
        output = result.stdout.strip()
        version = output.split()[1]
        if version > OPENSCAD_VERSION_REQUIRED:
            logging.info(f"OpenSCAD version {version} is valid.")
        else:
            raise OpenSCADValidationError(f"OpenSCAD version must be {OPENSCAD_VERSION_REQUIRED} or later.")
    except Exception as e:
        raise OpenSCADValidationError(f"Could not verify OpenSCAD version: {str(e)}")

def validate_system_requirements():
    """Check if system meets the minimum requirement."""
    memory = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    disk_space_free = shutil.disk_usage("/").free
    
    if memory < SYSTEM_REQUIREMENTS["min_memory"]:
        raise DependencyError(f"Insufficient memory. Required: {SYSTEM_REQUIREMENTS['min_memory']} bytes, Actual: {memory} bytes")
    
    if disk_space_free < SYSTEM_REQUIREMENTS["required_space"]:
        raise DependencyError(f"Insufficient disk space. Required: {SYSTEM_REQUIREMENTS['required_space']} bytes, Actual: {disk_space_free} bytes")

def check_required_files():
    """Check for the presence of required SCAD files."""
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Required file missing: {file}")

def validate_directory(directory):
    """Validate if the output directory exists or create it."""
    path = Path(directory)
    if path.is_dir():
        logging.info(f"Directory {directory} exists.")
    else:
        logging.info(f"Creating directory {directory}.")
        path.mkdir(parents=True, exist_ok=True)

def generate_stl(output_dir, size_preset="Medium", feature=None):
    """Generate STL files for the fidget toy assembly."""
    try:
        preset_arg = f"-D preset_size=\"{size_preset}\""
        if feature:
            cmd = f"{OPENSCAD_COMMAND} -D \"{feature}\" -o {os.path.join(output_dir, f'fidget_toy_{size_preset}_{feature.replace('=', '_')}.stl')} fidget_toy.scad"
        else:
            cmd = f"{OPENSCAD_COMMAND} -o {os.path.join(output_dir, f'fidget_toy_{size_preset}.stl')} fidget_toy.scad"
        logging.info(f"Generating STL for: {feature if feature else 'fidget_toy_all'}, Command: {cmd}")
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        raise FeatureControlError(f"Failed to generate STL: {str(e)}")

def create_test_prints(output_dir):
    """Create test prints for functional verification."""
    test_print_dir = os.path.join(output_dir, 'test_prints')
    os.makedirs(test_print_dir, exist_ok=True)

    components = ['bearing', 'hinge', 'gear', 'ratchet', 'spring', 'snap_fit', 'track_system']
    tasks = [(test_print_dir, f'enable_{comp}_True', comp) for comp in components]

    logging.info("Generating test prints in parallel...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(lambda task: generate_stl(task[0], 'Medium', task[1]), tasks), total=len(tasks)))

def parse_arguments():
    """Parse command-line arguments for customization options."""
    parser = argparse.ArgumentParser(description='Automate OpenSCAD builds for fidget toy.')
    parser.add_argument('--output-dir', required=True, help='Output directory for STLs and test prints.')
    parser.add_argument('--size', choices=['Small', 'Medium', 'Large'], default="Medium", help='Size preset for the fidget toy.')
    parser.add_argument('--enable', nargs='+', choices=['bear', 'gear', 'hinge', 'ratchet', 'spring', 'track'], help='Enable specific components.')
    parser.add_argument('--component-tests', action='store_true', help='Generate individual component test prints.')
    parser.add_argument('--progress', action='store_true', help='Display progress information.')
    parser.add_argument('--clean', action='store_true', help='Clean previous build before starting new one.')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    validate_directory(args.output_dir)
    validate_openscad_version()
    validate_system_requirements()
    check_required_files()
    
    state = load_state(args.output_dir)
    if args.clean and 'success' in state:
        rmtree(state['success'])  # Remove old successful builds if clean is specified

    if args.clean:
        for filename in os.listdir(args.output_dir):
            file_path = os.path.join(args.output_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    rmtree(file_path)
            except Exception as e:
                logging.error(f"Failed to delete {file_path}: {str(e)}")

    component_flags = []
    if args.enable:
        component_flags = [f"enable_{comp}=True" for comp in ['bear', 'gear', 'hinge', 'ratchet', 'spring', 'track'] if comp in args.enable]
    
    manifest_data = {
        "components": [],
        "state": {"status": "running"}
    }

    def record_result(component, result_status):
        status = "success" if result_status else "failed"
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        manifest_data['components'].append({"component": component, "time": current_time, "status": status})

    # Dependency graph initialization
    graph = nx.DiGraph()
    for k, v in DEPENDENCIES.items():
        graph.add_node(k)
        for dep in v:
            graph.add_edge(dep, k)

    # Sort topologically to ensure components are built in correct order
    ordered_components = list(nx.topological_sort(graph))

    for feature in tqdm(ordered_components, total=len(ordered_components), desc="Generating STL files for components"):
        try:
            generate_stl(args.output_dir, args.size, feature)
            record_result(feature, True)
        except FeatureControlError as e:
            logging.error(f"Feature control error: {str(e)}")
            record_result(feature, False)
    
    if args.component_tests:
        create_test_prints(args.output_dir)

    save_state(state, args.output_dir)
    manifest_filename = os.path.join(args.output_dir, BUILD_MANIFEST_FILE)
    with open(manifest_filename, 'w') as f:
        json.dump(manifest_data, f, indent=4)
            
if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\scad\requirements.txt
Language detected: plaintext
networkx>=2.5
tqdm>=4.60.0
pathlib>=1.0.1  # Note: pathlib is part of the Python Standard Library since Python 3.4
C:\mygit\BLazy\repo\scad\BUILD.md
Language detected: markdown
# Build Documentation for Fidget Toy Project

## Quick Start Guide

1. **Install OpenSCAD**: 
   - Download and install OpenSCAD from https://openscad.org/
   
2. **Clone Repository**:
   - Run `git clone https://github.com/your-repo/fidget_toy.git` in your terminal.

3. **Build the Fidget Toy**:
   - Navigate to the root of the cloned repository.
   - Run the build script: `python build.py --output-dir ./output`.

## Build Script Usage

The build script `build.py` helps automate the process of generating STL files and test prints for the fidget toy. 

### Command Line Options

- `--output-dir`: Directory where STL and test prints will be saved.
- `--size`: Size preset for the fidget toy (`Small`, `Medium`, `Large`). Default is `Medium`.
- `--enable`: Enable specific components (`bear`, `gear`, `hinge`, `ratchet`, `spring`, `track`).
- `--component-tests`: Generate individual component test prints if enabled.
- `--progress`: Display progress information during build.
- `--clean`: Clean previous build before starting a new one.

### Example Commands

- **Basic Build**:
C:\mygit\BLazy\repo\scad\test_build.py
Language detected: python
import os
import sys
import unittest
import subprocess
import tempfile
from shutil import rmtree
import time

# Custom exceptions
class OpenSCADValidationError(Exception):
    """Exception raised when OpenSCAD is not properly configured."""
    pass

class FeatureControlError(Exception):
    """Exception raised when there is an issue with enabling/disabling features."""
    pass

class DependencyError(Exception):
    """Exception raised when there is a dependency issue."""
    pass

# Setting up logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

REQUIRED_FILES = ['config.scad', 'utils.scad', 'bearing.scad', 'hinge.scad', 'gear.scad',
                  'ratchet.scad', 'spring.scad', 'snap_fit.scad', 'track_system.scad', 'fidget_toy.scad']
OPENSCAD_COMMAND = "openscad"
OPENSCAD_VERSION_REQUIRED = "2020.01"
SYSTEM_REQUIREMENTS = {"min_memory": 1<<30, "required_space": 1<<30}  # Minimum memory & space in bytes

def validate_openscad_version():
    """Verify the OpenSCAD version."""
    try:
        result = subprocess.run([OPENSCAD_COMMAND, "--version"], capture_output=True, text=True)
        output = result.stdout.strip()
        version = output.split()[1]
        if version >= OPENSCAD_VERSION_REQUIRED:
            logging.info(f"OpenSCAD version {version} is valid.")
        else:
            raise OpenSCADValidationError(f"OpenSCAD version must be {OPENSCAD_VERSION_REQUIRED} or later.")
    except Exception as e:
        raise OpenSCADValidationError(f"Could not verify OpenSCAD version: {str(e)}")

def validate_system_requirements():
    """Check if system meets the minimum requirement."""
    memory = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    if memory < SYSTEM_REQUIREMENTS["min_memory"]:
        raise DependencyError(f"Insufficient memory. Required: {SYSTEM_REQUIREMENTS['min_memory']} bytes, Actual: {memory} bytes")

def check_required_files():
    """Check for the presence of required SCAD files."""
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Required file missing: {file}")

def execute_build(output_dir, size_preset="Medium", feature=None):
    """Execute the build command and capture output."""
    try:
        preset_arg = f"-D preset_size=\"{size_preset}\""
        if feature:
            cmd = f'{OPENSCAD_COMMAND} -D "{feature}" -o {os.path.join(output_dir, f"fidget_toy_{size_preset}_{feature.replace("=", "_")}.stl")} fidget_toy.scad'
        else:
            cmd = f'{OPENSCAD_COMMAND} -o {os.path.join(output_dir, f"fidget_toy_{size_preset}.stl")} fidget_toy.scad'
        logging.info(f"Executing: {cmd}")
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        raise FeatureControlError(f"Failed to generate STL: {str(e)}")

class TestBuildSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        logging.info(f"Temporary directory created: {cls.temp_dir}")

    @classmethod
    def tearDownClass(cls):
        rmtree(cls.temp_dir)
        logging.info("Temporary directory removed.")

    def test_01_openscad_version(self):
        """Test OpenSCAD version validation."""
        self.validate_openscad_version()

    def test_02_system_requirements(self):
        """Test system requirements validation."""
        self.validate_system_requirements()

    def test_03_component_generation(self):
        """Test generation of individual components."""
        features = ["enable_bear=True", "enable_gear=True", "enable_hinge=True"]
        for feature in features:
            execute_build(self.temp_dir, feature=feature)
            self.assertTrue(os.path.exists(os.path.join(self.temp_dir, f"fidget_toy_Medium_{feature.replace('=', '_')}.stl")), f"Fidget toy component not found for {feature}")

    def test_04_validation(self):
        """Test build output validation."""
        output_file = os.path.join(self.temp_dir, "fidget_toy_Medium.stl")
        execute_build(self.temp_dir)
        self.assertTrue(os.path.exists(output_file), "Full fidget toy STL not found in output")

    def test_05_error_handling(self):
        """Test error handling during build process."""
        with self.assertRaises(FeatureControlError):
            try:
                execute_build(self.temp_dir, feature="invalid_feature")
            except FeatureControlError as e:
                logging.error(str(e))
                raise
        with self.assertRaises(FileNotFoundError):
            try:
                temp_invalid_file = os.path.join(self.temp_dir, "invalid_file")
                execute_build(temp_invalid_file)
            except FileNotFoundError as e:
                logging.error(str(e))
                raise

    def test_06_parallel_processing(self):
        """Test parallel component generation."""
        features = ["enable_bear=True", "enable_gear=True", "enable_hinge=True"]
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(execute_build, self.temp_dir, feature=feature) for feature in features]
            for future in futures:
                future.result()
            for feature in features:
                self.assertTrue(os.path.exists(os.path.join(self.temp_dir, f"fidget_toy_Medium_{feature.replace('=', '_')}.stl")), f"Fidget toy component not found for {feature}")

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
