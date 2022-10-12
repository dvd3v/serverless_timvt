"""AWS Lambda handler."""

import logging
from mangum import Mangum
from main import app

logging.getLogger("mangum.lifespan").setLevel(logging.ERROR)
logging.getLogger("mangum.http").setLevel(logging.DEBUG)

# Suppress credentials found in env vars warning
logging.getLogger("botocore.credentials").disabled = True
logging.getLogger("botocore.utils").disabled = True

handler = Mangum(app, lifespan="off")
