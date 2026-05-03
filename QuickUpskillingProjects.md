

# Note: An API defines and enforces a contract between client and server, and provides controlled access to data and behavior through that contract.
# Remember: You’re not done when it works—you’re done when you can rebuild it!
# If your API breaks under testing, you don’t understand it yet.


## Try tomorrow:

- 1) Run your API and use the built-in docs first


 - Add edge-case handling (this is where people fall apart)

   Test your API properly:
        
     - PUT non-existing ID → 404        
   - DELETE same ID twice → 404        
   - POST invalid data → 422        
   - PUT with missing fields → what happens?
   - Empty state: with empty products
   - try GET /products via API request (CURL/Postman)
   - try GET /products/1 via API request (CURL/Postman)


👉 This is where your understanding becomes real.

#  What FastAPI actually provides:
- **Defining how your server exposes and enforces a contract over HTTP**.

FastAPI handles:

 - **1. Routing**  
 maps request → function
 - **2. Parsing**  
 JSON → Python objects
- **3. Validation**  
enforces your schema (ProductCreate)
 - **4. Serialization**  
Python → JSON response

## Accordingly the BaseModel classes ensure
### Validation:
- correct types
required fields
constraints
### Parsing/Conversion:
- JSON: 
```
{"price": "2.5"} 
```
to Python: 
```
price = Decimal("2.5")
```
### Data structure:

You now have a real object:

```
product.name
product.price
```
Instead of dealing with raw dicts.

### Why this matters:

Without BaseModel, you’d have to:

 - manually parse JSON
 - check types
 - handle missing fields
 - convert values

That’s error-prone and repetitive.

## You’ve reached the point where “more theory” won’t help. Your next step is to complete the CRUD loop and fix your broken retrieval logic. Right now, your GET endpoint is still wrong. Fix that first—no shortcuts.
See:
https://chatgpt.com/g/g-p-68bf3bfd5e6c8191aa329a55070231de/c/69f22b05-c704-83eb-aef3-cfbee6a3fed6
 


# What a professional would actually do

Not your proposal.

## They would:

 - Load initial data
 - Define strict Pydantic models
 - Use endpoints to mutate that data
 - Later: replace JSON with a database

Example:
```
items = load_items()

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404)

    items[item_id] = item.dict()
    return items[item_id]
```
# What you should do next (this is the real step)

Your model is good enough. Stop refining it.

Now force it into reality:

## 1. Wire it into FastAPI
- POST /products
- GET /products
- PUT /products/{id}


## 2. Attack it with bad input

Send:
```
{
  "name": "This name is way too long for the constraint",
  "price": -5,
  "tags": ["invalid_tag"]
}
``` 
If your API doesn’t reject this cleanly → your model is incomplete.

## 3. Decide on strictness

Try both:

- current (coercion allowed)
- strict mode enabled

Observe the difference. That’s not theory — that’s API design.

## Bottom line
- Your model is already good enough
- Improving it further right now is low ROI
- The real gap is integration + behavior under bad input


## You need to define a data contract.

That contract is your Pydantic model:
```
class Item(BaseModel):
```
It answers:

What fields are required?
What types are allowed?
What can be missing?
What defaults apply?

That’s very different from “creating an object.”


## The correct responsibility split
### Your job

Define the rules:
```
price: float
supplier: Supplier | None

``` 
### FastAPI + Pydantic’s job

Create objects for you, from incoming requests:
```
def create_item(item: Item):
```
You never manually build that item.
It’s constructed from external JSON.


# 4-WEEK EXECUTION PLAN — AI TRANSLATION EVALUATION API

## System Definition (Step 0 — BEFORE Week 1)

**My system helps translation teams evaluate and compare machine translation outputs to decide which system or output is suitable for specific business contexts (e.g. contracts) using real or representative translation data and evaluation metrics (BLEU, chrF, METEOR, BARTScore).**

---

# WEEK 1 — FOUNDATION (FastAPI + Structure)

## Goal
Working API with clean structure, validation, and basic endpoint

## Tasks

- [ ] Setup project (FastAPI + Uvicorn)
- [ ] Create project structure:
  - `app/`
  - `routers/`
  - `services/`
  - `models/`
- [ ] Create `/evaluate` endpoint
- [ ] Define Pydantic models:
  - `source_text`
  - `translated_text`
- [ ] Implement placeholder evaluation logic
- [ ] Return structured JSON response
- [ ] Run API locally
- [ ] Test with Postman / curl

## Example

### Input
```json
{
  "source_text": "Hello world",
  "translated_text": "Hallo Welt"
}
```
### Output
```
{
  "scores": {},
  "message": "placeholder"
}
```


### Outcome

“I built a REST API using FastAPI with structured JSON validation and modular architecture.”






# WEEK 2 — CORE EVALUATION (BLEU + chrF)
## Goal

Real evaluation logic with two complementary metrics

## Tasks
 -  Implement BLEU (e.g. sacrebleu)
 -  Implement chrF
 -  Handle:
    -    tokenization
    - normalization
 -  Handle edge cases:
    - empty input
    - invalid text
 -  Integrate both metrics into response
 -  Add basic evaluation interpretation logic

## Output Example
```
{
  "scores": {
    "bleu": 0.42,
    "chrf": 0.55
  },
  "evaluation": "acceptable"
}
```
## Outcome

