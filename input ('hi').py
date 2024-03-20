import json
import os


def Similarity(UserInput,JsonData,devMode):
  MaxMatchPercentage = 85.00
  HighestMatch = None
  HighestMatchPercentage = 0.00


  for key in JsonData:
    MatchPercentage = CalculatePercentage(UserInput, key)
    if devMode is True:
      MatchPercentage =round(MatchPercentage,2)
      print("The match between",UserInput,"and",key,'is',MatchPercentage)

    if MatchPercentage > HighestMatchPercentage and MatchPercentage > MaxMatchPercentage:
      HighestMatchPercentage = MatchPercentage
      HighestMatch = key
  if devMode is True:
    HighestMatchPercentage =round(HighestMatchPercentage,2)
    print("Highest Match Percentage is",HighestMatchPercentage)
    print("Highest Match is",HighestMatch)

  if HighestMatchPercentage > MaxMatchPercentage:
    return HighestMatch
  return None


def CalculatePercentage(str1, str2):
  CharCount = {}

  for char in str1 + str2:
    if char in CharCount:
      CharCount[char] += 1
    else:
      CharCount[char] = 1

  CommonCharsCount = 0
  TotalUniqueChars = 0

  for char in CharCount:
    CommonCharsCount += CharCount[char] if char in str1 and char in str2 else 0
    TotalUniqueChars += max(CharCount[char] for s in [str1, str2] if char in s)
  if TotalUniqueChars <= 0 or CommonCharsCount <= 0:
    return 0
  return (CommonCharsCount / TotalUniqueChars) * 100



def characterRemoval(UserInput, devMode):
  RemoveCharacters = ['!','@', '#', '$', '%', '.', ',', '?','>','<','^','*','&','(',')']
  
  for char in RemoveCharacters:
    UserInput = UserInput.replace(char, '')
  
  UserInput = ' '.join(UserInput.split())
  if devMode is True:
    print("UserInput after character removal:", UserInput)
  return UserInput
  

def LoadJsonData(filename):
  if not os.path.exists(filename):
    with open(filename, 'w') as file:
      json.dump({}, file)

  with open(filename, 'r') as file:
    return json.load(file)


def SaveJsonData(filename, data):
  with open(filename, 'w') as file:
    json.dump(data, file)




JsonFilename = 'responses.json'
JsonData = LoadJsonData(JsonFilename)
devMode = False
os.system('cls' if os.name == 'nt' else 'clear')
while True:
  FirstUserInput = input('You: ').lower()

  if FirstUserInput == '/print':
    print(JsonData)
    continue

  if FirstUserInput == '/exit':
    break

  if FirstUserInput == '/dev':
    if devMode == False:
      devMode = True
      print('devMode true')
    else:
      devMode = False
      print('devMode false')
    continue


  if FirstUserInput.isspace() or FirstUserInput == '' or len(FirstUserInput) <= 1:
    continue

  UserInput = characterRemoval(FirstUserInput, devMode)
  
  if devMode is True:
    print('syncing to json data')

  HighestMatch = Similarity(UserInput, JsonData, devMode)

  if devMode is True:
    print('Data synced')
  if HighestMatch in JsonData and HighestMatch is not None:
    if FirstUserInput != HighestMatch:
      print('Bot: Auto Corrected Input :',HighestMatch)
    print('Bot:', JsonData[HighestMatch])

  else:
    print("Bot: I haven't heard of",FirstUserInput,"before.")
    print('Could you tell me what to so if someone else were to ask me that question?')
    response = input('Response : ').lower()
    response = response.capitalize()
    if devMode is True:
      print('Response capitalized')

    if response == 'No':
      continue

    JsonData[UserInput] = response
    SaveJsonData(JsonFilename, JsonData)



