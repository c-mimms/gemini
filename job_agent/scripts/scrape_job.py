
import asyncio
import os
import json
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv('/Users/chris/code/gemini/discord_bot/.env')

async def main():
    browser = Browser(config=BrowserConfig(headless=True))
    url = "https://www.linkedin.com/jobs/view/4385880637/"
    task = f"Go to {url} and extract the Job Title, Company Name, the full job description text, the salary (if available), and a link to the company's own LinkedIn page. Return the data as JSON."
    agent = Agent(task=task, browser=browser, llm=ChatOpenAI(model="gpt-4o"))
    result = await agent.run()
    print(result)
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
