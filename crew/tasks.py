from crewai import Task

class InvestmentTasks():

    def news_research(self, agent, company):
        return Task(
            description=f"""Collect and summarize news headlines for {company}, paying special
            attention to headlines regarding market sentiment, investor behaviour, upcoming events like earnings, etc. 
            
            {self.__tip_section}
            
            Make sure the data you use is as recent as possible.""",
            agent=agent
        )

    def market_trade(self, agent, company):
        return Task(
            description=f"""Find the current stock price of {company},
            
            {self.__tip_section}""",
            agent=agent
        )
    
    def fillings_research(self, agent, company):
        return Task(
            description=f"""Find out the spending patterns for {company} in the past three quarters.
            
            {self.__tip_section}""",
            agent=agent
        )
    
    def report_writing(self, agent):
        return Task(
            description=f"""Summarize the findings from the News Researcher and the Fillings Researcher and use that to
            Your final answer must be a full detailed report capturing all the qantitative and qualitative data provided
            and must be easy to read and understand as well.
            
            {self.__tip_section}""",
            agent=agent
        )
    
    def __tip_section(self):
        return "If you do your BEST job, I'll tip you $500."
