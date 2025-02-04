C:\mygit\BLazy\repo\scad\mechanical_lib.scad
Language detected: scad
// Mechanical Components Library

// Utility function to create a cylinder with parameters
module cylinder_hole(d, h, center = false, $fn = $fn) {
    // Data type checking
    assert(is_num(d) && is_num(h), "Diameter and height must be numbers");
    assert(is_bool(center), "Center must be a boolean");
    
    // Calculate radius
    r = d / 2;
    
    // Create cylinder hole
    cylinder(h = h, r = r, center = center, $fn = $fn);
}

// Module for creating basic washers with parameters
module washer(inner_diameter, outer_diameter, thickness, $fn = $fn) {
    // Data type checking
    assert(is_num(inner_diameter) && is_num(outer_diameter) && is_num(thickness), "Diameters and thickness must be numbers");
    
    // Calculate radii
    inner_r = inner_diameter / 2;
    outer_r = outer_diameter / 2;
    
    // Create washer
    difference() {
        // Outer cylinder
        cylinder(h = thickness, r = outer_r, $fn = $fn);
        
        // Inner cylinder hole
        cylinder_hole(inner_diameter, thickness + 0.1, $fn = $fn);
    }
}

// Module for creating pins with customizable tolerances
module pin(diameter, length, tolerance = 0.1, $fn = $fn) {
    // Data type checking
    assert(is_num(diameter) && is_num(length) && is_num(tolerance), "Diameter, length, and tolerance must be numbers");
    
    // Calculate radius
    r = diameter / 2;
    
    // Adjust diameter based on tolerance
    adjusted_diameter = diameter + tolerance;
    adjusted_r = adjusted_diameter / 2;
    
    // Create pin
    cylinder(h = length, r = adjusted_r, $fn = $fn);
}

// Module for creating basic gears
module gear(teeth, pitch_diameter, thickness, $fn = $fn) {
    // Data type checking
    assert(is_num(teeth) && is_num(pitch_diameter) && is_num(thickness), "Teeth, pitch diameter, and thickness must be numbers");
    
    // Calculate radius
    r = pitch_diameter / 2;
    
    // Calculate gear width
    width = pitch_diameter * pi / teeth;
    
    // Create gear
    difference() {
        // Outer cylinder
        cylinder(h = thickness, r = r, $fn = $fn);
        
        // Inner cylinder hole
        cylinder_hole(pitch_diameter - width, thickness + 0.1, $fn = $fn);
    }
    
    // Add teeth
    for (i = [0:teeth - 1]) {
        rotate([0, 0, i * 360 / teeth]) {
            // Tooth width
            tooth_width = width * 0.5;
            
            // Tooth height
            tooth_height = thickness + 0.1;
            
            // Create tooth
            translate([r - tooth_width / 2, 0, -tooth_height / 2]) {
                cube(size = [tooth_width, tooth_width, tooth_height]);
            }
        }
    }
}

// Example usage:
washer(10, 20, 2);
translate([30, 0, 0]) {
    pin(5, 10);
}
translate([60, 0, 0]) {
    gear(10, 20, 2);
}
C:\mygit\BLazy\repo\scad\gear_lib.scad
Language detected: openscad
// Involute Spur Gear Module
module involute_spur_gear(
    // Number of teeth on the gear
    tooth_count = 10,
    // Module size (pitch diameter divided by number of teeth)
    module_size = 1,
    // Pressure angle in degrees (typically 20)
    pressure_angle = 20,
    // Tooth width (default is 1/2 of module size)
    tooth_width = 0.5,
    // Clearance between gears (default is 0.1mm)
    clearance = 0.1,
    // Thickness of the gear
    thickness = 5,
    // Resolution of the gear curves (default is 100)
    $fn = 100
) {
    // Calculate pitch radius
    pitch_radius = module_size * tooth_count / 2;

    // Calculate base radius
    base_radius = pitch_radius * cos(pressure_angle);

    // Calculate addendum (tooth height above pitch radius)
    addendum = module_size;

    // Calculate dedendum (tooth height below pitch radius)
    dedendum = module_size;

    // Calculate tooth height (total)
    tooth_height = addendum + dedendum;

    // Calculate involute curve parameters
    involute_angle = acos(base_radius / pitch_radius);

    // Create the gear
    difference() {
        // Outer circle
        cylinder(h = thickness, r = pitch_radius + addendum, $fn = $fn);

        // Inner circle
        translate([0, 0, -thickness/2]) cylinder(h = thickness + 0.1, r = pitch_radius - dedendum - clearance, $fn = $fn);

        // Cut out involute curve
        for (i = [0 : tooth_count - 1]) {
            rotate([0, 0, i * 360 / tooth_count]) {
                // Involute curve
                translate([0, -pitch_radius, 0]) rotate([0, 0, involute_angle]) {
                    linear_extrude(height = thickness, center = true) {
                        polygon(points = [
                            [0, 0],
                            [pitch_radius - base_radius, 0],
                            [pitch_radius * cos(involute_angle), pitch_radius * sin(involute_angle)],
                            [0, pitch_radius * sin(involute_angle)]
                        ]);
                    }
                }
            }
        }
    }
}

