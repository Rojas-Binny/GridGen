"""
Generate test scenarios with both valid and invalid configurations.
This will create sample scenarios that can be used to test the validation system.
"""

import os
import json
import datetime

# Setup output directory
SCENARIOS_DIR = os.path.join("data", "processed")
os.makedirs(SCENARIOS_DIR, exist_ok=True)

def create_scenario(scenario_id, name, description, config, metadata):
    """Create a scenario with the given configuration"""
    
    # Create base network structure
    network = {
        "base_mva": 100,
        "bus": [],
        "ac_line": [],
        "simple_dispatchable_device": []
    }
    
    # Add buses
    for i in range(config["num_buses"]):
        bus_type = "SLACK" if i == 0 else "PV" if i < config["num_generators"] else "PQ"
        voltage = config.get("voltage", 1.0)
        
        # For invalid voltage scenarios, make some buses have invalid voltages
        if config.get("invalid_voltage", False) and i > 0:
            if i % 2 == 0:
                voltage = 0.92  # Below minimum
            else:
                voltage = 1.07  # Above maximum
        
        network["bus"].append({
            "bus_id": f"Bus{i+1}",
            "type": bus_type,
            "area": 1,
            "vm": voltage,
            "va": 0.0,
            "base_kv": 230.0,
            "zone": 1,
            "vmax": 1.1,
            "vmin": 0.9,
            "vm_lb": 0.95,
            "vm_ub": 1.05,
            "initial_status": {
              "vm": voltage,
              "va": 0.0
            }
        })
    
    # Add lines
    for i in range(config["num_buses"] - 1):
        # Connect in a ring for more than 2 buses
        to_bus = i + 2 if i + 2 <= config["num_buses"] else 1
        
        line_capacity = config.get("line_capacity", 300.0)
        r_value = config.get("r_value", 0.01)
        x_value = config.get("x_value", 0.1)
        
        network["ac_line"].append({
            "uid": f"Line{i+1}-{to_bus}",
            "fr_bus": f"Bus{i+1}",
            "to_bus": f"Bus{to_bus}",
            "r": r_value,
            "x": x_value,
            "b": 0.02,
            "rate_a": line_capacity,
            "rate_b": line_capacity + 50,
            "rate_c": line_capacity + 100,
            "status": 1,
            "mva_ub_nom": line_capacity,
            "initial_status": {
              "on_status": 1
            }
        })
    
    # Add generators and loads
    for i in range(config["num_generators"]):
        pg_value = config.get("pg_value", 100.0)
        network["simple_dispatchable_device"].append({
            "uid": f"Gen{i+1}",
            "bus": f"Bus{i+1}",
            "device_type": "producer",
            "pg": pg_value,
            "qg": 20.0,
            "qmax": 75.0,
            "qmin": -75.0,
            "vg": 1.0,
            "status": 1,
            "pmax": 150.0,
            "pmin": 20.0,
            "initial_status": {
              "p": pg_value / 100,
              "q": 0.1
            }
        })
    
    for i in range(config["num_loads"]):
        bus_idx = min(config["num_generators"] + i + 1, config["num_buses"])
        pd_value = config.get("pd_value", 100.0)
        network["simple_dispatchable_device"].append({
            "uid": f"Load{i+1}",
            "bus": f"Bus{bus_idx}",
            "device_type": "consumer",
            "pd": pd_value,
            "qd": 20.0,
            "status": 1,
            "initial_status": {
              "p": pd_value / 100,
              "q": 0.08
            }
        })
    
    # Create full scenario
    scenario = {
        "scenario_id": scenario_id,
        "name": name,
        "description": description,
        "network": network,
        "metadata": metadata
    }
    
    # Save to file
    file_path = os.path.join(SCENARIOS_DIR, f"{scenario_id}.json")
    with open(file_path, "w") as f:
        json.dump(scenario, f, indent=2)
    
    print(f"Created scenario: {file_path}")
    return scenario

