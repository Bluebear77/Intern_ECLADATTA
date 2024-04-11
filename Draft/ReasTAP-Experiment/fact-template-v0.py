REFACToR_templates = [
    {
        "reasoning_type": "conjunction",
        "sample_examples_per_table": 2,
        "enable": True,
        "templates": [
            {
                "template_str": "The [col1] that have [condition] are [executed_results].",
                "type": "conjunction"
            }
        ]
    },
    {
        "reasoning_type": "counting",
        "sample_examples_per_table": 2,
        "enable": True,
        "templates": [
            {
                "template_str": "[executed_results] [col1] have [col2] [condition].",
                "type": "counting"
            }
        ]
    },
    {
        "reasoning_type": "temporal_numerical_order",
        "sample_examples_per_table": 3,
        "enable": True,
        "templates": [
            {
                "template_str": "The [col1] ordered by [col3] are [executed_results].",
                "type": "temporal_numerical_order"
            },
            {
                "template_str": "The [col1], with [col2] [condition], ordered by [col3] are [executed_results].",
                "type": "temporal_numerical_order"
            }
        ]
    },
    {
        "reasoning_type": "temporal_numerical_comparison",
        "sample_examples_per_table": 3,
        "enable": True,
        "templates": [
            {
                "template_str": "The [col1] that [col2] [condition] are [executed_results].",
                "type": "temporal_numerical_comparison"
            }
        ]
    },
    {
        "reasoning_type": "numerical_operation_sum_avg",
        "sample_examples_per_table": 2,
        "enable": True,
        "templates": [
            {
                "template_str": "The [operator] of [col1] with [col2] [condition] is [executed_results].",
                "type": "numerical_operation"
            }
        ]
    },
    {
        "reasoning_type": "numerical_operation_diff",
        "sample_examples_per_table": 2,
        "enable": True,
        "templates": [
            {
                "template_str": "The difference between [val1] and [val2] in [col] is [executed_results].",
                "type": "numerical_operation_diff"
            }
        ]
    }
]

# Example of how to use the template
if __name__ == "__main__":
    # This would be used to iterate over tables and generate examples for pre-training based on the templates
    for template_info in REFACToR_templates:
        if template_info["enable"]:
            for template in template_info["templates"]:
                print(f"Generating examples for {template_info['reasoning_type']} using: {template['template_str']}")
                # Here you would add your logic to actually generate the examples
                # This is just a placeholder for the output structure
