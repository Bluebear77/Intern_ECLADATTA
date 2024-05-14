import json
import os

def process_file(i):
    input_file_path = f'./Raw/instance_{i}.json'
    processed_file_path = f'./P2/instance_{i}_processed.json'
    output_file_path = f'./P4/instance_{i}_v4.json'
    
    # Check if input and processed files exist
    if not os.path.exists(input_file_path) or not os.path.exists(processed_file_path):
        print(f"Skipping instance_{i} as one or more required files do not exist.")
        return
    
    try:
        # Read the input instance_i.json
        with open(input_file_path, 'r', encoding='utf-8') as file:
            instance_data = json.load(file)

        # Extract primaryKeyPosition and typingLabel from preprocessingMetadata
        preprocessing_metadata = instance_data['_source'].get('preprocessingMetadata', [])
        primary_key_position = None
        typing_label = []

        for tech_result in preprocessing_metadata:
            if 'technologyResults' in tech_result:
                tech_results = tech_result['technologyResults']
                for result in tech_results:
                    if 'dagobah' in result and 'preprocessed' in result['dagobah']:
                        preprocessed = result['dagobah']['preprocessed']
                        primary_key_position = preprocessed['primaryKeyInfo']['primaryKeyPosition']
                        typing_label = [label['typing'][0]['typingLabel'] for label in preprocessed['primitiveTyping']]

        # Sanity check to ensure the keys are found
        if primary_key_position is None or not typing_label:
            print(f"Skipping instance_{i} due to missing primaryKeyPosition or typingLabel.")
            return

        # Read the processed instance_i_processed.json
        with open(processed_file_path, 'r', encoding='utf-8') as file:
            processed_data = json.load(file)

        # Function to convert "DATE" to "datetime"
        def convert_typing_label(label):
            return "datetime" if label == "DATE" else label

        # Update all tables in the processed data
        for table in processed_data:
            table['key_column'] = primary_key_position
            table['column_types'] = [convert_typing_label(label) for label in typing_label]

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Save the updated data to instance_i_v4.json
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=4)

        print(f"Updated file saved to {output_file_path}")

    except Exception as e:
        print(f"Error processing instance_{i}: {e}")

# Process files from 1 to 100
for i in range(1, 101):
    process_file(i)
