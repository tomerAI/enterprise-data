import pandas as pd
from typing import List, Dict, Any, Tuple
from .base_processor import BaseProcessor

class GraphCSVProcessor(BaseProcessor):
    def __init__(self):
        self.required_columns = ['source', 'relationship', 'target']
        self.optional_columns = ['source_properties', 'target_properties', 'relationship_properties']

    def validate_headers(self, df: pd.DataFrame) -> bool:
        """Validate that required columns exist in the CSV"""
        return all(col in df.columns for col in self.required_columns)

    def process_properties(self, properties_str: str) -> Dict:
        """Convert properties string to dictionary"""
        if pd.isna(properties_str):
            return {}
        try:
            # Assuming properties are in format "key1:value1;key2:value2"
            props = dict(item.split(":") for item in properties_str.split(";"))
            return {k.strip(): v.strip() for k, v in props.items()}
        except:
            return {}

    def process(self, file_path: str) -> List[Dict[str, Any]]:
        """Process CSV file and return graph relationships"""
        df = pd.read_csv(file_path)
        
        if not self.validate_headers(df):
            raise ValueError(f"CSV must contain columns: {', '.join(self.required_columns)}")

        graph_elements = []
        
        for _, row in df.iterrows():
            element = {
                'source': row['source'],
                'relationship': row['relationship'],
                'target': row['target'],
                'source_properties': self.process_properties(row.get('source_properties', '')),
                'target_properties': self.process_properties(row.get('target_properties', '')),
                'relationship_properties': self.process_properties(row.get('relationship_properties', ''))
            }
            graph_elements.append(element)

        return graph_elements

    @classmethod
    def get_supported_extensions(cls) -> set:
        return {'.csv'} 