from google.genai import types

def build_retry_config():
     retry_config = types.HttpRetryOptions(
        attempts=5,
        exp_base=2,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    )
     
     return retry_config
