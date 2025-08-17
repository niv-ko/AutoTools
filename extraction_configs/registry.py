from extraction_configs.schema import ExtractionConfig, ParameterExtractionMethod, ExtractionMethod


def get_extraction_config(endpoint_name):
    return ExtractionConfig(
        parameter_extraction_methods=[
            ParameterExtractionMethod(
                parameter_name="a",
                extraction_method=ExtractionMethod(
                    extractor_name="example_extractor"
                )
            ),
            ParameterExtractionMethod(
                parameter_name="b",
                extraction_method=ExtractionMethod(
                    extractor_name="example_extractor"
                )
            )
        ]
    )
