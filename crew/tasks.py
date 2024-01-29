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
            
            {self.__tip_section}
            
            The input for your tool is only the ticker symbol for a given company. Do not add anything else asides the 
            ticker symbol to your input.""",
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
            description=f"""Review and synthesize all the findings from the News Research Expert, Stock Market Trader and the Fillings Research Expert and use that to
            write a clear, explanatory report to guide your user's investment decision making. Make sure the current stock price of the company is 
            emphasized in your report.

            Include a section for the current stock price of the company.

            Your final answer must be a full detailed report capturing all the qantitative and qualitative data provided
            and must be easy to read and understand as well.
            
            {self.__tip_section}""",
            agent=agent
        )
    
    def __tip_section(self):
        return "If you do your BEST job, I'll tip you $500."
