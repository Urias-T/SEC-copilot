from crewai import Crew

from crew.agents import InvestmentAgents
from crew.tasks import InvestmentTasks

# from dotenv import load_dotenv
# load_dotenv()

class CopilotCrew:
    def __init__(self, company):
        self.company = company

    def run(self):
        agents = InvestmentAgents()
        tasks = InvestmentTasks()

        fillings_researcher = agents.fillings_researcher()
        market_trader = agents.market_trader()
        news_researcher = agents.news_researcher()
        report_writer = agents.report_writer()

        fillings_research = tasks.fillings_research(fillings_researcher, self.company)
        market_trade = tasks.market_trade(market_trader, self.company)
        news_research = tasks.news_research(news_researcher, self.company)
        report_writing = tasks.report_writing(report_writer)

        crew = Crew(
            agents = [
                fillings_researcher,
                market_trader,
                news_researcher,
                report_writer
            ],
            tasks = [
                fillings_research,
                market_trade,
                news_research,
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


