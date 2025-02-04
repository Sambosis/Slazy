C:\mygit\BLazy\repo\3dsim\static\js\simulation.js
Language detected: javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';

let scene, camera, renderer, controls, gui;
let car, airflow, pressureField, carGroup;
let simulationParams = {
    length: 1.0,
    height: 0.5,
    width: 0.4,
    speed: 25,
    groundClearance: 0.1,
    hoodAngle: 15,
    rearAngle: 25,
	airDensity: 1.225, // kg/m^3
    temperature: 20, // °C
    dynamicViscosity: 1.81e-5 // kg/(m*s)
};

// Data display variables
let dragCoefficientDisplay, liftForceDisplay, pressureDisplay, velocityDisplay, reynoldsDisplay, airDensityDisplay, temperatureDisplay, powerDisplay;


// Initialize the scene
function init() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);

    // Camera setup
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(2, 2, 2);

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);
	
	// GUI setup
	  gui = new GUI();
	  const carFolder = gui.addFolder('Car Parameters');
  
	  carFolder.add(simulationParams, 'length', 0.5, 2.0).name('Length').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'height', 0.2, 1.0).name('Height').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'width', 0.2, 0.8).name('Width').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'groundClearance', 0, 0.3).name('Ground Clearance').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'hoodAngle', 0, 45).name('Hood Angle').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'rearAngle', 0, 45).name('Rear Angle').onChange(updateSimulation);
	  carFolder.open();
  
	  const airFolder = gui.addFolder('Air Parameters');
	  airFolder.add(simulationParams, 'airDensity', 0.5, 2.0).name('Air Density').onChange(updateSimulation);
	  airFolder.add(simulationParams, 'temperature', 0, 40).name('Temperature').onChange(updateSimulation);
	  airFolder.add(simulationParams,'speed',0, 100).name('Wind Speed').onChange(updateSimulation);
	  airFolder.open();

    // Controls setup
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);

    createCar();
    createAirflow();
	
	// Initialize data display elements
	dragCoefficientDisplay = document.getElementById('drag-coefficient');
    liftForceDisplay = document.getElementById('lift-force');
    pressureDisplay = document.getElementById('pressure');
    velocityDisplay = document.getElementById('velocity');
    reynoldsDisplay = document.getElementById('reynolds');
    airDensityDisplay = document.getElementById('air-density');
    temperatureDisplay = document.getElementById('temperature');
	powerDisplay = document.getElementById('power');


    // Handle window resize
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function createCar() {
    // Remove existing car if it exists
     if (car) {
        scene.remove(car);
    }

    carGroup = new THREE.Group();

    // Car material
    const carMaterial = new THREE.MeshPhongMaterial({
        color: 0x156289,
        transparent: true,
        opacity: 0.8
    });

     // Create main body
    const bodyGeometry = new THREE.BoxGeometry(
        simulationParams.length * 0.6,
        simulationParams.height * 0.6,
        simulationParams.width
    );
    const bodyMesh = new THREE.Mesh(bodyGeometry, carMaterial);
    bodyMesh.position.y = simulationParams.groundClearance + simulationParams.height * 0.3;
    carGroup.add(bodyMesh);

    // Create hood (front section)
    const hoodShape = new THREE.Shape();
    const hoodLength = simulationParams.length * 0.2;
    const hoodHeight = simulationParams.height * 0.4;
    const hoodAngleRad = (simulationParams.hoodAngle * Math.PI) / 180;
    
    hoodShape.moveTo(0, 0);
    hoodShape.lineTo(hoodLength * Math.cos(hoodAngleRad), hoodHeight);
    hoodShape.lineTo(hoodLength, 0);
    hoodShape.lineTo(0, 0);

    const extrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };

    const hoodGeometry = new THREE.ExtrudeGeometry(hoodShape, extrudeSettings);
    const hoodMesh = new THREE.Mesh(hoodGeometry, carMaterial);
    hoodMesh.rotation.y = Math.PI / 2;
    hoodMesh.position.set(
        simulationParams.length * 0.3,
        simulationParams.groundClearance,
        simulationParams.width / 2
    );
    carGroup.add(hoodMesh);

    // Create rear section
    const rearShape = new THREE.Shape();
    const rearLength = simulationParams.length * 0.2;
    const rearHeight = simulationParams.height * 0.5;
    const rearAngleRad = (simulationParams.rearAngle * Math.PI) / 180;

    rearShape.moveTo(0, 0);
    rearShape.lineTo(0, rearHeight);
    rearShape.lineTo(rearLength * Math.cos(rearAngleRad), 0);
    rearShape.lineTo(0, 0);

    const rearGeometry = new THREE.ExtrudeGeometry(rearShape, extrudeSettings);
    const rearMesh = new THREE.Mesh(rearGeometry, carMaterial);
    rearMesh.rotation.y = -Math.PI / 2;
    rearMesh.position.set(
        -simulationParams.length * 0.3,
        simulationParams.groundClearance,
        -simulationParams.width / 2
    );
    carGroup.add(rearMesh);
	
	
    // Add the car group to the scene and store it as car
    car = carGroup;
    scene.add(car);
}


function createAirflow() {
    // Create particle system for airflow visualization
    const particleCount = 2000;
    const particles = new THREE.BufferGeometry();
    const positions = [];
    const velocities = [];

    // Create initial particle positions in a grid pattern
    const spacing = 0.2;
    const xStart = -5;
    const yRange = 2;
    const zRange = 2;

    for (let x = xStart; x < 5; x += spacing) {
        for (let y = -yRange; y < yRange; y += spacing) {
            for (let z = -zRange; z < zRange; z += spacing) {
                positions.push(x, y, z);
                // Initial velocity (will be modified based on car shape)
                velocities.push(simulationParams.speed * 0.01, 0, 0);
            }
        }
    }

    particles.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    particles.userData = { velocities: velocities };

    const particleMaterial = new THREE.PointsMaterial({
        color: 0x00ff00,
        size: 0.03,
        transparent: true,
        opacity: 0.6
    });

    airflow = new THREE.Points(particles, particleMaterial);
    scene.add(airflow);
}

async function updateSimulation() {

    // Get current parameters
    const params = new URLSearchParams({
        length: simulationParams.length,
        height: simulationParams.height,
        width: simulationParams.width,
        speed: simulationParams.speed,
        groundClearance: simulationParams.groundClearance,
        hoodAngle: simulationParams.hoodAngle,
        rearAngle: simulationParams.rearAngle,
		airDensity: simulationParams.airDensity,
        temperature: simulationParams.temperature,
		dynamicViscosity: simulationParams.dynamicViscosity
    });

    try {
        const response = await fetch(`/simulation?${params}`);
        const data = await response.json();

        // Update visualization with new data
        updateCarGeometry();
        updateAirflowVisualization(data);
        updatePressureField(data);
		
		// Update data display
		updateDataDisplay(data);

		
        
    } catch (error) {
        console.error('Error updating simulation:', error);
    }
}

function updateCarGeometry() {
    scene.remove(car);
    createCar();
}

function updateAirflowVisualization(data) {
    const positions = airflow.geometry.attributes.position.array;
    const velocities = airflow.geometry.userData.velocities;
    const particleCount = positions.length / 3;

    // Car dimensions for collision detection
    const carBounds = {
        front: simulationParams.length * 0.3,
        back: -simulationParams.length * 0.3,
        top: simulationParams.height + simulationParams.groundClearance,
        bottom: simulationParams.groundClearance,
        right: simulationParams.width / 2,
        left: -simulationParams.width / 2
    };

    const hoodAngleRad = (simulationParams.hoodAngle * Math.PI) / 180;
    const rearAngleRad = (simulationParams.rearAngle * Math.PI) / 180;

    for (let i = 0; i < particleCount; i++) {
        const idx = i * 3;
        const x = positions[idx];
        const y = positions[idx + 1];
        const z = positions[idx + 2];

        // Check if particle is near the car
        if (x >= carBounds.back && x <= carBounds.front &&
            y >= carBounds.bottom && y <= carBounds.top &&
            z >= carBounds.left && z <= carBounds.right) {

            // Front hood deflection
            if (x > 0) {
                const hoodY = simulationParams.groundClearance + 
                    (x / carBounds.front) * simulationParams.height * 0.4;
                if (y < hoodY) {
                    velocities[idx + 1] = Math.abs(velocities[idx]) * Math.sin(hoodAngleRad);
                    velocities[idx] *= Math.cos(hoodAngleRad);
                }
            }
            // Rear deflection
            else if (x < 0) {
                const rearY = simulationParams.groundClearance + 
                    (1 + x / carBounds.back) * simulationParams.height * 0.5;
                if (y < rearY) {
                    velocities[idx + 1] = -Math.abs(velocities[idx]) * Math.sin(rearAngleRad);
                    velocities[idx] *= Math.cos(rearAngleRad);
                }
            }

            // Ground effect
            if (y < carBounds.bottom + 0.1) {
                velocities[idx + 1] = Math.abs(velocities[idx + 1]);
            }

            // Side deflection
            if (Math.abs(z) > carBounds.right * 0.8) {
                velocities[idx + 2] = Math.sign(z) * Math.abs(velocities[idx]) * 0.3;
            }
        }

        // Apply velocities
        positions[idx] += velocities[idx];
        positions[idx + 1] += velocities[idx + 1];
        positions[idx + 2] += velocities[idx + 2];

        // Gradually restore horizontal flow
        velocities[idx + 1] *= 0.98;
        velocities[idx + 2] *= 0.98;

        // Reset particles that go too far
        if (positions[idx] > 5) {
            positions[idx] = -5;
            positions[idx + 1] = Math.random() * 4 - 2;
            positions[idx + 2] = Math.random() * 4 - 2;
            velocities[idx] = simulationParams.speed * 0.01;
            velocities[idx + 1] = 0;
            velocities[idx + 2] = 0;
        }
    }

    airflow.geometry.attributes.position.needsUpdate = true;
}


function updatePressureField(data) {
    // Remove existing pressure field if it exists
    if (pressureField) {
        scene.remove(pressureField);
    }

    // Create visualization of pressure field using points with colors
    const geometry = new THREE.BufferGeometry();
    const positions = [];
    const colors = [];

    const pressureMin = Math.min(...data.pressure.flat());
    const pressureMax = Math.max(...data.pressure.flat());

    for (let i = 0; i < data.x_coords.length; i++) {
        for (let j = 0; j < data.x_coords[i].length; j++) {
            positions.push(
                data.x_coords[i][j],
                data.y_coords[i][j],
                0
            );

            // Color based on pressure (blue to red)
            const pressure = data.pressure[i][j];
            const t = (pressure - pressureMin) / (pressureMax - pressureMin);
            const color = new THREE.Color();
            color.setHSL(0.7 * (1 - t), 1, 0.5);
            colors.push(color.r, color.g, color.b);
        }
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
        size: 0.05,
        vertexColors: true,
        transparent: true,
        opacity: 0.6
    });

    pressureField = new THREE.Points(geometry, material);
    scene.add(pressureField);
}

function updateDataDisplay(data) {
    dragCoefficientDisplay.textContent = data.drag_coefficient.toFixed(3);
    liftForceDisplay.textContent = data.lift_force.toFixed(3);
	
	
    // Format pressure for display
    const avgPressure = data.pressure.flat().reduce((a, b) => a + b, 0) / data.pressure.flat().length;
    pressureDisplay.textContent = avgPressure.toFixed(2);


    velocityDisplay.textContent = simulationParams.speed.toFixed(1);
    reynoldsDisplay.textContent = data.reynolds_number.toFixed(0);
    airDensityDisplay.textContent = simulationParams.airDensity.toFixed(3);
	const tempInC = simulationParams.temperature
    temperatureDisplay.textContent = tempInC.toFixed(1);
	powerDisplay.textContent = data.power.toFixed(0);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    
    // Animate airflow particles
    if (airflow) {
        const positions = airflow.geometry.attributes.position.array;
        const particleCount = positions.length / 3;
        
        for (let i = 0; i < particleCount; i++) {
            const idx = i * 3;
            positions[idx] += simulationParams.speed * 0.001;
            
            if (positions[idx] > 5) {
                positions[idx] = -5;
            }
        }
        airflow.geometry.attributes.position.needsUpdate = true;
    }
    
    renderer.render(scene, camera);
}

// Initialize the simulation
init();
C:\mygit\BLazy\repo\3dsim\static\js\carGeometry.js
Language detected: javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';

let scene, camera, renderer, controls, gui;
let car, airflow, pressureField, carGroup;
let simulationParams = {
    length: 1.0,
    height: 0.5,
    width: 0.4,
    speed: 25,
    groundClearance: 0.1,
    hoodAngle: 15,
    rearAngle: 25,
    wheelRadius : 0.07,
    wheelWidth : 0.04,
	airDensity: 1.225, // kg/m^3
    temperature: 20, // °C
    dynamicViscosity: 1.81e-5 // kg/(m*s)
};

// Data display variables
let dragCoefficientDisplay, liftForceDisplay, pressureDisplay, velocityDisplay, reynoldsDisplay, airDensityDisplay, temperatureDisplay, powerDisplay;


// Initialize the scene
function init() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);

    // Camera setup
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(2, 2, 2);

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);
	
	// GUI setup
	  gui = new GUI();
	  const carFolder = gui.addFolder('Car Parameters');
  
	  carFolder.add(simulationParams, 'length', 0.5, 2.0).name('Length').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'height', 0.2, 1.0).name('Height').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'width', 0.2, 0.8).name('Width').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelRadius', 0.03, 0.15).name('Wheel Radius').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelWidth', 0.02, 0.10).name('Wheel Width').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'groundClearance', 0, 0.3).name('Ground Clearance').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'hoodAngle', 0, 45).name('Hood Angle').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'rearAngle', 0, 45).name('Rear Angle').onChange(updateSimulation);
	  carFolder.open();
  
	  const airFolder = gui.addFolder('Air Parameters');
	  airFolder.add(simulationParams, 'airDensity', 0.5, 2.0).name('Air Density').onChange(updateSimulation);
	  airFolder.add(simulationParams, 'temperature', 0, 40).name('Temperature').onChange(updateSimulation);
	  airFolder.add(simulationParams,'speed',0, 100).name('Wind Speed').onChange(updateSimulation);
	  airFolder.open();

    // Controls setup
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);

    createCar();
    createAirflow();
	
	// Initialize data display elements
	dragCoefficientDisplay = document.getElementById('drag-coefficient');
    liftForceDisplay = document.getElementById('lift-force');
    pressureDisplay = document.getElementById('pressure');
    velocityDisplay = document.getElementById('velocity');
    reynoldsDisplay = document.getElementById('reynolds');
    airDensityDisplay = document.getElementById('air-density');
    temperatureDisplay = document.getElementById('temperature');
	powerDisplay = document.getElementById('power');


    // Handle window resize
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function createCar() {
    // Remove existing car if it exists
     if (car) {
        scene.remove(car);
    }

    carGroup = new THREE.Group();

    // Car material
    const carMaterial = new THREE.MeshPhongMaterial({
        color: 0x156289,
        transparent: true,
        opacity: 0.8
    });

    // Function to create a rounded rectangle shape
    function createRoundedRectShape(width, height, radius) {
        const shape = new THREE.Shape();
        shape.moveTo(0, radius);
        shape.lineTo(0, height - radius);
        shape.quadraticCurveTo(0, height, radius, height);
        shape.lineTo(width - radius, height);
        shape.quadraticCurveTo(width, height, width, height - radius);
        shape.lineTo(width, radius);
        shape.quadraticCurveTo(width, 0, width - radius, 0);
        shape.lineTo(radius, 0);
        shape.quadraticCurveTo(0, 0, 0, radius);
        return shape;
    }
     // Create main body
    const bodyShape = createRoundedRectShape(
        simulationParams.length * 0.6,
        simulationParams.height * 0.6,
        simulationParams.height * 0.1
    );
    const bodyExtrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };
    const bodyGeometry = new THREE.ExtrudeGeometry(bodyShape, bodyExtrudeSettings);
    const bodyMesh = new THREE.Mesh(bodyGeometry, carMaterial);
    bodyMesh.position.y = simulationParams.groundClearance + simulationParams.height * 0.3;
    carGroup.add(bodyMesh);

    // Create hood (front section)
    const hoodShape = new THREE.Shape();
    const hoodLength = simulationParams.length * 0.2;
    const hoodHeight = simulationParams.height * 0.4;
    const hoodAngleRad = (simulationParams.hoodAngle * Math.PI) / 180;

    hoodShape.moveTo(0, 0);
    hoodShape.lineTo(hoodLength * Math.cos(hoodAngleRad), hoodHeight);
     hoodShape.lineTo(hoodLength,0);
    hoodShape.lineTo(0,0);
   
    const extrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };

    const hoodGeometry = new THREE.ExtrudeGeometry(hoodShape, extrudeSettings);
    const hoodMesh = new THREE.Mesh(hoodGeometry, carMaterial);
    hoodMesh.rotation.y = Math.PI / 2;
    hoodMesh.position.set(
        simulationParams.length * 0.3,
        simulationParams.groundClearance,
        simulationParams.width / 2
    );
    carGroup.add(hoodMesh);



    // Create rear section
    const rearShape = new THREE.Shape();
    const rearLength = simulationParams.length * 0.2;
	const rearHeight = simulationParams.height * 0.5;
    const rearAngleRad = (simulationParams.rearAngle * Math.PI) / 180;
    
    rearShape.moveTo(0, 0);
    rearShape.lineTo(0, rearHeight);
	rearShape.lineTo(rearLength * Math.cos(rearAngleRad),0);
    rearShape.lineTo(0, 0);

    const rearGeometry = new THREE.ExtrudeGeometry(rearShape, extrudeSettings);
    const rearMesh = new THREE.Mesh(rearGeometry, carMaterial);
    rearMesh.rotation.y = -Math.PI / 2;
    rearMesh.position.set(
        -simulationParams.length * 0.3,
        simulationParams.groundClearance,
        -simulationParams.width / 2
    );
     carGroup.add(rearMesh);
     
     // Create wheels
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x333333 });
    const wheelGeometry = new THREE.CylinderGeometry(simulationParams.wheelRadius, simulationParams.wheelRadius, simulationParams.wheelWidth, 32);

    //function to create wheel
     function createWheel(x, y, z) {
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, y, z);
		
        // Add hubcap
        const hubcapRadius = simulationParams.wheelRadius * 0.5
        const hubcapGeometry = new THREE.CylinderGeometry(hubcapRadius, hubcapRadius, simulationParams.wheelWidth+0.01, 32);
		const hubcapMaterial = new THREE.MeshPhongMaterial({color : 0xcccccc})//metallic silver
		const hubcap = new THREE.Mesh(hubcapGeometry,hubcapMaterial);
		hubcap.rotation.z = Math.PI / 2;
		wheel.add(hubcap);
		
        return wheel;
    }

    // Add wheels
	const wheelY = simulationParams.groundClearance + simulationParams.wheelRadius;
    const wheelZOffset = simulationParams.width/2 + simulationParams.wheelWidth/2;
    const wheelXOffset = simulationParams.length * 0.25
    const frontLeftWheel = createWheel(wheelXOffset, wheelY, wheelZOffset);
    const frontRightWheel = createWheel(wheelXOffset, wheelY, -wheelZOffset);
    const rearLeftWheel = createWheel(-wheelXOffset, wheelY, wheelZOffset);
    const rearRightWheel = createWheel(-wheelXOffset, wheelY, -wheelZOffset);
    carGroup.add(frontLeftWheel, frontRightWheel, rearLeftWheel, rearRightWheel);

	
    // Add the car group to the scene and store it as car
    car = carGroup;
    scene.add(car);
}


