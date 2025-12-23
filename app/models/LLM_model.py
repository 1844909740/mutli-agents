from strands.models.openai import OpenAIModel
import logging


class ModelInstances:
    try:
        LEADER_MODEL = OpenAIModel(
            client_args={
                "api_key": "",
                "base_url": ""
            },
            model_id="",
            params={
                "max_tokens": 8192,
                "temperature": 0.8,
                "top_p": 0.9
            }
        )
    except Exception as e:
        logging.error(f"Failed to initialize LEADER_MODEL: {str(e)}")
        raise

