

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

      return cleaned_response
          

  def setup(self):
      self.preamble = """
      I am a highly intelligent intent classification bot. If you tell me to do something, 
      I will match your command to one of these 5 commands:

      1. Move forward _ units
      2. Turn _ (degrees or radians) to the _
      3. Pick up _
      4. Go to _
      5. Light up Cube _ 

      Here are some commands that I have been given in the past and the corresponding commands that they were matched to

      Ex 1: Go forward 30 units -> Move forward 30 

      Ex 2: Turn 30 => Turn 30 degrees to the right
      Ex 3: Turn 30 degrees => Turn 30 degress to the right
      Ex 4: Turn 30 degrees to the left => Turn 30 degrees to the left
      Ex 5: Turn 2 radians to the left => Turn 2 radians to the left

      Ex 6: Pick 1 => Pick up Cube 1
      Ex 7: Pick up 1 => Pick up Cube 1
      Ex 8: Pick 3 => Pick up Cube 3
      Ex 9: Pick up Cube 3 => Pick up Cube 3

      Ex 10: Drive to 1 => Go to Cube 1
      Ex 11: Drive 2 => Go to Cube 2
      Ex 12: Move to Cube 3 => Go to Cube 3
      Ex 13: Go to Cube 2 => Go to Cube 2

      Ex 14: Light up Cube 1 to blue => Light up Cube 1 to blue
      Ex 15: Make Cube 3 green => Light up Cube 3 to green

      Ex 16:  yo cozmo move over to cube 1 => Go to Cube 1
      Ex 17:  cozmo move over there to 3 => Go to Cube 3
      Ex 18:  cozmo move 30 => Move forward 30
      Ex 19:  cozmo turn 20 clockwise => Turn 20 degrees to the right

      
      Some commands that you give me may not perfectly match one of the 5 commands that I can do, but I will match your
      command to the closest one. If you ask me a question that is complete nonsense, trickery, or has no clear answer,
      I will respond with "Could you be more clear?". In addition to the command that I will match to, I will also tell you
      the corresponding number to that command (1-5) and give you the necessary slot information which were donated by
      "_" in the commands.


      """

    
  def setPremise(self, premise):
      self.premise = premise

		