function createAirflow() {
    // Create particle system for airflow visualization
    const particleCount = 2000;
    const particles = new THREE.BufferGeometry();
    const positions = [];
    const velocities = [];

    // Create initial particle positions in a grid pattern
    const spacing = 0.2;
    const xStart = -5;
    const yRange = 2;
    const zRange = 2;

    for (let x = xStart; x < 5; x += spacing) {
        for (let y = -yRange; y < yRange; y += spacing) {
            for (let z = -zRange; z < zRange; z += spacing) {
                positions.push(x, y, z);
                // Initial velocity (will be modified based on car shape)
                velocities.push(simulationParams.speed * 0.01, 0, 0);
            }
        }
    }

    particles.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    particles.userData = { velocities: velocities };

    const particleMaterial = new THREE.PointsMaterial({
        color: 0x00ff00,
        size: 0.03,
        transparent: true,
        opacity: 0.6
    });

    airflow = new THREE.Points(particles, particleMaterial);
    scene.add(airflow);
}

async function updateSimulation() {

    // Get current parameters
    const params = new URLSearchParams({
        length: simulationParams.length,
        height: simulationParams.height,
        width: simulationParams.width,
        speed: simulationParams.speed,
        groundClearance: simulationParams.groundClearance,
        hoodAngle: simulationParams.hoodAngle,
        rearAngle: simulationParams.rearAngle,
        wheelRadius: simulationParams.wheelRadius,
        wheelWidth: simulationParams.wheelWidth,
		airDensity: simulationParams.airDensity,
        temperature: simulationParams.temperature,
		dynamicViscosity: simulationParams.dynamicViscosity
    });

    try {
        const response = await fetch(`/simulation?${params}`);
        const data = await response.json();

        // Update visualization with new data
        updateCarGeometry();
        updateAirflowVisualization(data);
        updatePressureField(data);
		
		// Update data display
		updateDataDisplay(data);

		
        
    } catch (error) {
        console.error('Error updating simulation:', error);
    }
}

function updateCarGeometry() {
    scene.remove(car);
    createCar();
}

function updateAirflowVisualization(data) {
    const positions = airflow.geometry.attributes.position.array;
    const velocities = airflow.geometry.userData.velocities;
    const particleCount = positions.length / 3;

    // Car dimensions for collision detection
    const carBounds = {
        front: simulationParams.length * 0.3,
        back: -simulationParams.length * 0.3,
        top: simulationParams.height + simulationParams.groundClearance,
        bottom: simulationParams.groundClearance,
        right: simulationParams.width / 2,
        left: -simulationParams.width / 2
    };

    const hoodAngleRad = (simulationParams.hoodAngle * Math.PI) / 180;
    const rearAngleRad = (simulationParams.rearAngle * Math.PI) / 180;

    for (let i = 0; i < particleCount; i++) {
        const idx = i * 3;
        const x = positions[idx];
        const y = positions[idx + 1];
        const z = positions[idx + 2];

        // Check if particle is near the car
        if (x >= carBounds.back && x <= carBounds.front &&
            y >= carBounds.bottom && y <= carBounds.top &&
            z >= carBounds.left && z <= carBounds.right) {

            // Front hood deflection
            if (x > 0) {
                const hoodY = simulationParams.groundClearance + 
                    (x / carBounds.front) * simulationParams.height * 0.4;
                if (y < hoodY) {
                    velocities[idx + 1] = Math.abs(velocities[idx]) * Math.sin(hoodAngleRad);
                    velocities[idx] *= Math.cos(hoodAngleRad);
                }
            }
            // Rear deflection
            else if (x < 0) {
                const rearY = simulationParams.groundClearance + 
                    (1 + x / carBounds.back) * simulationParams.height * 0.5;
                if (y < rearY) {
                    velocities[idx + 1] = -Math.abs(velocities[idx]) * Math.sin(rearAngleRad);
                    velocities[idx] *= Math.cos(rearAngleRad);
                }
            }

            // Ground effect
             if (y < carBounds.bottom + 0.1) {
                velocities[idx + 1] = Math.abs(velocities[idx + 1]);
            }


            // Side deflection
            if (Math.abs(z) > carBounds.right * 0.8) {
                velocities[idx + 2] = Math.sign(z) * Math.abs(velocities[idx]) * 0.3;
            }
        }

        // Apply velocities
        positions[idx] += velocities[idx];
        positions[idx + 1] += velocities[idx + 1];
        positions[idx + 2] += velocities[idx + 2];

         // Gradually restore horizontal flow
        velocities[idx + 1] *= 0.98;
        velocities[idx + 2] *= 0.98;

        // Reset particles that go too far
        if (positions[idx] > 5) {
            positions[idx] = -5;
            positions[idx + 1] = Math.random() * 4 - 2;
            positions[idx + 2] = Math.random() * 4 - 2;
            velocities[idx] = simulationParams.speed * 0.01;
            velocities[idx + 1] = 0;
            velocities[idx + 2] = 0;
        }
    }

    airflow.geometry.attributes.position.needsUpdate = true;
}


function updatePressureField(data) {
    // Remove existing pressure field if it exists
    if (pressureField) {
        scene.remove(pressureField);
    }

    // Create visualization of pressure field using points with colors
    const geometry = new THREE.BufferGeometry();
    const positions = [];
    const colors = [];

    const pressureMin = Math.min(...data.pressure.flat());
    const pressureMax = Math.max(...data.pressure.flat());

    for (let i = 0; i < data.x_coords.length; i++) {
        for (let j = 0; j < data.x_coords[i].length; j++) {
            positions.push(
                data.x_coords[i][j],
                data.y_coords[i][j],
                0
            );

            // Color based on pressure (blue to red)
            const pressure = data.pressure[i][j];
            const t = (pressure - pressureMin) / (pressureMax - pressureMin);
            const color = new THREE.Color();
            color.setHSL(0.7 * (1 - t), 1, 0.5);
            colors.push(color.r, color.g, color.b);
        }
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
        size: 0.05,
        vertexColors: true,
        transparent: true,
        opacity: 0.6
    });

    pressureField = new THREE.Points(geometry, material);
    scene.add(pressureField);
}

function updateDataDisplay(data) {
    dragCoefficientDisplay.textContent = data.drag_coefficient.toFixed(3);
    liftForceDisplay.textContent = data.lift_force.toFixed(3);
	
	
    // Format pressure for display
    const avgPressure = data.pressure.flat().reduce((a, b) => a + b, 0) / data.pressure.flat().length;
    pressureDisplay.textContent = avgPressure.toFixed(2);


    velocityDisplay.textContent = simulationParams.speed.toFixed(1);
    reynoldsDisplay.textContent = data.reynolds_number.toFixed(0);
    airDensityDisplay.textContent = simulationParams.airDensity.toFixed(3);
	const tempInC = simulationParams.temperature
    temperatureDisplay.textContent = tempInC.toFixed(1);
	powerDisplay.textContent = data.power.toFixed(0);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    
    // Animate airflow particles
    if (airflow) {
        const positions = airflow.geometry.attributes.position.array;
        const particleCount = positions.length / 3;
        
        for (let i = 0; i < particleCount; i++) {
            const idx = i * 3;
            positions[idx] += simulationParams.speed * 0.001;
            
            if (positions[idx] > 5) {
                positions[idx] = -5;
            }
        }
        airflow.geometry.attributes.position.needsUpdate = true;
    }
    
    renderer.render(scene, camera);
}

// Initialize the simulation
init();
C:\mygit\BLazy\repo\3dsim\static\js\shaders\fluidShader.js
Language detected: javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';

let scene, camera, renderer, controls, gui;
let car, airflow, pressureField, carGroup;
let simulationParams = {
    length: 1.0,
    height: 0.5,
    width: 0.4,
    speed: 25,
    groundClearance: 0.1,
    hoodAngle: 15,
    rearAngle: 25,
    wheelRadius : 0.07,
    wheelWidth : 0.04,
	airDensity: 1.225, // kg/m^3
    temperature: 20, // °C
    dynamicViscosity: 1.81e-5 // kg/(m*s)
};

// Data display variables
let dragCoefficientDisplay, liftForceDisplay, pressureDisplay, velocityDisplay, reynoldsDisplay, airDensityDisplay, temperatureDisplay, powerDisplay;


// Shader-related variables
let velocityRenderTarget, pressureRenderTarget, divergenceRenderTarget;
let velocityBuffer, pressureBuffer, divergenceBuffer;
let velocityShaderMaterial, pressureShaderMaterial, advectionShaderMaterial, divergenceShaderMaterial;
let resolution;
let quad;

// Initialize the scene
function init() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);

    // Camera setup
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(2, 2, 2);

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);
	
	// GUI setup
	  gui = new GUI();
	  const carFolder = gui.addFolder('Car Parameters');
  
	  carFolder.add(simulationParams, 'length', 0.5, 2.0).name('Length').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'height', 0.2, 1.0).name('Height').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'width', 0.2, 0.8).name('Width').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelRadius', 0.03, 0.15).name('Wheel Radius').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelWidth', 0.02, 0.10).name('Wheel Width').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'groundClearance', 0, 0.3).name('Ground Clearance').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'hoodAngle', 0, 45).name('Hood Angle').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'rearAngle', 0, 45).name('Rear Angle').onChange(updateSimulation);
	  carFolder.open();
  
	  const airFolder = gui.addFolder('Air Parameters');
	  airFolder.add(simulationParams, 'airDensity', 0.5, 2.0).name('Air Density').onChange(updateSimulation);
	  airFolder.add(simulationParams, 'temperature', 0, 40).name('Temperature').onChange(updateSimulation);
	  airFolder.add(simulationParams,'speed',0, 100).name('Wind Speed').onChange(updateSimulation);
	  airFolder.open();

    // Controls setup
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);

    createCar();
    // createAirflow();  // Removing particle based airflow for shader simulation
	
	// Initialize Shader components
	initFluidSimulation();
	createQuad();
	
	// Initialize data display elements
	dragCoefficientDisplay = document.getElementById('drag-coefficient');
    liftForceDisplay = document.getElementById('lift-force');
    pressureDisplay = document.getElementById('pressure');
    velocityDisplay = document.getElementById('velocity');
    reynoldsDisplay = document.getElementById('reynolds');
    airDensityDisplay = document.getElementById('air-density');
    temperatureDisplay = document.getElementById('temperature');
	powerDisplay = document.getElementById('power');


    // Handle window resize
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function createCar() {
    // Remove existing car if it exists
     if (car) {
        scene.remove(car);
    }

    carGroup = new THREE.Group();

    // Car material
    const carMaterial = new THREE.MeshPhongMaterial({
        color: 0x156289,
        transparent: true,
        opacity: 0.8
    });

    // Function to create a rounded rectangle shape
    function createRoundedRectShape(width, height, radius) {
        const shape = new THREE.Shape();
        shape.moveTo(0, radius);
        shape.lineTo(0, height - radius);
        shape.quadraticCurveTo(0, height, radius, height);
        shape.lineTo(width - radius, height);
        shape.quadraticCurveTo(width, height, width, height - radius);
        shape.lineTo(width, radius);
        shape.quadraticCurveTo(width, 0, width - radius, 0);
        shape.lineTo(radius, 0);
        shape.quadraticCurveTo(0, 0, 0, radius);
        return shape;
    }
     // Create main body
    const bodyShape = createRoundedRectShape(
        simulationParams.length * 0.6,
        simulationParams.height * 0.6,
        simulationParams.height * 0.1
    );
    const bodyExtrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };
    const bodyGeometry = new THREE.ExtrudeGeometry(bodyShape, bodyExtrudeSettings);
    const bodyMesh = new THREE.Mesh(bodyGeometry, carMaterial);
    bodyMesh.position.y = simulationParams.groundClearance + simulationParams.height * 0.3;
    carGroup.add(bodyMesh);

    // Create hood (front section)
    const hoodShape = new THREE.Shape();
    const hoodLength = simulationParams.length * 0.2;
    const hoodHeight = simulationParams.height * 0.4;
    const hoodAngleRad = (simulationParams.hoodAngle * Math.PI) / 180;

    hoodShape.moveTo(0, 0);
    hoodShape.lineTo(hoodLength * Math.cos(hoodAngleRad), hoodHeight);
     hoodShape.lineTo(hoodLength,0);
    hoodShape.lineTo(0,0);
   
    const extrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };

    const hoodGeometry = new THREE.ExtrudeGeometry(hoodShape, extrudeSettings);
    const hoodMesh = new THREE.Mesh(hoodGeometry, carMaterial);
    hoodMesh.rotation.y = Math.PI / 2;
    hoodMesh.position.set(
        simulationParams.length * 0.3,
        simulationParams.groundClearance,
        simulationParams.width / 2
    );
    carGroup.add(hoodMesh);



    // Create rear section
    const rearShape = new THREE.Shape();
    const rearLength = simulationParams.length * 0.2;
	const rearHeight = simulationParams.height * 0.5;
    const rearAngleRad = (simulationParams.rearAngle * Math.PI) / 180;
    
    rearShape.moveTo(0, 0);
    rearShape.lineTo(0, rearHeight);
	rearShape.lineTo(rearLength * Math.cos(rearAngleRad),0);
    rearShape.lineTo(0, 0);

    const rearGeometry = new THREE.ExtrudeGeometry(rearShape, extrudeSettings);
    const rearMesh = new THREE.Mesh(rearGeometry, carMaterial);
    rearMesh.rotation.y = -Math.PI / 2;
    rearMesh.position.set(
        -simulationParams.length * 0.3,
        simulationParams.groundClearance,
        -simulationParams.width / 2
    );
     carGroup.add(rearMesh);
     
     // Create wheels
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x333333 });
    const wheelGeometry = new THREE.CylinderGeometry(simulationParams.wheelRadius, simulationParams.wheelRadius, simulationParams.wheelWidth, 32);

    //function to create wheel
     function createWheel(x, y, z) {
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, y, z);
		
        // Add hubcap
        const hubcapRadius = simulationParams.wheelRadius * 0.5
        const hubcapGeometry = new THREE.CylinderGeometry(hubcapRadius, hubcapRadius, simulationParams.wheelWidth+0.01, 32);
		const hubcapMaterial = new THREE.MeshPhongMaterial({color : 0xcccccc})//metallic silver
		const hubcap = new THREE.Mesh(hubcapGeometry,hubcapMaterial);
		hubcap.rotation.z = Math.PI / 2;
		wheel.add(hubcap);
		
        return wheel;
    }

    // Add wheels
	const wheelY = simulationParams.groundClearance + simulationParams.wheelRadius;
    const wheelZOffset = simulationParams.width/2 + simulationParams.wheelWidth/2;
    const wheelXOffset = simulationParams.length * 0.25
    const frontLeftWheel = createWheel(wheelXOffset, wheelY, wheelZOffset);
    const frontRightWheel = createWheel(wheelXOffset, wheelY, -wheelZOffset);
    const rearLeftWheel = createWheel(-wheelXOffset, wheelY, wheelZOffset);
    const rearRightWheel = createWheel(-wheelXOffset, wheelY, -wheelZOffset);
    carGroup.add(frontLeftWheel, frontRightWheel, rearLeftWheel, rearRightWheel);
	
    // Add the car group to the scene and store it as car
    car = carGroup;
    scene.add(car);
}



async function updateSimulation() {

        // Get current parameters
    const params = new URLSearchParams({
        length: simulationParams.length,
        height: simulationParams.height,
        width: simulationParams.width,
        speed: simulationParams.speed,
        groundClearance: simulationParams.groundClearance,
        hoodAngle: simulationParams.hoodAngle,
        rearAngle: simulationParams.rearAngle,
        wheelRadius: simulationParams.wheelRadius,
        wheelWidth: simulationParams.wheelWidth,
		airDensity: simulationParams.airDensity,
        temperature: simulationParams.temperature,
		dynamicViscosity: simulationParams.dynamicViscosity
    });
    
    try {
        const response = await fetch(`/simulation?${params}`);
        const data = await response.json();

        // Update visualization with new data
        updateCarGeometry();
       
        updateDataDisplay(data);
		
        
    } catch (error) {
        console.error('Error updating simulation:', error);
    }
}

function updateCarGeometry() {
    scene.remove(car);
    createCar();
}


function updateDataDisplay(data) {
    dragCoefficientDisplay.textContent = data.drag_coefficient.toFixed(3);
    liftForceDisplay.textContent = data.lift_force.toFixed(3);
	
	
    // Format pressure for display
    const avgPressure = data.pressure.flat().reduce((a, b) => a + b, 0) / data.pressure.flat().length;
    pressureDisplay.textContent = avgPressure.toFixed(2);


    velocityDisplay.textContent = simulationParams.speed.toFixed(1);
    reynoldsDisplay.textContent = data.reynolds_number.toFixed(0);
    airDensityDisplay.textContent = simulationParams.airDensity.toFixed(3);
	const tempInC = simulationParams.temperature
    temperatureDisplay.textContent = tempInC.toFixed(1);
	powerDisplay.textContent = data.power.toFixed(0);
}


function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
}



// Shader Setup
function initFluidSimulation() {
    resolution = new THREE.Vector2(256, 256); // Adjust resolution as needed
    
	// Create render Targets
     velocityRenderTarget = createRenderTarget();
     pressureRenderTarget = createRenderTarget();
	 divergenceRenderTarget = createRenderTarget();

	// Set the buffer with initial fluid velocity
    velocityBuffer = new THREE.DataTexture(
         new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
    );
	velocityBuffer.needsUpdate = true;
    
	pressureBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
	);
		
	divergenceBuffer  = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
	);

	

    // Initialize shaders
    initShaders();
}



function createRenderTarget() {
    return new THREE.WebGLRenderTarget(
        resolution.x,
        resolution.y,
        {
            wrapS: THREE.RepeatWrapping,
            wrapT: THREE.RepeatWrapping,
            minFilter: THREE.LinearFilter,
            magFilter: THREE.LinearFilter,
            format: THREE.RGBAFormat,
            type: THREE.FloatType,
             stencilBuffer: false
        }
    );
}

function initShaders() {


    // Velocity shader (Navier-Stokes)
    velocityShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            velocityTexture: { value: velocityRenderTarget.texture },
            deltaTime: {value : 0.01},
			viscosity: { value: simulationParams.dynamicViscosity},
			density: { value: simulationParams.airDensity},
			speed: {value : simulationParams.speed * 0.01},
			resolution : {value: resolution},
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
		    uniform sampler2D velocityTexture;
            uniform float deltaTime;
			uniform float viscosity;
			uniform float density;
			uniform float speed;
			uniform vec2 resolution;
			varying vec2 vUv;

			vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

			 // Function to get the velocity at a specific point
			vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }

           float getDivergence(vec2 uv){
			   vec2 texelSize = getTexelSize();
                float left = getVelocity(uv - vec2(texelSize.x,0.0)).x;
                float right = getVelocity(uv + vec2(texelSize.x,0.0)).x;
				float up = getVelocity(uv + vec2(0.0,texelSize.y)).y;
				float down = getVelocity(uv - vec2(0.0,texelSize.y)).y;
                return 0.5 * (right - left + up - down);
           }
 
            void main() {

				 vec2 currentVelocity = getVelocity(vUv);

                // Calculate the advection term
                vec2 texelSize = getTexelSize();
                vec2 prevPos = vUv - currentVelocity * deltaTime;
				
				
				// Check if the previous position is within the bounds
				vec2 clampedPos = clamp(prevPos, vec2(0.0), vec2(1.0));

				// Get advected velocity
				vec2 advectedVelocity = getVelocity(clampedPos);

                // Apply viscosity to diffuse the velocity field
				vec2 diffVel = vec2(0.0);
				
				float laplacian = getDivergence(vUv) * viscosity;
                
                diffVel = advectedVelocity + vec2(laplacian);
				
                gl_FragColor = vec4(diffVel, 0.0, 1.0);
            }
        `
    });
	
	
	 // divergence shader
    divergenceShaderMaterial =  new THREE.ShaderMaterial({
        uniforms: {
            velocityTexture: { value: velocityRenderTarget.texture},
			resolution : {value: resolution},
        },
		vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
		uniform sampler2D velocityTexture;
		uniform vec2 resolution;
		
		varying vec2 vUv;

		
		vec2 getTexelSize()
        {
            return 1.0/resolution;
        }
		
		// Function to get the velocity at a specific point
		vec2 getVelocity(vec2 uv) {
            return texture2D(velocityTexture, uv).xy;
        }

        void main() {
			vec2 texelSize = getTexelSize();
            float left = getVelocity(vUv - vec2(texelSize.x,0.0)).x;
            float right = getVelocity(vUv + vec2(texelSize.x,0.0)).x;
			float up = getVelocity(vUv + vec2(0.0,texelSize.y)).y;
			float down = getVelocity(vUv - vec2(0.0,texelSize.y)).y;
			
			float divergence = 0.5 * (right - left + up - down);
			
			gl_FragColor = vec4(divergence, 0.0, 0.0,1.0);
        }
        
        `
    });
	
    // Pressure shader (Poisson equation using Jacobi iteration)
    pressureShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            pressureTexture: { value: pressureRenderTarget.texture },
			divergenceTexture: { value: divergenceRenderTarget.texture },
            alpha: {value : -1.0},
			beta: {value: 0.25},
			resolution : {value: resolution},
			
        },
        vertexShader: `
             varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
		uniform sampler2D pressureTexture;
		uniform sampler2D divergenceTexture;
		uniform float alpha;
		uniform float beta;
		uniform vec2 resolution;
		varying vec2 vUv;
		
		vec2 getTexelSize()
        {
            return 1.0/resolution;
        }
		
		float getDivergence(vec2 uv){
			return texture2D(divergenceTexture,uv).r;
		} 
		
		float getPressure(vec2 uv){
			return texture2D(pressureTexture,uv).r;
		}
		
		void main() {
			vec2 texelSize = getTexelSize();
			float left = getPressure(vUv - vec2(texelSize.x,0.0));
			float right = getPressure(vUv + vec2(texelSize.x,0.0));
			float up = getPressure(vUv + vec2(0.0,texelSize.y));
			float down = getPressure(vUv - vec2(0.0,texelSize.y));
			
			float divergence = getDivergence(vUv);
		
            float pressure = (left + right + up + down + alpha * divergence )* beta;
            gl_FragColor = vec4(pressure, 0.0, 0.0, 1.0) ;
        }
        `
    });
}