# Create valid scenarios
valid_scenarios = [
    {
        "id": "valid_balanced_system",
        "name": "Small Balanced System",
        "description": "A small, balanced 3-bus system with 2 generators and 1 load",
        "config": {
            "num_buses": 3,
            "num_generators": 2,
            "num_loads": 1,
            "voltage": 1.0,
            "line_capacity": 300.0,
            "pg_value": 100.0,
            "pd_value": 150.0
        },
        "metadata": {
            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0",
            "reliability_level": "high",
            "congestion_level": "low",
            "voltage_profile": "flat"
        }
    },
    {
        "id": "valid_medium_system",
        "name": "Medium Balanced System",
        "description": "A medium-sized, balanced 4-bus system with 2 generators and 2 loads",
        "config": {
            "num_buses": 4,
            "num_generators": 2,
            "num_loads": 2,
            "voltage": 1.0,
            "line_capacity": 300.0,
            "pg_value": 150.0,
            "pd_value": 120.0
        },
        "metadata": {
            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0",
            "reliability_level": "high",
            "congestion_level": "low",
            "voltage_profile": "flat"
        }
    }
]

# Create invalid scenarios
invalid_scenarios = [
    {
        "id": "invalid_voltage_violations",
        "name": "System with Voltage Violations",
        "description": "A 5-bus system with voltage violations (below 0.95 or above 1.05)",
        "config": {
            "num_buses": 5,
            "num_generators": 1,
            "num_loads": 4,
            "invalid_voltage": True,
            "line_capacity": 300.0,
            "pg_value": 100.0,
            "pd_value": 120.0
        },
        "metadata": {
            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0",
            "reliability_level": "low",
            "congestion_level": "high",
            "voltage_profile": "stressed"
        }
    },
    {
        "id": "invalid_overload_lines",
        "name": "System with Line Overloads",
        "description": "A 4-bus system with line overloads due to insufficient capacity",
        "config": {
            "num_buses": 4,
            "num_generators": 1,
            "num_loads": 3,
            "voltage": 1.0,
            "line_capacity": 150.0,  # lower capacity
            "pg_value": 300.0,       # higher generation
            "pd_value": 250.0        # higher load
        },
        "metadata": {
            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0",
            "reliability_level": "low",
            "congestion_level": "high",
            "voltage_profile": "flat"
        }
    },
    {
        "id": "invalid_load_imbalance",
        "name": "System with Load-Generation Imbalance",
        "description": "A 6-bus system with too many loads per generator",
        "config": {
            "num_buses": 6,
            "num_generators": 1,
            "num_loads": 5,  # 5 loads for 1 generator
            "voltage": 1.0,
            "line_capacity": 300.0,
            "pg_value": 120.0,
            "pd_value": 100.0
        },
        "metadata": {
            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0",
            "reliability_level": "low",
            "congestion_level": "medium",
            "voltage_profile": "varied"
        }
    }
]

def main():
    print("Generating test scenarios...")
    
    # Create valid scenarios
    print("\nCreating valid scenarios:")
    for scenario in valid_scenarios:
        create_scenario(
            scenario["id"],
            scenario["name"],
            scenario["description"],
            scenario["config"],
            scenario["metadata"]
        )
    
    # Create invalid scenarios
    print("\nCreating invalid scenarios:")
    for scenario in invalid_scenarios:
        create_scenario(
            scenario["id"],
            scenario["name"],
            scenario["description"],
            scenario["config"],
            scenario["metadata"]
        )
    
    print("\nAll test scenarios created successfully!")
    print(f"Scenarios are located in: {os.path.abspath(SCENARIOS_DIR)}")
    print("\nValid scenarios:")
    for scenario in valid_scenarios:
        print(f"- {scenario['id']}.json: {scenario['name']}")
    
    print("\nInvalid scenarios:")
    for scenario in invalid_scenarios:
        print(f"- {scenario['id']}.json: {scenario['name']}")

if __name__ == "__main__":
    main() 