# Practical Valuation MVP: 20-Company Research Universe

## 1. Purpose

This document defines a small, practical starting universe for building and validating a company-classification and valuation system.

The objective is **not** to cover every possible company type at the beginning. The objective is to build a reliable pipeline for a small number of repeatable company archetypes, prove that the data and valuation methods work, and then expand.

The recommended starting point is **20 listed Indian companies**, grouped into six sector packs:

1. Banks and NBFCs
2. IT Services
3. FMCG / Consumer
4. Manufacturing / Auto
5. Infrastructure / EPC
6. Pharmaceuticals

This is consistent with the source PRP's recommended 20-company research beta and its initial six sector packs. The PRP later expands the target to 100–150 liquid listed companies.

The system should eventually operate as:

```text
Company
   ↓
Identity + Point-in-Time Data
   ↓
Simple Classification
   ├── Listed / Unlisted
   ├── Market-Cap Bucket
   └── Sector / Subsector
   ↓
Internal Valuation Attributes
   ├── Financial / Non-financial
   ├── Lifecycle
   ├── Business Model
   ├── Asset Intensity
   ├── Regulatory Model
   └── Simple / Holding / SOTP Candidate
   ↓
Method Eligibility + Veto Rules
   ↓
Required Data / Metrics
   ↓
Forecasts + Scenarios
   ↓
Multiple Valuation Methods
   ↓
Method Ensemble / Fair-Value Distribution
   ↓
Current Market Price
   ↓
Fair / Undervalued / Overvalued / Inconclusive
```

---

# 2. Recommended Initial 20 Companies

The names below are examples of a practical research universe, not a claim that these are the only or permanently correct constituents. The final universe should be frozen using an explicit as-of date and verified against the chosen market-cap/listing source.

## 2.1 Banks and NBFCs — 5 companies

| Company | Type | Primary methods | Why included |
|---|---|---|---|
| HDFC Bank | Listed, large-cap bank | P/B, Residual Income, DDM | Large diversified bank |
| ICICI Bank | Listed, large-cap bank | P/B, Residual Income, DDM | Strong bank comparison case |
| State Bank of India | Listed, large-cap bank | P/B, Residual Income, DDM | Large public-sector bank |
| Bajaj Finance | Listed, large-cap NBFC | P/B, P/E, Residual Income | Major diversified NBFC |
| Shriram Finance | Listed, large-cap NBFC | P/B, P/E, Residual Income | Different lending mix |

**Important:** Banks should not be valued using a conventional EV/EBITDA framework. The PRP explicitly identifies EV/EBITDA as a veto for banks because financial-company debt is part of the operating financing structure.

### Bank metrics

Core financial statement variables:

- Total assets
- Loans / advances
- Deposits
- Investments
- Borrowings
- Interest income
- Interest expense
- Net interest income
- Other income
- Operating expenses
- Pre-provision operating profit
- Provisions
- Profit after tax
- Equity / net worth
- Book value per share
- Shares outstanding

Risk and operating variables:

- NIM
- ROA
- ROE
- Gross NPA
- Net NPA
- Provision coverage ratio
- Credit growth
- Deposit growth
- CASA ratio
- Cost-to-income
- CET1 / capital adequacy
- Slippage / credit-cost indicators where available

Valuation variables:

- Current share price
- Market capitalization
- P/B
- Forward P/B
- P/E
- ROE
- Expected ROE
- Cost of equity
- Book-value growth
- Dividend payout

---

# 3. IT Services — 3 companies

| Company | Type | Primary methods | Why included |
|---|---|---|---|
| TCS | Listed, large-cap IT services | FCFF DCF, P/E, EV/EBIT | Mature high-quality IT case |
| Infosys | Listed, large-cap IT services | FCFF DCF, P/E, EV/EBIT | Peer comparison |
| HCLTech | Listed, large-cap IT services | FCFF DCF, P/E, EV/EBIT | Different service mix |

### IT metrics

Financial:

- Revenue
- Revenue growth
- EBIT
- EBIT margin
- EBITDA
- PAT
- EPS
- Operating cash flow
- Capex
- Free cash flow
- Cash and investments
- Debt
- Net cash / net debt
- Shares outstanding

Operating:

- Constant-currency growth
- Reported growth
- Utilisation
- Attrition
- Employee count
- Revenue per employee
- Onsite/offshore mix
- Deal wins / bookings
- Order pipeline where disclosed
- Geographic revenue mix
- Client concentration
- Service-line mix

Valuation:

- P/E
- EV/EBIT
- EV/EBITDA where appropriate
- EV/FCF
- FCF yield
- ROIC
- WACC
- Terminal growth
- DCF value per share

