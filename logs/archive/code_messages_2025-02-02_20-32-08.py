C:\mygit\BLazy\repo\3dsim\CarAirflowSimulation.cs
Language detected: csharp
// CarAirflowSimulation.cs

using UnityEngine;
using System.Collections;

public class CarAirflowSimulation : MonoBehaviour
{
    // Customizable parameters
    public float carLength = 4.5f; // Car length in meters
    public float carWidth = 1.8f;  // Car width in meters
    public float carHeight = 1.2f; // Car height in meters
    public Vector3 airVelocity = new Vector3(10.0f, 0.0f, 0.0f); // Air velocity vector (m/s)
    public float airDensity = 1.225f; // Air density at sea level (kg/m^3)
    public float viscosity = 1.81e-5f; // Air dynamic viscosity (Pa·s)
    public float timeStep = 0.1f; // Time step for simulation (s)

    private ParticleSystem airFlowParticles;
    private ParticleSystem.Particle[] particles;

    void Start()
    {
        InitializeParticleSystem();
    }

    void Update()
    {
        UpdateParameters();
        SimulateAirflow();
    }

    void InitializeParticleSystem()
    {
        airFlowParticles = GetComponent<ParticleSystem>();
        particles = new ParticleSystem.Particle[airFlowParticles.main.maxParticles];
    }

    void UpdateParameters()
    {
        var mainModule = airFlowParticles.main;
        mainModule.simulationSpace = ParticleSystemSimulationSpace.World;

        // Update any particle properties based on the parameters (e.g., emission rate, start size, etc.)
    }

    void SimulateAirflow()
    {
        int numParticlesAlive = airFlowParticles.GetParticles(particles);

        for (int i = 0; i < numParticlesAlive; ++i)
        {
            // Simplified Navier-Stokes equation to update particle positions.
            // This is a placeholder for more complex fluid dynamics calculations.
            Vector3 force = CalculateDragForce(particles[i].velocity);
            particles[i].velocity += force * timeStep;
            particles[i].position += particles[i].velocity * timeStep;
        }

        airFlowParticles.SetParticles(particles, numParticlesAlive);
    }

    Vector3 CalculateDragForce(Vector3 velocity)
    {
        float dragCoefficient = 0.5f; // Placeholder value for drag coefficient
        Vector3 dragForce = -dragCoefficient * airDensity * velocity.sqrMagnitude * velocity / 2.0f;
        return dragForce;
    }
}
C:\mygit\BLazy\repo\3dsim\SimulationUIController.cs
Language detected: csharp
// UIControllerForAirflowSimulation.cs

using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using System.Collections;

public class UIControllerForAirflowSimulation : MonoBehaviour
{
    // References to UI elements
    public InputField lengthInput;
    public InputField widthInput;
    public InputField heightInput;
    public Dropdown airVelocityDropdown;
    public InputField airDensityInput;
    public InputField viscosityInput;
    public Button startStopButton;

    // Reference to our CarAirflowSimulation script
    private CarAirflowSimulation airflowSim;
    
    void Start()
    {
        // Fetch the CarAirflowSimulation component
        airflowSim = FindObjectOfType<CarAirflowSimulation>();

        // Set up event handlers for UI elements
        startStopButton.onClick.AddListener(ToggleSimulation);
        
        airVelocityDropdown.onValueChanged.AddListener(OnAirVelocityChanged);
    }

    public void ToggleSimulation()
    {
        airflowSim.enabled = !airflowSim.enabled;
        // Update button text to indicate current state
        startStopButton.GetComponentInChildren<Text>().text = airflowSim.enabled ? "Stop Simulation" : "Start Simulation";
    }

    public void OnAirVelocityChanged(int index)
    {
        Debug.Log("Air Velocity Changed to: " + GetAirVelocity(index));
        airflowSim.airVelocity = GetAirVelocity(index);
        airflowSim.UpdateParameters();
    }

    private Vector3 GetAirVelocity(int index)
    {
        switch (index)
        {
            case 0:
                return new Vector3(10.0f, 0.0f, 0.0f);
            case 1:
                return new Vector3(-10.0f, 0.0f, 0.0f);
            case 2:
                return new Vector3(0.0f, 10.0f, 0.0f);
            case 3:
                return new Vector3(0.0f, -10.0f, 0.0f);
            default:
                return airflowSim.airVelocity;
        }
    }

