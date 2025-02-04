C:\mygit\BLazy\repo\scad\utils.scad
Language detected: openscad
// Common 3D printing tolerances
$fn = 100;  // Default resolution for circles and curves
$tolerance = 0.1;  // Standard tolerance for 3D printing
$clearance = 0.2;  // Standard clearance for moving parts

// Layer height considerations
$layer_height = 0.2;  // Standard layer height for 3D printing

// Utility functions for rounded corners and other common operations
/**
 * Create a rounded corner on a rectangular prism.
 *
 * @param size The size of the rectangular prism (x, y, z).
 * @param radius The radius of the rounded corner.
 */
module rounded_corner(size, radius) {
    hull() {
        for (i = [0, 1]) {
            for (j = [0, 1]) {
                translate([i * size[0], j * size[1], 0])
                    sphere(r = radius, $fn = $fn);
            }
        }
    }
}

/**
 * Create a fillet on a rectangular prism.
 *
 * @param size The size of the rectangular prism (x, y, z).
 * @param radius The radius of the fillet.
 * @param chamfer Whether to create a chamfer (true) or a fillet (false).
 */
module fillet(size, radius, chamfer = false) {
    if (chamfer) {
        // Chamfer the corners
        hull() {
            for (i = [0, 1]) {
                for (j = [0, 1]) {
                    translate([i * size[0], j * size[1], 0])
                        cube([radius, radius, size[2]], center = true);
                }
            }
        }
    } else {
        // Fillet the corners
        rounded_corner(size, radius);
    }
}

// Basic geometric helper functions
/**
 * Create a circle with a given radius and resolution.
 *
 * @param radius The radius of the circle.
 * @param resolution The resolution of the circle (default: $fn).
 */
module circle(radius, resolution = $fn) {
    $fn = resolution;
    circle(r = radius);
}

/**
 * Create a cylinder with a given radius, height, and resolution.
 *
 * @param radius The radius of the cylinder.
 * @param height The height of the cylinder.
 * @param resolution The resolution of the cylinder (default: $fn).
 */
module cylinder(radius, height, resolution = $fn) {
    $fn = resolution;
    cylinder(r = radius, h = height);
}

/**
 * Create a sphere with a given radius and resolution.
 *
 * @param radius The radius of the sphere.
 * @param resolution The resolution of the sphere (default: $fn).
 */
module sphere(radius, resolution = $fn) {
    $fn = resolution;
    sphere(r = radius);
}