“I implemented translation evaluation using complementary metrics (BLEU and chrF) and handled preprocessing and edge cases.”


# WEEK 3 — ADVANCED METRICS + STRUCTURE
## Goal

+ Upgrade from technical demo → credible evaluation system

# Tasks
## Architecture
- Separate:
API layer (routers)
evaluation logic (services)
 Add logging
 Clean code structure

## Add advanced metrics
 Implement METEOR
 Integrate BARTScore (if feasible within timebox)
 Normalize output format across all metrics

## Interpretation Layer
 Combine metrics into:
aggregated score OR
rule-based recommendation
 Define trade-offs:
lexical vs semantic
## Documentation
 Write README section:
why multiple metrics?
strengths/limitations of each
## Output Example
```
{
  "scores": {
    "bleu": 0.42,
    "chrf": 0.55,
    "meteor": 0.48,
    "bartscore": -1.2
  },
  "analysis": "lexically strong, semantically moderate"
}
```
## Outcome

“I designed a multi-metric evaluation system and handled trade-offs between lexical and semantic evaluation.”

# WEEK 4 — COMPARISON + DECISION SUPPORT
## Goal

Turn system into decision-support tool

## Tasks
## Add /compare endpoint
 ## Input:
 ```
{
  "source_text": "...",
  "translation_a": "...",
  "translation_b": "..."
}
```

## Logic
 Evaluate both translations
 Compare across all metrics
 Define decision logic:
weighted scoring OR
rule-based selection
## Output
```
{
  "better_translation": "A",
  "scores": {
    "A": {
      "bleu": 0.45,
      "chrf": 0.60
    },
    "B": {
      "bleu": 0.40,
      "chrf": 0.55
    }
  },
  "reason": "higher lexical and character-level alignment"
}
```

## Repository
 Create GitHub repo
 Add README:
problem statement
use case (decision support)
API endpoints
example requests
metric explanation
## Outcome

“I built a decision-support API to compare machine translation outputs using multiple evaluation metrics and structured scoring logic.”

## BONUS (IF TIME REMAINS)
 Add batch evaluation endpoint
 Add dataset-based testing
 Add simple report output (JSON/CSV)
# RULES (NON-NEGOTIABLE)
Build > Plan
Ship weekly
Keep scope tight
No overengineering (no Docker/Kubernetes yet)
FINAL GOAL AFTER 4 WEEKS

You can confidently say:

“I built a system that evaluates and compares machine translation outputs using multiple metrics and supports decision-making in real-world translation workflows.”


---

# Final note (important)

Your metric knowledge is now actually a **competitive advantage**—but only if:

- you **explain trade-offs**
- you **don’t overengineer**
- you **tie everything to decisions**

---

If you want next:

👉 I can review your **project structure before you start coding**  
(or fix it after Day 1 so you don’t build on a weak foundation)


"*******************************************"


# 8. Timeline from NOW
## Week 1

✔ CV ready

✔ FastAPI project done

✔ first applications sent
## Week 2–3
✔ interviews start

✔ refine answers

✔ continue applications

## Month 2–3
✔ realistic offer range


# API BASICS (PRE-APPLICATION SPRINT — 2–3 DAYS)

## Goal

Gain practical REST API + JSON experience

---

# Tasks (26 April)

- [x] Install FastAPI + Uvicorn
- [x ] Create simple API endpoint
- [ ] Accept JSON input from messy JSON file
- [ ] Create Pydantic objects incl. validation
i.e. structural correctness and business/practical relevance
- [ ] Return JSON response
- [ ] Run locally
- [ ] Create GET/POST/PUT functions for API calls to FASTAPI for your data

---

## Example

Input:

{
  "text": "Hello world"
}

Output:

{
  "processed_text": "hello world"
}

---

## Stretch (optional)

- [ ] Add second endpoint
- [ ] Log requests
- [ ] Handle errors

---

## Outcome

Be able to say:

“I implemented a REST API using FastAPI,
handling JSON input/output and integrating processing logic.”

# 1-DAY FASTAPI MINI-PROJECT (REST API + JSON)

## GOAL

Build a simple REST API that:

- accepts JSON input
- processes text
- returns JSON output

At the end, you can say:

"I built a REST API using FastAPI that handles JSON requests and responses."

---

## TIMEBOX

- Setup: 30 min
- Implementation: 2–3h
- Testing: 1h
- Understanding + explanation: 1h

Total: ~5 hours

---

## STEP 1 — SETUP

### Create project structure



# MINI INTEGRATION PROJECT (2–3 DAYS EXTENSION)

## Goal

Demonstrate system integration thinking

---

## Scenario

Simulate:

System A → API → System B

---

## Example

Input system:
- sends user text

Your API:
- processes text
- transforms data

Output system:
- receives structured result

---

## Implementation

### Step 1 — Extend API

Add endpoint:

POST /integrate

Input:

{
  "user_id": 123,
  "text": "Hello World"
}

---

### Step 2 — Transform data

Return:

{
  "user_id": 123,
  "processed_text": "hello world",
  "length": 11,
  "status": "processed"
}

---

### Step 3 — Simulate second system

Create script:

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/integrate",
    json={"user_id": 1, "text": "Test"}
)

print(response.json())