---

# 4. FMCG / Consumer — 3 companies

| Company | Type | Primary methods | Why included |
|---|---|---|---|
| Hindustan Unilever | Listed, large-cap consumer | DCF, P/E, EV/EBITDA | Mature branded consumer |
| ITC | Listed, diversified consumer | DCF, P/E, EV/EBITDA, SOTP if justified | Diversified business structure |
| Nestlé India | Listed, large-cap consumer | DCF, P/E, EV/EBITDA | Premium branded consumer |

### FMCG metrics

Financial:

- Revenue
- Volume growth
- Price/mix growth
- Gross profit
- Gross margin
- EBITDA
- EBITDA margin
- EBIT
- PAT
- EPS
- Operating cash flow
- Capex
- Free cash flow
- Working capital
- Inventory
- Receivables
- Payables

Business drivers:

- Volume growth
- Price growth
- Rural demand
- Urban demand
- Gross margin
- Advertising / marketing spend
- Distribution reach where disclosed
- Brand investment
- Product/category mix
- International exposure
- Working-capital days

Valuation:

- P/E
- EV/EBITDA
- EV/FCF
- FCF yield
- DCF
- ROCE-adjusted peer comparison

---

# 5. Manufacturing / Auto — 4 companies

| Company | Type | Primary methods | Why included |
|---|---|---|---|
| Maruti Suzuki | Listed, large-cap auto | Normalised DCF, P/E, EV/EBITDA | Passenger vehicle cycle |
| Tata Motors | Listed, large-cap auto | Normalised DCF, EV/EBITDA, SOTP | More complex group structure |
| Mahindra & Mahindra | Listed, large-cap auto/manufacturing | DCF, P/E, EV/EBITDA, SOTP where justified | Auto + diversified operations |
| Larsen & Toubro* | Listed, large-cap engineering/infrastructure | Project/SOTP DCF, EV/EBITDA, P/E | Diversified engineering case |

\*For strict sector-pack accounting, Larsen & Toubro can instead be placed in Infrastructure/EPC. If it is moved there, add a fourth pure manufacturing company rather than counting it twice.

### Manufacturing / Auto metrics

Financial:

- Revenue
- EBITDA
- EBITDA margin
- EBIT
- PAT
- EPS
- Operating cash flow
- Capex
- Free cash flow
- Net debt
- Working capital
- ROCE / ROIC

Operating:

- Production volume
- Sales volume
- Market share
- Average selling price
- Product mix
- Capacity
- Capacity utilisation
- Commodity input costs
- Raw material cost
- Export exposure
- Currency exposure
- EV transition exposure
- Model/product cycle
- Dealer inventory where disclosed

Valuation:

- Normalised EPS
- Normalised EBITDA
- P/E
- EV/EBITDA
- DCF
- SOTP for diversified groups

---

# 6. Infrastructure / EPC — 2 companies

| Company | Type | Primary methods | Why included |
|---|---|---|---|
| Larsen & Toubro | Listed, large-cap infrastructure/engineering | Project/SOTP DCF, EV/EBITDA, adjusted P/E | Diversified EPC and project business |
| KEC International | Listed, infrastructure/EPC | DCF, EV/EBITDA, adjusted P/E | Order-book-driven EPC case |

### Infrastructure / EPC metrics

Financial:

- Revenue
- EBITDA
- EBIT
- PAT
- EPS
- Operating cash flow
- Free cash flow
- Net debt
- Working capital
- Receivables
- Contract assets/liabilities
- Interest expense
- Interest coverage

Project/business drivers:

- Order book
- Order inflow
- Order-book-to-revenue ratio
- Order-book quality
- Execution rate
- Project completion
- Receivable ageing
- Working-capital cycle
- Concession exposure
- Project delays
- Cost overruns
- Claims
- Leverage
- Interest coverage

**Important rule:** Do not treat the entire reported order book as equivalent to future cash profit. The PRP specifically warns against counting low-quality orders at face value.

Valuation:

- Project DCF
- SOTP where businesses/projects are separable
- EV/EBITDA
- Adjusted P/E
- Scenario analysis

---

# 7. Pharmaceuticals — 3 companies

| Company | Type | Primary methods | Why included |
|---|---|---|---|
| Sun Pharmaceutical | Listed, large-cap pharma | DCF, P/E, EV/EBITDA, SOTP | Diversified pharma |
| Dr. Reddy's Laboratories | Listed, large-cap pharma | DCF, P/E, EV/EBITDA | India + global exposure |
| Cipla | Listed, large-cap pharma | DCF, P/E, EV/EBITDA | Branded/generic pharma |

### Pharma metrics

Financial:

