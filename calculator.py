import json
import os

class CarbonCalculator:
    def __init__(self, data_file='data/emission_factors.json'):
        self.factors = self._load_data(data_file)

    def _load_data(self, filepath):
        base_path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_path, filepath)
        try:
            with open(full_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback data if file is missing (for safety)
            return {
                "transport": {"car_petrol": 0.192},
                "electricity": {"grid_avg": 0.82},
                "diet": {"vegetarian": 1.7},
                "fuel": {"lpg": 2.983}
            }

    def _safe_float(self, value, default=0.0):
        try:
            if not value or value == "":
                return default
            return float(value)
        except (ValueError, TypeError):
            return default

    def calculate(self, data):
        """
        Calculate total carbon footprint.
        data: dict containing user inputs
        Returns: dict with breakdown and total
        """
        emissions = {
            "transport": 0.0,
            "electricity": 0.0,
            "diet": 0.0,
            "fuel": 0.0
        }

        # Transport
        transport_mode = data.get('transport_mode', 'car_petrol')
        distance = self._safe_float(data.get('distance'))
        factor = self.factors.get('transport', {}).get(transport_mode, 0.192)
        emissions['transport'] = distance * factor

        # Electricity
        electricity_usage = self._safe_float(data.get('electricity'))
        # Assuming grid average for simplicity, could be user selected
        elec_factor = self.factors.get('electricity', {}).get('grid_avg', 0.82) 
        emissions['electricity'] = electricity_usage * elec_factor

        # Diet
        diet_type = data.get('diet', 'vegetarian')
        diet_factor = self.factors.get('diet', {}).get(diet_type, 1.7) # kg CO2e / day
        emissions['diet'] = diet_factor * 30 # Monthly est.

        # Fuel
        fuel_usage = self._safe_float(data.get('lpg')) # kg or m3
        fuel_type = data.get('fuel_type', 'lpg')
        fuel_factor = self.factors.get('fuel', {}).get(fuel_type, 2.983)
        emissions['fuel'] = fuel_usage * fuel_factor

        total = sum(emissions.values())
        
        return {
            "breakdown": emissions,
            "total": total,
            "units": "kg CO2e/month"
        }

    def get_recommendations(self, total_emissions):
        recommendations = []
        if total_emissions > 500: # Arbitrary high threshold for monthly
            recommendations.append("Consider switching to public transport or carpooling.")
            recommendations.append("Switch to LED bulbs and energy-efficient appliances.")
        
        if self.factors['diet']['heavy_meat'] > 2: # Check logic
             pass # Logic for diet specific recs can be added here based on input

        return recommendations

    def get_ecological_footprint(self, total_emissions):
        """
        Calculate ecological footprint stats.
        Target sustainable emission: ~166.7 kg CO2e/month (2 tons/year).
        """
        sustainable_target = 166.7 
        earths_needed = total_emissions / sustainable_target
        
        # Simplified extrapolation for demo purposes
        # Base increase 1.2C, +0.5C per extra Earth needed beyond 1
        if earths_needed <= 1:
            temp_rise = 1.5
        else:
            temp_rise = 1.2 + (earths_needed - 1) * 0.5
            
        return {
            "earths_needed": round(max(earths_needed, 0.5), 1), # Min 0.5 earths
            "temp_rise": round(temp_rise, 1)
        }
