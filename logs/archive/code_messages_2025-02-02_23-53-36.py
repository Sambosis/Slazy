C:\mygit\BLazy\repo\scad\bearing_module.scad
Language detected: openscad
// OpenSCAD code for a parametric print-in-place bearing module

// Parameters
// Outer diameter of the bearing in mm
outer_diameter = 20;  

// Inner diameter of the bearing, must be smaller than outer_diameter, in mm
inner_diameter = 14;  

// Height of the bearing, including balls, in mm 
height = 10;  

// Number of balls to fit into the bearing
number_of_balls = 6;  

// Clearance between race and balls for 3D printing, in mm
clearance = 0.25;  

// Ball diameter calculated from known parameters
ball_diameter = (outer_diameter - inner_diameter - clearance * 2) / (number_of_balls**0.5); 

// Radius calculations
outer_radius = outer_diameter / 2;
inner_radius = inner_diameter / 2;
rim_thickness = ball_diameter + clearance;

// Function to create the race (track) for the balls
module race() {
    difference() {
        cylinder(r = outer_radius, h = height, $fn = 50);
        translate([0, 0, -1]) // Subtract 1 to ensure proper machining with OpenSCAD
        cylinder(r = inner_radius * 1.5, h = height + 2, $fn = 50); // House the balls clear of the edges
    }
}

// Function to create the balls
module balls() {
    angle_step = 360 / number_of_balls;
    for (i = [0: number_of_balls - 1]) {
        rotate([0, 0, i * angle_step])
        translate([inner_radius + ball_diameter / 2 - clearance, 0, height / 2])
        sphere(r = ball_diameter / 2);
    }
}

// Main module
module print_in_place_bearing() {
    // Assemble the main bearing structure
    union() {
        difference() { // Construct the outer race
            race();
            // Create a hole in the central area to fit the balls in
            cylinder(r = inner_radius, h = height, $fn = 50);
        }
        // Place the balls inside the bearing
        balls();
    }
}

// Render the print-in-place bearing module
print_in_place_bearing();
C:\mygit\BLazy\repo\scad\hinge_module.scad
Language detected: scad
// OpenSCAD code for a parametric print-in-place hinge module

// Parameters
// Total length of the hinge in mm
hinge_length = 50;  

// Overall diameter of the hinge, including knuckles, in mm
hinge_diameter = 20;  

// Number of knuckle segments in the hinge
number_of_knuckles = 4;  

// Clearance between knuckle segments to allow smooth rotation, in mm
clearance = 0.2;  

// Diameter of the pin that goes through the hinge for articulation, in mm
pin_diameter = 3;  

// Maximum rotation angle for hinge if stops are included, defaults to 360 for full rotation
max_rotation = 360;

// Segment length (distance between knuckles) and number of segments
segment_length = hinge_length / number_of_knuckles;

// Function to create a single knuckle segment
module knuckle() {
    difference() {
        // Outer shape of the knuckle segment
        cylinder(r = hinge_diameter / 2, h = segment_length, $fn = 50);
        
        // Create clearance for movement and articulate holes for the pin
        translate([0, 0, -clearance])
        cylinder(r = (hinge_diameter - clearance * 2) / 2, h = segment_length + 2 * clearance, $fn = 50); // Slightly extended length for clearance

        // Hole in knuckle for pin
        translate([0, 0, segment_length / 2])
        cylinder(r = pin_diameter / 2 + clearance / 2, h = clearance * 3); // Slightly overextend for clearance
    }
}

// Function to create built-in stops if max rotation is less than 360 degrees
module built_in_stops(stop_angle) {
    rotate_extrude(convexity = 10, $fn = 50)
    translate([hinge_diameter / 4, 0, 0])
    polygon(points = [
        [0, 0],
        [segment_length, 0],
        [segment_length, -stop_angle / (360 / point_density)]
    ]);
}

// Main module to create the hinge
module print_in_place_hinge() {
    for (i = [0 : number_of_knuckles - 1]) {
        rotate([0, 0, i * 360 / number_of_knuckles])
        translate([0, 0, i * segment_length])
        knuckle();

        // Add built-in stops if necessary
        if (max_rotation != 360) {
            rotate([0, 0, i * 360 / number_of_knuckles + (360 - max_rotation) / 2])
            built_in_stops(360 - max_rotation);
        }
    }

    // Create the central pin for the hinge
    translate([0, 0, hinge_length / 2 - clearance])
    cylinder(r = pin_diameter / 2, h = hinge_length + 2 * clearance);
}