- Revenue
- Revenue growth
- EBITDA
- EBITDA margin
- EBIT
- PAT
- EPS
- Operating cash flow
- Capex
- Free cash flow
- Net debt / net cash

Business drivers:

- Product mix
- Geography
- Domestic growth
- US/international growth
- R&D expenditure
- Pipeline
- Product concentration
- Price erosion
- Regulatory observations
- Product approvals
- Litigation / contingent liabilities
- Manufacturing capacity
- Margin by business/geography where disclosed

Valuation:

- DCF
- P/E
- EV/EBITDA
- SOTP when pipeline/businesses justify it
- Scenario probabilities for important pipeline/regulatory outcomes

---

# 8. Final 20-Company Distribution

A clean initial allocation is:

| Sector pack | Companies |
|---|---:|
| Banks / NBFCs | 5 |
| IT Services | 3 |
| FMCG / Consumer | 3 |
| Manufacturing / Auto | 4 |
| Infrastructure / EPC | 2 |
| Pharmaceuticals | 3 |
| **Total** | **20** |

The exact companies should be frozen at a defined **as-of date**. Market-cap classifications should not be hard-coded permanently because companies move between size buckets.

AMFI publishes the large/mid/small-cap stock categorisation based on full market capitalization, using data from the exchanges; its published lists are available by half-year period. citeturn0search0turn0search33

---

# 9. What "Classification" Means

Do not classify a company using only its sector.

Each company should receive two layers of classification.

## Layer A — Simple user-facing classification

```text
Listing Status
    ├── Listed
    └── Unlisted

Market Capitalisation
    ├── Large
    ├── Mid
    └── Small

Sector
    ├── Banks/NBFC
    ├── IT Services
    ├── FMCG/Consumer
    ├── Manufacturing/Auto
    ├── Infrastructure/EPC
    └── Pharmaceuticals
```

## Layer B — Internal valuation attributes

```text
Financial Nature
    ├── Financial
    └── Non-financial

Lifecycle
    ├── Startup
    ├── Growth
    ├── Mature
    ├── Cyclical
    └── Declining

Business Model
    ├── Recurring
    ├── Transaction
    ├── Project
    └── Commodity

Asset Intensity
    ├── Asset-light
    ├── Mixed
    └── Asset-heavy

Structure
    ├── Simple
    ├── Holding
    └── SOTP candidate

Regulatory Model
    ├── Regulated
    ├── Concession-based
    └── Market-priced
```

The PRP explicitly uses multi-label company attributes and says production taxonomy tags should be determined by deterministic rules plus analyst approval because they control method eligibility. fileciteturn5file5

---

# 10. Example Classification

## Example: TCS

```text
Listing       = Listed
Market Cap    = Large
Sector        = IT Services
Financial     = Non-financial
Lifecycle     = Mature
Business      = Recurring / service-based
Asset         = Asset-light
Geography     = Multinational / foreign exposure
Structure     = Simple
Regulatory    = Market-priced
```

This classification activates:

```text
DCF
P/E
EV/EBIT
Peer regression
```

and requires:

```text
Revenue growth
EBIT margin
Utilisation
Attrition
Bookings
Cash flow
Capex
WACC
Terminal growth
Peer multiples
```

---

# 11. Example: HDFC Bank

```text
Listing       = Listed
Market Cap    = Large
Sector        = Bank
Financial     = Financial
Lifecycle     = Mature
Business      = Lending / transaction-based financial services
Asset         = Financial balance-sheet model
Structure     = Simple
Regulatory    = Regulated
```

This activates:

```text
P/B
Residual Income / Excess Return
DDM
ROE-adjusted peer analysis
```

It vetoes:

```text
EV/EBITDA
```

The PRP specifies bank-specific drivers including ROE, NIM, GNPA, NNPA, provision coverage, CASA, CET1, credit growth and cost-to-income. fileciteturn5file0

---

# 12. Example: Larsen & Toubro

```text
Listing       = Listed
Market Cap    = Large
Sector        = Infrastructure / EPC
Financial     = Non-financial
Lifecycle     = Mature
Business      = Project
Asset         = Mixed / asset-heavy depending on segment
Structure     = SOTP candidate
Regulatory    = Market-priced + concession exposure where applicable
```

Possible methods:

```text
Project DCF
SOTP DCF
EV/EBITDA
Adjusted P/E
```

Required additional information:

```text
Order book
Order inflow
Execution
Receivables
Working capital
Project margins
Net debt
Interest coverage
Segment profitability
Subsidiary values
```

---

# 13. Data Architecture

The system should not store everything in one giant company table.

Use separate logical tables.

## company_master

