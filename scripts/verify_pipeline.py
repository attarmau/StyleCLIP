import sys
import os

# Add current directory to path so we can import 'backend'
sys.path.append(os.getcwd())

try:
    from backend.app.pipeline.inference_pipeline import InferencePipeline
    print("✅ Successfully imported InferencePipeline")
    
    # Instantiate to check for init errors
    # pipeline = InferencePipeline() # We can't instantiate easily without AWS creds or mocking, so just import is good enough for syntax.
    # Actually, init just sets self.min_confidence, so it should be fine unless rekognition client fails on import.
    # rekognition client is created at module level in rekognition_wrapper.py.
    # If AWS creds are missing, boto3 might not fail immediately on client creation, only on call.
    # But let's verify import 
    
except ImportError as e:
    print(f"❌ ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