function createQuad(){
	const geometry = new THREE.PlaneGeometry(2,2);
	quad = new THREE.Mesh(geometry);
	scene.add(quad);
}

function runFluidSimulation(){
	// 1. Calculate Divergence
		renderer.setRenderTarget(divergenceRenderTarget);
		renderer.render(scene, camera, divergenceRenderTarget);
		quad.material = divergenceShaderMaterial;
		renderer.render(scene, camera);


	// 2. Apply velocity Calculation
        quad.material = velocityShaderMaterial;
		renderer.setRenderTarget(velocityRenderTarget);
		renderer.render(scene, camera);
		

    //3. Calculate pressure
     let iteration = 20;
	 quad.material = pressureShaderMaterial;
	 for(let i=0 ; i< iteration; i++){
		renderer.setRenderTarget(pressureRenderTarget);
		renderer.render(scene, camera);
	  }
	  
    
	// Reset render target
    renderer.setRenderTarget(null);
}


function animate() {
    requestAnimationFrame(animate);
    controls.update();
    runFluidSimulation();
	renderer.render(scene, camera); // Render the scene after fluid calculation
  }


// Initialize the simulation
init();
C:\mygit\BLazy\repo\3dsim\static\js\shaders\carAeroShader.js
Language detected: javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';

let scene, camera, renderer, controls, gui;
let car, airflow, pressureField, carGroup;
let simulationParams = {
    length: 1.0,
    height: 0.5,
    width: 0.4,
    speed: 25,
    groundClearance: 0.1,
    hoodAngle: 15,
    rearAngle: 25,
    wheelRadius : 0.07,
    wheelWidth : 0.04,
	airDensity: 1.225, // kg/m^3
    temperature: 20, // °C
    dynamicViscosity: 1.81e-5 // kg/(m*s)
};

// Data display variables
let dragCoefficientDisplay, liftForceDisplay, pressureDisplay, velocityDisplay, reynoldsDisplay, airDensityDisplay, temperatureDisplay, powerDisplay;


// Shader-related variables
let velocityRenderTarget, pressureRenderTarget, divergenceRenderTarget, boundaryRenderTarget;
let velocityBuffer, pressureBuffer, divergenceBuffer, boundaryBuffer;
let velocityShaderMaterial, pressureShaderMaterial, advectionShaderMaterial, divergenceShaderMaterial, boundaryShaderMaterial, visualizationShaderMaterial;
let resolution;
let quad;
let visualizationPlane; //plane for the visualization

// Initialize the scene
function init() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);

    // Camera setup
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(2, 2, 2);

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);
	
	// GUI setup
	  gui = new GUI();
	  const carFolder = gui.addFolder('Car Parameters');
  
	  carFolder.add(simulationParams, 'length', 0.5, 2.0).name('Length').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'height', 0.2, 1.0).name('Height').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'width', 0.2, 0.8).name('Width').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelRadius', 0.03, 0.15).name('Wheel Radius').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelWidth', 0.02, 0.10).name('Wheel Width').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'groundClearance', 0, 0.3).name('Ground Clearance').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'hoodAngle', 0, 45).name('Hood Angle').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'rearAngle', 0, 45).name('Rear Angle').onChange(updateSimulation);
	  carFolder.open();
  
	  const airFolder = gui.addFolder('Air Parameters');
	  airFolder.add(simulationParams, 'airDensity', 0.5, 2.0).name('Air Density').onChange(updateSimulation);
	  airFolder.add(simulationParams, 'temperature', 0, 40).name('Temperature').onChange(updateSimulation);
	  airFolder.add(simulationParams,'speed',0, 100).name('Wind Speed').onChange(updateSimulation);
	  airFolder.open();

    // Controls setup
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);

    createCar();

	
	// Initialize Shader components
	initFluidSimulation();
	createQuad();
    createVisualizationPlane(); // create visualization plane
	
	// Initialize data display elements
	dragCoefficientDisplay = document.getElementById('drag-coefficient');
    liftForceDisplay = document.getElementById('lift-force');
    pressureDisplay = document.getElementById('pressure');
    velocityDisplay = document.getElementById('velocity');
    reynoldsDisplay = document.getElementById('reynolds');
    airDensityDisplay = document.getElementById('air-density');
    temperatureDisplay = document.getElementById('temperature');
	powerDisplay = document.getElementById('power');


    // Handle window resize
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function createCar() {
    // Remove existing car if it exists
     if (car) {
        scene.remove(car);
    }

    carGroup = new THREE.Group();

    // Car material
    const carMaterial = new THREE.MeshPhongMaterial({
        color: 0x156289,
        transparent: true,
        opacity: 0.8
    });

    // Function to create a rounded rectangle shape
    function createRoundedRectShape(width, height, radius) {
        const shape = new THREE.Shape();
        shape.moveTo(0, radius);
        shape.lineTo(0, height - radius);
        shape.quadraticCurveTo(0, height, radius, height);
        shape.lineTo(width - radius, height);
        shape.quadraticCurveTo(width, height, width, height - radius);
        shape.lineTo(width, radius);
        shape.quadraticCurveTo(width, 0, width - radius, 0);
        shape.lineTo(radius, 0);
        shape.quadraticCurveTo(0, 0, 0, radius);
        return shape;
    }
     // Create main body
    const bodyShape = createRoundedRectShape(
        simulationParams.length * 0.6,
        simulationParams.height * 0.6,
        simulationParams.height * 0.1
    );
    const bodyExtrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };
    const bodyGeometry = new THREE.ExtrudeGeometry(bodyShape, bodyExtrudeSettings);
    const bodyMesh = new THREE.Mesh(bodyGeometry, carMaterial);
    bodyMesh.position.y = simulationParams.groundClearance + simulationParams.height * 0.3;
    carGroup.add(bodyMesh);

    // Create hood (front section)
    const hoodShape = new THREE.Shape();
    const hoodLength = simulationParams.length * 0.2;
    const hoodHeight = simulationParams.height * 0.4;
    const hoodAngleRad = (simulationParams.hoodAngle * Math.PI) / 180;

    hoodShape.moveTo(0, 0);
    hoodShape.lineTo(hoodLength * Math.cos(hoodAngleRad), hoodHeight);
     hoodShape.lineTo(hoodLength,0);
    hoodShape.lineTo(0,0);
   
    const extrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };

    const hoodGeometry = new THREE.ExtrudeGeometry(hoodShape, extrudeSettings);
    const hoodMesh = new THREE.Mesh(hoodGeometry, carMaterial);
    hoodMesh.rotation.y = Math.PI / 2;
    hoodMesh.position.set(
        simulationParams.length * 0.3,
        simulationParams.groundClearance,
        simulationParams.width / 2
    );
    carGroup.add(hoodMesh);



    // Create rear section
    const rearShape = new THREE.Shape();
    const rearLength = simulationParams.length * 0.2;
	const rearHeight = simulationParams.height * 0.5;
    const rearAngleRad = (simulationParams.rearAngle * Math.PI) / 180;
    
    rearShape.moveTo(0, 0);
    rearShape.lineTo(0, rearHeight);
	rearShape.lineTo(rearLength * Math.cos(rearAngleRad),0);
    rearShape.lineTo(0, 0);

    const rearGeometry = new THREE.ExtrudeGeometry(rearShape, extrudeSettings);
    const rearMesh = new THREE.Mesh(rearGeometry, carMaterial);
    rearMesh.rotation.y = -Math.PI / 2;
    rearMesh.position.set(
        -simulationParams.length * 0.3,
        simulationParams.groundClearance,
        -simulationParams.width / 2
    );
     carGroup.add(rearMesh);
     
     // Create wheels
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x333333 });
    const wheelGeometry = new THREE.CylinderGeometry(simulationParams.wheelRadius, simulationParams.wheelRadius, simulationParams.wheelWidth, 32);

    //function to create wheel
     function createWheel(x, y, z) {
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, y, z);
		
        // Add hubcap
        const hubcapRadius = simulationParams.wheelRadius * 0.5
        const hubcapGeometry = new THREE.CylinderGeometry(hubcapRadius, hubcapRadius, simulationParams.wheelWidth+0.01, 32);
		const hubcapMaterial = new THREE.MeshPhongMaterial({color : 0xcccccc})//metallic silver
		const hubcap = new THREE.Mesh(hubcapGeometry,hubcapMaterial);
		hubcap.rotation.z = Math.PI / 2;
		wheel.add(hubcap);
		
        return wheel;
    }

    // Add wheels
	const wheelY = simulationParams.groundClearance + simulationParams.wheelRadius;
    const wheelZOffset = simulationParams.width/2 + simulationParams.wheelWidth/2;
    const wheelXOffset = simulationParams.length * 0.25
    const frontLeftWheel = createWheel(wheelXOffset, wheelY, wheelZOffset);
    const frontRightWheel = createWheel(wheelXOffset, wheelY, -wheelZOffset);
    const rearLeftWheel = createWheel(-wheelXOffset, wheelY, wheelZOffset);
    const rearRightWheel = createWheel(-wheelXOffset, wheelY, -wheelZOffset);
    carGroup.add(frontLeftWheel, frontRightWheel, rearLeftWheel, rearRightWheel);
	
    // Add the car group to the scene and store it as car
    car = carGroup;
    scene.add(car);
}

function createVisualizationPlane(){
    const planeGeometry = new THREE.PlaneGeometry(10,10);
    visualizationPlane = new THREE.Mesh(planeGeometry);
    visualizationPlane.rotation.x = -Math.PI / 2;
    visualizationPlane.position.set(0,0.01,0);
    scene.add(visualizationPlane);
}


async function updateSimulation() {

        // Get current parameters
    const params = new URLSearchParams({
        length: simulationParams.length,
        height: simulationParams.height,
        width: simulationParams.width,
        speed: simulationParams.speed,
        groundClearance: simulationParams.groundClearance,
        hoodAngle: simulationParams.hoodAngle,
        rearAngle: simulationParams.rearAngle,
        wheelRadius: simulationParams.wheelRadius,
        wheelWidth: simulationParams.wheelWidth,
		airDensity: simulationParams.airDensity,
        temperature: simulationParams.temperature,
		dynamicViscosity: simulationParams.dynamicViscosity
    });
    
    try {
        const response = await fetch(`/simulation?${params}`);
        const data = await response.json();

        // Update visualization with new data
        updateCarGeometry();
       
        updateDataDisplay(data);
		
        
    } catch (error) {
        console.error('Error updating simulation:', error);
    }
}

function updateCarGeometry() {
    scene.remove(car);
    createCar();
}


function updateDataDisplay(data) {
    dragCoefficientDisplay.textContent = data.drag_coefficient.toFixed(3);
    liftForceDisplay.textContent = data.lift_force.toFixed(3);
	
	
    // Format pressure for display
    const avgPressure = data.pressure.flat().reduce((a, b) => a + b, 0) / data.pressure.flat().length;
    pressureDisplay.textContent = avgPressure.toFixed(2);


    velocityDisplay.textContent = simulationParams.speed.toFixed(1);
    reynoldsDisplay.textContent = data.reynolds_number.toFixed(0);
    airDensityDisplay.textContent = simulationParams.airDensity.toFixed(3);
	const tempInC = simulationParams.temperature
    temperatureDisplay.textContent = tempInC.toFixed(1);
	powerDisplay.textContent = data.power.toFixed(0);
}


function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
}



// Shader Setup
function initFluidSimulation() {
    resolution = new THREE.Vector2(256, 256); // Adjust resolution as needed
    
	// Create render Targets
     velocityRenderTarget = createRenderTarget();
     pressureRenderTarget = createRenderTarget();
	 divergenceRenderTarget = createRenderTarget();
     boundaryRenderTarget = createRenderTarget();

	// Set the buffer with initial fluid velocity
    velocityBuffer = new THREE.DataTexture(
         new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
    );
	velocityBuffer.needsUpdate = true;
    
	pressureBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
	);
		
	divergenceBuffer  = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
	);

    boundaryBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
		resolution.x,
		resolution.y,
		THREE.RGBAFormat,
		THREE.FloatType
	);
    boundaryBuffer.needsUpdate = true;

	

    // Initialize shaders
    initShaders();
}



function createRenderTarget() {
    return new THREE.WebGLRenderTarget(
        resolution.x,
        resolution.y,
        {
            wrapS: THREE.RepeatWrapping,
            wrapT: THREE.RepeatWrapping,
            minFilter: THREE.LinearFilter,
            magFilter: THREE.LinearFilter,
            format: THREE.RGBAFormat,
            type: THREE.FloatType,
             stencilBuffer: false
        }
    );
}