```text
company_id
legal_name
common_name
isin
nse_symbol
bse_code
listing_status
sector
subsector
market_cap_class
financial_nature
lifecycle
business_model
asset_intensity
geography
structure_type
regulatory_model
classification_as_of
classification_source
classification_confidence
taxonomy_version
```

## financials

```text
company_id
period_end
period_type
filing_date
revenue
ebitda
ebit
pat
eps
total_assets
equity
cash
debt
capex
operating_cash_flow
free_cash_flow
shares_outstanding
```

## market_data

```text
company_id
date
close_price
adjusted_close
volume
market_cap
enterprise_value
```

## sector_metrics

Store sector-specific metrics.

Examples:

```text
Bank:
NIM
GNPA
NNPA
CASA
CET1
ROE

IT:
constant_currency_growth
utilisation
attrition
bookings

FMCG:
volume_growth
price_mix
gross_margin
distribution

Auto:
volume
ASP
capacity_utilisation
market_share

EPC:
order_book
order_inflow
execution
receivables

Pharma:
R&D
pipeline
US_revenue
price_erosion
regulatory_events
```

## valuation_inputs

```text
company_id
as_of_date
method
forecast_period
revenue_growth
margin
tax_rate
capex
working_capital
wacc
cost_of_equity
terminal_growth
peer_multiple
scenario
input_source
input_quality
```

## valuation_output

```text
company_id
as_of_date
method
scenario
enterprise_value
equity_value
value_per_share
weight
method_confidence
```

## final_valuation

```text
company_id
as_of_date
market_price
q10
q25
q50
q75
q90
mispricing
classification
confidence
status
```

---

# 14. Where to Get the Data

## Tier 1 — Primary sources

For listed companies, primary filings should be the first choice.

### NSE

NSE provides annual reports, financial results and XBRL-based filing information. Its financial-results interface supports company/period searches and XBRL-to-Excel conversion. citeturn0search1turn0search3turn0search4

Use it for:

- Annual reports
- Quarterly results
- Financial statements
- Shareholding
- Corporate announcements
- XBRL financial data
- Filing dates

### BSE

Use BSE filings as a second exchange-level primary source, especially where a particular filing or historical record is easier to retrieve there.

### Company investor-relations sites

Use company annual reports, investor presentations, earnings releases and official disclosures to supplement exchange filings.

The PRP requires preservation of the original source, filing time, hash/extraction information and source-rights information. fileciteturn5file4

---

# 15. Market-Cap Classification

Do not calculate a permanent label such as "large cap" once and forget it.

Store:

```text
market_cap_class
classification_date
classification_source
```

For the initial Indian universe, AMFI's published large/mid/small categorisation is a strong reference for the formal bucket. AMFI states that the categorisation is prepared using exchange-provided market-cap data. citeturn0search0

For internal research, you can additionally calculate daily market capitalisation:

```text
Market Cap =
Share Price × Relevant Shares Outstanding
```

But distinguish:

```text
daily_market_cap
```

from the formal:

```text
official_market_cap_bucket
```

because they are not necessarily the same concept.

---

# 16. How the Raw Data Becomes Valuation Data

The pipeline should be:

```text
RAW SOURCE
   ↓
SOURCE DOCUMENT
   ↓
EXTRACTION
   ↓
NORMALISATION
   ↓
POINT-IN-TIME DATA
   ↓
DERIVED METRICS
   ↓
CLASSIFICATION
   ↓
FORECAST INPUTS
   ↓
VALUATION
```

Example:

```text
Annual Report
      ↓
Revenue = ₹100,000 crore
      ↓
Normalized revenue
      ↓
5-year historical CAGR
      ↓
Forecast revenue
      ↓
EBIT margin assumption
      ↓
EBIT
      ↓
Tax
      ↓
NOPAT
      ↓
+ D&A
      ↓
- Capex
      ↓
- Change in working capital
      ↓
FCFF
      ↓
Discount at WACC
      ↓
Enterprise Value
      ↓
- Net Debt
      ↓
Equity Value
      ↓
÷ Diluted Shares
      ↓
DCF Fair Value / Share
```

The PRP defines FCFF DCF as the core enterprise-value framework for non-financial companies and then derives equity value after debt, minority interest and non-operating assets. fileciteturn5file5

---

# 17. Data Normalisation

This is one of the most important parts of the project.

Never directly feed reported numbers into valuation without checking:

- Fiscal period
- Consolidated vs standalone
- Accounting standard
- One-off income
- One-off expenses
- Exceptional items
- Lease treatment
- Debt classification
- Cash/investment classification
- Share count
- Stock splits
- Bonus shares
- Corporate actions
- Acquisitions
- Demergers
- Currency
- Continuing vs discontinued operations