// Render the print-in-place hinge module
print_in_place_hinge();
C:\mygit\BLazy\repo\scad\gear_module.scad
Language detected: scad
C:\mygit\BLazy\repo\scad\spring_module.scad
Language detected: scad
// OpenSCAD code for a parametric print-in-place spring module

// Parameters
// Common parameters
wire_thickness = 2.0;         // Thickness of the wire in mm
clearance = 0.2;              // Clearance between coils for print-in-place

// Spiral Torsion Spring Parameters
torsion_spring_diameter = 20; // Diameter of the torsion spring in mm
torsion_num_coils = 10;       // Number of coils in the torsion spring

// Compression Spring Parameters
compression_spring_width = 10;   // Width (diameter) of the compression spring in mm
compression_length = 50;         // Length of the compression spring in mm

// Leaf Spring Parameters
leaf_spring_length = 80;   // Effective length of the leaf spring in mm
leaf_spring_thickness = 10;  // Thickness of the leaf spring in mm

// Spring Rate Adjustment Factors
torsion_spring_rate_factor = 1.0;
compression_spring_rate_factor = 1.0;
leaf_spring_rate_factor = 1.0;

// Function to create a single coil of a torsion spring
module torsion_coil() {
    difference() {
        tube(r = torsion_spring_diameter / 2, h = wire_thickness + clearance, $fn = 50);
        translate([0, 0, -clearance])
        tube(r = (torsion_spring_diameter - wire_thickness * 2 - clearance * 2) / 2, h = wire_thickness + 2 * clearance, $fn = 50);
    }
}

// Function to create the entire torsion spring
module torsion_spring() {
    union() {
        for (i = [0 : torsion_num_coils - 1]) {
            rotate([0, 0, i * 360 / torsion_num_coils]) {
                translate([0, 0, i * (wire_thickness + clearance)]) {
                    torsion_coil();
                }
            }
        }
    }
}

// Function to create a single coil of a compression spring
module compression_coil() {
    cylinder(r = compression_spring_width / 2, h = wire_thickness + clearance, $fn = 50);
}

// Function to create the entire compression spring
module compression_spring() {
    for (i = [0 : compression_length / (wire_thickness + clearance) - 1]) {
        translate([0, 0, i * (wire_thickness + clearance)])
        compression_coil();
    }
}

// Function to create the leaf spring
module leaf_spring() {
    hull() {
        translate([-leaf_spring_length / 2, 0, 0])
        cube([wire_thickness, leaf_spring_thickness, leaf_spring_thickness]);
        translate([leaf_spring_length / 2, 0, 0])
        cube([wire_thickness, leaf_spring_thickness, leaf_spring_thickness]);
    }
}

// Function to calculate and output approximate spring rates
module spring_rate() {
    echo("Torsion Spring Rate (approx. clockwise torque per radian): ", torsion_num_coils * wire_thickness * torsion_spring_rate_factor);
    echo("Compression Spring Rate (approx. force per unit of compression): ", (compression_length / (wire_thickness + clearance)) * wire_thickness * compression_spring_rate_factor);
    echo("Leaf Spring Rate (approx. force per unit of deflection): ", leaf_spring_length * leaf_spring_thickness * leaf_spring_rate_factor);
}

// Main module to assemble the print-in-place spring components
module print_in_place_spring() {
    // Torsion Spring
    translate([-50, 0, 0]) {
        color("Blue") torsion_spring();
    }

    // Compression Spring
    translate([0, 0, 0]) {
        color("Red") compression_spring();
    }

    // Leaf Spring
    translate([50, 0, 0]) {
        color("Green") leaf_spring();
    }
}

// Render the print-in-place spring module
spring_rate();
print_in_place_spring();
C:\mygit\BLazy\repo\scad\track_module.scad
Language detected: scad
// OpenSCAD code for a parametric track/rail system module

// Parameters
track_width = 20;            // Width of the track in mm
track_depth = 10;            // Depth of the track in mm
track_length = 100;          // Length of each track segment in mm
wall_thickness = 2;          // Wall thickness in mm

clearance = 0.2;             // Clearance for print-in-place

// Rail profiles
// "Dovetail", "T-slot", "V-groove"
rail_profile = "T-slot";    

// Function to create track with selected rail profile
module rail_profile_dovetail() {
    difference() {
        hull() {
            translate([-track_width/2, -track_depth/2, 0])
            cube([track_width/4, track_depth/4, track_length]);
            translate([-track_width/2, track_depth/2, 0])
            cube([track_width/4, track_depth/4, track_length]);
            translate([track_width/2, -track_depth/2, 0])
            cube([track_width/4, track_depth/4, track_length]);
        }
        translate([-track_width/2, 0, -1]) 
        cube([track_width, track_depth - clearance, track_length + 2]);
    }
}

