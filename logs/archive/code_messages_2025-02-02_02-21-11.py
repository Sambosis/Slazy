C:\mygit\BLazy\repo\3dsim\main.py
Language detected: python
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
import numpy as np
from scipy.interpolate import griddata
import uvicorn

app = FastAPI()

# Configure static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates directory
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/simulation")
async def run_simulation(
    length: float = 1.0, #car length in meters
    height: float = 0.5, #car height in meters
    width: float = 0.4, #car width in meters
    speed: float = 25, # m/s
    air_density: float=1.225, #kg/m^3
    viscosity: float=1.81e-5 #
):
    """
    Simulates airflow around a car using a simplified 2D CFD.

    Args:
    length (float): car's length
    height (float): car's height
    width (float): car's width
        speed (float): Airflow speed (m/s),
        air_density (float): Air density (kg/m^3),
        viscosity: Air Viscosity (Pa*s)

    Returns:
        dict: A dictionary containing the x,y grid and the pressure values
        
    """
    try:
        # Set up the simulation grid
        x = np.linspace(-length/2, length*1.5, 20)
        y = np.linspace(-height/2, height*1.5, 20)
    
        X, Y = np.meshgrid(x, y)
        
        # Define car shape as a rectangle
        car = (np.abs(X) <= length/2) & (np.abs(Y) <= height/2)
        
                #set initial pressure field
        pressure=np.zeros_like(X)
        
        # Initial velocity field approximation (potential flow)
        velocity_mag = np.sqrt(np.sum(speed**2, axis=0)) if isinstance(speed,np.ndarray) else speed
        u = np.ones_like(X)*velocity_mag
        v = np.zeros_like(X)
        
        
        for _ in range(500):
            # Compute pressure gradient from momentum equation (simplified)
            dp_dx = -air_density * (u * np.gradient(u, x[1]-x[0], axis=1)  )
            dp_dy = -air_density * ( v*np.gradient(v, y[1]-y[0], axis=0))
            
            # Update pressure field
            pressure=pressure+0.01*(-dp_dx-dp_dy)
            
            #boundary condition
            pressure[car]=0


        # Prepare resuts to be used in the frontend
        results = {
            "x_coords": X.tolist(),
            "y_coords": Y.tolist(),
            "pressure": pressure.tolist(),
            "car": car.tolist()
        }
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
