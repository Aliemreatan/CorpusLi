import logging
import traceback
from nlp.custom_bert_processor import create_custom_bert_processor

# Setup logging to see what's happening
logging.basicConfig(level=logging.INFO)

try:
    print("Attempting to load BERT model...")
    processor = create_custom_bert_processor()
    print(f"Is loaded: {processor.is_loaded}")
    if not processor.is_loaded:
        print("Model failed to load.")
except Exception as e:
    print(f"An error occurred during create_custom_bert_processor: {e}")
    traceback.print_exc()