    // Helper method to update the CarAirflowSimulation based on UI input
    public void UpdateParametersFromUI()
    {
        if (float.TryParse(lengthInput.text, out float length))
            airflowSim.carLength = length;

        if (float.TryParse(widthInput.text, out float width))
            airflowSim.carWidth = width;

        if (float.TryParse(heightInput.text, out float height))
            airflowSim.carHeight = height;

        if (float.TryParse(airDensityInput.text, out float airDensity))
            airflowSim.airDensity = airDensity;

        if (double.TryParse(viscosityInput.text, out double viscosity))
            airflowSim.viscosity = (float)viscosity;

        UpdateParameters();
    }

    // Method to update any particle properties based on the parameters
    private void UpdateParameters()
    {
        if (airflowSim != null)
            airflowSim.UpdateParameters();
    }
}
C:\mygit\BLazy\repo\3dsim\FluidDynamicsCalculator.cs
Language detected: csharp
// FluidDynamicsCalculator.cs

using UnityEngine;
using System.Collections;

public class FluidDynamicsCalculator : MonoBehaviour
{
    // Parameters
    public float carLength = 4.5f; // Car length in meters
    public float carWidth = 1.8f;  // Car width in meters
    public float carHeight = 1.2f; // Car height in meters
    public Vector3 airVelocity = new Vector3(10.0f, 0.0f, 0.0f); // Air velocity vector (m/s)
    public float airDensity = 1.225f; // Air density at sea level (kg/m^3)
    public float viscosity = 1.81e-5f; // Air dynamic viscosity (Pa·s)
    public float dt = 0.1f; // Time step for simulation (s)

    // Particle system
    private ParticleSystem airFlowParticles;
    private ParticleSystem.Particle[] particles;
    private const int gridSizeX = 10;
    private const int gridSizeY = 10;
    private const int gridSizeZ = 10;
    private Vector3[,] [,] pressureField;
    private Vector3[,] [,] velocityField;
    private float[,] [,] temperatureField;
    
    // Constants
    private const float kinematicViscosity = 1.81e-5f;
    private const float turbulenceKineticEnergy = 1.5f;
    private const float dissipationRate = 0.1f;

    void Start()
    {
        InitializeFields();
        InitializeParticleSystem();
    }

    void Update()
    {
        SimulateFluidDynamics();
    }

    void InitializeParticleSystem()
    {
        airFlowParticles = GetComponent<ParticleSystem>();
        particles = new ParticleSystem.Particle[airFlowParticles.main.maxParticles];

        pressureField = new Vector3[gridSizeX, gridSizeY, gridSizeZ, 3];
        velocityField = new Vector3[gridSizeX, gridSizeY, gridSizeZ, 3];
        temperatureField = new float[gridSizeX, gridSizeY, gridSizeZ];
    }

    void InitializeFields()
    {
        // Initialize fields with initial conditions
        for (int i = 0; i < gridSizeX; i++)
        {
            for (int j = 0; j < gridSizeY; j++)
            {
                for (int k = 0; k < gridSizeZ; k++)
                {
                    pressureField[i, j, k] = new Vector3(0, 0, 0);
                    temperatureField[i, j, k] = 293.15f; // 20 degrees Celsius in Kelvin
                    velocityField[i, j, k] = new Vector3(0, 0, 0);
                }
            }
        }
    }

    void SimulateFluidDynamics()
    {
        ComputePressureField();
        SolveNavierStokesEquations();
        CalculateBoundaryLayer();
        ComputeTurbulenceModel();
        UpdateParticlePositions();
    }

    void ComputePressureField()
    {
        // Compute pressure field using Poisson's equation
        // Placeholder implementation
    }

    void SolveNavierStokesEquations()
    {
        // Solve the full 3D Navier-Stokes equations
        // Placeholder implementation
    }

    void CalculateBoundaryLayer()
    {
        // Compute boundary layer effects
        // Placeholder implementation
    }

    void ComputeTurbulenceModel()
    {
        // Compute turbulence model using k-epsilon model
        // Placeholder implementation
    }