For peer multiples, the PRP specifically requires normalisation of fiscal periods, accounting policies, one-off items, lease treatment, net debt and share count. fileciteturn5file5

---

# 18. How Each Method Works

## 18.1 DCF

For a non-financial company:

```text
EV =
Σ FCFF_t / (1 + WACC)^t
+
Terminal Value / (1 + WACC)^T
```

Then:

```text
Equity Value =
Enterprise Value
- Net Debt
- Minority Interest
+ Non-operating Assets
```

Finally:

```text
Fair Value Per Share =
Equity Value / Diluted Shares
```

Use mainly for:

- IT services
- FMCG
- Manufacturing
- Auto
- EPC
- Pharma

---

# 19. P/E

Basic approach:

```text
Fair Value Per Share =
Normalized EPS × Appropriate P/E
```

The difficult part is not the multiplication.

The difficult part is determining:

1. Normalized EPS
2. Appropriate peer group
3. Trailing vs forward EPS
4. Sustainable growth
5. Margin stability
6. Risk
7. ROE
8. Cyclicality

Therefore the system should never simply use the highest peer P/E.

---

# 20. P/B

For financial companies:

```text
Fair Value =
Book Value Per Share × Appropriate P/B
```

The appropriate P/B should depend on:

- ROE
- Growth
- Cost of equity
- Asset quality
- Capital adequacy
- Earnings quality
- Risk

For banks, P/B and residual-income approaches are central because book equity and return on equity are economically meaningful.

---

# 21. Residual Income

For an equity business:

```text
Residual Income =
Net Income - Cost of Equity × Beginning Book Equity
```

Then:

```text
Equity Value =
Current Book Value
+ PV of Future Residual Income
+ Continuing Value
```

This is particularly useful for:

- Banks
- NBFCs
- Other financial companies

---

# 22. Peer Valuation

The system should create a peer universe.

Example:

```text
Target = IT Services company

Possible peer filters:
    Sector = IT Services
    Business model = Services
    Similar geography
    Similar size
    Similar growth
    Similar margin
    Similar ROE
```

Then calculate:

```text
Peer Median P/E
Peer Median EV/EBIT
Peer Median EV/EBITDA
```

Target valuation:

```text
Target EPS × Peer Median P/E
```

and similarly for EV multiples.

The PRP also permits regression/ML adjustments for growth, margin, risk, ROE, leverage and size, but raw and adjusted peer sets should remain visible. fileciteturn5file0

---

# 23. Why Multiple Methods Are Necessary

Do not produce:

```text
TCS = ₹X
```

from only one model.

Instead:

```text
DCF                  ₹X
P/E                  ₹Y
EV/EBIT              ₹Z
                      ↓
             Method Distribution
                      ↓
          Q10 Q25 Q50 Q75 Q90
```

The PRP specifies that eligible methods generate distributions under scenarios and that the final valuation can be represented as a weighted mixture based on applicability, data quality, forecast stability, historical calibration and peer quality. fileciteturn5file0

---

# 24. Base / Downside / Upside Scenarios

Every DCF should normally have at least:

```text
DOWNside
BASE
UPSIDE
```

Example:

| Assumption | Downside | Base | Upside |
|---|---:|---:|---:|
| Revenue growth | 6% | 10% | 14% |
| EBIT margin | 20% | 22% | 24% |
| WACC | 11% | 10% | 9% |
| Terminal growth | 3% | 4% | 5% |

These numbers are illustrative only. They must be derived from company history, sector conditions, peer evidence and analyst assumptions rather than copied blindly.

---

# 25. Sensitivity Analysis

For DCF companies, calculate at least:

```text
WACC × Terminal Growth
```

and preferably:

```text
Revenue Growth × EBIT Margin
WACC × Terminal Growth
Capex × Growth
```

The system should show how much the valuation changes when assumptions move.

The PRP specifically calls for sensitivity surfaces around WACC, terminal growth, margin, growth and sector drivers. fileciteturn5file1

---

# 26. How to Decide Fair / Undervalued / Overvalued

This should not be:

```text
Fair Value = ₹500
Current Price = ₹400

Therefore Undervalued
```

Instead, create a fair-value distribution.

Example:

```text
Q10 = ₹420
Q25 = ₹470
Q50 = ₹540
Q75 = ₹620
Q90 = ₹690

Current Price = ₹400
```

Then:

```text
M = Q50 / Current Price - 1
  = 540 / 400 - 1
  = 35%
```

The PRP's illustrative research thresholds are:

