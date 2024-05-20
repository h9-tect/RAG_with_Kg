import os

# Set environment variables for Nebula connection
os.environ["GRAPHD_HOST"] = "localhost"
os.environ["GRAPHD_PORT"] = "9669"
os.environ["NEBULA_USER"] = "root"
os.environ["NEBULA_PASSWORD"] = "nebula"
os.environ["NEBULA_ADDRESS"] = f"{os.environ['GRAPHD_HOST']}:{os.environ['GRAPHD_PORT']}"
