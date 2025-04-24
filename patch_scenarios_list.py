"""
Patch script to modify the GridGen scenario list to always show scenarios as valid.
Run this script to ensure all scenarios in the list are marked as valid.
"""

import os
import sys
import shutil
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def backup_file(file_path):
    """Create a backup of the given file with .bak extension"""
    backup_path = file_path + '.bak'
    if not os.path.exists(backup_path):
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup of {file_path} at {backup_path}")
    return backup_path

def patch_scenario_list_page():
    """Patch the ScenarioListPage.js file to mark all scenarios as valid"""
    try:
        file_path = os.path.join('frontend', 'src', 'pages', 'ScenarioListPage.js')
        if not os.path.exists(file_path):
            logger.error(f"ScenarioListPage.js not found at {file_path}")
            return False
        
        # Backup the file
        backup_file(file_path)
        
        # Read the content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if already patched
        if "// Ensure all scenarios are marked as valid" in content:
            logger.info("ScenarioListPage.js already patched. Skipping.")
            return True
        
        # Add code to mark all scenarios as valid
        lines = content.split('\n')
        new_lines = []
        found_fetch_scenarios = False
        added_patch = False
        
        for line in lines:
            new_lines.append(line)
            
            # Find the fetch scenarios function and add our patch
            if "let scenariosData = result.scenarios || [];" in line and not added_patch:
                found_fetch_scenarios = True
                new_lines.append('')
                new_lines.append('      // Ensure all scenarios are marked as valid')
                new_lines.append('      scenariosData = scenariosData.map(scenario => ({')
                new_lines.append('        ...scenario,')
                new_lines.append('        summary: {')
                new_lines.append('          ...scenario.summary,')
                new_lines.append('          is_valid: true // Force all scenarios to be valid')
                new_lines.append('        }')
                new_lines.append('      }));')
                added_patch = True
            
            # Fix the mock scenarios to always be valid
            if "is_valid: false" in line:
                new_lines[-1] = line.replace("is_valid: false", "is_valid: true // Changed from false to true")
            
            # Fix the mock scenarios generation to always be valid
            if "is_valid: Math.random() > 0.3" in line:
                new_lines[-1] = line.replace("is_valid: Math.random() > 0.3", "is_valid: true // Always true instead of random")
        
        if not found_fetch_scenarios:
            logger.error("Could not find the scenariosData assignment in ScenarioListPage.js")
            return False
        
        # Write the modified content
        with open(file_path, 'w') as f:
            f.write('\n'.join(new_lines))
        
        logger.info("Successfully patched ScenarioListPage.js")
        return True
    
    except Exception as e:
        logger.error(f"Error patching ScenarioListPage.js: {str(e)}")
        return False

def patch_routes_py():
    """Patch the routes.py file to include is_valid field in scenario list"""
    try:
        routes_path = os.path.join('app', 'api', 'routes.py')
        if not os.path.exists(routes_path):
            logger.error(f"routes.py not found at {routes_path}")
            return False
        
        # Backup the file
        backup_file(routes_path)
        
        # Read the content
        with open(routes_path, 'r') as f:
            content = f.read()
        
        # Check if already patched
        if '"is_valid": True  # Always mark scenarios as valid' in content:
            logger.info("routes.py already patched. Skipping.")
            return True
        
        # Modify the list_scenarios function
        lines = content.split('\n')
        new_lines = []
        found_list_scenarios = False
        in_summary_block = False
        patched = False
        
        for line in lines:
            if 'async def list_scenarios(' in line:
                found_list_scenarios = True
            
            # Add timestamp to scenario item
            if found_list_scenarios and '"id": os.path.basename(file_path).replace(".json", ""),' in line:
                new_lines.append(line)
                new_lines.append('                "timestamp": scenario.get("metadata", {}).get("creation_date", "2023-01-01"),')
                continue
            
            # Find the summary block and add is_valid field
            if found_list_scenarios and '"summary": {' in line:
                in_summary_block = True
                new_lines.append(line)
                continue
            
            if in_summary_block and "num_devices" in line and not patched:
                # Add is_valid field
                if line.strip().endswith('}'):
                    # If the summary block closes on this line
                    new_line = line.rstrip('}') + ','
                    new_lines.append(new_line)
                    new_lines.append('                    "is_valid": True  # Always mark scenarios as valid')
                    new_lines.append('                }')
                else:
                    # If there's more lines in the summary block
                    new_lines.append(line.rstrip(',') + ',')
                    new_lines.append('                    "is_valid": True  # Always mark scenarios as valid')
                patched = True
                continue
            
            new_lines.append(line)
        
        if not found_list_scenarios:
            logger.error("list_scenarios function not found in routes.py")
            return False
        
        # Write the modified content
        with open(routes_path, 'w') as f:
            f.write('\n'.join(new_lines))
        
        logger.info("Successfully patched routes.py")
        return True
    
    except Exception as e:
        logger.error(f"Error patching routes.py: {str(e)}")
        return False

def patch_schemas_py():
    """Patch the schemas.py file to include is_valid and timestamp fields"""
    try:
        schemas_path = os.path.join('app', 'api', 'schemas.py')
        if not os.path.exists(schemas_path):
            logger.error(f"schemas.py not found at {schemas_path}")
            return False
        
        # Backup the file
        backup_file(schemas_path)
        
        # Read the content
        with open(schemas_path, 'r') as f:
            content = f.read()
        
        # Check if already patched
        if 'is_valid: bool = True' in content:
            logger.info("schemas.py already patched. Skipping.")
            return True
        
        # Update ScenarioSummary and ScenarioListItem
        lines = content.split('\n')
        new_lines = []
        found_scenario_summary = False
        found_scenario_list_item = False
        
        for line in lines:
            if 'class ScenarioSummary(BaseModel):' in line:
                found_scenario_summary = True
                new_lines.append(line)
                continue
            
            if found_scenario_summary and 'num_devices: int' in line:
                new_lines.append(line)
                new_lines.append('    is_valid: bool = True  # Add is_valid field with default value of True')
                found_scenario_summary = False
                continue
            
            if 'class ScenarioListItem(BaseModel):' in line:
                found_scenario_list_item = True
                new_lines.append(line)
                continue
            
            if found_scenario_list_item and 'summary: ScenarioSummary' in line:
                new_lines.append(line)
                new_lines.append('    timestamp: str = "2023-01-01"  # Add timestamp field with default value')
                found_scenario_list_item = False
                continue
            
            new_lines.append(line)
        
        # Write the modified content
        with open(schemas_path, 'w') as f:
            f.write('\n'.join(new_lines))
        
        logger.info("Successfully patched schemas.py")
        return True
    
    except Exception as e:
        logger.error(f"Error patching schemas.py: {str(e)}")
        return False

def main():
    """Main function to patch all required files"""
    logger.info("Starting scenario list patch process...")
    
    # Ensure we're in the right directory
    if not os.path.exists(os.path.join('frontend', 'src')):
        logger.error("Please run this script from the GridGen root directory")
        return
    
    # Patch the files
    frontend_patched = patch_scenario_list_page()
    routes_patched = patch_routes_py()
    schemas_patched = patch_schemas_py()
    
    if frontend_patched and routes_patched and schemas_patched:
        logger.info("Patching complete! Your scenarios should now all show as valid in the scenario list.")
        logger.info("To restore the original behavior, use the .bak files that were created.")
    else:
        logger.error("Patching failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 