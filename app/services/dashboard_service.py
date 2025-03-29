import logging
from typing import Dict, List, Any
import pandas as pd

logger = logging.getLogger(__name__)

class DashboardService:
    @staticmethod
    def split_dashboard_data(data: Dict[str, Any], num_splits: int) -> List[Dict[str, Any]]:
        """Split dashboard data into multiple sections."""
        try:
            if not data:
                return []
            
            # Convert data to list format
            items = []
            for category, category_data in data.items():
                for item_name, item_data in category_data.items():
                    items.append({
                        'category': category,
                        'name': item_name,
                        **item_data
                    })
            
            # Calculate items per split
            total_items = len(items)
            items_per_split = max(1, total_items // num_splits)
            
            # Create splits
            splits = []
            for i in range(num_splits):
                start_idx = i * items_per_split
                end_idx = start_idx + items_per_split if i < num_splits - 1 else total_items
                
                split_items = items[start_idx:end_idx]
                if split_items:
                    splits.append({
                        'title': f'Dashboard {i + 1}',
                        'description': f'Analysis section {i + 1} of {num_splits}',
                        'data': split_items
                    })
            
            return splits
        except Exception as e:
            logger.error(f"Error splitting dashboard data: {str(e)}")
            return []

    @staticmethod
    def create_dynamic_dashboard(df_data: Dict, category: str, metrics: Dict) -> Dict[str, Any]:
        """Create dynamic dashboard with relationship visualizations."""
        try:
            dashboard_data = {
                'category': category,
                'metrics': metrics,
                'visualizations': [],
                'summary': {}
            }
            
            # Process metrics
            if category in df_data:
                category_data = df_data[category]
                dashboard_data['summary'] = {
                    'total_items': len(category_data),
                    'avg_importance': sum(item['importance'] for item in category_data.values()) / len(category_data),
                    'avg_selection': sum(item['selection_score'] for item in category_data.values()) / len(category_data),
                    'avg_rejection': sum(item['rejection_score'] for item in category_data.values()) / len(category_data)
                }
            
            # Split the data if number_of_dashboards is specified
            if 'number_of_dashboards' in metrics and metrics['number_of_dashboards'] > 1:
                dashboard_data['splits'] = DashboardService.split_dashboard_data(
                    df_data,
                    metrics['number_of_dashboards']
                )
            
            return dashboard_data
        except Exception as e:
            logger.error(f"Error creating dashboard: {str(e)}")
            return {}

    @staticmethod
    def calculate_threshold_scores(data: Dict) -> tuple:
        """Calculate selection and rejection threshold scores."""
        try:
            selection_threshold = 75.0  # Default value
            rejection_threshold = 25.0  # Default value
            
            if data:
                # Calculate thresholds based on data
                scores = [item['selection_score'] for items in data.values() for item in items.values()]
                if scores:
                    selection_threshold = sum(scores) / len(scores)
                    rejection_threshold = min(scores)
            
            return selection_threshold, rejection_threshold
        except Exception as e:
            logger.error(f"Error calculating thresholds: {str(e)}")
            return 75.0, 25.0 