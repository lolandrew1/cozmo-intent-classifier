

import os
import re
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

queries = []
answers = []

class IntentClassifier():
  def __init__(self):
      self.queries = []
      self.answers = []
      self.premise = ""
      self.preamble = ""
      self.setup()

      
  def classify(self, query):
      messages = [
                {"role": "system", "content": self.preamble},
                {"role": "user", "content": self.premise},
                {"role": "user", "content": self.queries},
                {"role": "assistant", "content": self.answers},
                {"role": "user", "content": f"Q: {query}"}
      ]

      response = client.chat.completions.create(
          model="gpt-4-turbo-preview",
          messages=messages
      )
      
      for choice in response.choices:
          # remove LaTeX brackets from response
          cleaned_response = re.sub(r'\\[\[\]\(\)]', '', choice.message.content)

      queries.append({"role": "user", "content": f"Q: {query}"})
      answers.append({"role": "assistant", "content": f"A: {cleaned_response}"})

      response_lines = cleaned_response.split("\n")

      try:
        command_line = response_lines[1]
        command_num = response_lines[1].split("-")[1]
        info = response_lines[2].split("-")[1].split(",")
        
        return (int(command_num), info)
      except:
        return(-1, [3])

     

          

  def setup(self):
      self.preamble = """
      I am a highly intelligent intent classification bot. If you tell me to do something, 
      I will match your command to one of these 4 commands:

      1. Move forward (integer) units
      2. Turn (integer) degrees to the (left/right)
      3. Pick up Cube (1-3)
      4. Go to Cube (1-3)

      Here are some commands that I have been given in the past and the corresponding commands that they were matched to

      Ex 1: Go forward 30 units -> Move forward 30 

      Ex 2: Turn 30 => Turn 30 degrees to the right
      Ex 3: Turn 30 degrees => Turn 30 degress to the right
      Ex 4: Turn 30 degrees to the left => Turn 30 degrees to the left

      Ex 6: Pick 1 => Pick up Cube 1
      Ex 7: Pick up 1 => Pick up Cube 1
      Ex 8: Pick 3 => Pick up Cube 3
      Ex 9: Pick up Cube 3 => Pick up Cube 3

      Ex 10: Drive to 1 => Go to Cube 1
      Ex 11: Drive 2 => Go to Cube 2
      Ex 12: Move to Cube 3 => Go to Cube 3
      Ex 13: Go to Cube 2 => Go to Cube 2

      Ex 14: Go grab Cube 1 => Pick up Cube 1
      Ex 15: Grab 3 => Pick up Cube 3

      Ex 16:  yo cozmo move over to cube 1 => Go to Cube 1
      Ex 17:  cozmo move over there to 3 => Go to Cube 3
      Ex 18:  cozmo move 30 => Move forward 30
      Ex 19:  cozmo turn 20 clockwise => Turn 20 degrees to the right
      
      I will give you a reponse in this exact format:

      Command-(the matched command) 
      Number-(the corresponding number to the matched command (1-4)) 
      Info-(slot information 1)-(slot information 2 (if necessary)) 
      
      The necessary slot information were donated by the parentheses in the commands.

      For example, a response that may be return might look like: 
      
      Command-Go to Cube 3
      Number-4
      Info-3

      If there are multiple information slots, the response might look like this:

      Command-Turn 30 degrees to the right
      Number-2
      Info-30,right

      Some commands that you give me may not perfectly match one of the 4 commands that I can do, but I will match your
      command to the closest one. 
      
      If you ask me a question that doesn't match any of the commands, I will see if you are asking a question about my premise. 
      If it seems like you are, I will do my best to answer. In this case I will return a response in this format: 5 for the number line
      and the answer to the question in the Info line. For example, if question was "Is cube 1 visible", I would look at my premise to see
      if cube1 was visible. In this case, my response might look something like 

      Command-question
      Number-5
      Info-Cube 1 is not visible

      If your question doesn't seem relevant to what I know from the premise or from previous requests,
      I will respond with "Could you be more clear?". 


      """

    
  def setPremise(self, premise):
      self.premise = "PREMISE" + "\n" + premise

        
