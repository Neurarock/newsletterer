from utils.template_tool import set_template
from utils.researcher import get_articles, write_article, rewrite_main_body

"""
Test Driver:
Please fill in the below 5 str variables

@main_article: the article from conversation with grok pasted in here, workaround to take url in progress.
@news_topic: the topic this month to be used to get a list of latest relevant news articles, their urls etc.
@article_topic: the AI agent will write an opinion piece on a topic, this can also prompt on direction of the view.

@month_year: relating to the 'edition' such as "Nov 2025"
@recipient_name: username such as "jonathan@neurarock"
"""

def main():

    month_year = "Nov 2025"
    recipient_name = "davidENfrance"

    main_article = """
# A Transatlantic Stablecoin Passport:  
## The Next Bretton Woods for Digital Money?
---

### **I. The Quiet Revolution in Anglo-American Regulatory Dialogue**

For the first time since the 1944 Bretton Woods conference, the **United States and United Kingdom** are on the cusp of forging a **bilateral financial accord**—not for gold or dollars, but for **stablecoins**.  

The **UK–US Financial Regulatory Working Group (FRWG)**, quietly upgraded in Q1 2025, has moved stablecoin **reciprocity** from academic panels to **active policy drafting**. The core proposal: **mutual recognition** of prudentially supervised stablecoin issuers. A US issuer chartered by the **OCC** or licensed under **NYDFS BitLicense** could, with minimal additional filing, offer GBP-pegged payment tokens in the UK. Conversely, an FCA-authorized UK issuer could distribute USD stablecoins to US institutional clients under a **federal safe harbor**.

This is not mere regulatory courtesy. It is the **first attempt to create a cross-border digital money corridor** with the rigor of traditional finance—but without the 70-year baggage of correspondent banking.

---

### **II. How It Compares to Traditional Finance Reciprocity**

| Dimension                   | **Traditional Finance (Basel/FSB Era)**                       | **Stablecoin Reciprocity (2025–2026)**                          |
|-----------------------------|--------------------------------------------------------------|----------------------------------------------------------------|
| **Legal Foundation**        | Bilateral treaties, MoUs, Basel III equivalence              | FRWG joint statement + statutory instruments (UK FSMA; US potential Lummis-Gillibrand) |
| **Scope**                   | Banks, insurers, market infrastructure                       | Narrow: fiat-backed, payment-focused stablecoins only          |
| **Supervisory Standard**    | Full home-host supervision; capital floors                   | **"Outcomes-based equivalence"** – focus on reserves, redemption, custody |
| **Speed of Recognition**    | 3–7 years (e.g., EU–US CCP equivalence took 5 years)         | **Target: 12–18 months** post-legislation                      |
| **Failure Regime**          | Resolution colleges, TLAC, living wills                      | **Pre-funded redemption pools + BoE/Fed liquidity backstops** |
| **Political Risk**          | Low (post-crisis consensus)                                  | **High (US Congress gridlock; UK election cycles)**            |

**Key Insight**: Traditional reciprocity was **bank-centric and risk-averse**. Stablecoin reciprocity is **payment-centric and innovation-forward**—a deliberate inversion of priorities.

---

### **III. The Strategic Upside**

1. **Liquidity Superhighway**  
   A USD/GBP stablecoin pair with **dual regulatory blessing** would rival **CHIPS + CHAPS** in speed while bypassing correspondent banks. Estimated annual savings: **$2.1 billion** in cross-border payment friction (McKinsey, 2025).

2. **De-risking the Dollar–Pound Axis**  
   Unlike MiCA’s euro-sovereignty firewall, the US–UK pact **reinforces Anglo-American financial hegemony** in programmable money. It is a **soft power play** disguised as technical alignment.

3. **Regulatory Arbitrage Vaccine**  
   By aligning early, both jurisdictions **pre-empt offshore havens** (e.g., Singapore, UAE) from dominating institutional stablecoin flows.

---

### **IV. The Unanswered Questions**

Despite the momentum, **critical ambiguities remain**—each a potential fracture point:

1. **Reserve Asset Divergence**  
   - UK: Allows up to **60% in short-dated gilts**  
   - US: OCC guidance limits to **cash + T-bills**  
   → *Will reciprocity require a **common eligible collateral basket**? Or will issuers run **dual-reserve silos** (costly and operationally fragile)?*

2. **Redemption in Stress**  
   - UK proposes **£20K individual holding caps**  
   - US has **no per-user limits** (only institutional KYC)  
   → *In a bank run, will the BoE cap redemptions from US-issued GBP tokens? Who bears the liquidity bridge?*

3. **Anti-Money Laundering (AML) Harmonization**  
   - UK: Travel Rule enforced via **FCA + NCA**  
   - US: FinCEN + state-level patchwork  
   → *Can the FRWG agree on **real-time transaction monitoring standards** without violating data sovereignty?*

4. **Congressional Buy-In**  
   - The **Lummis-Gillibrand Responsible Financial Innovation Act** stalled in committee (again) in September 2025.  
   → *Without federal preemption, will NYDFS or OCC charters suffice for UK recognition—or will the pact collapse into **state-by-state fragmentation**?*

5. **China and EU Response**  
   - PBOC watches closely; could accelerate **e-CNY wholesale pilots** with UK banks.  
   - EU fears **extra-territorial USD stablecoin dominance** under MiCA.  
   → *Is this reciprocity a **defensive alliance** against digital yuan and digital euro silos?*

---

### **V. Conclusion: A Fork in the Digital Road**

The US–UK stablecoin passport is **the most ambitious experiment in regulatory interoperability since the euro**. If successful, it will prove that **21st-century money can be both borderless and accountable**—a template for G7-wide digital cash.

But success hinges on **political courage** in Washington and **technical precision** in London. Fail to resolve the reserve, redemption, and congressional knots, and we risk a **splinternet of stablecoins**: USD silos, GBP silos, EUR silos—each compliant, each isolated.

> **The question is not whether stablecoins will cross borders. It is whether regulators can cross borders faster than the code.**

The clock is ticking. The FRWG’s next plenary is in March 2026. By then, we will know if Bretton Woods 2.0 runs on blockchain—or remains a whiteboard dream.


"""
    
    news_topic = "stablecoin payment legislative status in major economies"

    article_topic = "UK stablecoin legal consultation framework in a positive step to the right direction, " \
    "but is way too slow in progress compared to the us. " \
    "Worries remain that it will be just a successful sandbox scheme but real impactful projects might not take off"

    get_articles(news_topic)
    write_article(article_topic)
    rewrite_main_body(main_article)
    set_template(month_year, recipient_name)
    print('Executed successfully, please find newsletter in output folder')
    return

if __name__ == "__main__":
    main()