// Planetary Gear System Module
module planetary_gear_system(
    // Number of sun teeth
    sun_teeth = 10,
    // Number of planet teeth
    planet_teeth = 15,
    // Module size
    module_size = 1,
    // Pressure angle in degrees (typically 20)
    pressure_angle = 20,
    // Tooth width (default is 1/2 of module size)
    tooth_width = 0.5,
    // Clearance between gears (default is 0.1mm)
    clearance = 0.1,
    // Thickness of the gears
    thickness = 5,
    // Resolution of the gear curves (default is 100)
    $fn = 100
) {
    // Calculate sun gear parameters
    sun_pitch_radius = module_size * sun_teeth / 2;
    sun_base_radius = sun_pitch_radius * cos(pressure_angle);
    sun_addendum = module_size;
    sun_dedendum = module_size;

    // Calculate planet gear parameters
    planet_pitch_radius = module_size * planet_teeth / 2;
    planet_base_radius = planet_pitch_radius * cos(pressure_angle);
    planet_addendum = module_size;
    planet_dedendum = module_size;

    // Create sun gear
    translate([0, 0, 0]) involute_spur_gear(tooth_count = sun_teeth, module_size = module_size, pressure_angle = pressure_angle, tooth_width = tooth_width, clearance = clearance, thickness = thickness, $fn = $fn);

    // Create planet gears
    for (i = [0 : 2]) {
        rotate([0, 0, i * 120]) translate([sun_pitch_radius + planet_pitch_radius + clearance, 0, 0]) involute_spur_gear(tooth_count = planet_teeth, module_size = module_size, pressure_angle = pressure_angle, tooth_width = tooth_width, clearance = clearance, thickness = thickness, $fn = $fn);
    }
}

// Rack and Pinion Mechanism Module
module rack_and_pinion(
    // Number of teeth on the gear
    tooth_count = 10,
    // Module size
    module_size = 1,
    // Pressure angle in degrees (typically 20)
    pressure_angle = 20,
    // Tooth width (default is 1/2 of module size)
    tooth_width = 0.5,
    // Clearance between gears (default is 0.1mm)
    clearance = 0.1,
    // Thickness of the gear
    thickness = 5,
    // Length of the rack
    rack_length = 20,
    // Resolution of the gear curves (default is 100)
    $fn = 100
) {
    // Calculate pitch radius
    pitch_radius = module_size * tooth_count / 2;

    // Calculate base radius
    base_radius = pitch_radius * cos(pressure_angle);

    // Calculate addendum (tooth height above pitch radius)
    addendum = module_size;

    // Calculate dedendum (tooth height below pitch radius)
    dedendum = module_size;

    // Calculate tooth height (total)
    tooth_height = addendum + dedendum;

    // Create gear
    translate([0, 0, 0]) involute_spur_gear(tooth_count = tooth_count, module_size = module_size, pressure_angle = pressure_angle, tooth_width = tooth_width, clearance = clearance, thickness = thickness, $fn = $fn);

    // Create rack
    translate([pitch_radius + clearance, 0, 0]) cube([rack_length, tooth_height + 2 * clearance, thickness]);
}

// Helper Function for Calculating Gear Ratios
function gear_ratio(driven_teeth, driving_teeth) = driven_teeth / driving_teeth;

// Helper Function for Calculating Proper Gear Mesh Spacing
function gear_mesh_spacing(pitch_radius1, pitch_radius2, clearance) = pitch_radius1 + pitch_radius2 + clearance;

// Example Usage:
// Involute Spur Gear
involute_spur_gear(tooth_count = 15, module_size = 1, pressure_angle = 20, tooth_width = 0.5, clearance = 0.1, thickness = 5, $fn = 100);

// Planetary Gear System
translate([20, 0, 0]) planetary_gear_system(sun_teeth = 10, planet_teeth = 15, module_size = 1, pressure_angle = 20, tooth_width = 0.5, clearance = 0.1, thickness = 5, $fn = 100);

// Rack and Pinion Mechanism
translate([40, 0, 0]) rack_and_pinion(tooth_count = 10, module_size = 1, pressure_angle = 20, tooth_width = 0.5, clearance = 0.1, thickness = 5, rack_length = 20, $fn = 100);