    void UpdateParticlePositions()
    {
        int numParticlesAlive = airFlowParticles.GetParticles(particles);

        for (int i = 0; i < numParticlesAlive; ++i)
        {
            // Compute forces acting on each particle
            Vector3 force = CalculateTotalForce(i, particles[i].position);
            particles[i].velocity += force * dt;
            particles[i].position += particles[i].velocity * dt;
        }

        airFlowParticles.SetParticles(particles, numParticlesAlive);
    }

    Vector3 CalculateTotalForce(int particleIndex, Vector3 position)
    {
        Vector3 dragForce = CalculateDragForce(particles[particleIndex].velocity);
        Vector3 pressureForce = CalculatePressureForce(position);
        Vector3 buoyancyForce = CalculateBuoyancyForce(position);
        
        return dragForce + pressureForce + buoyancyForce;
    }

    Vector3 CalculateDragForce(Vector3 velocity)
    {
        float dragCoefficient = 0.5f; // Placeholder value for drag coefficient
        Vector3 dragForce = -dragCoefficient * airDensity * velocity.sqrMagnitude * velocity / 2.0f;
        return dragForce;
    }

    Vector3 CalculatePressureForce(Vector3 position)
    {
        // Placeholder implementation
        return new Vector3(0, 0, 0);
    }

    Vector3 CalculateBuoyancyForce(Vector3 position)
    {
        // Placeholder implementation
        return new Vector3(0, 0, 0);
    }
}
C:\mygit\BLazy\repo\3dsim\AirflowVisualizer.cs
Language detected: csharp
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;
using System.Linq;

public class AirflowVisualizationSystem : MonoBehaviour
{
    public FluidDynamicsCalculator fluidDynamicsCalc;
    public ParticleSystem airFlowParticles;
    private ParticleSystem.Particle[] particles;

    // For streamline visualization
    public LineRenderer[] streamlines;

    // Color gradients
    public Gradient speedGradient;
    public Gradient pressureGradient;
    public Gradient densityGradient;
    
    // Debug visualization settings
    public bool showStreamlines;
    public bool showSpeedGradient;
    public bool showPressureGradient;
    public bool showDensityGradient;

   void Start()
    {
        InitializeParticleSystem();
        InitializeDebugVisualizations();
    }

    void InitializeParticleSystem()
    {
        particles = new ParticleSystem.Particle[airFlowParticles.main.maxParticles];
    }

    void InitializeDebugVisualizations()
    {
        foreach (LineRenderer lr in streamlines)
        {
            lr.positionCount = 0;
            lr.enabled = showStreamlines;
        }
    }

    void Update()
    {
        UpdateParticleParticles();
        UpdateDebugVisualization();
    }

    void UpdateParticleParticles()
    {
        int numParticlesAlive = airFlowParticles.GetParticles(particles);

        for (int i = 0; i < numParticlesAlive; ++i)
        {
            Vector3 force = CalculateTotalForce(i, particles[i].position);
            particles[i].velocity += force * fluidDynamicsCalc.dt;
            particles[i].position += particles[i].velocity * fluidDynamicsCalc.dt;
        }

        airFlowParticles.SetParticles(particles, numParticlesAlive);
    }

    void UpdateDebugVisualization()
    {
        UpdateStreamlines(particles.ToList().Take((int)(particles.Length * fluidDynamicsCalc.dt)));
        UpdateGradientLines();
    }

    List<Color> CalculateGradientColors(Gradient gradient, float value, float min, float max)
    {
        return new List<Color> { gradient.Evaluate(Mathf.InverseLerp(min, max, value)) };
    }

    void UpdateStreamlines(ParticleSystem.Particle[] particleList)
    {
        if (!showStreamlines || streamlines.Length == 0)
            return;

        foreach (var line in streamlines)
        {
            var points = line.GetPositions().ToList();
            points.AddRange(particleList.Select(p => p.position).ToList());
            line.positionCount = points.Count;
            line.SetPositions(points.ToArray());
        }
    }

    void UpdateGradientLines()
    {
        if (!showSpeedGradient)
            UpdateGradient(Color.clear, speedGradient, "Velocity");

        if (!showPressureGradient)
            UpdateGradient(Color.clear, pressureGradient, "Pressure");

        if (!showDensityGradient)
            UpdateGradient(Color.clear, densityGradient, "Density");
    }

