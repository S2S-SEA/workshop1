

import datetime

def getDate(date):
    #there are no errors inside this function.
    if (date.count('') > 9):
        newDate = datetime.datetime.strptime(date, "%d/%m/%Y").date()
    else :
        newDate = datetime.datetime.strptime(date, "%d/%m/%y").date()
     
    return newDate.strftime('%d %b, %Y')


birthday = input('Please enter your birthday: ') 
birthDate = getDates(birthday, year)

print(birthDate)
isCorrect = input('Is your birthday correct (Y/N)?")

if isCorrect != 'Y' 
    newBirthday = input('Please enter your birthday in the following format DD/MM/YYYY: ')
      newBirthDate = getDate(newBirthday)
    print('Happy Birthday for ' + newBirthDate)
else:
    print('Happy Birthday for ' + birthDate)