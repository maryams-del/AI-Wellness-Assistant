## Testing:

**These responses are copy pasted from the terminal**

## Asking question for the lifestyle recommender

% Scenario 1 
**Input**: "I eat a burger everyday"
**Expected Agent**: LifestyleRecommenderAgent
**Given response**: 
        Agent says: * Increase fruit and vegetable intake.
                    * Choose leaner meats or plant-based alternatives.
                    * Incorporate whole grains and legumes.
                    * Reduce processed foods and saturated fats.
                    * Control portion sizes.

% Scenario 2
**Input**: "i have sore eyes and a headache"
**Expected Agent**: SymptomCheckerAgent
**Given response**:
        Agent says: * Eye irritation.
                    * Head pain.
                    * Consult a doctor for evaluation.

% Scenario 3
**Input**: "i have sore eyes and a headache, and i eat a burger everyday"
**Expected Agent**: SymptomCheckerAgent and LifestyleRecommenderAgent
**Given response**:
        Agent says: * Eye irritation.
                    * Head pain.
                    * Consult a doctor for evaluation.


                    * Increase fruit and vegetable intake.
                    * Choose leaner meats or plant-based alternatives.
                    * Incorporate whole grains and legumes.
                    * Reduce processed foods and saturated fats.
                    * Control portion sizes.

% Scenario 4
**Errors or asking non sensical things**


1. 
**Input**: quir
**Given response**:
    Agent says: I'm sorry, I don't understand what you mean by "quir".  Can you please rephrase your request or provide more information?

2. 
**Input**: give me a makeup list of products to buy
**Given response**:
    Agent says: I am sorry, I cannot fulfill this request. I do not have the functionality to provide makeup product recommendations.

3.
**Input**: whats the weather like today
**Given response**:
    Agent says: I cannot access real-time information, including weather data.  To get the weather, please check a local news website or weather app.

4. 
**Input**: dhfldhguhdjhgbgjt
**Given response**:
    Agent says: I'm sorry, I don't understand what you mean by "dhfldhguhdjhgbgjt".  Can you please rephrase your request?