function initShaders() {

    // Boundary shader
    boundaryShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
             resolution : {value: resolution},
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
        uniform vec2 resolution;
        varying vec2 vUv;

         vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

        void main(){
          vec2 texelSize = getTexelSize();
          vec4 boundary = vec4(0.0,0.0,0.0,1.0);
          if(vUv.x < texelSize.x || vUv.x> 1.0-texelSize.x|| vUv.y < texelSize.y || vUv.y > 1.0- texelSize.y){
            boundary = vec4(1.0,0.0,0.0,1.0);
          }
            
          gl_FragColor = boundary;
        }
        
        `
    });


    // Velocity shader (Navier-Stokes)
    velocityShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            velocityTexture: { value: velocityRenderTarget.texture },
            boundaryTexture: { value: boundaryRenderTarget.texture},
            deltaTime: {value : 0.01},
			viscosity: { value: simulationParams.dynamicViscosity},
			density: { value: simulationParams.airDensity},
			speed: {value : simulationParams.speed * 0.01},
			resolution : {value: resolution},
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
		    uniform sampler2D velocityTexture;
            uniform sampler2D boundaryTexture;
            uniform float deltaTime;
			uniform float viscosity;
			uniform float density;
			uniform float speed;
			uniform vec2 resolution;
			varying vec2 vUv;

			vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

			 // Function to get the velocity at a specific point
			vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }

             float getBoundary(vec2 uv) {
               return texture2D(boundaryTexture,uv).r;
            }

           float getDivergence(vec2 uv){
			   vec2 texelSize = getTexelSize();
                float left = getVelocity(uv - vec2(texelSize.x,0.0)).x;
                float right = getVelocity(uv + vec2(texelSize.x,0.0)).x;
				float up = getVelocity(uv + vec2(0.0,texelSize.y)).y;
				float down = getVelocity(uv - vec2(0.0,texelSize.y)).y;
                return 0.5 * (right - left + up - down);
           }
 
            void main() {

				 vec2 currentVelocity = getVelocity(vUv);
                  float isBoundary = getBoundary(vUv);

                // Calculate the advection term
                vec2 texelSize = getTexelSize();
                vec2 prevPos = vUv - currentVelocity * deltaTime;
				
				
				// Check if the previous position is within the bounds
				vec2 clampedPos = clamp(prevPos, vec2(0.0), vec2(1.0));


				// Get advected velocity
				vec2 advectedVelocity = getVelocity(clampedPos);

				// Apply external force (wind)
				vec2 force = vec2(speed,0.0) ;


                // Apply viscosity to diffuse the velocity field
				vec2 diffVel = vec2(0.0);
				
				float laplacian = getDivergence(vUv) * viscosity;
                
                diffVel = (advectedVelocity + vec2(laplacian));

                if(isBoundary > 0.0){
                    diffVel = vec2(0.0);
                } else {
                    diffVel = diffVel + force;
                }

                gl_FragColor = vec4(diffVel, 0.0, 1.0);
            }
        `
    });
	
	
	 // divergence shader
    divergenceShaderMaterial =  new THREE.ShaderMaterial({
        uniforms: {
            velocityTexture: { value: velocityRenderTarget.texture},
			boundaryTexture: { value: boundaryRenderTarget.texture},
			resolution : {value: resolution},
        },
		vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
		uniform sampler2D velocityTexture;
        uniform sampler2D boundaryTexture;
		uniform vec2 resolution;
		
		varying vec2 vUv;

		
		vec2 getTexelSize()
        {
            return 1.0/resolution;
        }
		
		// Function to get the velocity at a specific point
		vec2 getVelocity(vec2 uv) {
            return texture2D(velocityTexture, uv).xy;
        }

         float getBoundary(vec2 uv) {
             return texture2D(boundaryTexture,uv).r;
         }

        void main() {
			vec2 texelSize = getTexelSize();
            float left = getVelocity(vUv - vec2(texelSize.x,0.0)).x;
            float right = getVelocity(vUv + vec2(texelSize.x,0.0)).x;
			float up = getVelocity(vUv + vec2(0.0,texelSize.y)).y;
			float down = getVelocity(vUv - vec2(0.0,texelSize.y)).y;
			       float isBoundary = getBoundary(vUv);


			
			float divergence = 0.5 * (right - left + up - down);

             if(isBoundary > 0.0){
                    divergence = 0.0;
                }
			
			gl_FragColor = vec4(divergence, 0.0, 0.0,1.0);
        }
        
        `
    });
	
    // Pressure shader (Poisson equation using Jacobi iteration)
    pressureShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            pressureTexture: { value: pressureRenderTarget.texture },
			divergenceTexture: { value: divergenceRenderTarget.texture },
             boundaryTexture: { value: boundaryRenderTarget.texture},
            alpha: {value : -1.0},
			beta: {value: 0.25},
			resolution : {value: resolution},
			
        },
        vertexShader: `
             varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
		uniform sampler2D pressureTexture;
        uniform sampler2D boundaryTexture;
		uniform sampler2D divergenceTexture;
		uniform float alpha;
		uniform float beta;
		uniform vec2 resolution;
		varying vec2 vUv;
		
		vec2 getTexelSize()
        {
            return 1.0/resolution;
        }
		
		float getDivergence(vec2 uv){
			return texture2D(divergenceTexture,uv).r;
		} 
		
		float getPressure(vec2 uv){
			return texture2D(pressureTexture,uv).r;
		}
        float getBoundary(vec2 uv) {
             return texture2D(boundaryTexture,uv).r;
         }
		
		void main() {
            float isBoundary = getBoundary(vUv);
			vec2 texelSize = getTexelSize();
			float left = getPressure(vUv - vec2(texelSize.x,0.0));
			float right = getPressure(vUv + vec2(texelSize.x,0.0));
			float up = getPressure(vUv + vec2(0.0,texelSize.y));
			float down = getPressure(vUv - vec2(0.0,texelSize.y));
			
			float divergence = getDivergence(vUv);
		
            float pressure = (left + right + up + down + alpha * divergence )* beta;
            
             if(isBoundary > 0.0){
                 pressure = 0.0;
             }

            gl_FragColor = vec4(pressure, 0.0, 0.0, 1.0) ;
        }
        `
    });

    // Visualization shader to render fluid to the plane
    visualizationShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            velocityTexture : {value: velocityRenderTarget.texture},
            pressureTexture : {value: pressureRenderTarget.texture},
            resolution: {value : resolution}
        },
        vertexShader: `
            varying vec2 vUv;
             void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }

        `,
        fragmentShader: `
            uniform sampler2D velocityTexture;
            uniform sampler2D pressureTexture;
              uniform vec2 resolution;
            varying vec2 vUv;

            vec2 getTexelSize()
            {
                return 1.0/resolution;
            }


             // Function to get the velocity at a specific point
            vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }

            float getPressure(vec2 uv){
                return texture2D(pressureTexture,uv).r;
            }




            void main(){
                 vec2 velocity =   getVelocity(vUv);
                float pressure =  getPressure(vUv);


             // Convert velocity to color
                vec3 velColor = vec3(0.0);
                float velMag = length(velocity);   
                 velColor.r = clamp(velMag * 1.0, 0.0, 1.0) ;


                  vec3 pressureColor = vec3(0.0);
               
                pressureColor.b =  clamp(pressure , 0.0, 1.0) ;
                 pressureColor.r = 1.0 - clamp(pressure * 10.0, 0.0, 1.0);


                gl_FragColor =  vec4(velColor + pressureColor, 1.0) ;
            }
        `

    });
}

function createQuad(){
	const geometry = new THREE.PlaneGeometry(2,2);
	quad = new THREE.Mesh(geometry);
	scene.add(quad);
}

function runFluidSimulation(){

    // 0. Apply Boundary Conditions
     quad.material = boundaryShaderMaterial;
     renderer.setRenderTarget(boundaryRenderTarget);
     renderer.render(scene, camera);

	// 1. Calculate Divergence
		renderer.setRenderTarget(divergenceRenderTarget);
		quad.material = divergenceShaderMaterial;
		renderer.render(scene, camera);


	// 2. Apply velocity Calculation
        quad.material = velocityShaderMaterial;
		renderer.setRenderTarget(velocityRenderTarget);
		renderer.render(scene, camera);
		

    //3. Calculate pressure
     let iteration = 20; // Number of jacobi iterations
	 quad.material = pressureShaderMaterial;
	 for(let i=0 ; i< iteration; i++){
		renderer.setRenderTarget(pressureRenderTarget);
		renderer.render(scene, camera);
	  }
	  
    
	// Reset render target
    renderer.setRenderTarget(null);

    //Apply visualization
    visualizationPlane.material = visualizationShaderMaterial;
    visualizationShaderMaterial.uniforms.velocityTexture.value = velocityRenderTarget.texture;
     visualizationShaderMaterial.uniforms.pressureTexture.value = pressureRenderTarget.texture;


}


function animate() {
    requestAnimationFrame(animate);
    controls.update();
    runFluidSimulation();
	renderer.render(scene, camera); // Render the scene after fluid calculation
  }


// Initialize the simulation
init();
C:\mygit\BLazy\repo\3dsim\templates\index.html
Language detected: html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Car Aerodynamics Simulation</title>
    <style>
        body { margin: 0; overflow: hidden; }
        #canvas-container { position: absolute; top: 0; left: 0; width: 80%; height: 100%; }
        #stats-container {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: rgba(255, 255, 255, 0.8);
            padding: 10px;
            border-radius: 5px;
            z-index: 1;
            width: 18%;
              font-family: Arial, sans-serif;
        }

        #stats-container p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div id="canvas-container"></div>
    <div id="stats-container">
        <p><strong>Drag Coefficient:</strong> <span id="drag-coefficient">0.00</span></p>
        <p><strong>Lift Force:</strong> <span id="lift-force">0.00</span> N</p>
        <p><strong>Average Pressure:</strong> <span id="pressure">0.00</span> Pa</p>
		<p><strong>Velocity:</strong> <span id="velocity">0.0</span> m/s</p>
        <p><strong>Reynolds Number:</strong> <span id="reynolds">0</span></p>
		<p><strong>Air Density:</strong> <span id="air-density">1.225</span> kg/m3</p>
        <p><strong>Temperature:</strong> <span id="temperature">20</span> °C</p>
		 <p><strong>Power:</strong> <span id="power">0</span> W</p>
    </div>

    <script type="module" src="/static/js/shaders/carAeroShader.js"></script>
</body>
</html>
C:\mygit\BLazy\repo\3dsim\static\js\carGeometry.js
Language detected: javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';

let scene, camera, renderer, controls, gui;
let car, airflow, pressureField, carGroup;
let simulationParams = {
    length: 1.0,
    height: 0.5,
    width: 0.4,
    speed: 25,
    groundClearance: 0.1,
    hoodAngle: 15,
    rearAngle: 25,
    wheelRadius : 0.07,
    wheelWidth : 0.04,
	airDensity: 1.225, // kg/m^3
    temperature: 20, // °C
    dynamicViscosity: 1.81e-5 // kg/(m*s)
};

// Data display variables
let dragCoefficientDisplay, liftForceDisplay, pressureDisplay, velocityDisplay, reynoldsDisplay, airDensityDisplay, temperatureDisplay, powerDisplay;

// Initialize the scene
function init() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);

    // Camera setup
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(2, 2, 2);

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    // GUI setup
    gui = new GUI();
    const carFolder = gui.addFolder('Car Parameters');

    carFolder.add(simulationParams, 'length', 0.5, 2.0).name('Length').onChange(updateSimulation);
    carFolder.add(simulationParams, 'height', 0.2, 1.0).name('Height').onChange(updateSimulation);
    carFolder.add(simulationParams, 'width', 0.2, 0.8).name('Width').onChange(updateSimulation);
    carFolder.add(simulationParams, 'wheelRadius', 0.03, 0.15).name('Wheel Radius').onChange(updateSimulation);
    carFolder.add(simulationParams, 'wheelWidth', 0.02, 0.10).name('Wheel Width').onChange(updateSimulation);
    carFolder.add(simulationParams, 'groundClearance', 0, 0.3).name('Ground Clearance').onChange(updateSimulation);
    carFolder.add(simulationParams, 'hoodAngle', 0, 45).name('Hood Angle').onChange(updateSimulation);
    carFolder.add(simulationParams, 'rearAngle', 0, 45).name('Rear Angle').onChange(updateSimulation);
    carFolder.open();

    const airFolder = gui.addFolder('Air Parameters');
    airFolder.add(simulationParams, 'airDensity', 0.5, 2.0).name('Air Density').onChange(updateSimulation);
    airFolder.add(simulationParams, 'temperature', 0, 40).name('Temperature').onChange(updateSimulation);
    airFolder.add(simulationParams, 'speed', 0, 100).name('Wind Speed').onChange(updateSimulation);
    airFolder.open();

    // Controls setup
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);

    createCar();
    createAirflow();

    // Initialize data display elements
    dragCoefficientDisplay = document.getElementById('drag-coefficient');
    liftForceDisplay = document.getElementById('lift-force');
    pressureDisplay = document.getElementById('pressure');
    velocityDisplay = document.getElementById('velocity');
    reynoldsDisplay = document.getElementById('reynolds');
    airDensityDisplay = document.getElementById('air-density');
    temperatureDisplay = document.getElementById('temperature');
    powerDisplay = document.getElementById('power');


    // Handle window resize
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function createCar() {
    // Remove existing car if it exists
    if (car) {
        scene.remove(car);
    }

    carGroup = new THREE.Group();

    // Car material
    const carMaterial = new THREE.MeshPhongMaterial({
        color: 0x156289,
        transparent: true,
        opacity: 0.8
    });

  // Function to create a Bezier curve
    function createBezierCurve(start, control1, control2, end, segments) {
        const curve = new THREE.CubicBezierCurve(
            new THREE.Vector2(start.x, start.y),
            new THREE.Vector2(control1.x, control1.y),
            new THREE.Vector2(control2.x, control2.y),
            new THREE.Vector2(end.x, end.y)
        );
        return curve.getPoints(segments);
    }
    // Function to create a rounded rectangle shape
     function createRoundedRectShape(width, height, radius) {
        const shape = new THREE.Shape();
        shape.moveTo(0, radius);
        shape.lineTo(0, height - radius);
        shape.quadraticCurveTo(0, height, radius, height);
        shape.lineTo(width - radius, height);
        shape.quadraticCurveTo(width, height, width, height - radius);
        shape.lineTo(width, radius);
        shape.quadraticCurveTo(width, 0, width - radius, 0);
         shape.lineTo(radius, 0);
        shape.quadraticCurveTo(0, 0, 0, radius);
       return shape;
     }


    // Main body (using Bezier curve for top)
    const bodyWidth = simulationParams.length * 0.6;
    const bodyHeight = simulationParams.height * 0.6;

    const bodyShape = createRoundedRectShape(bodyWidth,bodyHeight,bodyHeight*0.1);
    const bodyExtrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };
    const bodyGeometry = new THREE.ExtrudeGeometry(bodyShape, bodyExtrudeSettings);
     const bodyMesh = new THREE.Mesh(bodyGeometry, carMaterial);
    bodyMesh.position.y = simulationParams.groundClearance + bodyHeight/2;
     carGroup.add(bodyMesh);

   // Create hood (front section)
    const hoodShape = new THREE.Shape();
    const hoodLength = simulationParams.length * 0.2;
    const hoodHeight = simulationParams.height * 0.4;
    const hoodAngleRad = (simulationParams.hoodAngle * Math.PI) / 180;

      hoodShape.moveTo(0, 0);
    hoodShape.lineTo(hoodLength * Math.cos(hoodAngleRad), hoodHeight);
    hoodShape.lineTo(hoodLength,0);
     hoodShape.lineTo(0,0);
   
    const extrudeSettings = {
         steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
     };

     const hoodGeometry = new THREE.ExtrudeGeometry(hoodShape, extrudeSettings);
    const hoodMesh = new THREE.Mesh(hoodGeometry, carMaterial);
     hoodMesh.rotation.y = Math.PI / 2;
    hoodMesh.position.set(
         simulationParams.length * 0.3,
       simulationParams.groundClearance,
       simulationParams.width / 2
     );
    carGroup.add(hoodMesh);


   // Create rear section
      const rearShape = new THREE.Shape();
      const rearLength = simulationParams.length * 0.2;
	  const rearHeight = simulationParams.height * 0.5;
      const rearAngleRad = (simulationParams.rearAngle * Math.PI) / 180;
    
       rearShape.moveTo(0, 0);
       rearShape.lineTo(0, rearHeight);
		rearShape.lineTo(rearLength * Math.cos(rearAngleRad),0);
       rearShape.lineTo(0, 0);

     const rearGeometry = new THREE.ExtrudeGeometry(rearShape, extrudeSettings);
     const rearMesh = new THREE.Mesh(rearGeometry, carMaterial);
     rearMesh.rotation.y = -Math.PI / 2;
     rearMesh.position.set(
         -simulationParams.length * 0.3,
       simulationParams.groundClearance,
       -simulationParams.width / 2
     );
    carGroup.add(rearMesh);



    // Create wheels
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x333333 });
    const wheelGeometry = new THREE.CylinderGeometry(simulationParams.wheelRadius, simulationParams.wheelRadius, simulationParams.wheelWidth, 32);

    //function to create wheel
    function createWheel(x, y, z) {
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, y, z);
		
        // Add hubcap
        const hubcapRadius = simulationParams.wheelRadius * 0.5
        const hubcapGeometry = new THREE.CylinderGeometry(hubcapRadius, hubcapRadius, simulationParams.wheelWidth+0.01, 32);
		const hubcapMaterial = new THREE.MeshPhongMaterial({color : 0xcccccc})//metallic silver
		const hubcap = new THREE.Mesh(hubcapGeometry,hubcapMaterial);
		hubcap.rotation.z = Math.PI / 2;
		wheel.add(hubcap);
		
        return wheel;
    }

    // Add wheels
	const wheelY = simulationParams.groundClearance + simulationParams.wheelRadius;
    const wheelZOffset = simulationParams.width/2 + simulationParams.wheelWidth/2;
    const wheelXOffset = simulationParams.length * 0.25
    const frontLeftWheel = createWheel(wheelXOffset, wheelY, wheelZOffset);
    const frontRightWheel = createWheel(wheelXOffset, wheelY, -wheelZOffset);
    const rearLeftWheel = createWheel(-wheelXOffset, wheelY, wheelZOffset);
    const rearRightWheel = createWheel(-wheelXOffset, wheelY, -wheelZOffset);
    carGroup.add(frontLeftWheel, frontRightWheel, rearLeftWheel, rearRightWheel);
	
    // Add the car group to the scene and store it as car
    car = carGroup;
    scene.add(car);
}


function createAirflow() {
    // Create particle system for airflow visualization
    const particleCount = 2000;
    const particles = new THREE.BufferGeometry();
    const positions = [];
    const velocities = [];

    // Create initial particle positions in a grid pattern
    const spacing = 0.2;
    const xStart = -5;
    const yRange = 2;
    const zRange = 2;

    for (let x = xStart; x < 5; x += spacing) {
        for (let y = -yRange; y < yRange; y += spacing) {
            for (let z = -zRange; z < zRange; z += spacing) {
                positions.push(x, y, z);
                // Initial velocity (will be modified based on car shape)
                velocities.push(simulationParams.speed * 0.01, 0, 0);
            }
        }
    }

    particles.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    particles.userData = { velocities: velocities };

    const particleMaterial = new THREE.PointsMaterial({
        color: 0x00ff00,
        size: 0.03,
        transparent: true,
        opacity: 0.6
    });

    airflow = new THREE.Points(particles, particleMaterial);
    scene.add(airflow);
}

async function updateSimulation() {

    // Get current parameters
    const params = new URLSearchParams({
        length: simulationParams.length,
        height: simulationParams.height,
        width: simulationParams.width,
        speed: simulationParams.speed,
        groundClearance: simulationParams.groundClearance,
        hoodAngle: simulationParams.hoodAngle,
        rearAngle: simulationParams.rearAngle,
        wheelRadius: simulationParams.wheelRadius,
        wheelWidth: simulationParams.wheelWidth,
		airDensity: simulationParams.airDensity,
        temperature: simulationParams.temperature,
		dynamicViscosity: simulationParams.dynamicViscosity
    });

    try {
        const response = await fetch(`/simulation?${params}`);
        const data = await response.json();

        // Update visualization with new data
        updateCarGeometry();
       // updateAirflowVisualization(data);   Commented this out for now.
    //   updatePressureField(data)
		
		// Update data display
		updateDataDisplay(data);

    } catch (error) {
        console.error('Error updating simulation:', error);
    }
}


function updateCarGeometry() {
    scene.remove(car);
    createCar();
}


function updateAirflowVisualization(data) {
    const positions = airflow.geometry.attributes.position.array;
    const velocities = airflow.geometry.userData.velocities;
    const particleCount = positions.length / 3;

    // Car dimensions for collision detection
    const carBounds = {
        front: simulationParams.length * 0.3,
        back: -simulationParams.length * 0.3,
        top: simulationParams.height + simulationParams.groundClearance,
        bottom: simulationParams.groundClearance,
        right: simulationParams.width / 2,
        left: -simulationParams.width / 2
    };

    const hoodAngleRad = (simulationParams.hoodAngle * Math.PI) / 180;
    const rearAngleRad = (simulationParams.rearAngle * Math.PI) / 180;

    for (let i = 0; i < particleCount; i++) {
        const idx = i * 3;
        const x = positions[idx];
        const y = positions[idx + 1];
        const z = positions[idx + 2];

        // Check if particle is near the car
        if (x >= carBounds.back && x <= carBounds.front &&
            y >= carBounds.bottom && y <= carBounds.top &&
            z >= carBounds.left && z <= carBounds.right) {

            // Front hood deflection
            if (x > 0) {
                const hoodY = simulationParams.groundClearance + 
                    (x / carBounds.front) * simulationParams.height * 0.4;
                if (y < hoodY) {
                    velocities[idx + 1] = Math.abs(velocities[idx]) * Math.sin(hoodAngleRad);
                    velocities[idx] *= Math.cos(hoodAngleRad);
                }
            }
            // Rear deflection
            else if (x < 0) {
                const rearY = simulationParams.groundClearance + 
                    (1 + x / carBounds.back) * simulationParams.height * 0.5;
                if (y < rearY) {
                    velocities[idx + 1] = -Math.abs(velocities[idx]) * Math.sin(rearAngleRad);
                    velocities[idx] *= Math.cos(rearAngleRad);
                }
            }

            // Ground effect
            if (y < carBounds.bottom + 0.1) {
                velocities[idx + 1] = Math.abs(velocities[idx + 1]);
            }
             // Side deflection
            if (Math.abs(z) > carBounds.right * 0.8) {
                velocities[idx + 2] = Math.sign(z) * Math.abs(velocities[idx]) * 0.3;
            }
        }

        // Apply velocities
        positions[idx] += velocities[idx];
        positions[idx + 1] += velocities[idx + 1];
        positions[idx + 2] += velocities[idx + 2];

         // Gradually restore horizontal flow
        velocities[idx + 1] *= 0.98;
        velocities[idx + 2] *= 0.98;

        // Reset particles that go too far
        if (positions[idx] > 5) {
            positions[idx] = -5;
            positions[idx + 1] = Math.random() * 4 - 2;
            positions[idx + 2] = Math.random() * 4 - 2;
            velocities[idx] = simulationParams.speed * 0.01;
            velocities[idx + 1] = 0;
            velocities[idx + 2] = 0;
        }
    }

    airflow.geometry.attributes.position.needsUpdate = true;
}


function updatePressureField(data) {
    // Remove existing pressure field if it exists
    if (pressureField) {
        scene.remove(pressureField);
    }

    // Create visualization of pressure field using points with colors
    const geometry = new THREE.BufferGeometry();
    const positions = [];
    const colors = [];

    const pressureMin = Math.min(...data.pressure.flat());
    const pressureMax = Math.max(...data.pressure.flat());

    for (let i = 0; i < data.x_coords.length; i++) {
        for (let j = 0; j < data.x_coords[i].length; j++) {
            positions.push(
                data.x_coords[i][j],
                data.y_coords[i][j],
                0
            );

            // Color based on pressure (blue to red)
            const pressure = data.pressure[i][j];
            const t = (pressure - pressureMin) / (pressureMax - pressureMin);
            const color = new THREE.Color();
            color.setHSL(0.7 * (1 - t), 1, 0.5);
            colors.push(color.r, color.g, color.b);
        }
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
        size: 0.05,
        vertexColors: true,
        transparent: true,
        opacity: 0.6
    });

    pressureField = new THREE.Points(geometry, material);
    scene.add(pressureField);
}


function updateDataDisplay(data) {
    dragCoefficientDisplay.textContent = data.drag_coefficient.toFixed(3);
    liftForceDisplay.textContent = data.lift_force.toFixed(3);
	
	
    // Format pressure for display
    const avgPressure = data.pressure.flat().reduce((a, b) => a + b, 0) / data.pressure.flat().length;
    pressureDisplay.textContent = avgPressure.toFixed(2);


    velocityDisplay.textContent = simulationParams.speed.toFixed(1);
    reynoldsDisplay.textContent = data.reynolds_number.toFixed(0);
    airDensityDisplay.textContent = simulationParams.airDensity.toFixed(3);
	const tempInC = simulationParams.temperature
    temperatureDisplay.textContent = tempInC.toFixed(1);
	powerDisplay.textContent = data.power.toFixed(0);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
      
    // Animate airflow particles (if used)
    if (airflow) {
         const positions = airflow.geometry.attributes.position.array;
        const particleCount = positions.length / 3;
       
        
        for (let i = 0; i < particleCount; i++) {
            const idx = i * 3;
             positions[idx] += simulationParams.speed * 0.001;
           
            if (positions[idx] > 5) {
                positions[idx] = -5;
           }
         }
         airflow.geometry.attributes.position.needsUpdate = true;
    }


    renderer.render(scene, camera);
}

// Initialize the simulation
init();
C:\mygit\BLazy\repo\3dsim\static\js\fluidDynamics.js
Language detected: javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';

let scene, camera, renderer, controls, gui;
let car, airflow, pressureField, carGroup;
let simulationParams = {
    length: 1.0,
    height: 0.5,
    width: 0.4,
    speed: 25,
    groundClearance: 0.1,
    hoodAngle: 15,
    rearAngle: 25,
    wheelRadius : 0.07,
    wheelWidth : 0.04,
	airDensity: 1.225, // kg/m^3
    temperature: 20, // °C
    dynamicViscosity: 1.81e-5 // kg/(m*s)
};

// Data display variables
let dragCoefficientDisplay, liftForceDisplay, pressureDisplay, velocityDisplay, reynoldsDisplay, airDensityDisplay, temperatureDisplay, powerDisplay;


// Shader-related variables
let velocityRenderTarget, pressureRenderTarget, divergenceRenderTarget, boundaryRenderTarget;
let velocityBuffer, pressureBuffer, divergenceBuffer, boundaryBuffer, obstacleBuffer;
let velocityShaderMaterial, pressureShaderMaterial, advectionShaderMaterial, divergenceShaderMaterial, boundaryShaderMaterial, visualizationShaderMaterial, obstacleShaderMaterial;
let resolution;
let quad;
let visualizationPlane; //plane for the visualization

// Initialize the scene
function init() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);

    // Camera setup
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(2, 2, 2);

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);
	
	// GUI setup
	  gui = new GUI();
	  const carFolder = gui.addFolder('Car Parameters');
  
	  carFolder.add(simulationParams, 'length', 0.5, 2.0).name('Length').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'height', 0.2, 1.0).name('Height').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'width', 0.2, 0.8).name('Width').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelRadius', 0.03, 0.15).name('Wheel Radius').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelWidth', 0.02, 0.10).name('Wheel Width').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'groundClearance', 0, 0.3).name('Ground Clearance').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'hoodAngle', 0, 45).name('Hood Angle').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'rearAngle', 0, 45).name('Rear Angle').onChange(updateSimulation);
	  carFolder.open();
  
	  const airFolder = gui.addFolder('Air Parameters');
	  airFolder.add(simulationParams, 'airDensity', 0.5, 2.0).name('Air Density').onChange(updateSimulation);
	  airFolder.add(simulationParams, 'temperature', 0, 40).name('Temperature').onChange(updateSimulation);
	  airFolder.add(simulationParams,'speed',0, 100).name('Wind Speed').onChange(updateSimulation);
	  airFolder.open();

    // Controls setup
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);

    createCar();

	
	// Initialize Shader components
	initFluidSimulation();
	createQuad();
    createVisualizationPlane(); // create visualization plane
	
	// Initialize data display elements
	dragCoefficientDisplay = document.getElementById('drag-coefficient');
    liftForceDisplay = document.getElementById('lift-force');
    pressureDisplay = document.getElementById('pressure');
    velocityDisplay = document.getElementById('velocity');
    reynoldsDisplay = document.getElementById('reynolds');
    airDensityDisplay = document.getElementById('air-density');
    temperatureDisplay = document.getElementById('temperature');
	powerDisplay = document.getElementById('power');


    // Handle window resize
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function createCar() {
    // Remove existing car if it exists
     if (car) {
        scene.remove(car);
    }

    carGroup = new THREE.Group();

    // Car material
    const carMaterial = new THREE.MeshPhongMaterial({
        color: 0x156289,
        transparent: true,
        opacity: 0.8
    });

    // Function to create a rounded rectangle shape
    function createRoundedRectShape(width, height, radius) {
        const shape = new THREE.Shape();
        shape.moveTo(0, radius);
        shape.lineTo(0, height - radius);
        shape.quadraticCurveTo(0, height, radius, height);
        shape.lineTo(width - radius, height);
        shape.quadraticCurveTo(width, height, width, height - radius);
        shape.lineTo(width, radius);
        shape.quadraticCurveTo(width, 0, width - radius, 0);
        shape.lineTo(radius, 0);
        shape.quadraticCurveTo(0, 0, 0, radius);
        return shape;
    }
     // Create main body
    const bodyShape = createRoundedRectShape(
        simulationParams.length * 0.6,
        simulationParams.height * 0.6,
        simulationParams.height * 0.1
    );
    const bodyExtrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };
    const bodyGeometry = new THREE.ExtrudeGeometry(bodyShape, bodyExtrudeSettings);
    const bodyMesh = new THREE.Mesh(bodyGeometry, carMaterial);
    bodyMesh.position.y = simulationParams.groundClearance + simulationParams.height * 0.3;
    carGroup.add(bodyMesh);

    // Create hood (front section)
    const hoodShape = new THREE.Shape();
    const hoodLength = simulationParams.length * 0.2;
    const hoodHeight = simulationParams.height * 0.4;
    const hoodAngleRad = (simulationParams.hoodAngle * Math.PI) / 180;

    hoodShape.moveTo(0, 0);
    hoodShape.lineTo(hoodLength * Math.cos(hoodAngleRad), hoodHeight);
     hoodShape.lineTo(hoodLength,0);
    hoodShape.lineTo(0,0);
   
    const extrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };

    const hoodGeometry = new THREE.ExtrudeGeometry(hoodShape, extrudeSettings);
    const hoodMesh = new THREE.Mesh(hoodGeometry, carMaterial);
    hoodMesh.rotation.y = Math.PI / 2;
    hoodMesh.position.set(
        simulationParams.length * 0.3,
        simulationParams.groundClearance,
        simulationParams.width / 2
    );
    carGroup.add(hoodMesh);



    // Create rear section
    const rearShape = new THREE.Shape();
    const rearLength = simulationParams.length * 0.2;
	const rearHeight = simulationParams.height * 0.5;
    const rearAngleRad = (simulationParams.rearAngle * Math.PI) / 180;
    
    rearShape.moveTo(0, 0);
    rearShape.lineTo(0, rearHeight);
	rearShape.lineTo(rearLength * Math.cos(rearAngleRad),0);
    rearShape.lineTo(0, 0);

    const rearGeometry = new THREE.ExtrudeGeometry(rearShape, extrudeSettings);
    const rearMesh = new THREE.Mesh(rearGeometry, carMaterial);
    rearMesh.rotation.y = -Math.PI / 2;
    rearMesh.position.set(
        -simulationParams.length * 0.3,
        simulationParams.groundClearance,
        -simulationParams.width / 2
    );
     carGroup.add(rearMesh);
     
     // Create wheels
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x333333 });
    const wheelGeometry = new THREE.CylinderGeometry(simulationParams.wheelRadius, simulationParams.wheelRadius, simulationParams.wheelWidth, 32);

    //function to create wheel
     function createWheel(x, y, z) {
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, y, z);
		
        // Add hubcap
        const hubcapRadius = simulationParams.wheelRadius * 0.5
        const hubcapGeometry = new THREE.CylinderGeometry(hubcapRadius, hubcapRadius, simulationParams.wheelWidth+0.01, 32);
		const hubcapMaterial = new THREE.MeshPhongMaterial({color : 0xcccccc})//metallic silver
		const hubcap = new THREE.Mesh(hubcapGeometry,hubcapMaterial);
		hubcap.rotation.z = Math.PI / 2;
		wheel.add(hubcap);
		
        return wheel;
    }

    // Add wheels
	const wheelY = simulationParams.groundClearance + simulationParams.wheelRadius;
    const wheelZOffset = simulationParams.width/2 + simulationParams.wheelWidth/2;
    const wheelXOffset = simulationParams.length * 0.25
    const frontLeftWheel = createWheel(wheelXOffset, wheelY, wheelZOffset);
    const frontRightWheel = createWheel(wheelXOffset, wheelY, -wheelZOffset);
    const rearLeftWheel = createWheel(-wheelXOffset, wheelY, wheelZOffset);
    const rearRightWheel = createWheel(-wheelXOffset, wheelY, -wheelZOffset);
    carGroup.add(frontLeftWheel, frontRightWheel, rearLeftWheel, rearRightWheel);
	
    // Add the car group to the scene and store it as car
    car = carGroup;
    scene.add(car);
}

function createVisualizationPlane(){
    const planeGeometry = new THREE.PlaneGeometry(10,10);
    visualizationPlane = new THREE.Mesh(planeGeometry);
    visualizationPlane.rotation.x = -Math.PI / 2;
    visualizationPlane.position.set(0,0.01,0);
    scene.add(visualizationPlane);
}


async function updateSimulation() {

        // Get current parameters
    const params = new URLSearchParams({
        length: simulationParams.length,
        height: simulationParams.height,
        width: simulationParams.width,
        speed: simulationParams.speed,
        groundClearance: simulationParams.groundClearance,
        hoodAngle: simulationParams.hoodAngle,
        rearAngle: simulationParams.rearAngle,
        wheelRadius: simulationParams.wheelRadius,
        wheelWidth: simulationParams.wheelWidth,
		airDensity: simulationParams.airDensity,
        temperature: simulationParams.temperature,
		dynamicViscosity: simulationParams.dynamicViscosity
    });
    
    try {
        const response = await fetch(`/simulation?${params}`);
        const data = await response.json();

        // Update visualization with new data
        updateCarGeometry();
       
        updateDataDisplay(data);
		
        
    } catch (error) {
        console.error('Error updating simulation:', error);
    }
}

function updateCarGeometry() {
    scene.remove(car);
    createCar();
	createObstacleField() //recreate obstacle buffer when car geometry changes
}


function updateDataDisplay(data) {
    dragCoefficientDisplay.textContent = data.drag_coefficient.toFixed(3);
    liftForceDisplay.textContent = data.lift_force.toFixed(3);
	
	
    // Format pressure for display
    const avgPressure = data.pressure.flat().reduce((a, b) => a + b, 0) / data.pressure.flat().length;
    pressureDisplay.textContent = avgPressure.toFixed(2);


    velocityDisplay.textContent = simulationParams.speed.toFixed(1);
    reynoldsDisplay.textContent = data.reynolds_number.toFixed(0);
    airDensityDisplay.textContent = simulationParams.airDensity.toFixed(3);
	const tempInC = simulationParams.temperature
    temperatureDisplay.textContent = tempInC.toFixed(1);
	powerDisplay.textContent = data.power.toFixed(0);
}


function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
}



// Shader Setup
function initFluidSimulation() {
    resolution = new THREE.Vector2(256, 256); // Adjust resolution as needed
    
	// Create render Targets
     velocityRenderTarget = createRenderTarget();
     pressureRenderTarget = createRenderTarget();
	 divergenceRenderTarget = createRenderTarget();
     boundaryRenderTarget = createRenderTarget();

    //Obstacle buffer
     obstacleBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
		resolution.x,
		resolution.y,
		THREE.RGBAFormat,
		THREE.FloatType
	);
    obstacleBuffer.needsUpdate = true;

	// Set the buffer with initial fluid velocity
    velocityBuffer = new THREE.DataTexture(
         new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
    );
	velocityBuffer.needsUpdate = true;
    
	pressureBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
	);
		
	divergenceBuffer  = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
	);

    boundaryBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
		resolution.x,
		resolution.y,
		THREE.RGBAFormat,
		THREE.FloatType
	);
    boundaryBuffer.needsUpdate = true;

	

    // Initialize shaders
    initShaders();
	createObstacleField();
}



function createRenderTarget() {
    return new THREE.WebGLRenderTarget(
        resolution.x,
        resolution.y,
        {
            wrapS: THREE.RepeatWrapping,
            wrapT: THREE.RepeatWrapping,
            minFilter: THREE.LinearFilter,
            magFilter: THREE.LinearFilter,
            format: THREE.RGBAFormat,
            type: THREE.FloatType,
             stencilBuffer: false
        }
    );
}

function initShaders() {

    // Obstacle shader
     obstacleShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
             resolution : {value: resolution},
              carDimensions: { value: new THREE.Vector3(simulationParams.length, simulationParams.height, simulationParams.width) },
            carPosition: { value: new THREE.Vector3(0, simulationParams.groundClearance, 0) },
              hoodAngle : { value:  simulationParams.hoodAngle * Math.PI / 180},
              rearAngle : { value: simulationParams.rearAngle * Math.PI / 180},

        },
         vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
         fragmentShader: `
             uniform vec2 resolution;
            uniform vec3 carDimensions;
            uniform vec3 carPosition;
             uniform float hoodAngle;
            uniform float rearAngle;


            varying vec2 vUv;

            vec2 getTexelSize()
            {
              return 1.0/resolution;
            }

            bool isInsideCar(vec2 uv){
              vec2 texelSize = getTexelSize();
              // Transform uv coordinates to world coordinates (-5 to 5 range)
              vec2 worldUV = (uv * 10.0) - 5.0 ; //scale up for the size of simulation


                // Car bounds
               float carFront = carPosition.x + carDimensions.x * 0.3;
              float carBack = carPosition.x - carDimensions.x * 0.3;
              float carTop = carPosition.y + carDimensions.y;
              float carBottom = carPosition.y;
             float carRight = carPosition.z + carDimensions.z/2.0;
            float carLeft = carPosition.z - carDimensions.z/2.0;



               // Check bounding box first
              if (worldUV.x >= carBack && worldUV.x <= carFront &&
                worldUV.y >= carBottom && worldUV.y <=carTop &&
               worldUV.y   >= carBottom && worldUV.y <= carTop &&
                  worldUV.x >= carLeft && worldUV.x <= carRight ){
                   //then check front and rear
                    float hoodY = carPosition.y + 
                           (worldUV.x / (carDimensions.x * 0.3)) * carDimensions.y * 0.4;

                   float rearY =  carPosition.y + 
                           (1.0 + worldUV.x / (carDimensions.x * -0.3)) * carDimensions.y * 0.5;
                   if(worldUV.x > 0.0 ){
                        //Inside the front
                        if(worldUV.y < hoodY){
                             return true;
                          }

                     } else if (worldUV.x < 0.0){
                           //Inside the rear 
                        if(worldUV.y< rearY){
                           return true;
                         }
                     }


                   return true;

              }

               return false;
            }

            void main(){
                vec4 obstacle = vec4(0.0,0.0,0.0,1.0);
                   if(isInsideCar(vUv)){
                      obstacle = vec4(1.0,0.0,0.0,1.0);
                   }

                 gl_FragColor = obstacle;
            }
        `
    });

    // Boundary shader
    boundaryShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
             resolution : {value: resolution},
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
        uniform vec2 resolution;
        varying vec2 vUv;

         vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

        void main(){
          vec2 texelSize = getTexelSize();
          vec4 boundary = vec4(0.0,0.0,0.0,1.0);
          if(vUv.x < texelSize.x || vUv.x> 1.0-texelSize.x|| vUv.y < texelSize.y || vUv.y > 1.0- texelSize.y){
            boundary = vec4(1.0,0.0,0.0,1.0);
          }
            
          gl_FragColor = boundary;
        }
        
        `
    });


    // Velocity shader (Navier-Stokes)
    velocityShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            velocityTexture: { value: velocityRenderTarget.texture },
            boundaryTexture: { value: boundaryRenderTarget.texture},
             obstacleTexture: {value: obstacleBuffer},
            deltaTime: {value : 0.01},
			viscosity: { value: simulationParams.dynamicViscosity},
			density: { value: simulationParams.airDensity},
			speed: {value : simulationParams.speed * 0.01},
			resolution : {value: resolution},
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
		    uniform sampler2D velocityTexture;
            uniform sampler2D boundaryTexture;
            uniform sampler2D obstacleTexture;
            uniform float deltaTime;
			uniform float viscosity;
			uniform float density;
			uniform float speed;
			uniform vec2 resolution;
			varying vec2 vUv;

			vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

			 // Function to get the velocity at a specific point
			vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }

             float getBoundary(vec2 uv) {
               return texture2D(boundaryTexture,uv).r;
            }

             float getObstacle(vec2 uv) {
               return texture2D(obstacleTexture,uv).r;
            }

           float getDivergence(vec2 uv){
			   vec2 texelSize = getTexelSize();
                float left = getVelocity(uv - vec2(texelSize.x,0.0)).x;
                float right = getVelocity(uv + vec2(texelSize.x,0.0)).x;
				float up = getVelocity(uv + vec2(0.0,texelSize.y)).y;
				float down = getVelocity(uv - vec2(0.0,texelSize.y)).y;
                return 0.5 * (right - left + up - down);
           }
 
            void main() {

				 vec2 currentVelocity = getVelocity(vUv);
                  float isBoundary = getBoundary(vUv);
                 float isObstacle = getObstacle(vUv);

                // Calculate the advection term
                vec2 texelSize = getTexelSize();
                vec2 prevPos = vUv - currentVelocity * deltaTime;
				
				
				// Check if the previous position is within the bounds
				vec2 clampedPos = clamp(prevPos, vec2(0.0), vec2(1.0));


				// Get advected velocity
				vec2 advectedVelocity = getVelocity(clampedPos);

				// Apply external force (wind)
				vec2 force = vec2(speed,0.0) ;


                // Apply viscosity to diffuse the velocity field
				vec2 diffVel = vec2(0.0);
				
				float laplacian = getDivergence(vUv) * viscosity;
                
                diffVel = (advectedVelocity + vec2(laplacian));

                if(isBoundary > 0.0 || isObstacle > 0.0){
                    diffVel = vec2(0.0);
                } else {
                    diffVel = diffVel + force;
                }

                gl_FragColor = vec4(diffVel, 0.0, 1.0);
            }
        `
    });
	
	
	 // divergence shader
    divergenceShaderMaterial =  new THREE.ShaderMaterial({
        uniforms: {
            velocityTexture: { value: velocityRenderTarget.texture},
			boundaryTexture: { value: boundaryRenderTarget.texture},
             obstacleTexture: {value: obstacleBuffer},
			resolution : {value: resolution},
        },
		vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
		uniform sampler2D velocityTexture;
        uniform sampler2D boundaryTexture;
          uniform sampler2D obstacleTexture;
		uniform vec2 resolution;
		
		varying vec2 vUv;

		
		vec2 getTexelSize()
        {
            return 1.0/resolution;
        }
		
		// Function to get the velocity at a specific point
		vec2 getVelocity(vec2 uv) {
            return texture2D(velocityTexture, uv).xy;
        }

         float getBoundary(vec2 uv) {
             return texture2D(boundaryTexture,uv).r;
         }
         float getObstacle(vec2 uv) {
             return texture2D(obstacleTexture,uv).r;
            }

        void main() {
			vec2 texelSize = getTexelSize();
            float left = getVelocity(vUv - vec2(texelSize.x,0.0)).x;
            float right = getVelocity(vUv + vec2(texelSize.x,0.0)).x;
			float up = getVelocity(vUv + vec2(0.0,texelSize.y)).y;
			float down = getVelocity(vUv - vec2(0.0,texelSize.y)).y;
			       float isBoundary = getBoundary(vUv);
                   float isObstacle = getObstacle(vUv);

			
			float divergence = 0.5 * (right - left + up - down);

             if(isBoundary > 0.0 || isObstacle > 0.0){
                    divergence = 0.0;
                }
			
			gl_FragColor = vec4(divergence, 0.0, 0.0,1.0);
        }
        
        `
    });
	
    // Pressure shader (Poisson equation using Jacobi iteration)
    pressureShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            pressureTexture: { value: pressureRenderTarget.texture },
			divergenceTexture: { value: divergenceRenderTarget.texture },
             boundaryTexture: { value: boundaryRenderTarget.texture},
             obstacleTexture: {value: obstacleBuffer},
            alpha: {value : -1.0},
			beta: {value: 0.25},
			resolution : {value: resolution},
			
        },
        vertexShader: `
             varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
		uniform sampler2D pressureTexture;
        uniform sampler2D boundaryTexture;
        uniform sampler2D obstacleTexture
		uniform sampler2D divergenceTexture;
		uniform float alpha;
		uniform float beta;
		uniform vec2 resolution;
		varying vec2 vUv;
		
		vec2 getTexelSize()
        {
            return 1.0/resolution;
        }
		
		float getDivergence(vec2 uv){
			return texture2D(divergenceTexture,uv).r;
		} 
		
		float getPressure(vec2 uv){
			return texture2D(pressureTexture,uv).r;
		}
        float getBoundary(vec2 uv) {
             return texture2D(boundaryTexture,uv).r;
         }
         float getObstacle(vec2 uv) {
             return texture2D(obstacleTexture,uv).r;
         }
		
		void main() {
            float isBoundary = getBoundary(vUv);
              float isObstacle = getObstacle(vUv);
			vec2 texelSize = getTexelSize();
			float left = getPressure(vUv - vec2(texelSize.x,0.0));
			float right = getPressure(vUv + vec2(texelSize.x,0.0));
			float up = getPressure(vUv + vec2(0.0,texelSize.y));
			float down = getPressure(vUv - vec2(0.0,texelSize.y));
			
			float divergence = getDivergence(vUv);
		
            float pressure = (left + right + up + down + alpha * divergence )* beta;
            
             if(isBoundary > 0.0 || isObstacle > 0.0){
                 pressure = 0.0;
             }

            gl_FragColor = vec4(pressure, 0.0, 0.0, 1.0) ;
        }
        `
    });

    // Visualization shader to render fluid to the plane
    visualizationShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            velocityTexture : {value: velocityRenderTarget.texture},
            pressureTexture : {value: pressureRenderTarget.texture},
            resolution: {value : resolution}
        },
        vertexShader: `
            varying vec2 vUv;
             void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }

        `,
        fragmentShader: `
            uniform sampler2D velocityTexture;
            uniform sampler2D pressureTexture;
              uniform vec2 resolution;
            varying vec2 vUv;

            vec2 getTexelSize()
            {
                return 1.0/resolution;
            }


             // Function to get the velocity at a specific point
            vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }

            float getPressure(vec2 uv){
                return texture2D(pressureTexture,uv).r;
            }




            void main(){
                 vec2 velocity =   getVelocity(vUv);
                float pressure =  getPressure(vUv);


             // Convert velocity to color
                vec3 velColor = vec3(0.0);
                float velMag = length(velocity);   
                 velColor.r = clamp(velMag * 1.0, 0.0, 1.0) ;


                  vec3 pressureColor = vec3(0.0);
               
                pressureColor.b =  clamp(pressure , 0.0, 1.0) ;
                 pressureColor.r = 1.0 - clamp(pressure * 10.0, 0.0, 1.0);


                gl_FragColor =  vec4(velColor + pressureColor, 1.0) ;
            }
        `

    });
}

