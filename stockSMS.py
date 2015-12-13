import getpass
import os
import smtplib
import urllib
from time import sleep


def symbol_entry():
    print "SMS Stock Alert"
    print "Enter a symbol followed by return."
    print "Enter 'done' when finished.\n"
    stock_list = []

    while True:
        add_symbol = raw_input('Enter symbol: ')
        add_symbol = add_symbol.upper()
        if add_symbol != 'DONE':
            stock_list.append(add_symbol)
        else:
            break
    return stock_list


def error_check(stock_list):
    print '\n'
    print "Is this list correct?"
    x = 0
    for items in stock_list:
        x += 1
        print("{}) " + "{}").format(x, items)

    error_check = raw_input("Enter 'y' or 'n' >>> ")

    if error_check == 'n':
        start()
    elif error_check == 'y':
        pass
    else:
        print "You entered something other than 'y' or 'n'"
        error_check()


def start():
    stock_list = symbol_entry()
    error_check(stock_list)
    return stock_list


def phone_info():
    print"\n"
    phone_number = raw_input("Enter cell phone number: ")
    print "\nWho is your wireless Carrier?:"
    print "(V)erizon Wireless"
    print "(A)T&T"
    print "(S)print \n"
    carrier = raw_input("Enter 'V', 'A' or 'S' >>> ")
    if carrier.lower() == 'a':
        carrier = '@txt.att.net'
    elif carrier.lower() == 'v':
        carrier = '@vtext.com'
    elif carrier.lower() == 's':
        carrier = '@messaging.sprintpcs.com'
    from_email = raw_input("Enter a GMAIL email address: ")
    gmail_password = getpass.getpass('Password: ')
    to_email = phone_number + carrier
    return from_email, to_email, gmail_password


def time_interval():
    minutes = int(raw_input("\nSMS alert interval in minutes: "))
    print "\nUpdating price via SMS every %d minutes." % minutes
    print "ctrl-c to terminate..."
    seconds = minutes * 60
    return seconds


def get_price(symbol):
    url = "http://download.finance.yahoo.com/d/quotes.csv?s="\
        "%s&f=sl1d1c1hgv" % symbol
    f = urllib.urlopen(url)
    s = f.read()
    f.close()
    s = s.strip()
    L = s.split(',')
    price = L[1]
    change = L[3]
    return price, change


def send_email(from_email, to_email, gmail_password, txt_msg):
    SERVER = 'smtp.gmail.com'
    PORT = 587
    password = gmail_password
    sender = from_email
    recipient = to_email
    body = txt_msg
    body = "" + body + ""
    headers = ["To: " + recipient]
    headers = "\r\n".join(headers)
    session = smtplib.SMTP(SERVER, PORT)

    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, password)
    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
    session.quit()


os.system('cls' if os.name == 'nt' else 'clear')

# 1) User inputs stocks
stock_list = start()
stock_list.sort()

# 2) User inputs Phone info
from_email, to_email, gmail_password = phone_info()

# 3) How often would the user like updates?
seconds = time_interval()

stocks_list_price = []
stocks_list_change = []
txt = open('txt_msg.txt', 'r+')
txt.truncate()

for stocks in stock_list:
    price, change = get_price(stocks)
    stocks_list_price.append(price)
    stocks_list_change.append(change)
    str = stocks + ':   $' + price + '\n'
    txt.write(str)


txt.seek(0)
txt_msg = txt.read()

while True:
    send_email(from_email, to_email, gmail_password, txt_msg)
    sleep(seconds)
