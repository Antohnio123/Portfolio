from urllib import request
import xlsxwriter
import smtplib
from email.message import EmailMessage
import win32com.client as win32
from os import getcwd


# Входные данные ----------------------------------------------------------
web_page1 = 'https://yandex.ru/news/quotes/2002.html'       # Доллар
web_page2 = 'https://yandex.ru/news/quotes/2000.html'       # Евро
RESULTFILE = 'PythonResult.xlsx'
worksheetName = "CurrencyDynamic"
SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465
SENDER_LOGIN = "a.a.test@mail.ru"
SENDER_PASSWORD = "uipathTest"
RECIEVER_EMAIL = "antohnio@mail.ru"
SUBJECT = "Результат теста по скраппингу курсов валют - А.А. Макаров, Python"
BEGIN_MESSAGE = "Это результат теста с курсами валют на Питоне. В файле "


# Выгружаем данные с Яндекса -----------------------------------------------
def cut(source, begin, end, startindex=0):
    """An inside-parser function to cut one row of a data"""
    Ind1 = source[startindex:].index(begin)+len(begin)
    Ind2 = source[(startindex + Ind1):].index(end)
    finalindex = startindex + Ind1 + Ind2
    result = source[(startindex+Ind1):(startindex+Ind1+Ind2)]
    return result, finalindex


def scrapper(web_site):
    """A parser, that takes data from a target site, in this case - currency rates from Yandex."""
    req = request.Request(web_site)
    response = request.urlopen(req)
    web_page = str(response.read())
    table = cut(web_page, '</th></tr><tr class="quote__day quote', '</table>')[0]
    index=0
    date = ['Дата']
    value = ['Курс']
    change = ['Изменение']
    try:
        while table:
            currentdate = cut(table, '<td class="quote__date">', '</t', index)
            date.append(currentdate[0])
            index = currentdate[1]
            curerentvalue = cut(table, '<td class="quote__value"><span class="quote__sgn"></span>', '</t', index)
            value.append(float(curerentvalue[0].replace(',', '.')))
            index = curerentvalue[1]
            currentsign = cut(table, '<span class="quote__sgn">', '</span>', index)
            sign = currentsign[0]
            index = currentsign[1]
            currentchange = cut(table, '</span>', '</t', index)
            change.append(float(sign+currentchange[0].replace(',', '.')))
            index = currentchange[1]
    except ValueError:
        pass
    return date, value, change


D = scrapper(web_page1)
E = scrapper(web_page2)


# Работаем с файлом Эксель -----------------------------------------------₽$
def excelwork(RESULTFILE, worksheetName, D, E):
    """Pastes data into the Excel, changing a format to Numeric,
     finds the average between two courses, makes the Autowidth"""
    with xlsxwriter.Workbook(RESULTFILE) as workbook:
        ws1 = workbook.add_worksheet(worksheetName)
        row=0
        col=0
        cell_format = workbook.add_format({'num_format': '# ###,##0.00 ₽;-# ###,##0.00 ₽'})


        for i in range(0, len(D[0])):
            ws1.write(row, col, D[0][i])
            ws1.write(row, col +1, D[1][i], cell_format)
            ws1.write(row, col + 2, D[2][i], cell_format)
            ws1.write(row, col + 3, E[0][i])
            ws1.write(row, col + 4, E[1][i], cell_format)
            ws1.write(row, col + 5, E[2][i], cell_format)
            ws1.set_column(1, 8, 20)
            row += 1
        row=1
        col=6
        for i in range(2, len(D[0])+1):
            ws1.write(row, col, "=B"+str(i)+"/E"+str(i))
            row += 1

    # автоширина через Win32.com.client
    Dir=getcwd()
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(Dir+'/'+RESULTFILE)
    ws = wb.Worksheets(worksheetName)
    ws.Columns.AutoFit()
    wb.Save()
    excel.Application.Quit()


excelwork(RESULTFILE, worksheetName, D, E)


# Отправляем SMTP-письмо -----------------------------------------------
def sendmessage(SMTP_SERVER, SMTP_PORT, SENDER_LOGIN, SENDER_PASSWORD, RECIEVER_EMAIL, SUBJECT, BEGIN_MESSAGE):
    """Sends the result excel file via email."""
    if (len(D[0]) % 10) == 1 and (len(D[0]) % 100) != 11:
        finalofmessage = " строку."
    elif (len(D[0]) % 10) < 5 and (len(D[0]) % 10) > 1 and ((len(D[0]) % 100) >14 or (len(D[0]) % 100) < 11):
        finalofmessage = " строки."
    else:
        finalofmessage = " строк."
    MESSAGE_BODY = BEGIN_MESSAGE + str(len(D[0])) + finalofmessage
    MESSAGE = EmailMessage()
    MESSAGE['Subject'] = SUBJECT
    MESSAGE['From'] = SENDER_LOGIN
    MESSAGE['To'] = RECIEVER_EMAIL
    MESSAGE.set_content(MESSAGE_BODY)
    with open(RESULTFILE, 'rb') as f:
        file_data = f.read()
    MESSAGE.add_attachment(file_data, maintype = 'file', subtype='xlsx', filename = RESULTFILE)
    with smtplib.SMTP_SSL (SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(SENDER_LOGIN, SENDER_PASSWORD, initial_response_ok=True)
        smtp.send_message(MESSAGE)


sendmessage(SMTP_SERVER, SMTP_PORT, SENDER_LOGIN, SENDER_PASSWORD, RECIEVER_EMAIL, SUBJECT, BEGIN_MESSAGE)
