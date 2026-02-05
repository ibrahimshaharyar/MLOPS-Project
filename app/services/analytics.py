"""
Analytics service for generating dashboard statistics and visualizations
from the training dataset.
"""
import pandas as pd
import numpy as np
from pathlib import Path


class AnalyticsService:
    """Service to generate analytics data for the dashboard"""
    
    def __init__(self, data_path: str = "artifacts/train.csv"):
        """Initialize with path to training data"""
        self.data_path = Path(data_path)
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """Load the training data"""
        if self.data_path.exists():
            self.df = pd.read_csv(self.data_path)
            # Add calculated columns like in the EDA notebook
            self.df['total_score'] = (
                self.df['math_score'] + 
                self.df['reading_score'] + 
                self.df['writing_score']
            )
            self.df['average'] = self.df['total_score'] / 3
        else:
            raise FileNotFoundError(f"Training data not found at {self.data_path}")
    
    def get_summary_statistics(self) -> dict:
        """Get overall summary statistics"""
        return {
            "total_students": len(self.df),
            "avg_math": round(self.df['math_score'].mean(), 2),
            "avg_reading": round(self.df['reading_score'].mean(), 2),
            "avg_writing": round(self.df['writing_score'].mean(), 2),
            "avg_overall": round(self.df['average'].mean(), 2),
            "gender_distribution": self.df['gender'].value_counts().to_dict(),
            "students_with_test_prep": len(self.df[self.df['test_preparation_course'] == 'completed'])
        }
    
    def get_score_distributions(self) -> dict:
        """Get score distribution data for histograms"""
        bins = 20
        
        # Math scores
        math_hist, math_bins = np.histogram(self.df['math_score'], bins=bins)
        
        # Reading scores
        reading_hist, reading_bins = np.histogram(self.df['reading_score'], bins=bins)
        
        # Writing scores
        writing_hist, writing_bins = np.histogram(self.df['writing_score'], bins=bins)
        
        return {
            "math": {
                "counts": math_hist.tolist(),
                "bins": math_bins.tolist()
            },
            "reading": {
                "counts": reading_hist.tolist(),
                "bins": reading_bins.tolist()
            },
            "writing": {
                "counts": writing_hist.tolist(),
                "bins": writing_bins.tolist()
            }
        }
    
    def get_gender_distribution(self) -> dict:
        """Get gender distribution for pie chart"""
        gender_counts = self.df['gender'].value_counts()
        return {
            "labels": gender_counts.index.tolist(),
            "values": gender_counts.values.tolist()
        }
    
    def get_race_distribution(self) -> dict:
        """Get race/ethnicity distribution for pie chart"""
        race_counts = self.df['race_ethnicity'].value_counts()
        return {
            "labels": race_counts.index.tolist(),
            "values": race_counts.values.tolist()
        }
    
    def get_lunch_distribution(self) -> dict:
        """Get lunch type distribution for pie chart"""
        lunch_counts = self.df['lunch'].value_counts()
        return {
            "labels": lunch_counts.index.tolist(),
            "values": lunch_counts.values.tolist()
        }
    
    def get_test_prep_distribution(self) -> dict:
        """Get test preparation course distribution for pie chart"""
        prep_counts = self.df['test_preparation_course'].value_counts()
        return {
            "labels": prep_counts.index.tolist(),
            "values": prep_counts.values.tolist()
        }
    
    def get_parental_education_distribution(self) -> dict:
        """Get parental education distribution"""
        edu_counts = self.df['parental_level_of_education'].value_counts()
        return {
            "labels": edu_counts.index.tolist(),
            "values": edu_counts.values.tolist()
        }
    
    def get_scores_by_gender(self) -> dict:
        """Get score statistics grouped by gender for box plots"""
        gender_groups = self.df.groupby('gender')
        
        return {
            "math": {
                gender: group['math_score'].tolist()
                for gender, group in gender_groups
            },
            "reading": {
                gender: group['reading_score'].tolist()
                for gender, group in gender_groups
            },
            "writing": {
                gender: group['writing_score'].tolist()
                for gender, group in gender_groups
            }
        }
    
    def get_correlation_matrix(self) -> dict:
        """Get correlation matrix for scores"""
        score_columns = ['math_score', 'reading_score', 'writing_score']
        corr_matrix = self.df[score_columns].corr()
        
        return {
            "labels": score_columns,
            "matrix": corr_matrix.values.tolist()
        }


# Global instance
_analytics_service = None

def get_analytics_service() -> AnalyticsService:
    """Get or create the analytics service singleton"""
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = AnalyticsService()
    return _analytics_service