    void UpdateGradient(Color defaultValue, Gradient gradient, string variable)
    {
        // Placeholder for fetching data from the fluid dynamics simulator
        float minVal = 0, maxVal = 20, value;

        switch (variable)
        {
            case "Pressure":
                value = fluidDynamicsCalc.pressureFieldValue; // Example
                break;

            case "Velocity":
                value = fluidDynamicsCalc.velocityFieldValue; // Example
                break;

            case "Density":
                value = fluidDynamicsCalc.densityFieldValue; // Example
                break;

            default:
                value = 0;
                break;
        }

        var colors = CalculateGradientColors(gradient, value, minVal, maxVal);
        Debug.DrawRay(transform.position, transform.forward, colors.First());
    }

    Vector3 CalculateTotalForce(int particleIndex, Vector3 position)
    {
        Vector3 dragForce = CalculateDragForce(fluidDynamicsCalc.particles[particleIndex].velocity);
        Vector3 pressureForce = CalculatePressureForce(position);
        Vector3 buoyancyForce = CalculateBuoyancyForce(position);

        return dragForce + pressureForce + buoyancyForce;
    }

    Vector3 CalculateDragForce(Vector3 velocity)
    {
        float dragCoefficient = 0.5f; // Placeholder value for drag coefficient
        Vector3 dragForce = -dragCoefficient * fluidDynamicsCalc.airDensity * velocity.sqrMagnitude * velocity / 2.0f;
        return dragForce;
    }

    Vector3 CalculatePressureForce(Vector3 position)
    {
        // Placeholder implementation
        return new Vector3(0, 0, 0);
    }

    Vector3 CalculateBuoyancyForce(Vector3 position)
    {
        // Placeholder implementation
        return new Vector3(0, 0, 0);
    }
}
C:\mygit\BLazy\repo\3dsim\CarAirflowSimulationController.cs
Language detected: csharp
// MainControllerForCarAirflowSimulation.cs

