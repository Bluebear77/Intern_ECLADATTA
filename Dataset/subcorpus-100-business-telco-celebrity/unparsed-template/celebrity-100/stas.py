import os
import pandas as pd
import matplotlib.pyplot as plt

def analyze_templates():
    # Collect all CSV files in the current directory
    csv_files = [file for file in os.listdir('.') if file.endswith('.csv')]
    
    # Dictionary to hold template counts
    template_counts = {}
    
    # Process each CSV file
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        
        if 'Template Name' in df.columns:
            templates = df['Template Name']
            for template in templates:
                if template in template_counts:
                    template_counts[template] += 1
                else:
                    template_counts[template] = 1
    
    # Compute total number of templates
    total_templates = sum(template_counts.values())
    
    # Compute percentages
    template_percentages = {template: (count / total_templates) * 100 for template, count in template_counts.items()}
    
    # Create a pie chart with better visualization
    fig, ax = plt.subplots(figsize=(12, 8))
    wedges, texts, autotexts = ax.pie(template_percentages.values(), labels=template_percentages.keys(), autopct='%1.1f%%', startangle=140, textprops=dict(color="w"))
    
    # Improve the legend and labels
    ax.legend(wedges, template_percentages.keys(), title="Templates", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=10, weight="bold")
    ax.set_title('Template Distribution in CSV Files')
    
    plt.tight_layout()
    plt.savefig('template_distribution_pie_chart.png')
    plt.close()

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(14, 8))
    templates = list(template_percentages.keys())
    percentages = list(template_percentages.values())
    
    ax.barh(templates, percentages, color='skyblue')
    ax.set_xlabel('Percentage')
    ax.set_title('Template Distribution in CSV Files')
    
    plt.tight_layout()
    plt.savefig('template_distribution_bar_chart.png')
    plt.close()
    
    # Generate the Markdown report
    with open('template_distribution_report.md', 'w') as report_file:
        report_file.write('# Template Distribution Report\n')
        report_file.write('This report analyzes the distribution of templates across all CSV files in the current directory.\n\n')
        report_file.write('## Summary\n')
        report_file.write(f'Total number of templates: {total_templates}\n\n')
        
        report_file.write('## Template Distribution\n')
        for template, percentage in template_percentages.items():
            report_file.write(f'- **{template}**: {percentage:.2f}%\n')
        
        report_file.write('\n## Pie Chart\n')
        report_file.write('![Template Distribution Pie Chart](template_distribution_pie_chart.png)\n')
        
        report_file.write('\n## Bar Chart\n')
        report_file.write('![Template Distribution Bar Chart](template_distribution_bar_chart.png)\n')

if __name__ == '__main__':
    analyze_templates()
