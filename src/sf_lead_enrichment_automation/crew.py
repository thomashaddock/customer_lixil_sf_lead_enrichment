import os
import json
import base64
from datetime import datetime

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool, ScrapeWebsiteTool
)

from crewai_tools import CrewaiEnterpriseTools
from sf_lead_enrichment_automation.tools.custom_tool import MyCustomTool

def google_vertex_llm():
    """
    Configure and return a Vertex AI LLM instance using service account credentials.
    """
    # Get the base64 encoded service account JSON from environment
    service_account_b64 = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON_B64")
    
    # Decode the base64 service account JSON
    service_account_json = base64.b64decode(service_account_b64).decode("utf-8")
    service_account_info = json.loads(service_account_json)
    
    # Extract project ID from service account
    project_id = service_account_info["project_id"]
    
    return LLM(
        model="vertex_ai/gemini-2.5-flash",
        vertex_project=project_id,
        vertex_credentials=service_account_info,
        temperature=0.3,
    )

@CrewBase
class SfLeadEnrichmentAutomationCrew:
    """SfLeadEnrichmentAutomation crew"""
    
    @agent
    def lead_ingestion_agent(self) -> Agent:
        enterprise_actions_tool = CrewaiEnterpriseTools(
            enterprise_token=os.getenv("CREWAI_ENTERPRISE_TOOLS_KEY"),
            actions_list=[
                "salesforce_search_records_lead",
            ],
        )
        
        return Agent(
            config=self.agents_config["lead_ingestion_agent"],
            tools=[
				*enterprise_actions_tool
            ],
            inject_date=True,
            llm=google_vertex_llm(),

        )
    
    @agent
    def lead_enrichment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_enrichment_agent"],
            tools=[
				SerperDevTool(n_results=1), ScrapeWebsiteTool()
            ],
            llm=google_vertex_llm(),

        )
    
    @agent
    def qa_data_verification_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["qa_data_verification_agent"],
            tools=[
				SerperDevTool()
            ],
            llm=google_vertex_llm(),

        )
    
    @agent
    def lead_scoring_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_scoring_agent"],
            llm=google_vertex_llm(),
        )
    
    # @agent
    # def salesforce_integration_agent(self) -> Agent:
    #     enterprise_actions_tool = CrewaiEnterpriseTools(
    #         enterprise_token=os.getenv("CREWAI_ENTERPRISE_TOOLS_KEY"),
    #         actions_list=[
    #             "salesforce_search_records_lead",
    #             "salesforce_update_record_lead",
                
    #         ],
    #     )
        
    #     return Agent(
    #         config=self.agents_config["salesforce_integration_agent"],
    #         tools=[
	#			*enterprise_actions_tool
    #         ],
    #         reasoning=False,
    #         max_reasoning_attempts=None,
    #         inject_date=True,
    #         allow_delegation=False,
    #         max_iter=25,
    #         llm=google_vertex_llm(),
            
    #     )
    
    @task
    def scan_for_new_leads_in_salesforce(self) -> Task:
        return Task(
            config=self.tasks_config["scan_for_new_leads_in_salesforce"],
        )
    
    @task
    def enrich_missing_lead_fields(self) -> Task:
        return Task(
            config=self.tasks_config["enrich_missing_lead_fields"],
        )
    
    @task
    def validate_enriched_lead_data(self) -> Task:
        return Task(
            config=self.tasks_config["validate_enriched_lead_data"],
        )
    
    @task
    def score_lead_quality(self) -> Task:
        return Task(
            config=self.tasks_config["score_lead_quality"],
        )
    
    # @task
    # def update_leads_and_mark_as_reviewed(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["update_leads_and_mark_as_reviewed"],
    #         markdown=False,
            
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the SfLeadEnrichmentAutomation crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            tracing=True,
            llm=google_vertex_llm(), 
        )