using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class MainControllerForCarAirflowSimulation : MonoBehaviour
{
    // References to other scripts and GameObjects
    public CarAirflowSimulation carAirflowSimulation;
    public FluidDynamicsCalculator fluidDynamicsCalculator;
    public AirflowVisualizationSystem airflowVisualization;
    public UIControllerForAirflowSimulation uiController;
    public Button playPauseButton;
    public Button resetButton;

    // Simulation state flags
    private bool isSimulationRunning = false;

    void Start()
    {
        // Initialize references
        carAirflowSimulation = FindObjectOfType<CarAirflowSimulation>();
        fluidDynamicsCalculator = FindObjectOfType<FluidDynamicsCalculator>();
        airflowVisualization = FindObjectOfType<AirflowVisualizationSystem>();
        uiController = FindObjectOfType<UIControllerForAirflowSimulation>();

        // Initialize Play/Pause button and Reset button
        if (playPauseButton != null)
            playPauseButton.onClick.AddListener(ToggleSimulation);

        if (resetButton != null)
            resetButton.onClick.AddListener(ResetSimulation);
    }

    void Update()
    {
        // Manage real-time updates if the simulation is running
        if (isSimulationRunning)
        {
            carAirflowSimulation.Update();
            fluidDynamicsCalculator.Update();
            airflowVisualization.Update();
        }
    }

    public void ToggleSimulation()
    {
        isSimulationRunning = !isSimulationRunning;
        playPauseButton.GetComponentInChildren<Text>().text = isSimulationRunning ? "Pause Simulation" : "Play Simulation";

        carAirflowSimulation.enabled = isSimulationRunning;
        fluidDynamicsCalculator.enabled = isSimulationRunning;
        airflowVisualization.enabled = isSimulationRunning;
    }

    public void ResetSimulation()
    {
        // Reset car model and parameters
        carAirflowSimulation.carLength = 4.5f;
        carAirflowSimulation.carWidth = 1.8f;
        carAirflowSimulation.carHeight = 1.2f;
        carAirflowSimulation.airVelocity = new Vector3(10.0f, 0.0f, 0.0f);
        carAirflowSimulation.airDensity = 1.225f;
        carAirflowSimulation.viscosity = 1.81e-5f;
        carAirflowSimulation.timeStep = 0.1f;

        // Reset physics calculation fields and parameters
        fluidDynamicsCalculator.InitializeFields();
        fluidDynamicsCalculator.InitializeParticleSystem();

        // Reset visualization
        airflowVisualization.InitializeParticleSystem();
        airflowVisualization.InitializeDebugVisualizations();

        // Stop the simulation
        ToggleSimulation();
    }

    public void UserInputHandler(string parameterName, float newValue)
    {
        // Handle user input and update parameters
        switch (parameterName)
        {
            case "Length":
                carAirflowSimulation.carLength = newValue;
                break;
            case "Width":
                carAirflowSimulation.carWidth = newValue;
                break;
            case "Height":
                carAirflowSimulation.carHeight = newValue;
                break;
            case "AirDensity":
                fluidDynamicsCalculator.airDensity = newValue;
                break;
            case "Viscosity":
                fluidDynamicsCalculator.viscosity = newValue;
                break;
            case "VelocityX":
                fluidDynamicsCalculator.airVelocity.x = newValue;
                break;
            case "VelocityY":
                fluidDynamicsCalculator.airVelocity.y = newValue;
                break;
            case "VelocityZ":
                fluidDynamicsCalculator.airVelocity.z = newValue;
                break;
        }

        // Update parameters for all components
        carAirflowSimulation.UpdateParameters();
        fluidDynamicsCalculator.UpdateParameters();
        uiController.UpdateParametersFromUI();
    }
}
C:\mygit\BLazy\repo\3dsim\SimulationSceneSetup.cs
Language detected: csharp
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class SceneInitializer : MonoBehaviour
{
    public Camera mainCamera;
    public Light directionalLight;
    public Canvas uICanvas;
    public GameObject carPrefab;
    public ParticleSystem airFlowParticles;
    public Text debugText;
    public Slider carLengthSlider;
    public Slider carWidthSlider;
    public Slider carHeightSlider;
    public Slider airflowVelocitySlider;
    public Slider airDensitySlider;
    public Slider viscositySlider;
    public Button playPauseButton;
    public Button resetButton;

    private MainControllerForCarAirflowSimulation mainController;

    void Start()
    {
        // Scene Initialization
        InitializeScene();
        InitializeUIComponents();
        InitializeControllers();
        InitializeSimulation();
        SetupDebugView();
    }

    void InitializeScene()
    {
        CreateMainCamera();
        CreateDirectionalLight();
        EnableRealtimeShadows();
    }

    void InitializeUIComponents()
    {
        CreateUICanvas();
        CreateSlidersAndButtons();
    }

    void InitializeControllers()
    {
        CreateMainController();
        LinkUIReferences();
    }

    void InitializeSimulation()
    {
        InstantiateCarModel();
        InitializeAirFlowParticles();
        InitializeComponents();
    }

    void SetupDebugView()
    {
        EnableDebugDrawings();
    }

    void CreateMainCamera()
    {
        mainCamera = Camera.main;
        if (mainCamera == null)
        {
            mainCamera = Camera.main = new GameObject("MainCamera").AddComponent<Camera>();
            mainCamera.transform.position = new Vector3(0, 20, -25);
            mainCamera.transform.rotation = Quaternion.Euler(30, 45, 0);
        }
    }

    void CreateDirectionalLight()
    {
        directionalLight = new GameObject("DirectionalLight").AddComponent<DirectionalLight>();
        directionalLight.transform.rotation = Quaternion.Euler(-30, 45, 0);
    }

    void CreateUICanvas()
    {
        if (uICanvas == null)
        {
            uICanvas = new GameObject("UICanvas").AddComponent<Canvas>();
            uICanvas.renderMode = RenderMode.ScreenSpaceOverlay;
            uICanvas.gameObject.AddComponent<CanvasScaler>();
            uICanvas.gameObject.AddComponent<GraphicRaycaster>();
        }
    }

    void CreateMainController()
    {
        mainController = new GameObject("MainController").AddComponent<MainControllerForCarAirflowSimulation>();
    }

    void CreateSlidersAndButtons()
    {
        // Assuming you have prefabs or UI objects for sliders and buttons
        GameObject lengthSlider = Instantiate(carLengthSlider.gameObject, uICanvas.transform);
        GameObject widthSlider = Instantiate(carWidthSlider.gameObject, uICanvas.transform);
        GameObject heightSlider = Instantiate(carHeightSlider.gameObject, uICanvas.transform);
        GameObject airflowVelocitySlider = Instantiate(airflowVelocitySlider.gameObject, uICanvas.transform);
        GameObject airDensitySlider = Instantiate(airDensitySlider.gameObject, uICanvas.transform);
        GameObject viscositySlider = Instantiate(viscositySlider.gameObject, uICanvas.transform);
        GameObject playPauseButton = Instantiate(this.playPauseButton.gameObject, uICanvas.transform);
        GameObject resetButton = Instantiate(this.resetButton.gameObject, uICanvas.transform);
    }

    void InstantiateCarModel()
    {
        Instantiate(carPrefab, new Vector3(0, 0, 0), Quaternion.identity);
    }

    void InitializeAirFlowParticles()
    {
        airFlowParticles.gameObject.SetActive(true);
    }

    void InitializeComponents()
    {
        carLengthSlider.onValueChanged.AddListener(SetCarLength);
        carWidthSlider.onValueChanged.AddListener(SetCarWidth);
        carHeightSlider.onValueChanged.AddListener(SetCarHeight);
        airflowVelocitySlider.onValueChanged.AddListener(SetAirflowVelocity);
        airDensitySlider.onValueChanged.AddListener(SetAirDensity);
        viscositySlider.onValueChanged.AddListener(SetViscosity);

        mainController.UserInputHandler = HandleUserInput;
    }

    void LinkUIReferences()
    {
        mainController.uiController = new GameObject("UIController").AddComponent<UIControllerForAirflowSimulation>();
        mainController.uiController.lengthInput = carLengthSlider.GetComponent<Slider>().GetComponent<MinSlider>().minSlider;
        mainController.uiController.widthInput = carWidthSlider.GetComponent<Slider>().GetComponent<MinSlider>().minSlider;
        mainController.uiController.heightInput = carHeightSlider.GetComponent<Slider>().GetComponent<MinSlider>().minSlider;
        mainController.uiController.airVelocityDropdown = new GameObject("Dropdown").AddComponent<Dropdown>();
        mainController.uiController.airDensityInput = airDensitySlider.GetComponent<Slider>().GetComponent<MinSlider>().minSlider;
        mainController.uiController.viscosityInput = viscositySlider.GetComponent<Slider>().GetComponent<MinSlider>().minSlider;
        mainController.uiController.startStopButton = playPauseButton.gameObject.GetComponent<Button>();
    }

    void EnableRealtimeShadows()
    {
        QualitySettings.realtimeShadows = true;
    }

    void EnableDebugDrawings()
    {
        debugText.gameObject.SetActive(true);
    }

    void SetCarLength(float value)
    {
        mainController.UserInputHandler("Length", value);
    }

    void SetCarWidth(float value)
    {
        mainController.UserInputHandler("Width", value);
    }

    void SetCarHeight(float value)
    {
        mainController.UserInputHandler("Height", value);
    }

    void SetAirflowVelocity(float value)
    {
        mainController.UserInputHandler("VelocityX", value);
    }

    void SetAirDensity(float value)
    {
        mainController.UserInputHandler("AirDensity", value);
    }

    void SetViscosity(float value)
    {
        mainController.UserInputHandler("Viscosity", value);
    }

    void HandleUserInput(string parameterName, float newValue)
    {
        mainController.UserInputHandler(parameterName, newValue);
    }
}
C:\mygit\BLazy\repo\3dsim\setup_unity_environment.py
Language detected: python
import os
import subprocess
import requests
import zipfile
import shutil

