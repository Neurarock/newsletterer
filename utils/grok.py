import requests
from playwright.sync_api import sync_playwright
from pathlib import Path
import os

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
url = "https://grok.com/share/c2hhcmQtMi1jb3B5_b84b07fd-d356-47da-a8b6-d2e6c956603d"

def parse_grok(url:str):

    output_dir = Path(f'./grok_convo_scrap')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = f'./grok_convo_scrap/{url[-10:]}.md'
    output_path_html = f'./grok_convo_scrap/{url[-10:]}.html'
    output_path_ss = f'./grok_convo_scrap/screenshot_{url[-10:]}.jpg'

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            user_agent = user_agent,
        )
        page = context.new_page()
        # Remove hidden/offscreen elements so page.content() only contains visible content
        page.add_init_script(
        """
        (function() {
            function isHidden(el) {
                try {
                    const s = window.getComputedStyle(el);
                    if (!s) return false;
                    if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) === 0) return true;
                } catch (e) {}
                if (el.hidden || el.getAttribute('aria-hidden') === 'true') return true;
                return false;
            }
            function removeHidden() {
                const all = Array.from(document.querySelectorAll('*'));
                for (const el of all) {
                    if (isHidden(el)) el.remove();
                }
            }
            document.addEventListener('DOMContentLoaded', removeHidden, {once: true});
            window.addEventListener('load', removeHidden, {once: true});
            new MutationObserver(removeHidden).observe(document.documentElement || document, {childList: true, subtree: true});
        })();
        """
        )

        page.goto(url)
        page.screenshot(path = output_path_ss, full_page=True)
        content = page.content()
        browser.close()
        print(content)

    """
        with open("grok.html", "w") as f:
            f.write(content)
    """

    """
    with open(output_path_html, "w", encoding="utf-8") as f:
        f.write(content)
    """
    
    """
    with open('grok.html') as f:
        content = f.read()
    """

    """
    split = content.split(')]1,')

    grok_response = split[1]
    response = grok_response.split('</script><script nonce="">')
    formatted = response[0]

    output_dir = Path(f'./grok_convo_scrap')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = f'./grok_convo_scrap/{url[-10:]}.md'

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(formatted)

    print(f"\n✅ Parsed Grok response ({url[-10:]}) to {output_path}")
    return formatted
    """

if __name__=="__main__":
    parse_grok(url)
