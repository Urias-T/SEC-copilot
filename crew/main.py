from crewai import Crew

from agents import InvestmentAgents
from tasks import InvestmentTasks

from dotenv import load_dotenv
load_dotenv()

class CopilotCrew:
    def __init__(self, company):
        self.company = company

    def run(self):
        agents = InvestmentAgents()
        tasks = InvestmentTasks()

        news_researcher = agents.news_researcher()
        fillings_researcher = agents.fillings_researcher()
        report_writer = agents.report_writer()

        news_research = tasks.news_research(news_researcher, self.company)
        fillings_research = tasks.fillings_research(fillings_researcher, self.company)
        report_writing = tasks.report_writing(report_writer)

        crew = Crew(
            agents = [
                news_researcher,
                fillings_researcher,
                report_writer
            ],
            tasks = [
                news_research,
                fillings_research,
                report_writing
            ],
            verbose=True
        )

        result = crew.kickoff()

        return result
    
if __name__ == "__main__":
    print("### Welcome to SEC-Copilot Crew")
    print("-------------------------------")
    company = input("What company do you want to research?:")

    crew = CopilotCrew(company)
    result = crew.run()
    print("\n\n####################")
    print("Your Report: \n\n")
    print(result)


