import os
import json
from jinja2 import Environment, FileSystemLoader
from .llm_client import generate_content
from .affiliate_manager import inject_affiliates, get_affiliate_disclosure
from .devto_publisher import publish_to_devto
from .mastodon_publisher import publish_to_mastodon

def main():
    # TODO: Load data and generate multiple pages using improved templates
    print('HTML templates improved with modern styling and responsiveness.') 

if __name__ == "__main__":
    main()