# Constants
UNITY_HUB_VERSION = "3.0.0"
UNITY_URL_TEMPLATE = "https://download.unity3d.com/download_unity/install-command-line/UnitySetup-{version}-mac"
UNITY_PROJECT_NAME = "CarAirflowSimulationProject"
PROJECT_STRUCTURE = ["Assets", "Plugins", "Resources", "Scenes", "Scripts"]
BASE_DIR = os.getcwd()

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded successfully: {save_path}")
    else:
        raise Exception(f"Failed to download file: {response.status_code}")

def install_unity_hub():
    try:
        unity_hub_url = UNITY_URL_TEMPLATE.format(version=UNITY_HUB_VERSION)
        install_path = os.path.join(BASE_DIR, "UnityHub.app")
        download_file(unity_hub_url, install_path)
        print("Unity Hub installed successfully.")
    except Exception as e:
        print(f"Failed to install Unity Hub: {e}")

def create_unity_project(project_name):
    try:
        subprocess.run(["open", "-n", BASE_DIR, "--args", f"-nouse Existing={project_name}"])
        print(f"Unity project '{project_name}' created successfully.")
    except Exception as e:
        print(f"Failed to create Unity project: {e}")

def setup_project_structure(base_dir, structure):
    for folder in structure:
        folder_path = os.path.join(base_dir, folder)
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder '{folder}' created successfully.")
        except Exception as e:
            print(f"Failed to create folder '{folder}': {e}")