module rail_profile_tslot() {
    union() {
        difference() {
            cube([track_width, track_depth, track_length]);
            translate([wall_thickness + clearance, -clearance, -1])
            cube([track_width - 2 * wall_thickness - clearance * 2, track_depth + 2 * clearance, track_length + 2]);
        }
        for (i = [-1, 1]) {
            translate([wall_thickness + i * (track_width - 2 * wall_thickness) / 2, track_depth, -clearance])
            cylinder(r = wall_thickness/2 + clearance, h = clearance * 2, $fn = 50);
        }
    }
}

module rail_profile_vgroove() {
    difference() {
        cube([track_width, track_depth, track_length]);
        translate([wall_thickness, 0, -1]) 
        cube([track_width - 2 * wall_thickness, track_depth/2, track_length + 2]);
    }
}

module rail() {
    if (rail_profile == "Dovetail") {
        rail_profile_dovetail();
    } else if (rail_profile == "T-slot") {
        rail_profile_tslot();
    } else if (rail_profile == "V-groove") {
        rail_profile_vgroove();
    }
}

// Function to create matching slider component
module slider() {
    difference() {
        cube([track_width, wall_thickness * 2, wall_thickness * 2]);
        translate([wall_thickness + clearance, -clearance, -clearance])
        cube([track_width - 2 * wall_thickness - clearance * 2, wall_thickness * 2 + 2 * clearance, wall_thickness * 2 + 2 * clearance]);
    }
}

// Function to create end stops
module end_stop() {
    difference() {
        cube([track_width, track_depth, wall_thickness * 3]);
        translate([wall_thickness + clearance, -clearance, -clearance])
        cube([track_width - 2 * wall_thickness - clearance * 2, track_depth + 2 * clearance, wall_thickness * 3 + 2 * clearance]);
    }
}

// Main module to create the track assembly with sliders and end stops
module print_in_place_track() {
    color("Blue") {
        for (x = [0 : track_length : 300]) {
            translate([x, 0, 0])
            rail();
        }
        translate([200, 0, 0])
        end_stop();
    }
    
    color("Red") {
        translate([100, -track_depth / 2 - wall_thickness * 4, 0]) 
        rotate([0, 90, 0])
        slider();
    }
}

// Render the print-in-place track system
print_in_place_track();
C:\mygit\BLazy\repo\scad\ratchet_module.scad
Language detected: scad
// OpenSCAD code for a parametric print-in-place ratchet mechanism

// Parameters
wheel_diameter = 40;          // Diameter of the ratchet wheel in mm
wheel_thickness = 5;          // Thickness of the ratchet wheel in mm
number_of_teeth = 24;         // Number of teeth on the ratchet wheel
tooth_angle = 360 / number_of_teeth; // Angle of each tooth in degrees
tooth_height = 3;             // Height of each tooth in mm
tooth_depth = 2;              // Depth of each tooth in mm
pawl_length = wheel_diameter / 2; // Length of the pawl in mm
pawl_width = 5;               // Width of the pawl in mm
screw_head_hole_diameter = 3; // Diameter of mounting screw holes in mm
clearance = 0.25;             // Clearance for print-in-place

// Optional: Reverse direction
reverse_direction = false;    // Set to true for reverse direction

// Derived Values
inner_radius = wheel_diameter / 2 - tooth_depth - clearance;
outer_radius = inner_radius - tooth_height;


// Function to create a tooth
module tooth() {
    difference() {
        hull() {
            translate([outer_radius, 0, 0])
            cube([tooth_depth, tooth_height, wheel_thickness], center = true);
            translate([outer_radius, wheel_thickness / 2, 0])
            rotate([90, 0, 0])
            cube([tooth_height, tooth_depth, wheel_thickness], center = true);
        }
        translate([inner_radius, 0, -1])
        cube([wheel_thickness, tooth_height * 1.2, wheel_thickness + 2], center = true);
    }
}

// Function to create the ratchet wheel with teeth
module ratchet_wheel() {
    difference() {
        cylinder(r = inner_radius, h = wheel_thickness, $fn = 100);
        for (i = [0 : number_of_teeth - 1]) {
            rotate([0, 0, i * tooth_angle]) {
                translate([inner_radius, 0, -clearance])
                rotate([0, 0, -tooth_angle / 2]) // Align tooth correctly
                tooth();
            }
        }
    }
}

