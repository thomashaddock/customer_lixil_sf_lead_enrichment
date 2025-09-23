#!/usr/bin/env python
import sys
import os
import logging
from datetime import datetime
from typing import Dict, Any

from sf_lead_enrichment_automation.crew import SfLeadEnrichmentAutomationCrew

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sf_lead_enrichment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run():
    """
    Run the crew to process new leads in Salesforce.
    """
    logger.info("Starting Salesforce Lead Enrichment Automation")
    
    # Validate environment variables
    if not os.getenv("CREWAI_ENTERPRISE_TOOLS_KEY"):
        logger.error("CREWAI_ENTERPRISE_TOOLS_KEY environment variable is required")
        raise ValueError("CREWAI_ENTERPRISE_TOOLS_KEY environment variable is required")
    
    inputs = {
    }
    
    try:
        crew = SfLeadEnrichmentAutomationCrew()
        
        # Enable verbose logging for debugging
        logger.info("Starting crew execution with verbose logging...")
        result = crew.crew().kickoff(inputs=inputs)
        
        logger.info("Lead enrichment process completed successfully")
        logger.info(f"Processing result: {result}")
        
        # Log detailed results for debugging
        if hasattr(result, 'raw'):
            logger.info(f"Raw result: {result.raw}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error during lead enrichment process: {str(e)}")
        logger.error(f"Exception type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        
    }
    try:
        SfLeadEnrichmentAutomationCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SfLeadEnrichmentAutomationCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        
    }
    try:
        SfLeadEnrichmentAutomationCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
