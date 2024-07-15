"""
YouTube summariser
By Mohammed Amer

This program takes a video URL as input and gives you its summary if the video has English subtitles present.
"""

import os
import openai

# Read the API key from file
with open("api_key.txt", "r") as file:
    openai.api_key = file.read().strip()

# Get the YouTube video's URL as input
url = input('Input the URL of the video you want to summarise:\n')

#Download transcript using yt-dlp
os.system('yt-dlp --write-sub --sub-format vtt --sub-lang en --skip-download -o transcript '+url)

#Read transcript
file = open("transcript.en.vtt","r")

#Filter out timestamps and blank lines
transcript = ''

line_number = 1
for line in file:
    if line_number >3:
        if line != '\n' and line[0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            transcript += line
    line_number += 1

#Create summary using ChatGPT API
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Summarise this transcript: \""+ transcript + "\""}])

#Print summary
print('Summary:\n')
print(response['choices'][0]['message']['content'])

#Print token usage
print('')
print('Tokens used:')
tokens_used = response['usage']['total_tokens']
print(tokens_used)

#Print cost
print('')
cost = tokens_used * 0.00016
print('Cost:')
print('₹ '+str(cost))
