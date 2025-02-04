C:\mygit\BLazy\repo\scad\mechanical_lib.scad
Language detected: openscad
// Mechanical Library for 3D Printing

// Module for creating print-in-place ball bearings
/**
 * Creates a print-in-place ball bearing with customizable parameters.
 * 
 * @param {float} od - Outer diameter of the bearing
 * @param {int} ball_count - Number of balls in the bearing
 * @param {float} clearance - Clearance between the balls and the outer ring
 * @param {float} tol - Tolerance for 3D printing (default: 0.1)
 */
module ball_bearing(od, ball_count, clearance, tol = 0.1) {
    // Calculate the ball diameter based on the outer diameter and ball count
    ball_diameter = (od / (ball_count + 1)) * 2;
    
    // Create the outer ring
    difference() {
        cylinder(h = 10, d = od, center = true);
        // Subtract the ball cavity
        for (i = [0 : ball_count - 1]) {
            rotate([0, 0, 360 / ball_count * i]) {
                translate([od / 2 - ball_diameter / 2 - clearance / 2, 0, 0]) {
                    sphere(d = ball_diameter + clearance);
                }
            }
        }
    }
    
    // Create the balls
    for (i = [0 : ball_count - 1]) {
        rotate([0, 0, 360 / ball_count * i]) {
            translate([od / 2 - ball_diameter / 2 - clearance / 2, 0, 0]) {
                sphere(d = ball_diameter);
            }
        }
    }
}

// Module for creating print-in-place hinges
/**
 * Creates a print-in-place hinge with adjustable parameters.
 * 
 * @param {float} pin_diameter - Diameter of the hinge pin
 * @param {int} knuckle_count - Number of knuckles in the hinge
 * @param {float} tol - Tolerance for 3D printing (default: 0.1)
 */
module hinge(pin_diameter, knuckle_count, tol = 0.1) {
    // Calculate the knuckle diameter based on the pin diameter and knuckle count
    knuckle_diameter = pin_diameter * 2;
    
    // Create the knuckles
    for (i = [0 : knuckle_count - 1]) {
        translate([i * (knuckle_diameter + pin_diameter), 0, 0]) {
            cylinder(h = 10, d = knuckle_diameter, center = true);
        }
    }
    
    // Create the pin
    for (i = [0 : knuckle_count - 1]) {
        translate([i * (knuckle_diameter + pin_diameter) + knuckle_diameter / 2, 0, 0]) {
            cylinder(h = 10, d = pin_diameter, center = true);
        }
    }
}

// Utility function for managing printer tolerances
/**
 * Calculates the proper clearance based on the tolerance and desired clearance.
 * 
 * @param {float} tol - Tolerance for 3D printing
 * @param {float} clearance - Desired clearance
 * @return {float} Calculated clearance
 */
function calculate_clearance(tol, clearance) {
    return clearance + tol;
}

// Example usage:
ball_bearing(od = 20, ball_count = 5, clearance = 0.5);
translate([30, 0, 0]) {
    hinge(pin_diameter = 5, knuckle_count = 3);
}

// Test the calculate_clearance function
clearance = calculate_clearance(tol = 0.1, clearance = 0.5);
echo("Calculated clearance:", clearance);
