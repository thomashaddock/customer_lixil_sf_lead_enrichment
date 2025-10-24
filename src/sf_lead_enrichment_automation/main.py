#!/usr/bin/env python
import sys
import os
import logging
from datetime import datetime
from typing import Dict, Any

from sf_lead_enrichment_automation.crew import SfLeadEnrichmentAutomationCrew

def run():
    """
    Run the crew to process new leads in Salesforce.
    """
    
    inputs = {
    }
    
    try:
        crew = SfLeadEnrichmentAutomationCrew()       
        result = crew.crew().kickoff(inputs=inputs)       
        return result
        
    except Exception as e:
        import traceback
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
