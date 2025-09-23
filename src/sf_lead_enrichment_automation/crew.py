import os
from datetime import datetime

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool, ScrapeWebsiteTool
)

from crewai_tools import CrewaiEnterpriseTools
from sf_lead_enrichment_automation.tools.custom_tool import MyCustomTool

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
        )
    
    # @agent
    # def lead_enrichment_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["lead_enrichment_agent"],
    #         tools=[
	# 			SerperDevTool(n_results=1), ScrapeWebsiteTool()
    #         ],
    #     )
    
    # @agent
    # def qa_data_verification_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["qa_data_verification_agent"],
    #         tools=[
	# 			SerperDevTool()
    #         ],
    #     )
    
    # @agent
    # def salesforce_integration_agent(self) -> Agent:
    #     enterprise_actions_tool = CrewaiEnterpriseTools(
    #         enterprise_token=os.getenv("CREWAI_ENTERPRISE_TOOLS_KEY"),
    #         actions_list=[
    #             "salesforce_search_records_lead",
    #             # "salesforce_update_record_lead",
                
    #         ],
    #     )
        
    #     return Agent(
    #         config=self.agents_config["salesforce_integration_agent"],
            
            
    #         tools=[
	# 			*enterprise_actions_tool
    #         ],
    #         reasoning=False,
    #         max_reasoning_attempts=None,
    #         inject_date=True,
    #         allow_delegation=False,
    #         max_iter=25,
    #         max_rpm=None,
    #         max_execution_time=None,
    #         llm=LLM(
    #             model="gpt-4.1-mini",
    #             temperature=0.7,
    #         ),
            
    #     )
    
    
    @task
    def scan_for_new_leads_in_salesforce(self) -> Task:
        return Task(
            config=self.tasks_config["scan_for_new_leads_in_salesforce"],
        )
    
    # @task
    # def enrich_missing_lead_fields(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["enrich_missing_lead_fields"],
    #     )
    
    # @task
    # def validate_enriched_lead_data(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["validate_enriched_lead_data"],
    #     )
    
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
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