function createQuad(){
	const geometry = new THREE.PlaneGeometry(2,2);
	quad = new THREE.Mesh(geometry);
	scene.add(quad);
}
	
function createObstacleField(){
    //Set the obstalce field with the location of the car
    renderer.setRenderTarget(obstacleBuffer);
    quad.material = obstacleShaderMaterial;
    renderer.render(scene, camera);
    renderer.setRenderTarget(null);
}

function runFluidSimulation(){
     // 0. Apply Obstacle Conditions
     createObstacleField();
    
    // 0. Apply Boundary Conditions
     quad.material = boundaryShaderMaterial;
     renderer.setRenderTarget(boundaryRenderTarget);
     renderer.render(scene, camera);

	// 1. Calculate Divergence
		renderer.setRenderTarget(divergenceRenderTarget);
		quad.material = divergenceShaderMaterial;
		renderer.render(scene, camera);


	// 2. Apply velocity Calculation
        quad.material = velocityShaderMaterial;
		renderer.setRenderTarget(velocityRenderTarget);
		renderer.render(scene, camera);
		

    //3. Calculate pressure
     let iteration = 20; // Number of jacobi iterations
	 quad.material = pressureShaderMaterial;
	 for(let i=0 ; i< iteration; i++){
		renderer.setRenderTarget(pressureRenderTarget);
		renderer.render(scene, camera);
	  }
	  
    
	// Reset render target
    renderer.setRenderTarget(null);

    //Apply visualization
    visualizationPlane.material = visualizationShaderMaterial;
    visualizationShaderMaterial.uniforms.velocityTexture.value = velocityRenderTarget.texture;
     visualizationShaderMaterial.uniforms.pressureTexture.value = pressureRenderTarget.texture;


}


