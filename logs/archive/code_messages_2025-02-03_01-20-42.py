C:\mygit\BLazy\repo\reroute\route_optimizer.py
Language detected: python
C:\mygit\BLazy\repo\reroute\route_analysis.py
Language detected: python
# Import necessary libraries
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from datetime import datetime

# Function to calculate total distance traveled for a route
def calculate_total_distance(route):
    """Calculate total distance traveled for a route"""
    total_distance = 0
    for i in range(len(route) - 1):
        lat1, lon1 = route.iloc[i]['latitude'], route.iloc[i]['longitude']
        lat2, lon2 = route.iloc[i+1]['latitude'], route.iloc[i+1]['longitude']
        distance = geodesic((lat1, lon1), (lat2, lon2)).miles
        total_distance += distance
    return total_distance

# Function to calculate sales distribution percentages and deviation from targets
def calculate_sales_distribution(route, targets):
    """Calculate sales distribution percentages and deviation from targets"""
    sales = route['sales'].sum()
    distribution_percentage = (sales / targets) * 100
    deviation = abs(distribution_percentage - 100)
    return distribution_percentage, deviation

# Function to calculate geographic clustering metrics (average distance between stops within same route)
def calculate_geographic_clustering(route):
    """Calculate geographic clustering metrics (average distance between stops within same route)"""
    distances = []
    for i in range(len(route) - 1):
        lat1, lon1 = route.iloc[i]['latitude'], route.iloc[i]['longitude']
        lat2, lon2 = route.iloc[i+1]['latitude'], route.iloc[i+1]['longitude']
        distance = geodesic((lat1, lon1), (lat2, lon2)).miles
        distances.append(distance)
    average_distance = np.mean(distances)
    return average_distance

# Load both original and optimized route data
def load_route_data(original_route_file, optimized_route_file):
    """Load both original and optimized route data"""
    original_route = pd.read_csv(original_route_file)
    optimized_route = pd.read_csv(optimized_route_file)
    return original_route, optimized_route

# Calculate metrics for both datasets
def calculate_metrics(original_route, optimized_route, targets):
    """Calculate metrics for both datasets"""
    original_total_distance = calculate_total_distance(original_route)
    optimized_total_distance = calculate_total_distance(optimized_route)
    original_distribution_percentage, original_deviation = calculate_sales_distribution(original_route, targets)
    optimized_distribution_percentage, optimized_deviation = calculate_sales_distribution(optimized_route, targets)
    original_average_distance = calculate_geographic_clustering(original_route)
    optimized_average_distance = calculate_geographic_clustering(optimized_route)
    return original_total_distance, optimized_total_distance, original_distribution_percentage, optimized_distribution_percentage, original_deviation, optimized_deviation, original_average_distance, optimized_average_distance

# Compare and report improvements
def compare_and_report_improvements(original_total_distance, optimized_total_distance, original_distribution_percentage, optimized_distribution_percentage, original_deviation, optimized_deviation, original_average_distance, optimized_average_distance):
    """Compare and report improvements"""
    distance_improvement = (original_total_distance - optimized_total_distance) / original_total_distance * 100
    distribution_improvement = (original_deviation - optimized_deviation) / original_deviation * 100
    clustering_improvement = (original_average_distance - optimized_average_distance) / original_average_distance * 100
    return distance_improvement, distribution_improvement, clustering_improvement

# Save results to a cumulative log file
def save_results_to_log_file(results, log_file):
    """Save results to a cumulative log file"""
    with open(log_file, 'a') as f:
        f.write(f"{results}\n")