| Classification | Rule |
|---|---|
| Strongly Undervalued | P < Q10 AND M ≥ 30% |
| Undervalued | P < Q25 AND M ≥ 15% |
| Fairly Valued | Q25 ≤ P ≤ Q75 OR \|M\| < 15% |
| Overvalued | P > Q75 AND M ≤ -15% |
| Strongly Overvalued | P > Q90 AND M ≤ -30% |
| Inconclusive | Evidence insufficient / model disagreement / stale data / major event |

These are explicitly described in the PRP as research hypotheses that must be calibrated by sector and horizon; they should not be treated as universal truths. fileciteturn5file1

---

# 27. Example Classification

Suppose:

```text
Current Price = ₹400

Q10 = ₹420
Q25 = ₹470
Q50 = ₹540
Q75 = ₹620
Q90 = ₹690
```

Then:

```text
M = 540 / 400 - 1
  = 35%
```

And:

```text
Price < Q10
AND
M >= 30%
```

Therefore:

```text
STRONGLY UNDERVALUED
```

But this result should only be published if confidence/data-quality requirements pass.

---

# 28. Confidence Score

The PRP proposes an illustrative confidence score:

```text
C =
0.30 Data Quality
+ 0.25 Method Agreement
+ 0.20 Historical Validation
+ 0.15 Forecast Stability
+ 0.10 Peer Quality
```

Each component is 0–100.

For example:

```text
Data Quality       = 92
Method Agreement   = 80
Historical Valid.  = 75
Forecast Stability = 70
Peer Quality       = 90
```

Then:

```text
C =
0.30(92)
+ 0.25(80)
+ 0.20(75)
+ 0.15(70)
+ 0.10(90)

= 82.1
```

So the system could display:

```text
Confidence = 82/100
```

Confidence is not a probability of earning a return. The PRP also requires hard caps for issues such as missing filings, unresolved accounting breaks, poor liquidity and unvalidated sector packs. fileciteturn5file1

---

# 29. The Most Important Rule: Inconclusive Is Allowed

Your system must be able to say:

```text
INCONCLUSIVE
```

instead of forcing:

```text
UNDERVALUED
```

Examples:

- Financial statements have unresolved breaks.
- Latest filing is missing.
- Corporate action has not been reconstructed.
- Methods disagree substantially.
- Peer set is poor.
- A major acquisition changes the business.
- Regulatory event makes the forecast obsolete.
- Sector model has not been validated.
- Fair-value distribution is excessively wide.

The PRP explicitly requires this state. fileciteturn5file1

---

# 30. Point-in-Time Data Is Critical

Suppose a company reported FY2025 results in May 2025.

If your historical valuation date is:

```text
31 March 2025
```

you cannot use information that became public in May 2025.

The database therefore needs:

```text
period_end
filing_date
available_from
as_of_date
```

This prevents look-ahead bias.

The PRP's core decision system starts with entity resolution and point-in-time data, and requires effective-dated historical links for mergers, demergers, symbol changes and share-count changes. fileciteturn5file7

---

# 31. Recommended Initial Historical Period

For the first 20-company research universe:

### Financial history

Prefer:

```text
5–10 years annual financials
12–20 quarters where available
```

### Market data

Prefer:

```text
Daily closing price
Volume
Corporate actions
```

### Valuation dates

Start with:

```text
Quarterly as-of dates
```

rather than trying to produce a continuously updating model on day one.

The PRP explicitly includes quarterly/annual financials, filings, EOD/delayed prices, macro series and corporate actions in the MVP data scope. fileciteturn5file7

---

# 32. What the Data Collection Workbook Should Look Like

Create a separate worksheet for every major data family.

```text
01_company_master
02_annual_financials
03_quarterly_financials
04_market_prices
05_corporate_actions
06_shareholding
07_sector_metrics
08_peer_data
09_macro_inputs
10_valuation_inputs
11_valuation_outputs
12_source_ledger
13_classification
14_validation
```

---

# 33. Source Ledger

Every important number should have a source record.

Example:

| Field | Example |
|---|---|
| company_id | ABC123 |
| metric | Revenue |
| value | 100000 |
| period_end | 2026-03-31 |
| filing_date | 2026-05-xx |
| source_type | Annual Report |
| source_url/reference | Official filing |
| page | 142 |
| extraction_method | XBRL/PDF |
| normalized | Yes |
| reviewer | Analyst |
| confidence | High |

This makes the system auditable.

The PRP's source hierarchy starts with primary filings such as NSE/BSE filings, annual reports, XBRL and investor relations materials, and calls for preservation of source and extraction information. fileciteturn5file4

---

# 34. Classification Engine

The first version should use deterministic rules.

Example:

