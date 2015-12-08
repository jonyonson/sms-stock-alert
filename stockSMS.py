import urllib
import os, sys
from time import sleep
import smtplib

#------------------------------------------------------------------------------

def symbol_entry():
    print "\n"
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

    x = 0
    for items in stock_list:
        x += 1
        print("{}) " + "{}").format(x, items)

    print '\n'
    print "Enter '1' if the above list is complete and correct."
    print "Enter '2' to restart if an error exists. \n"
    error_check = raw_input("Enter '1' or '2' >>> ")

    if error_check == '2':
        start()
    elif error_check == '1':
        pass
    else:
        print "You entered something other than '1' or '2'"
        error_check()

def start():
    stock_list = symbol_entry()
    error_check(stock_list)
    return stock_list

def phone_info():
    print"\n"
    phone_number = raw_input("Enter cell phone number: ")
    print "\nWho is your wireless Carrier?:"
    print "1. Verizon Wireless"
    print "2. AT&T"
    print "3. Sprint \n"
    carrier = raw_input("Enter '1', '2' or '3' >>> ")
    if carrier == '2':
        carrier = '@txt.att.net'
    elif carrier == '1':
        carrier = '@vtext.com'
    elif carrier == '3':
        carrier = '@messaging.sprintpcs.com'
    from_email = raw_input("Enter a GMAIL email address: ")
    gmail_password = raw_input("Enter your gmail password: ")
    to_email = phone_number + carrier
    return from_email, to_email, gmail_password

def time_interval():
    minutes = int(raw_input("\nHow often would you like to receive updates (minutes): "))
    seconds = minutes * 60
    return seconds

def get_price(symbol):
    url = "http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1c1hgv" % symbol
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

#------------------------------------------------------------------------------

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
    l_str = stocks + ":   "
    r_str = '$' + price
    #str = l_str.ljust(9) + r_str.rjust(8) + "\n" # up to 8 stocks in a txt
    str = l_str + r_str + '\n'
    txt.write(str)


txt.seek(0)
txt_msg = txt.read()

while True:
    send_email(from_email, to_email, gmail_password, txt_msg)
    sleep(seconds)
