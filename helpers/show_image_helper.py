
import base64

from IPython.display import display, Image as IPImage



def show_image(response):
    for event in response:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "function_response") and part.function_response:
                    for item in part.function_response.response.get("content", []):
                        if item.get("type") == "image":
                            display(IPImage(data=base64.b64decode(item["data"])))



