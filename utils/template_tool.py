from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import json
from pathlib import Path
import glob
import os

month_year = "Nov 2025"
recipient_name = "DAVIDENFRANCE"

def set_template(month_year, recipient_name):
    month_year = month_year
    recipient_name = recipient_name
    now = datetime.now()

    folder = Path(f'./output/articles_{now.strftime("%B")}_{now.strftime("%Y")}')
    article_index = len(os.listdir(folder)) - 1

    pattern = f"{folder}/{article_index}*.json"

    file = glob.glob(pattern)
    if file:
        with open(file[0], "r", encoding="utf-8") as f:
            agent_article = json.load(f)  # or json.load(f) if JSON

    with open(f'./output/articles_{now.strftime("%B")}_{now.strftime("%Y")}.json', "r", encoding="utf-8") as f:
        news_summary = json.load(f)
    
    with open(f'./output/articles_{now.strftime("%B")}_{now.strftime("%Y")}/main_body_{now.strftime("%B")}_{now.strftime("%Y")}.json', "r", encoding="utf-8") as f:
        main_body = json.load(f)
        if main_body["quote"]!='':
            main_body["quote"]=f'<div class="quote">{main_body["quote"]}</div>'
    

    for article in news_summary:
        dt = datetime.fromisoformat(article["date"])  # handles "+00:00"
        article["formatted_date"] = dt.strftime("%d %b %Y")  # "10 Nov 2025"

    # loading the environment
    env = Environment(loader = FileSystemLoader('templates'))

    # loading the template
    template = env.get_template('newsletter.html')


    time_frame = now.strftime("%A %d %m %Y")

    # rendering the template and storing the resultant text in variable output
    output = template.render(time_frame=time_frame,
                             articles=news_summary,
                             article_content=agent_article["content"],
                             article_sub_title=agent_article["article_sub_title"],
                             recipient_name=recipient_name,
                             edition = month_year,
                             title = main_body["title"],
                             exec_sum = main_body["executive_sum"],
                             quote = main_body["quote"],
                             highlight = main_body["highlight"],
                             take_aways = main_body["key_takeaway"],
    )
    output_dir= Path(f'./output/newsletter_{now.strftime("%B")}_{now.strftime("%Y")}')
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(f"{output_dir}/newsletter.html", "w", encoding="utf-8") as f:
        f.write(output)

    print("✅ HTML file generated successfully: output.html")

if __name__ == "__main__":
    set_template()