# Main function
def main():
    # Load route data
    original_route_file = 'original_route.csv'
    optimized_route_file = 'optimized_route.csv'
    original_route, optimized_route = load_route_data(original_route_file, optimized_route_file)

    # Define targets
    targets = 1000

    # Calculate metrics
    original_total_distance, optimized_total_distance, original_distribution_percentage, optimized_distribution_percentage, original_deviation, optimized_deviation, original_average_distance, optimized_average_distance = calculate_metrics(original_route, optimized_route, targets)

    # Compare and report improvements
    distance_improvement, distribution_improvement, clustering_improvement = compare_and_report_improvements(original_total_distance, optimized_total_distance, original_distribution_percentage, optimized_distribution_percentage, original_deviation, optimized_deviation, original_average_distance, optimized_average_distance)

    # Create a timestamp and iteration number
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    iteration_number = 1

    # Create a results string
    results = f"Timestamp: {timestamp}, Iteration Number: {iteration_number}, Original Total Distance: {original_total_distance}, Optimized Total Distance: {optimized_total_distance}, Original Distribution Percentage: {original_distribution_percentage}, Optimized Distribution Percentage: {optimized_distribution_percentage}, Original Deviation: {original_deviation}, Optimized Deviation: {optimized_deviation}, Original Average Distance: {original_average_distance}, Optimized Average Distance: {optimized_average_distance}, Distance Improvement: {distance_improvement}, Distribution Improvement: {distribution_improvement}, Clustering Improvement: {clustering_improvement}"

    # Save results to log file
    log_file = 'log_file.txt'
    save_results_to_log_file(results, log_file)

    # Print summary to console
    print(results)

# Run main function
if __name__ == "__main__":
    main()
C:\mygit\BLazy\repo\reroute\route_analysis_runner.py
Language detected: python
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from route_optimizer import RouteOptimizer
from route_analysis import RouteAnalyzer

def run_optimization_iterations(csv_file, max_iterations=10, improvement_threshold=1):
    """
    Run multiple iterations of route optimization and track improvements.

    :param csv_file: Path to the input CSV file.
    :param max_iterations: Maximum number of iterations to run.
    :param improvement_threshold: Minimum improvement percentage required to continue iterations.
    """
    # Create RouteOptimizer and RouteAnalyzer instances
    depot_coords = (39.341270, -76.479261)
    depot_address = "8912 Yellow Brick rd. Rosedale, MD 21237"
    optimizer = RouteOptimizer(depot_coords, depot_address)
    analyzer = RouteAnalyzer()

    # Load initial data
    optimizer.load_and_process_data(csv_file)
    original_df = pd.read_csv(csv_file)

    # Initialize tracking variables
    improvements = []
    distances = []
    sales_balances = []
    clustering_efficiencies = []

    for iteration in range(max_iterations):
        print(f"Iteration {iteration + 1}...")
        
        # Optimize routes
        optimizer.optimize_routes_main()
        updated_df = optimizer.data_df.copy()
        
        # Analyze improvements
        improvements_dict = analyzer.analyze_improvement(original_df, updated_df)
        improvement = improvements_dict['total_distance']['improvement_pct']
        improvements.append(improvement)
        distances.append(improvements_dict['total_distance']['optimized'])
        sales_balances.append(improvements_dict['sales_balance_improvement']['improvement_pct'])
        clustering_efficiencies.append(improvements_dict['clustering_efficiency'])

        # Save updated routes to CSV
        optimizer.save_results_to_csv(f"updated_reroute_{iteration}.csv")

        # Check for stopping criteria
        if improvement < improvement_threshold:
            print("Improvements have plateaued. Stopping iterations.")
            break

        # Update original data for next iteration
        original_df = updated_df.copy()

    # Generate summary statistics and visualizations
    plt.figure(figsize=(10, 6))
    plt.plot(improvements)
    plt.xlabel("Iteration")
    plt.ylabel("Improvement Percentage")
    plt.title("Route Optimization Improvements Over Iterations")
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(distances)
    plt.xlabel("Iteration")
    plt.ylabel("Total Distance")
    plt.title("Total Distance Over Iterations")
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(sales_balances)
    plt.xlabel("Iteration")
    plt.ylabel("Sales Balance Improvement Percentage")
    plt.title("Sales Balance Improvements Over Iterations")
    plt.show()

    plt.figure(figsize=(10, 6))
    for i in range(1, 4):
        efficiencies = [clustering_efficiencies[j][str(i)] for j in range(len(clustering_efficiencies))]
        plt.plot(efficiencies, label=f"Route {i}")
    plt.xlabel("Iteration")
    plt.ylabel("Clustering Efficiency")
    plt.title("Clustering Efficiencies Over Iterations")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run_optimization_iterations('reroute.csv')
