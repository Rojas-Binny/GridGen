"""
Service for generating prompts for power grid scenario generation.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

class PromptService:
    """Service for generating prompts for power grid scenario generation."""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialize the prompt service.
        
        Args:
            templates_dir: Directory containing prompt templates
        """
        self.templates_dir = templates_dir or os.path.join('app', 'templates')
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=True
        )
        self.templates = {}
        
        # Load templates
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load prompt templates from directory."""
        try:
            if not os.path.exists(self.templates_dir):
                os.makedirs(self.templates_dir)
                logger.info(f"Created templates directory: {self.templates_dir}")
            
            # Load default templates
            default_templates = {
                'base': self._create_base_template(),
                'physics': self._create_physics_template(),
                'reliability': self._create_reliability_template()
            }
            
            # Save default templates if they don't exist
            for name, template in default_templates.items():
                template_path = os.path.join(self.templates_dir, f"{name}.jinja2")
                if not os.path.exists(template_path):
                    with open(template_path, 'w') as f:
                        f.write(template)
            
            # Load all templates
            for filename in os.listdir(self.templates_dir):
                if filename.endswith('.jinja2'):
                    name = filename.replace('.jinja2', '')
                    self.templates[name] = self.env.get_template(filename)
            
            logger.info(f"Loaded {len(self.templates)} prompt templates")
        except Exception as e:
            logger.error(f"Error loading templates: {str(e)}")
    
    def _create_base_template(self) -> str:
        """Create base prompt template."""
        return """Generate a power grid scenario with the following specifications:

Network Configuration:
- Number of buses: {{ num_buses }}
- Number of generators: {{ num_generators }}
- Number of loads: {{ num_loads }}
{% if topology %}
- Topology: {{ topology }}
{% endif %}

Generation:
{% if generation_profile %}
- Generation profile: {{ generation_profile }}
{% endif %}
{% if generator_types %}
- Generator types: {{ generator_types|join(', ') }}
{% endif %}

Load:
{% if load_profile %}
- Load profile: {{ load_profile }}
{% endif %}
{% if load_types %}
- Load types: {{ load_types|join(', ') }}
{% endif %}

Constraints:
- Voltage limits: 0.95-1.05 p.u.
- Line flow limits: As specified in line data
- Generator limits: As specified in generator data

Please generate a scenario that meets these specifications while maintaining power flow balance and respecting all constraints."""
    
    def _create_physics_template(self) -> str:
        """Create physics-based prompt template."""
        return """Generate a power grid scenario that satisfies the following physics-based constraints:

Power Flow Equations:
- Active power balance at each bus
- Reactive power balance at each bus
- Line flow equations
- Transformer equations

Voltage Constraints:
- Bus voltage magnitudes: 0.95-1.05 p.u.
- Voltage angle differences: Within stability limits

Line Flow Constraints:
- Active power flow: Within thermal limits
- Reactive power flow: Within voltage stability limits

Generation Constraints:
- Active power limits
- Reactive power limits
- Ramp rate limits
- Minimum up/down times

Load Constraints:
- Active power demand
- Reactive power demand
- Power factor limits

Please ensure the generated scenario satisfies all these physics-based constraints."""
    
    def _create_reliability_template(self) -> str:
        """Create reliability-based prompt template."""
        return """Generate a power grid scenario that meets the following reliability requirements:

System Reliability:
- N-1 contingency criteria
- Voltage stability margin
- Frequency stability margin
- Spinning reserve requirements

Component Reliability:
- Generator availability
- Line availability
- Transformer availability
- Load reliability requirements

Reliability Metrics:
- Expected Energy Not Served (EENS)
- Loss of Load Probability (LOLP)
- Expected Interruption Frequency (EIF)
- Expected Interruption Duration (EID)

Please generate a scenario that meets these reliability requirements while maintaining system stability."""
    
    def create_prompt(
        self,
        parameters: Dict[str, Any],
        template_name: str = 'base',
        context: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Create a prompt for scenario generation.
        
        Args:
            parameters: Generation parameters
            template_name: Name of template to use
            context: Optional RAG context
            
        Returns:
            Generated prompt
        """
        try:
            # Get template
            template = self.templates.get(template_name)
            if not template:
                raise ValueError(f"Template '{template_name}' not found")
            
            # Add context if available
            if context:
                parameters['context'] = self._format_context(context)
            
            # Render template
            prompt = template.render(**parameters)
            
            return prompt
        except Exception as e:
            logger.error(f"Error creating prompt: {str(e)}")
            raise
    
    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        """
        Format RAG context for inclusion in prompt.
        
        Args:
            context: List of similar scenarios
            
        Returns:
            Formatted context text
        """
        context_parts = ["Similar Scenarios:"]
        
        for item in context:
            scenario = item['scenario']
            similarity = item['similarity']
            
            # Extract key information
            network = scenario['network']
            buses = network['bus']
            lines = network['ac_line']
            devices = network['simple_dispatchable_device']
            
            # Format scenario information
            scenario_text = [
                f"Scenario (similarity: {similarity:.4f}):",
                f"- Buses: {len(buses)}",
                f"- Lines: {len(lines)}",
                f"- Devices: {len(devices)}"
            ]
            
            # Add bus information
            for bus in buses[:3]:  # Limit to first 3 buses
                scenario_text.append(
                    f"- Bus {bus['uid']}: "
                    f"V={bus['initial_status']['vm']:.4f} p.u., "
                    f"θ={bus['initial_status']['va']:.4f} rad"
                )
            
            if len(buses) > 3:
                scenario_text.append(f"- ... and {len(buses) - 3} more buses")
            
            context_parts.append('\n'.join(scenario_text))
        
        return '\n\n'.join(context_parts)
    
    def create_template(
        self,
        name: str,
        template: str,
        parameters: List[str]
    ) -> str:
        """
        Create a new prompt template.
        
        Args:
            name: Template name
            template: Template text
            parameters: List of required parameters
            
        Returns:
            Template ID
        """
        try:
            # Validate template
            self.env.from_string(template)
        
        # Save template
            template_path = os.path.join(self.templates_dir, f"{name}.jinja2")
            with open(template_path, 'w') as f:
                f.write(template)
            
            # Reload templates
            self._load_templates()
            
            return name
        except Exception as e:
            logger.error(f"Error creating template: {str(e)}")
            raise
    
    def get_template(self, name: str) -> Optional[str]:
        """
        Get a template by name.
        
        Args:
            name: Template name
            
        Returns:
            Template text or None if not found
        """
        template = self.templates.get(name)
        if template:
            return template.template
        return None
    
    def list_templates(self) -> List[str]:
        """
        List all available templates.
            
        Returns:
            List of template names
        """
        return list(self.templates.keys())

# Create a global instance of the PromptService
prompt_service = PromptService()