if __name__ == "__main__":
    # Install Unity Hub
    install_unity_hub()

    # Create Unity project
    create_unity_project(UNITY_PROJECT_NAME)

    # Wait for the project window to open
    input("Press Enter after opening Unity Hub and creating the project...")

    # Setup project structure
    project_dir = os.path.join(BASE_DIR, UNITY_PROJECT_NAME)
    setup_project_structure(project_dir, PROJECT_STRUCTURE)

    print("Project setup completed successfully.")
C:\mygit\BLazy\repo\3dsim\setup_unity_environment.py
Language detected: python
import os
import subprocess
import requests
import zipfile
import shutil
import platform

# Constants
UNITY_HUB_VERSION = "3.0.0"
UNITY_URL_TEMPLATE = "https://download.unity3d.com/download_unity/install-command-line/UnitySetup-{version}-win"
UNITY_PROJECT_NAME = "CarAirflowSimulationProject"
PROJECT_STRUCTURE = ["Assets", "Plugins", "Resources", "Scenes", "Scripts"]
BASE_DIR = os.getcwd()

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded successfully: {save_path}")
    else:
        raise Exception(f"Failed to download file: {response.status_code}")

def install_unity_hub():
    try:
        unity_hub_url = UNITY_URL_TEMPLATE.format(version=UNITY_HUB_VERSION)
        install_path = os.path.join(BASE_DIR, "UnityHubSetup.exe")
        download_file(unity_hub_url, install_path)

        # Run the installer using PowerShell
        subprocess.run(["powershell", "-Command", f"& {{Start-Process -FilePath '{install_path}' -ArgumentList '/S /D=%ProgramFiles%\\Unity Hub' -Wait}}"], check=True)
        print("Unity Hub installed successfully.")
    except Exception as e:
        print(f"Failed to install Unity Hub: {e}")

def create_unity_project(project_name):
    try:
        # Use PowerShell to run the command to open Unity Hub and create a project
        subprocess.run(["powershell", "-Command", f"Start-Process -FilePath 'Unity Hub' -ArgumentList '--create-project {os.path.join(BASE_DIR, project_name)}'"], check=True)
        print(f"Unity project '{project_name}' created successfully.")
    except Exception as e:
        print(f"Failed to create Unity project: {e}")

def setup_project_structure(base_dir, structure):
    for folder in structure:
        folder_path = os.path.join(base_dir, folder)
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder '{folder}' created successfully.")
        except Exception as e:
            print(f"Failed to create folder '{folder}': {e}")

if __name__ == "__main__":
    # Install Unity Hub
    install_unity_hub()

    # Give time for Unity Hub to launch
    input("Press Enter to continue after Unity Hub has launched...")

    # Create Unity project
    create_unity_project(UNITY_PROJECT_NAME)

    # Give time for Unity Editor to launch and project creation to complete
    input("Press Enter after creating the Unity project to continue...")

    # Setup project structure
    project_dir = os.path.join(BASE_DIR, UNITY_PROJECT_NAME)
    setup_project_structure(project_dir, PROJECT_STRUCTURE)

    print("Project setup completed successfully.")
