import os
from scrapper.spiders.paths import absolute_paths
export_dir = absolute_paths()

def handle_failure_function(self, failure, code):
    request = failure.request
    proxy = request.meta.get("proxy", "No proxy set")
    
    self.logger.warning(
        f"Request failed or timed out: {request.url} - "
        f"Reason: {failure.value} - Proxy: {proxy}"
    )
    
    with open(os.path.join(export_dir,f"failed_urls_{code}.txt"), "a", encoding="utf-8") as f:
        f.write(f"{request.url} | Proxy: {proxy}\n")
