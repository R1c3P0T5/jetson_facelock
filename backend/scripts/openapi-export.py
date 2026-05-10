import json
import sys

sys.path.insert(0, ".")
from main import app

print(json.dumps(app.openapi(), indent=2))
