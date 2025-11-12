import os
from datetime import datetime
from typing import Optional
import re
from pathlib import Path
import json
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel, ImageUrl
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

load_dotenv()
now = datetime.now()
curr_month=now.strftime("%B")
curr_year=now.strftime("%Y")

model_name='gpt-4o-mini'
model = OpenAIChatModel(model_name, provider=OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY")))
print(f'{model_name} model loaded')

news_topic = "stablecoin regulations"
def get_articles(news_topic:str):

    class Article(BaseModel):
        title: str
        url: str
        summary: str
        source: str
        date: datetime

    agent = Agent(model,
                  tools=[duckduckgo_search_tool()],
                  output_type=list[Article],
                  system_prompt=f'We are in {curr_month} {curr_year}. Search DuckDuckGo for the given query and return the results. Do not include articles about daily price analysis, '
                                'please only include articles with significance in policy change, and business activities.'
                                ' Please only include articles from reputable sources.'
                                'Please do not include articles that are overviews or recaps.'
                                'Do not include articles talking about the same thing. ' \
                                'Please include a wide range of topics, not just a few different articles on the same topic. ',)
    print(f'agent created')

    result = agent.run_sync(f'Please list top three news articles about {news_topic} from this month?')

    print(f'agent run completed')
    for i, article in enumerate(result.output, start=1):
        print(f"\n{i}. {article.title}\n{article.url}\n{article.summary}\nSource: {article.source}\nSource: {article.date}\n")
    print(result.usage())

    output_dir = Path('./output')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = f'{output_dir}/articles_{now.strftime("%B")}_{now.strftime("%Y")}.json'

    class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            return super().default(o)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([article.model_dump() for article in result.output], f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
    print(f"\n✅ Saved {len(result.output)} articles to {output_path}")


article_topic = "UK stablecoin legal consultation framework"
def write_article(article_topic: str):


    class ResearchResult(BaseModel):
        article_sub_title: str = Field(description='This is a top level string heading for a sub-section of a email newsletter')
        content: str = Field(description='This is section with the main opinion piece of the topic')

    agent = Agent(model,
                  tools=[duckduckgo_search_tool()],
                  output_type=ResearchResult,
                  system_prompt=f'We are in {curr_month} {curr_year}. '
                                'You are an expert marketing writer in the cryptocurrency space targeting institutional financial industry professionals.'
                                'Given a topic of interest, please search for and read through the top 3-5 most relevant and authoratative articles, '
                                'then combine the article in to a coherent expert written newsletter section, aim for 100 words.' \
                                'Your writing style is engaging and thought provoking with attention-grabbing titles.' \
                                'Please format the article with main body wrapped in <p></p>, and use <ul></ul>,<li></li> if it is appropriate to use bulletpoints' \
                                'Feel free to use other html elements as you see fit but the content will need to work within a <div> class pre-supplied'
                                )
    print(f'agent created')
    result = agent.run_sync(f'Please write a subsection article: {article_topic}')

    print(result.output.article_sub_title)
    print(result.output.content)
    

    output_dir = Path(f'./output/articles_{now.strftime("%B")}_{now.strftime("%Y")}')
    output_dir.mkdir(parents=True, exist_ok=True)

    len_dir_article = sum(1 for f in output_dir.iterdir() if f.is_file())
    safe_file_name = f'{len_dir_article}_{re.sub(r"[^a-zA-Z0-9_-]+", "_", result.output.article_sub_title)}'
    output_path = output_dir/f'{safe_file_name}.json'
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result.output.model_dump(), f, ensure_ascii=False, indent=2)
    print(f"\n✅ Saved Article: {result.output.article_sub_title} to {output_path}")


def rewrite_main_body(article:str):
    formatted = article

    class MainBody(BaseModel):
        title: str
        executive_sum: str = Field(description='This is a top level summary of the main opinion piece on a newsletter derived from the input writing')
        quote: str = Field(description='This is a quote relevant to the story')
        highlight: str = Field(description='This is a highlighted section on the newsletter to show the main technical processes in the writing')
        key_takeaway: str = Field(description='Bullet points of 3 key take aways from the writing')

    agent = Agent(model,
                  output_type=MainBody,
                  tools=[duckduckgo_search_tool()],
                  system_prompt=f'We are in {curr_month} {curr_year}. '
                                'You are an expert marketing writer in the cryptocurrency space targeting institutional financial industry professionals. '
                                'You are given a draft write up of the main body of a newsletter, please format it to fit the output requirement. '
                                'Aim for 300 words in total. ' \
                                'Your writing style is engaging, provocative and quirky with attention-grabbing insights. ' \
                                'If you cannot find a quote from writing, please must search for an appropriate quote on the topic on duckduckgo. ' \
                                'You must write executive_sum in html and not markdown.' \
                                'You must write everthing as html, you must not write markdown style str' \
                                'All of your output individually must be able to run independently in a <div> class with styling. ' \
                                'Please extract an eye catching title' \
                                'Please format the executive_sum and wrapped the text in <p></p> and bolden key words with <strong></strong>. ' \
                                'Quote is optional, please include this if and only if there is a quote in the supplied draft writing, please end the quote with <br> and quote source with <cite></cite>. ' \
                                'The highlight section should show some technical process described in the writing perhaps with some questions raised. ' \
                                'Please format the highlight section with a combination of <p></p>,<ul></ul>,<li></li>,<em></em>,<strong></strong> as you see fit, as long as it can run within a <div> class.'
                                'Please sum up three most relevant and actionable bullet points for an professional in the space as take away from the writing, wrap them in <li></li> and bolden with <strong></strong> when approapriate. ' \
                                )

    print(f'agent created')
    result = agent.run_sync(f'Please format and minimally rewrite {formatted}')

    print(result.output.title)
    print('\n')
    print(result.output.executive_sum)
    print('\n')
    print(result.output.quote)
    print('\n')
    print(result.output.highlight)
    print('\n')
    print(result.output.key_takeaway)
    print('\n')

    output_dir = Path(f'./output/articles_{now.strftime("%B")}_{now.strftime("%Y")}')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir/f'main_body_{now.strftime("%B")}_{now.strftime("%Y")}.json'
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result.output.model_dump(), f, ensure_ascii=False, indent=2)
    print(f"\n✅ Saved main body article {result.output.title} to {output_path}")

    return result



if __name__=="__main__":
    get_articles(news_topic)