// Function to create the pawl
module pawl() {
    union() {
        // Pawl body
        translate([0, inner_radius, pawl_length / 2]) {
            cube([pawl_width, pawl_length - tooth_depth, wheel_thickness + 1]);
        }
        // Pawl spring
        translate([0, inner_radius - pawl_width / 2 + tooth_depth / 2, pawl_length - tooth_depth])
        rotate([90, 0, 0])
        cylinder(r = pawl_width / 2 + clearance, h = pawl_width + clearance * 2);
        // Reverse pawl if needed
        if (reverse_direction) {
            translate([0, 2 * inner_radius, wheel_thickness])
            rotate([0, 0, 180])
            pawl();
        }
    }
}

// Function to create mounting holes
module mounting_holes() {
    for (angle = [0, 180]) {
        rotate([0, 0, angle])
        translate([0, wheel_diameter / 4, -clearance])
        cylinder(r = screw_head_hole_diameter / 2, h = wheel_thickness + 2 * clearance);
    }
}

// Main module to create the print-in-place ratchet mechanism
module print_in_place_ratchet() {
    difference() {
        union() {
            color("Blue") ratchet_wheel();
            color("Red") pawl();
        }
        // Mounting holes
        mounting_holes();
    }
}

// Render the print-in-place ratchet mechanism
print_in_place_ratchet();
C:\mygit\BLazy\repo\scad\snap_fit_module.scad
Language detected: scad
// OpenSCAD code for a parametric snap-fit mechanism module

// Parameters
ball_diameter = 8;              // Diameter of the ball/socket joint in mm
socket_diameter = ball_diameter + 2; // Diameter of the socket (with some interference) in mm
socket_depth = ball_diameter + 0.5; // Depth of the socket, including engagement depth in mm
cantilever_length = 20;         // Length of the cantilever snap fit arms in mm
cantilever_width = 5;           // Width of the cantilever snap fit arms in mm
cantilever_thickness = 2;       // Thickness of the cantilever snap fit arms in mm
cantilever_depth = 3;           // Depth of the cantilever snap fit (engagement) in mm
interference = 0.2;             // Interference fit tolerance in mm
material_flexibility = 1;       // Material flexibility consideration (1 = rigid, >1 = more flexible)
clearance = 0.1;                // General clearance value for all snap-fit features in mm

// Derived Values
socket_outer_diameter = socket_diameter + clearance;

// Module for Ball and Socket Joint
module ball_and_socket() {
    difference() {
        // Socket
        cylinder(d = socket_outer_diameter, h = socket_depth, $fn=100);
        
        // Ball (engagement)
        translate([0, 0, -1]) // Slight offset for correct machining
        sphere(d = ball_diameter + interference);
    }
}

// Module for Cantilever Snap Fit
module cantilever_snap() {
    difference() {
        // Base body
        cube([cantilever_length, cantilever_width, cantilever_thickness], center=true);
        
        // Cutout for snap fit
        translate([0, 0, -1]) // Slight offset for correct machining
        cube([cantilever_length - 2*interference, cantilever_width, cantilever_depth + 2*interference], center=true);
    }
    
    // Snap arm
    translate([0, -cantilever_width/2 - cantilever_thickness, -interference])
    cube([material_flexibility*cantilever_depth, (cantilever_width + 2*clearance), cantilever_thickness]);
}

// Module for Annular Snap Fit
module annular_snap() {
    difference() {
        // Outer ring
        cylinder(h = material_flexibility, d = socket_outer_diameter, $fn=100);
        
        // Inner cutout
        cylinder(h = material_flexibility + 2*clearance, d = socket_diameter - 2*clearance);
    }
    
    // Snap lip
    translate([0, 0, -clearance])
    cylinder(h = material_flexibility, d = socket_diameter + 2*interference, $fn=100);
}

// Module for Detent Mechanism
module detent() {
    difference() {
        // Detent body
        cylinder(d = socket_diameter + 2*interference, h = socket_depth/4, $fn=100);
        
        // Central hub
        cylinder(d = socket_diameter/2, h = socket_depth/2, $fn=50);
    }
}

// Main Module - Combine all snap-fit features
module print_in_place_snap_fit() {
    difference() {
        // Combine all components
        union() {
            color("lightblue") ball_and_socket();
            color("lightgreen") translate([-40, 0, 0]) cantilever_snap();
            color("salmon") translate([40, 0, 0]) annular_snap();
            color("lightcoral") translate([0, -40, 0]) detent();
        }
        
        // Optional: additional clearance cutouts to facilitate assembly
        for (i = [0: 20: 120]) {
            rotate([0, 0, i])
            translate([0, 0, -clearance])
            cylinder(d = 1, h = 50, $fn=50);
        }
    }
}

// Render the complete snap-fit mechanism
print_in_place_snap_fit();
