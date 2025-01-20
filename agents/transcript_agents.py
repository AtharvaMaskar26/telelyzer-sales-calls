from typing import List
import json
from pydantic import BaseModel

class ScoringFormat(BaseModel):
    """This class defines the structured output format for KPIs"""
    score: bool
    feedback: str
    
class TranscriptAgents:
    """This class consists of all the agents that take care of the transcripts."""

    def __init__(self, raw_transcripts: List, cleaned_transcripts: str) -> None:
        """
        This function initializes the Transcripts Agents Class

        Parameters:
            - raw_transcripts (List) -> Raw transcripts in Lists
            - cleaned_transcripts (str) -> Cleaned Transcripts. 
        """
        self.raw_transcripts = raw_transcripts
        self.cleaned_transcripts = cleaned_transcripts
        self.keywords = ', '.join(open("../data/keywords.txt", "r").readlines())

    def transcript_correction_agent(self, raw_transcripts: List) -> str:
        """
        This function corrects the raw_transcripts provided using keywords. 

        Parameters:
            - raw_transcripts (List) -> Raw transcripts

        Returns:
            - corrected_transcripts (str) -> Concatenated corrected transcripts
        """

        system_prompt = f"""You are a helpful assistant for the company Choice Finx. Your task is to correct any spelling discrepancies in the transcribed text. Make sure that the names of the following products are spelled correctly: Choice Finx, Choice Broking, {self.keywords}. Only add necessary punctuation such as periods, commas, and capitalization, and use only the context provided.
        """
        corrected_transcripts = []

        for transcript in self.transcript:
            completion = self.client.beta.chat.completions.parse(
                model="gpt-3.5-turbo",
                temperature=0,
                messages=[
                    {"role": "developer", "content": system_prompt},
                    {
                        "role": "user",
                        "content": transcript
                    }
                ]
            )
            translated_transcript = completion.choices[0].message.content
            corrected_transcripts.append(translated_transcript)
        
        self.corrected_transcripts = corrected_transcripts
        self.cleaned_corrected_transcripts = ' '.join([t for t in corrected_transcripts])

        return self.cleaned_corrected_transcripts
    
    def benefits_agent(self) -> ScoringFormat:
        """
        This agent checks if the customer support agent has covered the benefits of the choice App. This is the first part of the script that the agent has to follow. 
        """

        system_prompt = f"""
        You are a professional Customer Support Script Adherence Checker working for Choice Finx. You will be provided with a transcript of a call between the customer support agent and the customer. Your job is to:

        1. Carefully read through the entire transcript and evaluate if the agent has mentioned **all the benefits** of the Choice Finx app as outlined in the reference script.
        2. For each point in the reference script, determine:
        - If the point was **fully covered**, **partially covered**, or **missed entirely**.
        - If partially covered or missed, provide **exactly what the agent said** and explain how it differs from the expected script.
        - Provide a suggested response that the agent should use next time to fully cover the point.

        3. At the end, return the following:
        - A **boolean value (True/False)** indicating whether all points were fully covered.
        - A list of all points that were partially covered or missed, along with the agent’s errors and suggested corrections.

        --- Reference Script ---
        1. All-in-one App: Trade and invest in all segments (like equity, commodity, currency) and invest in insurance, MF, Basket.  
        2. Recommended calls from Mr. Sumit Bagadia (research head) with call accuracy in the recommendation option.                                                               
        3. Chat with experts through the app (recommendation chat option available on the right side of recommendations).                                                   
        4. Brokerage transparency: Clients can see brokerage and other charges at the time of placing an order.                                                      
        5. Advanced Buy/Sell orders through GTC, GTD, and Bracket Orders.                                                                                                           
        6. Clients can contact support and back office directly through the app.                                                                                                       
        7. Clients can add funds through UPI (not chargeable) and Net Banking (chargeable). Guide clients to add funds through UPI.             
        8. Fund addition pitching to clients is important.

        Your output should strictly follow this format:

        1. Boolean Result: [True/False]
        2. Missed or Partially Covered Points:
        - Point [Number]: [Summary of the error]
        - What the agent said: [Agent’s words]
        - Suggested correction: [What the agent should have said]

        If all points are fully covered, return:
        1. Boolean Result: True
        2. Message: "The agent has covered all points as per the script."

        """


        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "developer", "content": system_prompt.strip()},
                {
                    "role": "user",
                    "content": self.cleaned_corrected_transcripts
                }
            ], 
            response_format=ScoringFormat
        )

        result = completion.choices[0].message.content 
        self.benefits = json.loads(result)

        return self.benefits
    
    def brokerage_amc_charges_agent(self) -> ScoringFormat:
        """
        This function checks if the customer support agent has talked about the brokerage and AMC charges to the customers.
        """

        system_prompt = f"""
        You are a professional Customer Support Script Adherence Checker working for Choice Finx. You will be provided with a transcript of a call between the customer support agent and the customer. Your job is to:

        1. Carefully read through the entire transcript and evaluate if the agent has mentioned about the **brokerage and AMC charges on the platform** of the Choice Finx app as outlined in the reference script.
        2. For each point in the reference script, determine:
        - If the point was **fully covered**, **partially covered**, or **missed entirely**.
        - If partially covered or missed, provide **exactly what the agent said** and explain how it differs from the expected script.
        - Provide a suggested response that the agent should use next time to fully cover the point.

        3. At the end, return the following:
        - A **boolean value (True/False)** indicating whether all points were fully covered.
        - A list of all points that were partially covered or missed, along with the agent’s errors and suggested corrections.

        --- Reference Script ---
        1. AMC is free for 1st year & from 2nd year is (200+18%gst=Rs. 236).                                                                                                       
        2. DP transaction charges Rs 10 + gst.
        3. We have customised brokerage plan in our company. Brokerage are as follow: Delivery - 0.20% (20 paisa) Intraday - 0.02%(2 paisa), Future -0.02%(2 paisa), Option - Rs 25 per lot.                                                                                                                                                                     

        Your output should strictly follow this format:

        1. Boolean Result: [True/False]
        2. Missed or Partially Covered Points:
        - Point [Number]: [Summary of the error]
        - What the agent said: [Agent’s words]
        - Suggested correction: [What the agent should have said]

        If all points are fully covered, return:
        1. Boolean Result: True
        2. Message: "The agent has covered all points as per the script."
        """

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "developer", "content": system_prompt.strip()},
                {
                    "role": "user",
                    "content": self.cleaned_corrected_transcripts
                }
            ], 
            response_format=ScoringFormat
        )

        result = completion.choices[0].message.content 
        self.brokerage_amc_charges = json.loads(result)

        return self.brokerage_amc_charges
    
    def usps_of_choice_agent(self) -> ScoringFormat:
        """
        This function checks if the customer support agent has covered all the USPs of Choice. 
        """

        system_prompt = f"""
        You are a professional Customer Support Script Adherence Checker working for Choice Finx. You will be provided with a transcript of a call between the customer support agent and the customer. Your job is to:

        1. Carefully read through the entire transcript and evaluate if the agent has mentioned about the **USPs of Choice** of the Choice Finx app as outlined in the reference script.
        2. For each point in the reference script, determine:
        - If the point was **fully covered**, **partially covered**, or **missed entirely**.
        - If partially covered or missed, provide **exactly what the agent said** and explain how it differs from the expected script.
        - Provide a suggested response that the agent should use next time to fully cover the point.

        3. At the end, return the following:
        - A **boolean value (True/False)** indicating whether all points were fully covered.
        - A list of all points that were partially covered or missed, along with the agent’s errors and suggested corrections.

        --- Reference Script ---
        1.We provide you daily Research calls & market News update/ notification in app
        2.We have Same day pay-out facility, No charges for Auto square off  & No charges for call & trade facility.
        3. Sumeet sir live session Monday & Thursday 11.30 am on YouTube channel. subscribe the channel. Live session notification will get in choice finx app
        4.Client can see Real-Time Research Advisory from 9.15 am to 3.15pm in app.                                                                                            
        5. MARGIN TRADING FUNDING (MTF)                                                                                                                                                       
        5.1. MTF facility available in Cash segment only .Leverage upto 4x (depend upon shares).                                                                           
        5.2. MTF can be hold upto 90 days (after 90 days MTF stocks will be squared off by the broker).
        5.3. Interest charge will be 0.58% (per day will be charged on the funded amount till you hold the stocks) for example: on 1 lakh funding through MTF then interest will (1lakh * 0.058%)= 58rs/ perday.                                                                                                   
        5.4.Pledge/unpledge will cost Rs.10+GST/stock                                                                                                                                                  
        5.5. To use the MTF facility  client have to activate the DDPI(POA) & MTF through app it self.                                                 "

        Your output should strictly follow this format:

        1. Boolean Result: [True/False]
        2. Missed or Partially Covered Points:
        - Point [Number]: [Summary of the error]
        - What the agent said: [Agent’s words]
        - Suggested correction: [What the agent should have said]

        If all points are fully covered, return:
        1. Boolean Result: True
        2. Message: "The agent has covered all points as per the script."
        """

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "developer", "content": system_prompt.strip()},
                {
                    "role": "user",
                    "content": self.cleaned_corrected_transcripts
                }
            ], 
            response_format=ScoringFormat
        )

        result = completion.choices[0].message.content 
        self.usps_of_choice = json.loads(result)

        return self.usps_of_choice

    def basket_agent(self) -> ScoringFormat:
        """
        This function checks if the customer support agent has talked about the baskets
        """

        system_prompt = f"""
        You are a professional Customer Support Script Adherence Checker working for Choice Finx. You will be provided with a transcript of a call between the customer support agent and the customer. Your job is to:

        1. Carefully read through the entire transcript and evaluate if the agent has mentioned about the **Baskets** of the Choice Finx app as outlined in the reference script.
        2. For each point in the reference script, determine:
        - If the point was **fully covered**, **partially covered**, or **missed entirely**.
        - If partially covered or missed, provide **exactly what the agent said** and explain how it differs from the expected script.
        - Provide a suggested response that the agent should use next time to fully cover the point.

        3. At the end, return the following:
        - A **boolean value (True/False)** indicating whether all points were fully covered.
        - A list of all points that were partially covered or missed, along with the agent’s errors and suggested corrections.

        --- Reference Script ---
        1. Basket offer diversified portfolio for long-term investment. Client can invest in various stocks through 1 basket.
        2. No lock in period (any time withdraw).               
        3. No maintenance charges .(only brokerage charge).                                                         
        4. Minimum investment starting Rs. 8k

        Your output should strictly follow this format:

        1. Boolean Result: [True/False]
        2. Missed or Partially Covered Points:
        - Point [Number]: [Summary of the error]
        - What the agent said: [Agent’s words]
        - Suggested correction: [What the agent should have said]

        If all points are fully covered, return:
        1. Boolean Result: True
        2. Message: "The agent has covered all points as per the script."
        """

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "developer", "content": system_prompt.strip()},
                {
                    "role": "user",
                    "content": self.cleaned_corrected_transcripts
                }
            ], 
            response_format=ScoringFormat
        )

        result = completion.choices[0].message.content 
        self.baskets = json.loads(result)

        return self.baskets
    
    def algo_agent(self) -> ScoringFormat:
        """
        This function checks if the customer support agent has talked about the algo feature to the customer. 
        """

        system_prompt = f"""
        You are a professional Customer Support Script Adherence Checker working for Choice Finx. You will be provided with a transcript of a call between the customer support agent and the customer. Your job is to:

        1. Carefully read through the entire transcript and evaluate if the agent has mentioned about the **Algo** of the Choice Finx app as outlined in the reference script.
        2. For each point in the reference script, determine:
        - If the point was **fully covered**, **partially covered**, or **missed entirely**.
        - If partially covered or missed, provide **exactly what the agent said** and explain how it differs from the expected script.
        - Provide a suggested response that the agent should use next time to fully cover the point.

        3. At the end, return the following:
        - A **boolean value (True/False)** indicating whether all points were fully covered.
        - A list of all points that were partially covered or missed, along with the agent’s errors and suggested corrections.

        --- Reference Script ---
        Algo trading is automatic strategy based trading were client can work on system based  strategy of can create own strategy.
        1. Client can trade in Cash / Intraday / FNO.
        2. Emotions free trading                                                                                      
        3. In case client is busy and do not have the time to track the market, then algo  will trade on behalf of client as per the strategy.  4 Client can also analyse & understand  the strategy with the help of demo facility.

        Your output should strictly follow this format:

        1. Boolean Result: [True/False]
        2. Missed or Partially Covered Points:
        - Point [Number]: [Summary of the error]
        - What the agent said: [Agent’s words]
        - Suggested correction: [What the agent should have said]

        If all points are fully covered, return:
        1. Boolean Result: True
        2. Message: "The agent has covered all points as per the script."
        """

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "developer", "content": system_prompt.strip()},
                {
                    "role": "user",
                    "content": self.cleaned_corrected_transcripts
                }
            ], 
            response_format=ScoringFormat
        )

        result = completion.choices[0].message.content 
        self.algo = json.loads(result)

        return self.algo

    def mutual_funds_agent(self) -> ScoringFormat:
        """
        This function checks if the customer support agent checks if the customer support agent has talked about the mutual funds to the customer.
        """

        system_prompt = f"""
        You are a professional Customer Support Script Adherence Checker working for Choice Finx. You will be provided with a transcript of a call between the customer support agent and the customer. Your job is to:

        1. Carefully read through the entire transcript and evaluate if the agent has mentioned about the **Mutual Funds** of the Choice Finx app as outlined in the reference script.
        2. For each point in the reference script, determine:
        - If the point was **fully covered**, **partially covered**, or **missed entirely**.
        - If partially covered or missed, provide **exactly what the agent said** and explain how it differs from the expected script.
        - Provide a suggested response that the agent should use next time to fully cover the point.

        3. At the end, return the following:
        - A **boolean value (True/False)** indicating whether all points were fully covered.
        - A list of all points that were partially covered or missed, along with the agent’s errors and suggested corrections.

        --- Reference Script ---
        Mutual fund is long term secure investment plan. Which helps in diversifications of funds. managed by professional.   
        1. Client can invest through sip for long term and short term. 
        2. Minimum locking period for 3yrs in tax saving mutual funds. 
        3. Client can start minimum sip from Rs,1000.

        Your output should strictly follow this format:

        1. Boolean Result: [True/False]
        2. Missed or Partially Covered Points:
        - Point [Number]: [Summary of the error]
        - What the agent said: [Agent’s words]
        - Suggested correction: [What the agent should have said]

        If all points are fully covered, return:
        1. Boolean Result: True
        2. Message: "The agent has covered all points as per the script."
        """

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "developer", "content": system_prompt.strip()},
                {
                    "role": "user",
                    "content": self.cleaned_corrected_transcripts
                }
            ], 
            response_format=ScoringFormat
        )

        result = completion.choices[0].message.content 
        self.mutual_funds = json.loads(result)

        return self.mutual_funds     

    def insurance_agent(self) -> ScoringFormat:
        """
        This function checks if the customer support agent has talked about the insurance to the agent. 
        """

        system_prompt = f"""
        You are a professional Customer Support Script Adherence Checker working for Choice Finx. You will be provided with a transcript of a call between the customer support agent and the customer. Your job is to:

        1. Carefully read through the entire transcript and evaluate if the agent has mentioned about the **Insurance** of the Choice Finx app as outlined in the reference script.
        2. For each point in the reference script, determine:
        - If the point was **fully covered**, **partially covered**, or **missed entirely**.
        - If partially covered or missed, provide **exactly what the agent said** and explain how it differs from the expected script.
        - Provide a suggested response that the agent should use next time to fully cover the point.

        3. At the end, return the following:
        - A **boolean value (True/False)** indicating whether all points were fully covered.
        - A list of all points that were partially covered or missed, along with the agent’s errors and suggested corrections.

        --- Reference Script ---
        1.We offer Life & General insurance like (Health , motor etc). 
        2.We offer guaranteed return plan 
        3.Life cover + Tax  saving plan    
        4. Own and family protection.

        Your output should strictly follow this format:

        1. Boolean Result: [True/False]
        2. Missed or Partially Covered Points:
        - Point [Number]: [Summary of the error]
        - What the agent said: [Agent’s words]
        - Suggested correction: [What the agent should have said]

        If all points are fully covered, return:
        1. Boolean Result: True
        2. Message: "The agent has covered all points as per the script."
        """

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "developer", "content": system_prompt.strip()},
                {
                    "role": "user",
                    "content": self.cleaned_corrected_transcripts
                }
            ], 
            response_format=ScoringFormat
        )

        result = completion.choices[0].message.content 
        self.insurance = json.loads(result)

        return self.insurance     
    
    def referral_accounts(self) -> ScoringFormat:
        """
        This function checks if the customer support agent has talked about the referral accounts to the customer. 
        """

        system_prompt = f"""
        You are a professional Customer Support Script Adherence Checker working for Choice Finx. You will be provided with a transcript of a call between the customer support agent and the customer. Your job is to:

        1. Carefully read through the entire transcript and evaluate if the agent has mentioned about the **Referral Accounts** of the Choice Finx app as outlined in the reference script.
        2. For each point in the reference script, determine:
        - If the point was **fully covered**, **partially covered**, or **missed entirely**.
        - If partially covered or missed, provide **exactly what the agent said** and explain how it differs from the expected script.
        - Provide a suggested response that the agent should use next time to fully cover the point.

        3. At the end, return the following:
        - A **boolean value (True/False)** indicating whether all points were fully covered.
        - A list of all points that were partially covered or missed, along with the agent’s errors and suggested corrections.

        --- Reference Script ---
        1. Ask for the referal account from the client. They will get benefit of Rs 500 in a form  of broekarge reversal.

        Your output should strictly follow this format:

        1. Boolean Result: [True/False]
        2. Missed or Partially Covered Points:
        - Point [Number]: [Summary of the error]
        - What the agent said: [Agent’s words]
        - Suggested correction: [What the agent should have said]

        If all points are fully covered, return:
        1. Boolean Result: True
        2. Message: "The agent has covered all points as per the script."
        """

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "developer", "content": system_prompt.strip()},
                {
                    "role": "user",
                    "content": self.cleaned_corrected_transcripts
                }
            ], 
            response_format=ScoringFormat
        )

        result = completion.choices[0].message.content 
        self.referral = json.loads(result)

        return self.referral