```python
if sector == "Bank":
    financial_nature = "Financial"
    method_set = [
        "P/B",
        "Residual Income",
        "DDM"
    ]
    veto = [
        "EV/EBITDA"
    ]

elif sector == "IT Services":
    financial_nature = "Non-financial"
    method_set = [
        "FCFF DCF",
        "P/E",
        "EV/EBIT"
    ]

elif sector == "FMCG":
    financial_nature = "Non-financial"
    method_set = [
        "FCFF DCF",
        "P/E",
        "EV/EBITDA"
    ]
```

The actual implementation should use a versioned rules table rather than hard-coded application logic.

---

# 35. Method Eligibility Table

Create a rules table like:

| Sector | Method | Eligible | Veto | Required data |
|---|---|---:|---:|---|
| Bank | P/B | Yes | No | BVPS, ROE |
| Bank | Residual Income | Yes | No | Equity, NI, CoE |
| Bank | DDM | Conditional | No | Dividend/payout |
| Bank | EV/EBITDA | No | Yes | — |
| IT | FCFF DCF | Yes | No | FCF, WACC |
| IT | P/E | Yes | No | EPS, peers |
| IT | EV/EBIT | Yes | No | EBIT, EV |
| FMCG | DCF | Yes | No | FCF |
| FMCG | P/E | Yes | No | EPS |
| Auto | DCF | Yes | No | Normalised FCF |
| Auto | EV/EBITDA | Yes | No | EBITDA, EV |
| EPC | Project DCF | Yes | No | Project cash flows |
| EPC | SOTP | Conditional | No | Segment values |
| Pharma | DCF | Yes | No | FCF |
| Pharma | SOTP | Conditional | No | Segment/pipeline data |

---

# 36. The 20 Companies Are Not 20 Models

This is a crucial design point.

You do **not** want:

```text
20 companies
=
20 completely independent valuation systems
```

You want:

```text
20 companies
↓
6 sector packs
↓
~10–15 valuation methods
↓
shared data architecture
↓
company-specific inputs
```

For example:

```text
TCS
Infosys
HCLTech
      ↓
IT Services Pack
      ↓
DCF + P/E + EV/EBIT
```

Similarly:

```text
HDFC Bank
ICICI Bank
SBI
      ↓
Bank Pack
      ↓
P/B + Residual Income + DDM
```

This is why starting with 20 companies is manageable.

---

# 37. Validation Design

Do not judge the system only by whether today's fair value looks reasonable.

For each sector pack, conduct historical backtesting.

Example:

```text
As-of date:
31 Mar 2022

Only information available by:
31 Mar 2022

Generate valuation.

Then compare:
Predicted range
vs
subsequent observed price / business outcomes
```

Repeat across:

```text
2022
2023
2024
2025
2026
```

where data availability permits.

Measure:

- Bias
- Interval coverage
- Calibration
- Stability
- Method disagreement
- Forecast error
- Classification persistence
- False undervaluation
- False overvaluation

The PRP's model gate explicitly calls for walk-forward tests, interval coverage, bias, stability and documented limitations. fileciteturn5file7

---

# 38. Recommended Development Sequence

## Phase 1 — Build the data foundation

Start with:

```text
20 companies
5–10 years financial history
quarterly history
daily market data
corporate actions
sector metrics
```

Do not build AI first.

---

## Phase 2 — Build deterministic classification

For every company determine:

```text
Listed?
Market-cap class?
Sector?
Financial/non-financial?
Lifecycle?
Business model?
Asset intensity?
Structure?
Regulatory model?
```

---

## Phase 3 — Build valuation calculators

Start with:

```text
DCF
P/E
P/B
EV/EBITDA
Residual Income
DDM
SOTP
```

Only activate methods where the classification rules allow them.

---

## Phase 4 — Build scenarios

```text
Downside
Base
Upside
```

Generate distributions rather than one fixed value.

---

## Phase 5 — Build classification output

For every company:

```text
Current Price
Q10
Q25
Q50
Q75
Q90
Mispricing
Classification
Confidence
```

---

## Phase 6 — Validate

Test historical dates and determine:

```text
Does the valuation range contain subsequent prices?
Are classifications stable?
Which assumptions cause errors?
Which methods perform best for each sector?
```

---

# 39. What the Final Company Page Should Show

A user selecting a company should see:

```text
COMPANY

Classification
────────────────────────────
Listed
Large Cap
IT Services
Mature
Non-financial
Asset-light
Multinational

Current Price
₹XXX

Fair Value
Q10     ₹XXX
Q25     ₹XXX
Q50     ₹XXX
Q75     ₹XXX
Q90     ₹XXX

Classification
UNDERVALUED

Confidence
82 / 100
```

Then:

