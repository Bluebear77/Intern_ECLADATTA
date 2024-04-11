[
    {
        "reasoning_type": "conjunction",
        "sample_examples_per_table": 2,
        "enable": True,
        "templates": [
            {
                "template_str": "The [target_col] that have [condition] are [executed_results].",
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
                "template_str": "[executed_results] [target_col] have [source_col] [condition].",
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
                "template_str": "The [target_col] ordered by [source_col] are [executed_results].",
                "type": "temporal_numerical_order"
            },
            {
                "template_str": "The [target_col], with [source_col] [condition], ordered by [source_col_2] are [executed_results].",
                "type": "temporal_numerical_order_with_condition"
            }
        ]
    },
    {
        "reasoning_type": "temporal_numerical_comparison",
        "sample_examples_per_table": 3,
        "enable": True,
        "templates": [
            {
                "template_str": "The [target_col] that [source_col] [condition] are [executed_results].",
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
                "template_str": "The [operator] of [target_col] with [source_col] [condition] is [executed_results].",
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
                "template_str": "The difference between [val1] and [val2] in [target_col] is [executed_results].",
                "type": "numerical_operation_diff"
            }
        ]
    }
]