function animate() {
    requestAnimationFrame(animate);
    controls.update();
    runFluidSimulation();
	renderer.render(scene, camera); // Render the scene after fluid calculation
  }


// Initialize the simulation
init();
C:\mygit\BLazy\repo\3dsim\static\js\FluidSimulation.js
Language detected: 
```javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';

let scene, camera, renderer, controls, gui;
let car, airflow, pressureField, carGroup;
let simulationParams = {
    length: 1.0,
    height: 0.5,
    width: 0.4,
    speed: 25,
    groundClearance: 0.1,
    hoodAngle: 15,
    rearAngle: 25,
    wheelRadius : 0.07,
    wheelWidth : 0.04,
	airDensity: 1.225, // kg/m^3
    temperature: 20, // °C
    dynamicViscosity: 1.81e-5, // kg/(m*s)
	turbulentIntensity: 0.05,
	k_epsilon_mixingLength : 0.05
};

// Data display variables
let dragCoefficientDisplay, liftForceDisplay, pressureDisplay, velocityDisplay, reynoldsDisplay, airDensityDisplay, temperatureDisplay, powerDisplay;


// Shader-related variables
let velocityRenderTarget, pressureRenderTarget, divergenceRenderTarget, boundaryRenderTarget, kRenderTarget, epsilonRenderTarget;
let velocityBuffer, pressureBuffer, divergenceBuffer, boundaryBuffer, kBuffer, epsilonBuffer;
let velocityShaderMaterial, pressureShaderMaterial, advectionShaderMaterial, divergenceShaderMaterial, boundaryShaderMaterial, visualizationShaderMaterial, obstacleShaderMaterial, kShaderMaterial, epsilonShaderMaterial;
let resolution;
let quad;
let visualizationPlane; //plane for the visualization

// Initialize the scene
function init() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);

    // Camera setup
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(2, 2, 2);

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);
	
	// GUI setup
	  gui = new GUI();
	  const carFolder = gui.addFolder('Car Parameters');
  
	  carFolder.add(simulationParams, 'length', 0.5, 2.0).name('Length').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'height', 0.2, 1.0).name('Height').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'width', 0.2, 0.8).name('Width').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelRadius', 0.03, 0.15).name('Wheel Radius').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelWidth', 0.02, 0.10).name('Wheel Width').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'groundClearance', 0, 0.3).name('Ground Clearance').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'hoodAngle', 0, 45).name('Hood Angle').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'rearAngle', 0, 45).name('Rear Angle').onChange(updateSimulation);
	  carFolder.open();
  
	  const airFolder = gui.addFolder('Air Parameters');
	  airFolder.add(simulationParams, 'airDensity', 0.5, 2.0).name('Air Density').onChange(updateSimulation);
	  airFolder.add(simulationParams, 'temperature', 0, 40).name('Temperature').onChange(updateSimulation);
	  airFolder.add(simulationParams,'speed',0, 100).name('Wind Speed').onChange(updateSimulation);
	  airFolder.add(simulationParams,'turbulentIntensity',0.01, 0.20).name('Turbulent Intensity').onChange(updateSimulation);
	  airFolder.add(simulationParams,'k_epsilon_mixingLength', 0.01, 0.20).name('Mixing Length').onChange(updateSimulation);
	  airFolder.open();

    // Controls setup
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);

    createCar();

	
	// Initialize Shader components
	initFluidSimulation();
	createQuad();
    createVisualizationPlane(); // create visualization plane
	
	// Initialize data display elements
	dragCoefficientDisplay = document.getElementById('drag-coefficient');
    liftForceDisplay = document.getElementById('lift-force');
    pressureDisplay = document.getElementById('pressure');
    velocityDisplay = document.getElementById('velocity');
    reynoldsDisplay = document.getElementById('reynolds');
    airDensityDisplay = document.getElementById('air-density');
    temperatureDisplay = document.getElementById('temperature');
	powerDisplay = document.getElementById('power');


    // Handle window resize
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function createCar() {
    // Remove existing car if it exists
     if (car) {
        scene.remove(car);
    }

    carGroup = new THREE.Group();

    // Car material
    const carMaterial = new THREE.MeshPhongMaterial({
        color: 0x156289,
        transparent: true,
        opacity: 0.8
    });

    // Function to create a rounded rectangle shape
    function createRoundedRectShape(width, height, radius) {
        const shape = new THREE.Shape();
        shape.moveTo(0, radius);
        shape.lineTo(0, height - radius);
        shape.quadraticCurveTo(0, height, radius, height);
        shape.lineTo(width - radius, height);
        shape.quadraticCurveTo(width, height, width, height - radius);
        shape.lineTo(width, radius);
        shape.quadraticCurveTo(width, 0, width - radius, 0);
        shape.lineTo(radius, 0);
        shape.quadraticCurveTo(0, 0, 0, radius);
        return shape;
    }
     // Create main body
    const bodyShape = createRoundedRectShape(
        simulationParams.length * 0.6,
        simulationParams.height * 0.6,
        simulationParams.height * 0.1
    );
    const bodyExtrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };
    const bodyGeometry = new THREE.ExtrudeGeometry(bodyShape, bodyExtrudeSettings);
    const bodyMesh = new THREE.Mesh(bodyGeometry, carMaterial);
    bodyMesh.position.y = simulationParams.groundClearance + simulationParams.height * 0.3;
    carGroup.add(bodyMesh);

    // Create hood (front section)
    const hoodShape = new THREE.Shape();
    const hoodLength = simulationParams.length * 0.2;
    const hoodHeight = simulationParams.height * 0.4;
    const hoodAngleRad = (simulationParams.hoodAngle * Math.PI) / 180;

    hoodShape.moveTo(0, 0);
    hoodShape.lineTo(hoodLength * Math.cos(hoodAngleRad), hoodHeight);
     hoodShape.lineTo(hoodLength,0);
    hoodShape.lineTo(0,0);
   
    const extrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };

    const hoodGeometry = new THREE.ExtrudeGeometry(hoodShape, extrudeSettings);
    const hoodMesh = new THREE.Mesh(hoodGeometry, carMaterial);
    hoodMesh.rotation.y = Math.PI / 2;
    hoodMesh.position.set(
        simulationParams.length * 0.3,
        simulationParams.groundClearance,
        simulationParams.width / 2
    );
    carGroup.add(hoodMesh);



    // Create rear section
    const rearShape = new THREE.Shape();
    const rearLength = simulationParams.length * 0.2;
	const rearHeight = simulationParams.height * 0.5;
    const rearAngleRad = (simulationParams.rearAngle * Math.PI) / 180;
    
    rearShape.moveTo(0, 0);
    rearShape.lineTo(0, rearHeight);
	rearShape.lineTo(rearLength * Math.cos(rearAngleRad),0);
    rearShape.lineTo(0, 0);

    const rearGeometry = new THREE.ExtrudeGeometry(rearShape, extrudeSettings);
    const rearMesh = new THREE.Mesh(rearGeometry, carMaterial);
    rearMesh.rotation.y = -Math.PI / 2;
    rearMesh.position.set(
        -simulationParams.length * 0.3,
        simulationParams.groundClearance,
        -simulationParams.width / 2
    );
     carGroup.add(rearMesh);
     
     // Create wheels
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x333333 });
    const wheelGeometry = new THREE.CylinderGeometry(simulationParams.wheelRadius, simulationParams.wheelRadius, simulationParams.wheelWidth, 32);

    //function to create wheel
     function createWheel(x, y, z) {
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, y, z);
		
        // Add hubcap
        const hubcapRadius = simulationParams.wheelRadius * 0.5
        const hubcapGeometry = new THREE.CylinderGeometry(hubcapRadius, hubcapRadius, simulationParams.wheelWidth+0.01, 32);
		const hubcapMaterial = new THREE.MeshPhongMaterial({color : 0xcccccc})//metallic silver
		const hubcap = new THREE.Mesh(hubcapGeometry,hubcapMaterial);
		hubcap.rotation.z = Math.PI / 2;
		wheel.add(hubcap);
		
        return wheel;
    }

    // Add wheels
	const wheelY = simulationParams.groundClearance + simulationParams.wheelRadius;
    const wheelZOffset = simulationParams.width/2 + simulationParams.wheelWidth/2;
    const wheelXOffset = simulationParams.length * 0.25
    const frontLeftWheel = createWheel(wheelXOffset, wheelY, wheelZOffset);
    const frontRightWheel = createWheel(wheelXOffset, wheelY, -wheelZOffset);
    const rearLeftWheel = createWheel(-wheelXOffset, wheelY, wheelZOffset);
    const rearRightWheel = createWheel(-wheelXOffset, wheelY, -wheelZOffset);
    carGroup.add(frontLeftWheel, frontRightWheel, rearLeftWheel, rearRightWheel);
	
    // Add the car group to the scene and store it as car
    car = carGroup;
    scene.add(car);
}

function createVisualizationPlane(){
    const planeGeometry = new THREE.PlaneGeometry(10,10);
    visualizationPlane = new THREE.Mesh(planeGeometry);
    visualizationPlane.rotation.x = -Math.PI / 2;
    visualizationPlane.position.set(0,0.01,0);
    scene.add(visualizationPlane);
}


async function updateSimulation() {

        // Get current parameters
    const params = new URLSearchParams({
        length: simulationParams.length,
        height: simulationParams.height,
        width: simulationParams.width,
        speed: simulationParams.speed,
        groundClearance: simulationParams.groundClearance,
        hoodAngle: simulationParams.hoodAngle,
        rearAngle: simulationParams.rearAngle,
        wheelRadius: simulationParams.wheelRadius,
        wheelWidth: simulationParams.wheelWidth,
		airDensity: simulationParams.airDensity,
        temperature: simulationParams.temperature,
		dynamicViscosity: simulationParams.dynamicViscosity,
		turbulentIntensity : simulationParams.turbulentIntensity,
		k_epsilon_mixingLength: simulationParams.k_epsilon_mixingLength
		
    });
    
    try {
        const response = await fetch(`/simulation?${params}`);
        const data = await response.json();

        // Update visualization with new data
        updateCarGeometry();
       
        updateDataDisplay(data);
		
        
    } catch (error) {
        console.error('Error updating simulation:', error);
    }
}

function updateCarGeometry() {
    scene.remove(car);
    createCar();
	createObstacleField() //recreate obstacle buffer when car geometry changes
}


function updateDataDisplay(data) {
    dragCoefficientDisplay.textContent = data.drag_coefficient.toFixed(3);
    liftForceDisplay.textContent = data.lift_force.toFixed(3);
	
	
    // Format pressure for display
    const avgPressure = data.pressure.flat().reduce((a, b) => a + b, 0) / data.pressure.flat().length;
    pressureDisplay.textContent = avgPressure.toFixed(2);


    velocityDisplay.textContent = simulationParams.speed.toFixed(1);
    reynoldsDisplay.textContent = data.reynolds_number.toFixed(0);
    airDensityDisplay.textContent = simulationParams.airDensity.toFixed(3);
	const tempInC = simulationParams.temperature
    temperatureDisplay.textContent = tempInC.toFixed(1);
	powerDisplay.textContent = data.power.toFixed(0);
}


function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
}



// Shader Setup
function initFluidSimulation() {
    resolution = new THREE.Vector2(256, 256); // Adjust resolution as needed
    
	// Create render Targets
     velocityRenderTarget = createRenderTarget();
     pressureRenderTarget = createRenderTarget();
	 divergenceRenderTarget = createRenderTarget();
     boundaryRenderTarget = createRenderTarget();
	 kRenderTarget = createRenderTarget();
	 epsilonRenderTarget = createRenderTarget();

    //Obstacle buffer
     obstacleBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
		resolution.x,
		resolution.y,
		THREE.RGBAFormat,
		THREE.FloatType
	);
    obstacleBuffer.needsUpdate = true;

	// Set the buffer with initial fluid velocity
    velocityBuffer = new THREE.DataTexture(
         new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
    );
	velocityBuffer.needsUpdate = true;
    
	pressureBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
	);
		
	divergenceBuffer  = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
	);

    boundaryBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
		resolution.x,
		resolution.y,
		THREE.RGBAFormat,
		THREE.FloatType
	);
    boundaryBuffer.needsUpdate = true;
	
	kBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
		resolution.x,
		resolution.y,
		THREE.RGBAFormat,
		THREE.FloatType
	);
	kBuffer.needsUpdate = true;
	
	
	epsilonBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
		resolution.x,
		resolution.y,
		THREE.RGBAFormat,
		THREE.FloatType
	);
	epsilonBuffer.needsUpdate = true;

	

    // Initialize shaders
    initShaders();
	createObstacleField();
}



function createRenderTarget() {
    return new THREE.WebGLRenderTarget(
        resolution.x,
        resolution.y,
        {
            wrapS: THREE.RepeatWrapping,
            wrapT: THREE.RepeatWrapping,
            minFilter: THREE.LinearFilter,
            magFilter: THREE.LinearFilter,
            format: THREE.RGBAFormat,
            type: THREE.FloatType,
             stencilBuffer: false
        }
    );
}

function initShaders() {

    // Obstacle shader
     obstacleShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
             resolution : {value: resolution},
              carDimensions: { value: new THREE.Vector3(simulationParams.length, simulationParams.height, simulationParams.width) },
            carPosition: { value: new THREE.Vector3(0, simulationParams.groundClearance, 0) },
              hoodAngle : { value:  simulationParams.hoodAngle * Math.PI / 180},
              rearAngle : { value: simulationParams.rearAngle * Math.PI / 180},

        },
         vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
         fragmentShader: `
             uniform vec2 resolution;
            uniform vec3 carDimensions;
            uniform vec3 carPosition;
             uniform float hoodAngle;
            uniform float rearAngle;


            varying vec2 vUv;

            vec2 getTexelSize()
            {
              return 1.0/resolution;
            }

            bool isInsideCar(vec2 uv){
              vec2 texelSize = getTexelSize();
              // Transform uv coordinates to world coordinates (-5 to 5 range)
              vec2 worldUV = (uv * 10.0) - 5.0 ; //scale up for the size of simulation


                // Car bounds
               float carFront = carPosition.x + carDimensions.x * 0.3;
              float carBack = carPosition.x - carDimensions.x * 0.3;
              float carTop = carPosition.y + carDimensions.y;
              float carBottom = carPosition.y;
             float carRight = carPosition.z + carDimensions.z/2.0;
            float carLeft = carPosition.z - carDimensions.z/2.0;



               // Check bounding box first
              if (worldUV.x >= carBack && worldUV.x <= carFront &&
                worldUV.y >= carBottom && worldUV.y <=carTop &&
               worldUV.y   >= carBottom && worldUV.y <= carTop &&
                  worldUV.x >= carLeft && worldUV.x <= carRight ){
                   //then check front and rear
                    float hoodY = carPosition.y + 
                           (worldUV.x / (carDimensions.x * 0.3)) * carDimensions.y * 0.4;

                   float rearY =  carPosition.y + 
                           (1.0 + worldUV.x / (carDimensions.x * -0.3)) * carDimensions.y * 0.5;
                   if(worldUV.x > 0.0 ){
                        //Inside the front
                        if(worldUV.y < hoodY){
                             return true;
                          }

                     } else if (worldUV.x < 0.0){
                           //Inside the rear 
                        if(worldUV.y< rearY){
                           return true;
                         }
                     }


                   return true;

              }

               return false;
            }

            void main(){
                vec4 obstacle = vec4(0.0,0.0,0.0,1.0);
                   if(isInsideCar(vUv)){
                      obstacle = vec4(1.0,0.0,0.0,1.0);
                   }

                 gl_FragColor = obstacle;
            }
        `
    });

    // Boundary shader
    boundaryShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
             resolution : {value: resolution},
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
        uniform vec2 resolution;
        varying vec2 vUv;

         vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

        void main(){
          vec2 texelSize = getTexelSize();
          vec4 boundary = vec4(0.0,0.0,0.0,1.0);
          if(vUv.x < texelSize.x || vUv.x> 1.0-texelSize.x|| vUv.y < texelSize.y || vUv.y > 1.0- texelSize.y){
            boundary = vec4(1.0,0.0,0.0,1.0);
          }
            
          gl_FragColor = boundary;
        }
        
        `
    });
	
	  // k shader (Turbulence Kinetic Energy)
    kShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            kTexture: { value: kRenderTarget.texture },
            velocityTexture: { value: velocityRenderTarget.texture },
             obstacleTexture: {value: obstacleBuffer},
            deltaTime: {value : 0.01},
			viscosity: { value: simulationParams.dynamicViscosity},
			density: { value: simulationParams.airDensity},
			speed: {value : simulationParams.speed * 0.01},
			turbulentIntensity : {value : simulationParams.turbulentIntensity},
			resolution : {value: resolution},
			k_epsilon_mixingLength : {value : simulationParams.k_epsilon_mixingLength},

        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
		fragmentShader: `
		    uniform sampler2D kTexture;
            uniform sampler2D velocityTexture;
             uniform sampler2D obstacleTexture;
            uniform float deltaTime;
			uniform float viscosity;
			uniform float density;
			uniform float speed;
			uniform float turbulentIntensity;
			uniform vec2 resolution;
            uniform float k_epsilon_mixingLength;
			varying vec2 vUv;

			vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

			 // Function to get the velocity at a specific point
			vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }
			float getK(vec2 uv){
				return texture2D(kTexture,uv).r;
			}
			float getObstacle(vec2 uv) {
               return texture2D(obstacleTexture,uv).r;
            }


           float getDivergence(vec2 uv){
			   vec2 texelSize = getTexelSize();
                float left = getVelocity(uv - vec2(texelSize.x,0.0)).x;
                float right = getVelocity(uv + vec2(texelSize.x,0.0)).x;
				float up = getVelocity(uv + vec2(0.0,texelSize.y)).y;
				float down = getVelocity(uv - vec2(0.0,texelSize.y)).y;
                return 0.5 * (right - left + up - down);
           }


            void main() {
                  float isObstacle = getObstacle(vUv);
				   float currentK = getK(vUv);
				  vec2 currentVelocity = getVelocity(vUv);
					
                // Calculate the advection term
                vec2 texelSize = getTexelSize();
                vec2 prevPos = vUv - currentVelocity * deltaTime;
				
				
				// Check if the previous position is within the bounds
				vec2 clampedPos = clamp(prevPos, vec2(0.0), vec2(1.0));

				
				 float advectedK =  getK(clampedPos);

                 // Production Term 
                 float production = 0.5 * viscosity * pow(getDivergence(vUv),2.0);


				// Dissipation of k
				 float dissipation =  pow(currentK,1.5) * 0.09 / k_epsilon_mixingLength   / sqrt(currentK);

				
				 float nextK = (advectedK + production - dissipation) ;
                  if(isObstacle > 0.0){
                      nextK = currentK; //Keep k at same value
                   } else {
                        nextK = nextK +  turbulentIntensity * speed * speed * 0.5  ;
				   }



                gl_FragColor = vec4(max(nextK,0.0), 0.0, 0.0, 1.0);
            }
        `
    });
	
	// Epsilon Shader (Turbulence Dissipation Rate)
	epsilonShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            kTexture: { value: kRenderTarget.texture },
			epsilonTexture : { value : epsilonRenderTarget.texture},
            velocityTexture: { value: velocityRenderTarget.texture },
             obstacleTexture: {value: obstacleBuffer},
            deltaTime: {value : 0.01},
			viscosity: { value: simulationParams.dynamicViscosity},
			density: { value: simulationParams.airDensity},
			speed: {value : simulationParams.speed * 0.01},
			turbulentIntensity : {value : simulationParams.turbulentIntensity},
			resolution : {value: resolution},
			k_epsilon_mixingLength : {value : simulationParams.k_epsilon_mixingLength},

        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
		fragmentShader: `
		    uniform sampler2D kTexture;
			uniform sampler2D epsilonTexture;
            uniform sampler2D velocityTexture;
             uniform sampler2D obstacleTexture;
            uniform float deltaTime;
			uniform float viscosity;
			uniform float density;
			uniform float speed;
			uniform float turbulentIntensity;
			uniform vec2 resolution;
            uniform float k_epsilon_mixingLength;
			varying vec2 vUv;

			vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

			 // Function to get the velocity at a specific point
			vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }
			float getK(vec2 uv){
				return texture2D(kTexture,uv).r;
			}
			float getEpsilon(vec2 uv){
				return texture2D(epsilonTexture,uv).r;
			}
			float getObstacle(vec2 uv) {
               return texture2D(obstacleTexture,uv).r;
            }


           float getDivergence(vec2 uv){
			   vec2 texelSize = getTexelSize();
                float left = getVelocity(uv - vec2(texelSize.x,0.0)).x;
                float right = getVelocity(uv + vec2(texelSize.x,0.0)).x;
				float up = getVelocity(uv + vec2(0.0,texelSize.y)).y;
				float down = getVelocity(uv - vec2(0.0,texelSize.y)).y;
                return 0.5 * (right - left + up - down);
           }


            void main() {
                float isObstacle = getObstacle(vUv);
				  float currentK = getK(vUv);
				  float currentEpsilon = getEpsilon(vUv);
				   vec2 currentVelocity = getVelocity(vUv);
					
                // Calculate the advection term
                vec2 texelSize = getTexelSize();
                vec2 prevPos = vUv - currentVelocity * deltaTime;
				
				
				// Check if the previous position is within the bounds
				vec2 clampedPos = clamp(prevPos, vec2(0.0), vec2(1.0));

			    float advectedEpsilon =  getEpsilon(clampedPos);


                 // Production Term 
                 float production = 0.5 * 1.44 * viscosity *  pow(getDivergence(vUv) * currentK , 2.0)/ currentEpsilon;
 
                 //Dissipation
				 float dissipation =  1.92 * pow(currentEpsilon,2.0) / currentK;

				 float nextEpsilon = advectedEpsilon + production - dissipation;

                   if(isObstacle > 0.0){
                      nextEpsilon= currentEpsilon;
                   } else{
                         nextEpsilon = nextEpsilon +   0.09 * turbulentIntensity * pow(speed,3.0) / k_epsilon_mixingLength;
                   }



                gl_FragColor = vec4(max(nextEpsilon,0.0), 0.0, 0.0, 1.0);
            }
        `
    });
	


    // Velocity shader (Navier-Stokes)
    velocityShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            velocityTexture: { value: velocityRenderTarget.texture },
            boundaryTexture: { value: boundaryRenderTarget.texture},
             obstacleTexture: {value: obstacleBuffer},
			  kTexture: { value: kRenderTarget.texture },
			epsilonTexture : { value : epsilonRenderTarget.texture},
            deltaTime: {value : 0.01},
			viscosity: { value: simulationParams.dynamicViscosity},
			density: { value: simulationParams.airDensity},
			speed: {value : simulationParams.speed * 0.01},
			resolution : {value: resolution},
			k_epsilon_mixingLength : {value : simulationParams.k_epsilon_mixingLength}
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
		    uniform sampler2D velocityTexture;
            uniform sampler2D boundaryTexture;
            uniform sampler2D obstacleTexture;
			uniform sampler2D kTexture;
			uniform sampler2D epsilonTexture;
            uniform float deltaTime;
			uniform float viscosity;
			uniform float density;
			uniform float speed;
			uniform vec2 resolution;
			 uniform float k_epsilon_mixingLength;
			varying vec2 vUv;

			vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

			 // Function to get the velocity at a specific point
			vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }

             float getBoundary(vec2 uv) {
               return texture2D(boundaryTexture,uv).r;
            }

             float getObstacle(vec2 uv) {
               return texture2D(obstacleTexture,uv).r;
            }
			float getK(vec2 uv){
				return texture2D(kTexture,uv).r;
			}
			float getEpsilon(vec2 uv){
				return texture2D(epsilonTexture,uv).r;
			}

           float getDivergence(vec2 uv){
			   vec2 texelSize = getTexelSize();
                float left = getVelocity(uv - vec2(texelSize.x,0.0)).x;
                float right = getVelocity(uv + vec2(texelSize.x,0.0)).x;
				float up = getVelocity(uv + vec2(0.0,texelSize.y)).y;
				float down = getVelocity(uv - vec2(0.0,texelSize.y)).y;
                return 0.5 * (right - left + up - down);
           }
 
            void main() {

				 vec2 currentVelocity = getVelocity(vUv);
                  float isBoundary = getBoundary(vUv);
                 float isObstacle = getObstacle(vUv);
				  float currentK = getK(vUv);
                 float currentEpsilon = getEpsilon(vUv);


                // Calculate the advection term
                vec2 texelSize = getTexelSize();
                vec2 prevPos = vUv - currentVelocity * deltaTime;
				
				
				// Check if the previous position is within the bounds
				vec2 clampedPos = clamp(prevPos, vec2(0.0), vec2(1.0));


				// Get advected velocity
				vec2 advectedVelocity = getVelocity(clampedPos);

				// Apply external force (wind)
				vec2 force = vec2(speed,0.0) ;


                // Apply viscosity to diffuse the velocity field
				vec2 diffVel = vec2(0.0);
				
				float turbulentViscosity = 0.09 * density * pow(currentK,2.0) / currentEpsilon; // Calculate turbulent viscosity
				float laplacian = getDivergence(vUv) *  (viscosity + turbulentViscosity) ;
                
                diffVel = (
C:\mygit\BLazy\repo\3dsim\static\js\shaders\velocityShader.js
Language detected: 
```javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';

let scene, camera, renderer, controls, gui;
let car, airflow, pressureField, carGroup;
let simulationParams = {
    length: 1.0,
    height: 0.5,
    width: 0.4,
    speed: 25,
    groundClearance: 0.1,
    hoodAngle: 15,
    rearAngle: 25,
    wheelRadius : 0.07,
    wheelWidth : 0.04,
	airDensity: 1.225, // kg/m^3
    temperature: 20, // °C
    dynamicViscosity: 1.81e-5, // kg/(m*s)
	turbulentIntensity: 0.05,
	k_epsilon_mixingLength : 0.05
};

// Data display variables
let dragCoefficientDisplay, liftForceDisplay, pressureDisplay, velocityDisplay, reynoldsDisplay, airDensityDisplay, temperatureDisplay, powerDisplay;


// Shader-related variables
let velocityRenderTarget, pressureRenderTarget, divergenceRenderTarget, boundaryRenderTarget, kRenderTarget, epsilonRenderTarget;
let velocityBuffer, pressureBuffer, divergenceBuffer, boundaryBuffer, kBuffer, epsilonBuffer;
let velocityShaderMaterial, pressureShaderMaterial, advectionShaderMaterial, divergenceShaderMaterial, boundaryShaderMaterial, visualizationShaderMaterial, obstacleShaderMaterial, kShaderMaterial, epsilonShaderMaterial;
let resolution;
let quad;
let visualizationPlane; //plane for the visualization

// Initialize the scene
function init() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);

    // Camera setup
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(2, 2, 2);

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);
	
	// GUI setup
	  gui = new GUI();
	  const carFolder = gui.addFolder('Car Parameters');
  
	  carFolder.add(simulationParams, 'length', 0.5, 2.0).name('Length').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'height', 0.2, 1.0).name('Height').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'width', 0.2, 0.8).name('Width').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelRadius', 0.03, 0.15).name('Wheel Radius').onChange(updateSimulation);
      carFolder.add(simulationParams, 'wheelWidth', 0.02, 0.10).name('Wheel Width').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'groundClearance', 0, 0.3).name('Ground Clearance').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'hoodAngle', 0, 45).name('Hood Angle').onChange(updateSimulation);
	  carFolder.add(simulationParams, 'rearAngle', 0, 45).name('Rear Angle').onChange(updateSimulation);
	  carFolder.open();
  
	  const airFolder = gui.addFolder('Air Parameters');
	  airFolder.add(simulationParams, 'airDensity', 0.5, 2.0).name('Air Density').onChange(updateSimulation);
	  airFolder.add(simulationParams, 'temperature', 0, 40).name('Temperature').onChange(updateSimulation);
	  airFolder.add(simulationParams,'speed',0, 100).name('Wind Speed').onChange(updateSimulation);
	  airFolder.add(simulationParams,'turbulentIntensity',0.01, 0.20).name('Turbulent Intensity').onChange(updateSimulation);
	  airFolder.add(simulationParams,'k_epsilon_mixingLength', 0.01, 0.20).name('Mixing Length').onChange(updateSimulation);
	  airFolder.open();

    // Controls setup
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    // Add grid helper
    const gridHelper = new THREE.GridHelper(10, 10);
    scene.add(gridHelper);

    createCar();

	
	// Initialize Shader components
	initFluidSimulation();
	createQuad();
    createVisualizationPlane(); // create visualization plane
	
	// Initialize data display elements
	dragCoefficientDisplay = document.getElementById('drag-coefficient');
    liftForceDisplay = document.getElementById('lift-force');
    pressureDisplay = document.getElementById('pressure');
    velocityDisplay = document.getElementById('velocity');
    reynoldsDisplay = document.getElementById('reynolds');
    airDensityDisplay = document.getElementById('air-density');
    temperatureDisplay = document.getElementById('temperature');
	powerDisplay = document.getElementById('power');


    // Handle window resize
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function createCar() {
    // Remove existing car if it exists
     if (car) {
        scene.remove(car);
    }

    carGroup = new THREE.Group();

    // Car material
    const carMaterial = new THREE.MeshPhongMaterial({
        color: 0x156289,
        transparent: true,
        opacity: 0.8
    });

    // Function to create a rounded rectangle shape
    function createRoundedRectShape(width, height, radius) {
        const shape = new THREE.Shape();
        shape.moveTo(0, radius);
        shape.lineTo(0, height - radius);
        shape.quadraticCurveTo(0, height, radius, height);
        shape.lineTo(width - radius, height);
        shape.quadraticCurveTo(width, height, width, height - radius);
        shape.lineTo(width, radius);
        shape.quadraticCurveTo(width, 0, width - radius, 0);
        shape.lineTo(radius, 0);
        shape.quadraticCurveTo(0, 0, 0, radius);
        return shape;
    }
     // Create main body
    const bodyShape = createRoundedRectShape(
        simulationParams.length * 0.6,
        simulationParams.height * 0.6,
        simulationParams.height * 0.1
    );
    const bodyExtrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };
    const bodyGeometry = new THREE.ExtrudeGeometry(bodyShape, bodyExtrudeSettings);
    const bodyMesh = new THREE.Mesh(bodyGeometry, carMaterial);
    bodyMesh.position.y = simulationParams.groundClearance + simulationParams.height * 0.3;
    carGroup.add(bodyMesh);

    // Create hood (front section)
    const hoodShape = new THREE.Shape();
    const hoodLength = simulationParams.length * 0.2;
    const hoodHeight = simulationParams.height * 0.4;
    const hoodAngleRad = (simulationParams.hoodAngle * Math.PI) / 180;

    hoodShape.moveTo(0, 0);
    hoodShape.lineTo(hoodLength * Math.cos(hoodAngleRad), hoodHeight);
     hoodShape.lineTo(hoodLength,0);
    hoodShape.lineTo(0,0);
   
    const extrudeSettings = {
        steps: 1,
        depth: simulationParams.width,
        bevelEnabled: false
    };

    const hoodGeometry = new THREE.ExtrudeGeometry(hoodShape, extrudeSettings);
    const hoodMesh = new THREE.Mesh(hoodGeometry, carMaterial);
    hoodMesh.rotation.y = Math.PI / 2;
    hoodMesh.position.set(
        simulationParams.length * 0.3,
        simulationParams.groundClearance,
        simulationParams.width / 2
    );
    carGroup.add(hoodMesh);



    // Create rear section
    const rearShape = new THREE.Shape();
    const rearLength = simulationParams.length * 0.2;
	const rearHeight = simulationParams.height * 0.5;
    const rearAngleRad = (simulationParams.rearAngle * Math.PI) / 180;
    
    rearShape.moveTo(0, 0);
    rearShape.lineTo(0, rearHeight);
	rearShape.lineTo(rearLength * Math.cos(rearAngleRad),0);
    rearShape.lineTo(0, 0);

    const rearGeometry = new THREE.ExtrudeGeometry(rearShape, extrudeSettings);
    const rearMesh = new THREE.Mesh(rearGeometry, carMaterial);
    rearMesh.rotation.y = -Math.PI / 2;
    rearMesh.position.set(
        -simulationParams.length * 0.3,
        simulationParams.groundClearance,
        -simulationParams.width / 2
    );
     carGroup.add(rearMesh);
     
     // Create wheels
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x333333 });
    const wheelGeometry = new THREE.CylinderGeometry(simulationParams.wheelRadius, simulationParams.wheelRadius, simulationParams.wheelWidth, 32);

    //function to create wheel
     function createWheel(x, y, z) {
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, y, z);
		
        // Add hubcap
        const hubcapRadius = simulationParams.wheelRadius * 0.5
        const hubcapGeometry = new THREE.CylinderGeometry(hubcapRadius, hubcapRadius, simulationParams.wheelWidth+0.01, 32);
		const hubcapMaterial = new THREE.MeshPhongMaterial({color : 0xcccccc})//metallic silver
		const hubcap = new THREE.Mesh(hubcapGeometry,hubcapMaterial);
		hubcap.rotation.z = Math.PI / 2;
		wheel.add(hubcap);
		
        return wheel;
    }

    // Add wheels
	const wheelY = simulationParams.groundClearance + simulationParams.wheelRadius;
    const wheelZOffset = simulationParams.width/2 + simulationParams.wheelWidth/2;
    const wheelXOffset = simulationParams.length * 0.25
    const frontLeftWheel = createWheel(wheelXOffset, wheelY, wheelZOffset);
    const frontRightWheel = createWheel(wheelXOffset, wheelY, -wheelZOffset);
    const rearLeftWheel = createWheel(-wheelXOffset, wheelY, wheelZOffset);
    const rearRightWheel = createWheel(-wheelXOffset, wheelY, -wheelZOffset);
    carGroup.add(frontLeftWheel, frontRightWheel, rearLeftWheel, rearRightWheel);
	
    // Add the car group to the scene and store it as car
    car = carGroup;
    scene.add(car);
}

function createVisualizationPlane(){
    const planeGeometry = new THREE.PlaneGeometry(10,10);
    visualizationPlane = new THREE.Mesh(planeGeometry);
    visualizationPlane.rotation.x = -Math.PI / 2;
    visualizationPlane.position.set(0,0.01,0);
    scene.add(visualizationPlane);
}


async function updateSimulation() {

        // Get current parameters
    const params = new URLSearchParams({
        length: simulationParams.length,
        height: simulationParams.height,
        width: simulationParams.width,
        speed: simulationParams.speed,
        groundClearance: simulationParams.groundClearance,
        hoodAngle: simulationParams.hoodAngle,
        rearAngle: simulationParams.rearAngle,
        wheelRadius: simulationParams.wheelRadius,
        wheelWidth: simulationParams.wheelWidth,
		airDensity: simulationParams.airDensity,
        temperature: simulationParams.temperature,
		dynamicViscosity: simulationParams.dynamicViscosity,
		turbulentIntensity : simulationParams.turbulentIntensity,
		k_epsilon_mixingLength: simulationParams.k_epsilon_mixingLength
		
    });
    
    try {
        const response = await fetch(`/simulation?${params}`);
        const data = await response.json();

        // Update visualization with new data
        updateCarGeometry();
       
        updateDataDisplay(data);
		
        
    } catch (error) {
        console.error('Error updating simulation:', error);
    }
}

function updateCarGeometry() {
    scene.remove(car);
    createCar();
	createObstacleField() //recreate obstacle buffer when car geometry changes
}


function updateDataDisplay(data) {
    dragCoefficientDisplay.textContent = data.drag_coefficient.toFixed(3);
    liftForceDisplay.textContent = data.lift_force.toFixed(3);
	
	
    // Format pressure for display
    const avgPressure = data.pressure.flat().reduce((a, b) => a + b, 0) / data.pressure.flat().length;
    pressureDisplay.textContent = avgPressure.toFixed(2);


    velocityDisplay.textContent = simulationParams.speed.toFixed(1);
    reynoldsDisplay.textContent = data.reynolds_number.toFixed(0);
    airDensityDisplay.textContent = simulationParams.airDensity.toFixed(3);
	const tempInC = simulationParams.temperature
    temperatureDisplay.textContent = tempInC.toFixed(1);
	powerDisplay.textContent = data.power.toFixed(0);
}


function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth * 0.8, window.innerHeight);
}



// Shader Setup
function initFluidSimulation() {
    resolution = new THREE.Vector2(256, 256); // Adjust resolution as needed
    
	// Create render Targets
     velocityRenderTarget = createRenderTarget();
     pressureRenderTarget = createRenderTarget();
	 divergenceRenderTarget = createRenderTarget();
     boundaryRenderTarget = createRenderTarget();
	 kRenderTarget = createRenderTarget();
	 epsilonRenderTarget = createRenderTarget();

    //Obstacle buffer
     obstacleBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
		resolution.x,
		resolution.y,
		THREE.RGBAFormat,
		THREE.FloatType
	);
    obstacleBuffer.needsUpdate = true;

	// Set the buffer with initial fluid velocity
    velocityBuffer = new THREE.DataTexture(
         new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
    );
	velocityBuffer.needsUpdate = true;
    
	pressureBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
	);
		
	divergenceBuffer  = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
            resolution.x,
            resolution.y,
            THREE.RGBAFormat,
            THREE.FloatType
	);

    boundaryBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
		resolution.x,
		resolution.y,
		THREE.RGBAFormat,
		THREE.FloatType
	);
    boundaryBuffer.needsUpdate = true;
	
	kBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
		resolution.x,
		resolution.y,
		THREE.RGBAFormat,
		THREE.FloatType
	);
	kBuffer.needsUpdate = true;
	
	
	epsilonBuffer = new THREE.DataTexture(
		new Float32Array(resolution.x * resolution.y * 4),
		resolution.x,
		resolution.y,
		THREE.RGBAFormat,
		THREE.FloatType
	);
	epsilonBuffer.needsUpdate = true;

	

    // Initialize shaders
    initShaders();
	createObstacleField();
}



function createRenderTarget() {
    return new THREE.WebGLRenderTarget(
        resolution.x,
        resolution.y,
        {
            wrapS: THREE.RepeatWrapping,
            wrapT: THREE.RepeatWrapping,
            minFilter: THREE.LinearFilter,
            magFilter: THREE.LinearFilter,
            format: THREE.RGBAFormat,
            type: THREE.FloatType,
             stencilBuffer: false
        }
    );
}

function initShaders() {

    // Obstacle shader
     obstacleShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
             resolution : {value: resolution},
              carDimensions: { value: new THREE.Vector3(simulationParams.length, simulationParams.height, simulationParams.width) },
            carPosition: { value: new THREE.Vector3(0, simulationParams.groundClearance, 0) },
              hoodAngle : { value:  simulationParams.hoodAngle * Math.PI / 180},
              rearAngle : { value: simulationParams.rearAngle * Math.PI / 180},

        },
         vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
         fragmentShader: `
             uniform vec2 resolution;
            uniform vec3 carDimensions;
            uniform vec3 carPosition;
             uniform float hoodAngle;
            uniform float rearAngle;


            varying vec2 vUv;

            vec2 getTexelSize()
            {
              return 1.0/resolution;
            }

            bool isInsideCar(vec2 uv){
              vec2 texelSize = getTexelSize();
              // Transform uv coordinates to world coordinates (-5 to 5 range)
              vec2 worldUV = (uv * 10.0) - 5.0 ; //scale up for the size of simulation


                // Car bounds
               float carFront = carPosition.x + carDimensions.x * 0.3;
              float carBack = carPosition.x - carDimensions.x * 0.3;
              float carTop = carPosition.y + carDimensions.y;
              float carBottom = carPosition.y;
             float carRight = carPosition.z + carDimensions.z/2.0;
            float carLeft = carPosition.z - carDimensions.z/2.0;



               // Check bounding box first
              if (worldUV.x >= carBack && worldUV.x <= carFront &&
                worldUV.y >= carBottom && worldUV.y <=carTop &&
               worldUV.y   >= carBottom && worldUV.y <= carTop &&
                  worldUV.x >= carLeft && worldUV.x <= carRight ){
                   //then check front and rear
                    float hoodY = carPosition.y + 
                           (worldUV.x / (carDimensions.x * 0.3)) * carDimensions.y * 0.4;

                   float rearY =  carPosition.y + 
                           (1.0 + worldUV.x / (carDimensions.x * -0.3)) * carDimensions.y * 0.5;
                   if(worldUV.x > 0.0 ){
                        //Inside the front
                        if(worldUV.y < hoodY){
                             return true;
                          }

                     } else if (worldUV.x < 0.0){
                           //Inside the rear 
                        if(worldUV.y< rearY){
                           return true;
                         }
                     }


                   return true;

              }

               return false;
            }

            void main(){
                vec4 obstacle = vec4(0.0,0.0,0.0,1.0);
                   if(isInsideCar(vUv)){
                      obstacle = vec4(1.0,0.0,0.0,1.0);
                   }

                 gl_FragColor = obstacle;
            }
        `
    });

    // Boundary shader
    boundaryShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
             resolution : {value: resolution},
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
        uniform vec2 resolution;
        varying vec2 vUv;

         vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

        void main(){
          vec2 texelSize = getTexelSize();
          vec4 boundary = vec4(0.0,0.0,0.0,1.0);
          if(vUv.x < texelSize.x || vUv.x> 1.0-texelSize.x|| vUv.y < texelSize.y || vUv.y > 1.0- texelSize.y){
            boundary = vec4(1.0,0.0,0.0,1.0);
          }
            
          gl_FragColor = boundary;
        }
        
        `
    });
	
	  // k shader (Turbulence Kinetic Energy)
    kShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            kTexture: { value: kRenderTarget.texture },
            velocityTexture: { value: velocityRenderTarget.texture },
             obstacleTexture: {value: obstacleBuffer},
            deltaTime: {value : 0.01},
			viscosity: { value: simulationParams.dynamicViscosity},
			density: { value: simulationParams.airDensity},
			speed: {value : simulationParams.speed * 0.01},
			turbulentIntensity : {value : simulationParams.turbulentIntensity},
			resolution : {value: resolution},
			k_epsilon_mixingLength : {value : simulationParams.k_epsilon_mixingLength},

        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
		fragmentShader: `
		    uniform sampler2D kTexture;
            uniform sampler2D velocityTexture;
             uniform sampler2D obstacleTexture;
            uniform float deltaTime;
			uniform float viscosity;
			uniform float density;
			uniform float speed;
			uniform float turbulentIntensity;
			uniform vec2 resolution;
            uniform float k_epsilon_mixingLength;
			varying vec2 vUv;

			vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

			 // Function to get the velocity at a specific point
			vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }
			float getK(vec2 uv){
				return texture2D(kTexture,uv).r;
			}
			float getObstacle(vec2 uv) {
               return texture2D(obstacleTexture,uv).r;
            }


           float getDivergence(vec2 uv){
			   vec2 texelSize = getTexelSize();
                float left = getVelocity(uv - vec2(texelSize.x,0.0)).x;
                float right = getVelocity(uv + vec2(texelSize.x,0.0)).x;
				float up = getVelocity(uv + vec2(0.0,texelSize.y)).y;
				float down = getVelocity(uv - vec2(0.0,texelSize.y)).y;
                return 0.5 * (right - left + up - down);
           }


            void main() {
                  float isObstacle = getObstacle(vUv);
				   float currentK = getK(vUv);
				  vec2 currentVelocity = getVelocity(vUv);
					
                // Calculate the advection term
                vec2 texelSize = getTexelSize();
                vec2 prevPos = vUv - currentVelocity * deltaTime;
				
				
				// Check if the previous position is within the bounds
				vec2 clampedPos = clamp(prevPos, vec2(0.0), vec2(1.0));

				
				 float advectedK =  getK(clampedPos);

                 // Production Term 
                 float production = 0.5 * viscosity * pow(getDivergence(vUv),2.0);


				// Dissipation of k
				 float dissipation =  pow(currentK,1.5) * 0.09 / k_epsilon_mixingLength   / sqrt(currentK);

				
				 float nextK = (advectedK + production - dissipation) ;
                  if(isObstacle > 0.0){
                      nextK = currentK; //Keep k at same value
                   } else {
                        nextK = nextK +  turbulentIntensity * speed * speed * 0.5  ;
				   }



                gl_FragColor = vec4(max(nextK,0.0), 0.0, 0.0, 1.0);
            }
        `
    });
	
	// Epsilon Shader (Turbulence Dissipation Rate)
	epsilonShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            kTexture: { value: kRenderTarget.texture },
			epsilonTexture : { value : epsilonRenderTarget.texture},
            velocityTexture: { value: velocityRenderTarget.texture },
             obstacleTexture: {value: obstacleBuffer},
            deltaTime: {value : 0.01},
			viscosity: { value: simulationParams.dynamicViscosity},
			density: { value: simulationParams.airDensity},
			speed: {value : simulationParams.speed * 0.01},
			turbulentIntensity : {value : simulationParams.turbulentIntensity},
			resolution : {value: resolution},
			k_epsilon_mixingLength : {value : simulationParams.k_epsilon_mixingLength},

        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
		fragmentShader: `
		    uniform sampler2D kTexture;
			uniform sampler2D epsilonTexture;
            uniform sampler2D velocityTexture;
             uniform sampler2D obstacleTexture;
            uniform float deltaTime;
			uniform float viscosity;
			uniform float density;
			uniform float speed;
			uniform float turbulentIntensity;
			uniform vec2 resolution;
            uniform float k_epsilon_mixingLength;
			varying vec2 vUv;

			vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

			 // Function to get the velocity at a specific point
			vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }
			float getK(vec2 uv){
				return texture2D(kTexture,uv).r;
			}
			float getEpsilon(vec2 uv){
				return texture2D(epsilonTexture,uv).r;
			}
			float getObstacle(vec2 uv) {
               return texture2D(obstacleTexture,uv).r;
            }


           float getDivergence(vec2 uv){
			   vec2 texelSize = getTexelSize();
                float left = getVelocity(uv - vec2(texelSize.x,0.0)).x;
                float right = getVelocity(uv + vec2(texelSize.x,0.0)).x;
				float up = getVelocity(uv + vec2(0.0,texelSize.y)).y;
				float down = getVelocity(uv - vec2(0.0,texelSize.y)).y;
                return 0.5 * (right - left + up - down);
           }


            void main() {
                float isObstacle = getObstacle(vUv);
				  float currentK = getK(vUv);
				  float currentEpsilon = getEpsilon(vUv);
				   vec2 currentVelocity = getVelocity(vUv);
					
                // Calculate the advection term
                vec2 texelSize = getTexelSize();
                vec2 prevPos = vUv - currentVelocity * deltaTime;
				
				
				// Check if the previous position is within the bounds
				vec2 clampedPos = clamp(prevPos, vec2(0.0), vec2(1.0));

			    float advectedEpsilon =  getEpsilon(clampedPos);


                 // Production Term 
                 float production = 0.5 * 1.44 * viscosity *  pow(getDivergence(vUv) * currentK , 2.0)/ currentEpsilon;
 
                 //Dissipation
				 float dissipation =  1.92 * pow(currentEpsilon,2.0) / currentK;

				 float nextEpsilon = advectedEpsilon + production - dissipation;

                   if(isObstacle > 0.0){
                      nextEpsilon= currentEpsilon;
                   } else{
                         nextEpsilon = nextEpsilon +   0.09 * turbulentIntensity * pow(speed,3.0) / k_epsilon_mixingLength;
                   }



                gl_FragColor = vec4(max(nextEpsilon,0.0), 0.0, 0.0, 1.0);
            }
        `
    });
	


    // Velocity shader (Navier-Stokes)
    velocityShaderMaterial = new THREE.ShaderMaterial({
        uniforms: {
            velocityTexture: { value: velocityRenderTarget.texture },
            boundaryTexture: { value: boundaryRenderTarget.texture},
             obstacleTexture: {value: obstacleBuffer},
			  kTexture: { value: kRenderTarget.texture },
			epsilonTexture : { value : epsilonRenderTarget.texture},
            deltaTime: {value : 0.01},
			viscosity: { value: simulationParams.dynamicViscosity},
			density: { value: simulationParams.airDensity},
			speed: {value : simulationParams.speed * 0.01},
			resolution : {value: resolution},
			k_epsilon_mixingLength : {value : simulationParams.k_epsilon_mixingLength}
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
		    uniform sampler2D velocityTexture;
            uniform sampler2D boundaryTexture;
            uniform sampler2D obstacleTexture;
			uniform sampler2D kTexture;
			uniform sampler2D epsilonTexture;
            uniform float deltaTime;
			uniform float viscosity;
			uniform float density;
			uniform float speed;
			uniform vec2 resolution;
			 uniform float k_epsilon_mixingLength;
			varying vec2 vUv;

			vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

			 // Function to get the velocity at a specific point
			vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }

             float getBoundary(vec2 uv) {
               return texture2D(boundaryTexture,uv).r;
            }

             float getObstacle(vec2 uv) {
               return texture2D(obstacleTexture,uv).r;
            }
			float getK(vec2 uv){
				return texture2D(kTexture,uv).r;
			}
			float getEpsilon(vec2 uv){
				return texture2D(epsilonTexture,uv).r;
			}

           float getDivergence(vec2 uv){
			   vec2 texelSize = getTexelSize();
                float left = getVelocity(uv - vec2(texelSize.x,0.0)).x;
                float right = getVelocity(uv + vec2(texelSize.x,0.0)).x;
				float up = getVelocity(uv + vec2(0.0,texelSize.y)).y;
				float down = getVelocity(uv - vec2(0.0,texelSize.y)).y;
                return 0.5 * (right - left + up - down);
           }
 
            void main() {

				 vec2 currentVelocity = getVelocity(vUv);
                  float isBoundary = getBoundary(vUv);
                 float isObstacle = getObstacle(vUv);
				  float currentK = getK(vUv);
                 float currentEpsilon = getEpsilon(vUv);


                // Calculate the advection term
                vec2 texelSize = getTexelSize();
                vec2 prevPos = vUv - currentVelocity * deltaTime;
				
				
				// Check if the previous position is within the bounds
				vec2 clampedPos = clamp(prevPos, vec2(0.0), vec2(1.0));


				// Get advected velocity
				vec2 advectedVelocity = getVelocity(clampedPos);

				// Apply external force (wind)
				vec2 force = vec2(speed,0.0) ;


                // Apply viscosity to diffuse the velocity field
				vec2 diffVel = vec2(0.0);
				
				float turbulentViscosity = 0.09 * density * pow(currentK,2.0) / currentEpsilon; // Calculate turbulent viscosity
				float laplacian = getDivergence(vUv) *  (viscosity + turbulentViscosity) ;
                
                diffVel = (
C:\mygit\BLazy\repo\3dsim\static\js\shaders\velocityShaderComplete.js
Language detected: javascript
import * as THREE from 'three';

// This is the complete content for velocityShader.js
function velocityShader() {
    return new THREE.ShaderMaterial({
        uniforms: {
            velocityTexture: { value: null },
            boundaryTexture: { value: null },
            obstacleTexture: { value: null },
            kTexture: { value: null },
            epsilonTexture: { value: null },
            deltaTime: { value: 0.01 },
            viscosity: { value: 1.81e-5 },
            density: { value: 1.225 },
            speed: { value: 0.25 },
            resolution: { value: new THREE.Vector2(256, 256) },
            k_epsilon_mixingLength: { value: 0.05 }
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
        uniform sampler2D velocityTexture;
            uniform sampler2D boundaryTexture;
            uniform sampler2D obstacleTexture;
            uniform sampler2D kTexture;
            uniform sampler2D epsilonTexture;
            uniform float deltaTime;
            uniform float viscosity;
            uniform float density;
            uniform float speed;
            uniform vec2 resolution;
             uniform float k_epsilon_mixingLength;
            varying vec2 vUv;

            vec2 getTexelSize()
            {
                return 1.0/resolution;
            }

             // Function to get the velocity at a specific point
            vec2 getVelocity(vec2 uv) {
                return texture2D(velocityTexture, uv).xy;
            }

             float getBoundary(vec2 uv) {
               return texture2D(boundaryTexture,uv).r;
            }

             float getObstacle(vec2 uv) {
               return texture2D(obstacleTexture,uv).r;
            }
            float getK(vec2 uv){
                return texture2D(kTexture,uv).r;
            }
            float getEpsilon(vec2 uv){
                return texture2D(epsilonTexture,uv).r;
            }

           float getDivergence(vec2 uv){
               vec2 texelSize = getTexelSize();
                float left = getVelocity(uv - vec2(texelSize.x,0.0)).x;
                float right = getVelocity(uv + vec2(texelSize.x,0.0)).x;
                float up = getVelocity(uv + vec2(0.0,texelSize.y)).y;
                float down = getVelocity(uv - vec2(0.0,texelSize.y)).y;
                return 0.5 * (right - left + up - down);
           }
 
            void main() {

                 vec2 currentVelocity = getVelocity(vUv);
                  float isBoundary = getBoundary(vUv);
                 float isObstacle = getObstacle(vUv);
                  float currentK = getK(vUv);
                 float currentEpsilon = getEpsilon(vUv);


                // Calculate the advection term
                vec2 texelSize = getTexelSize();
                vec2 prevPos = vUv - currentVelocity * deltaTime;
                
                
                // Check if the previous position is within the bounds
                vec2 clampedPos = clamp(prevPos, vec2(0.0), vec2(1.0));


                // Get advected velocity
                vec2 advectedVelocity = getVelocity(clampedPos);

                // Apply external force (wind)
                vec2 force = vec2(speed,0.0) ;


                // Apply viscosity to diffuse the velocity field
                vec2 diffVel = vec2(0.0);
                
				float turbulentViscosity = 0.09 * density * pow(currentK,2.0) / currentEpsilon; // Calculate turbulent viscosity
                float laplacian = getDivergence(vUv) *  (viscosity + turbulentViscosity)/ density;
               
                 diffVel = (
                    (laplacian)
                )* deltaTime;

                // Combine advection, force, and diffusion
                vec2 nextVelocity = advectedVelocity + force * deltaTime + diffVel;
                

                 // Apply boundary conditions
                  if (isBoundary > 0.0) {
                        nextVelocity = vec2(0.0);
                   }

                 if(isObstacle > 0.0){
                     nextVelocity =  vec2(0.0);  //Set velocity of obstacle to 0
                  }

                gl_FragColor = vec4(nextVelocity, 0.0, 1.0);
            }
        `
    });
}
export default velocityShader;