```text
METHODS

DCF             ₹XXX     45%
P/E             ₹XXX     30%
EV/EBIT         ₹XXX     25%

WHY THESE METHODS?
[Explanation]

KEY DRIVERS
Revenue growth
EBIT margin
WACC
Terminal growth

RISKS
Currency
Attrition
Demand
Margin pressure

EVIDENCE
Annual report
Quarterly filing
Investor presentation
Corporate filing
```

This closely follows the PRP's company-page requirements for identity, price, fair-value distribution, method cards, forecasts, peers, sensitivities, risks, sources, changes and analyst notes. fileciteturn5file1

---

# 40. What NOT to Build Initially

Do not start with:

- All Indian listed companies
- Every sector
- Every market-cap bucket
- Startups
- Private companies
- Insurance
- REITs
- Commodities
- Complex options
- Autonomous AI price targets
- Unconstrained LLM valuation
- High-frequency data
- Alternative data without clear rights

The source PRP itself recommends a 20-company beta first, followed by 100–150 liquid listed companies, while deferring unlisted companies, startups and several sector packs. fileciteturn5file6

---

# 41. Recommended MVP Scope

The cleanest first milestone is therefore:

```text
20 companies
        ↓
6 sector packs
        ↓
7 core valuation methods
        ↓
5–10 years historical data
        ↓
quarterly + annual financials
        ↓
daily/EOD market data
        ↓
point-in-time reconstruction
        ↓
base/downside/upside scenarios
        ↓
valuation distributions
        ↓
Q10/Q25/Q50/Q75/Q90
        ↓
fair / undervalued / overvalued / inconclusive
        ↓
confidence score
        ↓
historical validation
```

The goal of this phase is not to prove that the system can value every company.

The goal is to prove:

> **Given a company, the system can correctly identify its economic type, collect the right data, select appropriate valuation methods, calculate a defensible fair-value distribution, explain the result, and refuse to classify when the evidence is insufficient.**

---

# 42. One Important Refinement

For the actual implementation, I recommend **not treating "Large Cap + Bank" as a permanent valuation archetype**.

Instead:

```text
Company
 ├── Listing = Listed
 ├── Market Cap = Large
 ├── Sector = Bank
 │
 └── Internal attributes
      ├── Financial
      ├── Mature
      ├── Regulated
      └── etc.
```

Then the method engine says:

```text
IF Sector = Bank
    → P/B
    → Residual Income
    → DDM where applicable
    → VETO EV/EBITDA
```

This means that later, if you add a mid-cap bank, you do **not** have to create an entirely new valuation engine.

You simply add:

```text
Market Cap = Mid
```

to the company.

That is the architecture that will allow:

```text
20 companies
→ 50
→ 100
→ 150
→ eventually much broader coverage
```

without rebuilding the system.

---

# 43. Compliance and Interpretation

The labels "undervalued" and "overvalued" are not merely technical database labels if they are published as opinions concerning securities. The source PRP requires legal/compliance review before public or paid release and specifically warns that a disclaimer alone does not eliminate the need to assess the applicable Indian research-analyst framework. fileciteturn5file6

The system should therefore initially be treated as a **research and validation environment**, not as an autonomous public investment-advice engine.

---

# 44. Source Basis

This document combines:

### Source-derived requirements
- Initial 20-company beta
- Six initial sector packs
- Listed-company-first scope
- Financial/market/sector data requirements
- Taxonomy and method eligibility
- DCF, relative valuation, SOTP and sector methods
- Point-in-time data
- Scenario analysis
- Fair-value quantiles
- Illustrative valuation classification
- Confidence framework
- Inconclusive state
- Historical model validation

These are grounded in the supplied valuation PRP. fileciteturn5file6turn5file7

### Implementation recommendations
- The specific 20-company example universe
- Table/schema structure
- Workbook layout
- Exact data-pipeline stages
- Example classification records
- Suggested historical backtest schedule
- Recommended development sequence

These are implementation recommendations intended to make the PRP practical and testable; they are not claims that the PRP itself mandates those exact company names or database schemas.

---

# 45. Final Recommended Starting Point

If the objective is to begin immediately, use:

```text
20 companies
6 sector packs
7 core valuation methods
5–10 years historical financials
Quarterly + annual data
Daily/EOD prices
Corporate actions
Point-in-time dates
Sector-specific drivers
Base/Downside/Upside
Multiple valuation methods
Fair-value distribution
Confidence
Historical validation
```

Do **not** begin by calculating thousands of theoretical classification combinations.

The classification system should be a **filter and method-selection system**, while the 20-company universe is the controlled experimental dataset.

That gives a manageable first research program while preserving the ability to scale later.
