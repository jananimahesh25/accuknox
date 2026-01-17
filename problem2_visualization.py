
import requests
import matplotlib.pyplot as plt
import json
from statistics import mean, median, stdev
from collections import defaultdict

class StudentScoreAnalyzer:
    def __init__(self):
        self.student_data = []
        
    def fetch_student_data(self):
        """
        Fetch student data from API
        Using JSONPlaceholder as mock API with simulated student scores
        """
        try:
            # Mock student data (in real scenario, use actual API)
            # For demonstration, creating synthetic data
            self.student_data = self._generate_mock_data()
            
            print(f"✓ Fetched data for {len(self.student_data)} students")
            return self.student_data
            
        except Exception as e:
            print(f"✗ Error fetching data: {e}")
            return []
    
    def _generate_mock_data(self):
        """Generate mock student data for demonstration"""
        import random
        
        subjects = ['Math', 'Science', 'English', 'History', 'Geography']
        students = []
        
        for i in range(20):
            student = {
                'id': i + 1,
                'name': f'Student {i + 1}',
                'scores': {}
            }
            for subject in subjects:
                student['scores'][subject] = random.randint(60, 100)
            students.append(student)
        
        return students
    
    def calculate_statistics(self):
        """Calculate various statistics from student data"""
        if not self.student_data:
            print("No data available")
            return None
        
        # Calculate average scores per subject
        subject_scores = defaultdict(list)
        
        for student in self.student_data:
            for subject, score in student['scores'].items():
                subject_scores[subject].append(score)
        
        statistics = {}
        for subject, scores in subject_scores.items():
            statistics[subject] = {
                'average': round(mean(scores), 2),
                'median': round(median(scores), 2),
                'std_dev': round(stdev(scores), 2),
                'min': min(scores),
                'max': max(scores)
            }
        
        return statistics
    
    def display_statistics(self, stats):
        """Display calculated statistics"""
        if not stats:
            return
        
        print("\n" + "="*80)
        print("STUDENT SCORE STATISTICS")
        print("="*80)
        
        for subject, metrics in stats.items():
            print(f"\n{subject}:")
            print(f"  Average: {metrics['average']}")
            print(f"  Median: {metrics['median']}")
            print(f"  Std Dev: {metrics['std_dev']}")
            print(f"  Range: {metrics['min']} - {metrics['max']}")
    
    def create_visualizations(self, stats):
        """Create bar charts and other visualizations"""
        if not stats:
            print("No statistics to visualize")
            return
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Student Score Analysis', fontsize=16, fontweight='bold')
        
        subjects = list(stats.keys())
        averages = [stats[s]['average'] for s in subjects]
        medians = [stats[s]['median'] for s in subjects]
        std_devs = [stats[s]['std_dev'] for s in subjects]
        
        # 1. Average Scores Bar Chart
        ax1 = axes[0, 0]
        bars1 = ax1.bar(subjects, averages, color='steelblue', alpha=0.8)
        ax1.set_title('Average Scores by Subject', fontweight='bold')
        ax1.set_ylabel('Average Score')
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')
        
        # 2. Comparison: Average vs Median
        ax2 = axes[0, 1]
        x = range(len(subjects))
        width = 0.35
        ax2.bar([i - width/2 for i in x], averages, width, 
                label='Average', color='steelblue', alpha=0.8)
        ax2.bar([i + width/2 for i in x], medians, width,
                label='Median', color='coral', alpha=0.8)
        ax2.set_title('Average vs Median Scores', fontweight='bold')
        ax2.set_ylabel('Score')
        ax2.set_xticks(x)
        ax2.set_xticklabels(subjects, rotation=45)
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # 3. Standard Deviation
        ax3 = axes[1, 0]
        bars3 = ax3.bar(subjects, std_devs, color='seagreen', alpha=0.8)
        ax3.set_title('Score Variability (Standard Deviation)', fontweight='bold')
        ax3.set_ylabel('Standard Deviation')
        ax3.grid(axis='y', alpha=0.3)
        
        for bar in bars3:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')
        
        # 4. Score Distribution Box Plot
        ax4 = axes[1, 1]
        score_data = []
        for subject in subjects:
            subject_scores = [s['scores'][subject] for s in self.student_data]
            score_data.append(subject_scores)
        
        bp = ax4.boxplot(score_data, labels=subjects, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
            patch.set_alpha(0.7)
        
        ax4.set_title('Score Distribution by Subject', fontweight='bold')
        ax4.set_ylabel('Score')
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('student_scores_analysis.png', dpi=300, bbox_inches='tight')
        print("\n✓ Visualization saved as 'student_scores_analysis.png'")
        plt.show()
    
    def export_results(self, stats):
        """Export results to JSON file"""
        output = {
            'total_students': len(self.student_data),
            'statistics': stats,
            'student_data': self.student_data
        }
        
        with open('student_analysis_results.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print("✓ Results exported to 'student_analysis_results.json'")

def main():
    """Main execution function"""
    analyzer = StudentScoreAnalyzer()
    
    print("Starting Student Score Analysis...")
    print("-" * 80)
    
    # Step 1: Fetch data
    analyzer.fetch_student_data()
    
    # Step 2: Calculate statistics
    stats = analyzer.calculate_statistics()
    
    # Step 3: Display results
    analyzer.display_statistics(stats)
    
    # Step 4: Create visualizations
    analyzer.create_visualizations(stats)
    
    # Step 5: Export results
    analyzer.export_results(stats)
    
    print("\n" + "="*80)
    print("Analysis Complete!")
    print("="*80)

if __name__ == "__main__":
    main()