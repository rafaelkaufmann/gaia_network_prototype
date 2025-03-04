#!/usr/bin/env python3
"""
Gaia Network Web Client Demo

This script demonstrates how to interact with the Gaia Network nodes
exposed as web services. It follows a similar flow to the original demo
but uses HTTP requests instead of direct method calls.

Each node is exposed as a separate web service on a different port:
- Node A (Real Estate Finance): http://127.0.0.1:8011
- Node B (Climate Risk): http://127.0.0.1:8012
- Node C (Actuarial Data): http://127.0.0.1:8013
"""

import json
import requests
import time
from pprint import pprint


def print_separator(title):
    """Print a separator with a title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")


def main():
    """Run the Gaia Network web client demo."""
    # Base URLs for each node
    node_a_url = "http://127.0.0.1:8011"
    node_b_url = "http://127.0.0.1:8012"
    node_c_url = "http://127.0.0.1:8013"
    
    print_separator("Gaia Network Web Client Demo")
    
    # Get information about the nodes
    print("Getting node information...")
    node_a_info = requests.get(f"{node_a_url}/info").json()
    node_b_info = requests.get(f"{node_b_url}/info").json()
    node_c_info = requests.get(f"{node_c_url}/info").json()
    
    print(f"Node A (Real Estate Finance): {node_a_info['id']}")
    print(f"Node B (Climate Risk): {node_b_info['id']}")
    print(f"Node C (Actuarial Data): {node_c_info['id']}")
    
    # Step 1: Set location and IPCC scenario
    print_separator("Step 1: Set location and IPCC scenario")
    location = "Miami"
    ipcc_scenario = "SSP2-4.5"
    print(f"Location: {location}")
    print(f"IPCC Scenario: {ipcc_scenario}")
    
    # Step 2: Get Node B's schema
    print_separator("Step 2: Get Node B's schema")
    schema_response = requests.get(f"{node_b_url}/schema").json()
    
    print("\nLatent variables:")
    for var in schema_response["latents"]:
        print(f"  - {var['name']}: {var['description']}")
    
    print("\nObservable variables:")
    for var in schema_response["observables"]:
        print(f"  - {var['name']}: {var['description']}")
    
    print("\nCovariates:")
    for var in schema_response["covariates"]:
        print(f"  - {var['name']}: {var['description']}")
    
    # Step 3: Query Node B for flood probability
    print_separator("Step 3: Query Node B for flood probability")
    print(f"Querying flood probability for {location} under {ipcc_scenario} scenario...")
    
    flood_response = requests.post(
        f"{node_b_url}/query/flood-probability",
        json={
            "location": location,
            "ipcc_scenario": ipcc_scenario
        }
    ).json()
    
    print("Raw flood response:", flood_response)
    
    print("Response type:", flood_response["response_type"])
    
    if flood_response["response_type"] == "posterior":
        distribution_data = flood_response["content"]["distribution"]
        print("\nFlood probability distribution:")
        print(f"  - Name: {distribution_data['name']}")
        print(f"  - Type: {distribution_data['distribution']['type']}")
        print(f"  - Parameters: {distribution_data['distribution']['parameters']}")
        print(f"  - Metadata: {distribution_data['metadata']}")
        
        # Calculate expected value for Beta distribution
        alpha = distribution_data['distribution']['parameters']['alpha']
        beta = distribution_data['distribution']['parameters']['beta']
        expected_value = alpha / (alpha + beta)
        print(f"\nExpected flood probability: {expected_value:.4f}")
    
    # Step 4: Query Node A for ROI
    print_separator("Step 4: Query Node A for ROI")
    print("Calculating expected ROI for the real estate project...")
    
    roi_response = requests.post(
        f"{node_a_url}/query/roi",
        json={
            "location": location,
            "ipcc_scenario": ipcc_scenario
        }
    ).json()
    
    if roi_response["response_type"] == "posterior":
        roi_dist_data = roi_response["content"]["distribution"]
        print("\nROI distribution:")
        print(f"  - Name: {roi_dist_data['name']}")
        print(f"  - Type: {roi_dist_data['distribution']['type']}")
        print(f"  - Parameters: {roi_dist_data['distribution']['parameters']}")
        print(f"  - Metadata: {roi_dist_data['metadata']}")
        
        expected_roi = roi_dist_data['distribution']['parameters']['mean']
        print(f"\nExpected ROI: {expected_roi:.2%}")
    
    # Step 5: Add new data to Node C
    print_separator("Step 5: Add new data to Node C")
    print("Adding new actuarial data to Node C...")
    
    add_data_response = requests.post(
        f"{node_c_url}/add-data",
        json={
            "location": location,
            "value": 0.4
        }
    ).json()
    
    print("Status:", add_data_response.get("status", "success"))
    
    # Step 6: Query Node C for updated data
    print_separator("Step 6: Query Node C for updated data")
    print("Querying Node C for updated actuarial data...")
    
    actuarial_response = requests.post(
        f"{node_c_url}/query/historical-data",
        json={
            "location": location
        }
    ).json()
    
    if actuarial_response["response_type"] == "posterior":
        actuarial_dist_data = actuarial_response["content"]["distribution"]
        print("\nActuarial data distribution:")
        print(f"  - Name: {actuarial_dist_data['name']}")
        print(f"  - Type: {actuarial_dist_data['distribution']['type']}")
        print(f"  - Parameters: {actuarial_dist_data['distribution']['parameters']}")
        print(f"  - Metadata: {actuarial_dist_data['metadata']}")
    
    # Step 7: Update Node B with new data
    print_separator("Step 7: Update Node B with new data")
    print("Updating Node B with new actuarial data...")
    
    update_response = requests.post(
        f"{node_b_url}/update",
        json={
            "location": location
        }
    ).json()
    
    # Handle the update response safely with error checking
    if "response_type" in update_response and "content" in update_response:
        print("Response type:", update_response["response_type"])
        print("Update status:", update_response["content"]["status"])
    else:
        print("Update completed with response:", update_response)
    
    # Step 8: Query Node B again for updated flood probability
    print_separator("Step 8: Query Node B again for updated flood probability")
    print("Querying updated flood probability for Miami under SSP2-4.5 scenario...")
    
    updated_flood_response = requests.post(
        f"{node_b_url}/query/flood-probability",
        json={
            "location": location,
            "ipcc_scenario": ipcc_scenario
        }
    ).json()
    
    if updated_flood_response["response_type"] == "posterior":
        updated_dist_data = updated_flood_response["content"]["distribution"]
        print("\nUpdated flood probability distribution:")
        print(f"  - Name: {updated_dist_data['name']}")
        print(f"  - Type: {updated_dist_data['distribution']['type']}")
        print(f"  - Parameters: {updated_dist_data['distribution']['parameters']}")
        print(f"  - Metadata: {updated_dist_data['metadata']}")
        
        # Calculate expected value for Beta distribution
        alpha = updated_dist_data['distribution']['parameters']['alpha']
        beta = updated_dist_data['distribution']['parameters']['beta']
        updated_expected_value = alpha / (alpha + beta)
        print(f"\nUpdated expected flood probability: {updated_expected_value:.4f}")
        print(f"Change in flood probability: {updated_expected_value - expected_value:.4f}")
    
    # Step 9: Query Node B with rationale
    print_separator("Step 9: Query Node B with rationale")
    print("Querying flood probability with rationale for Miami under SSP2-4.5 scenario...")
    
    rationale_response = requests.post(
        f"{node_b_url}/query/flood-probability",
        json={
            "location": location,
            "ipcc_scenario": ipcc_scenario,
            "rationale": True
        }
    ).json()
    
    if rationale_response["response_type"] == "posterior":
        rationale_dist_data = rationale_response["content"]["distribution"]
        print("\nFlood probability distribution with rationale:")
        print(f"  - Name: {rationale_dist_data['name']}")
        print(f"  - Type: {rationale_dist_data['distribution']['type']}")
        print(f"  - Parameters: {rationale_dist_data['distribution']['parameters']}")
        
        if "rationale" in rationale_response["content"]:
            print("\nRationale:\n")
            rationale = rationale_response["content"]["rationale"]
            
            if "calculation_details" in rationale:
                print("Calculation details:")
                for key, value in rationale["calculation_details"].items():
                    print(f"  - {key}: {value}")
            
            if "observations" in rationale:
                print("\nObservations that caused the update:")
                for obs in rationale["observations"]:
                    print(f"  - {obs['variable_name']}: {obs['value']} (timestamp: {obs['timestamp']})")
    
    # Step 10: Query Node A for updated ROI
    print_separator("Step 10: Query Node A for updated ROI")
    print("Recalculating expected ROI for the real estate project...")
    
    updated_roi_response = requests.post(
        f"{node_a_url}/query/roi",
        json={
            "location": location,
            "ipcc_scenario": ipcc_scenario
        }
    ).json()
    
    if updated_roi_response["response_type"] == "posterior":
        updated_roi_dist_data = updated_roi_response["content"]["distribution"]
        print("\nUpdated ROI distribution:")
        print(f"  - Name: {updated_roi_dist_data['name']}")
        print(f"  - Type: {updated_roi_dist_data['distribution']['type']}")
        print(f"  - Parameters: {updated_roi_dist_data['distribution']['parameters']}")
        print(f"  - Metadata: {updated_roi_dist_data['metadata']}")
        
        updated_expected_roi = updated_roi_dist_data['distribution']['parameters']['mean']
        print(f"\nUpdated expected ROI: {updated_expected_roi:.2%}")
        print(f"Change in ROI: {updated_expected_roi - expected_roi:.2%}")
    
    print_separator("Demo Complete")


if __name__ == "__main__":
    main()
