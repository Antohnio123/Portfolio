from urllib import request
import smtplib
from email.message import EmailMessage
import pandas as pd
# xlrd, lxml, xlsxwriter, jinja2


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


def scrapper(web_site):
    """A Pandas parser, that takes table-data from a target site Yandex"""
    req = request.Request(web_site)
    response = request.urlopen(req)
    web_page = str(response.read().decode('utf-8'))
    df_list = pd.read_html(web_page)  # this parses all the tables in webpages to a list
    df = df_list[0]
    df['Курс'], df['Изменение'] = df['Курс']/10000, df['Изменение']/10000
    df['Дата'] = pd.to_datetime(df['Дата']).dt.date
    return df


def excel_wrapper(resultfile_name, sheet_name, dataframe1, dataframe2=None):
    result = pd.concat([dataframe1, dataframe2], axis='columns')
    result['USDtoEUR'] = result.iloc[:,1]/result.iloc[:,4]
    with pd.ExcelWriter(resultfile_name, engine='xlsxwriter') as writer:
        result.to_excel(writer, sheet_name=sheet_name)
        worksheet = writer.sheets[sheet_name]
        worksheet.set_column('A:G', 18)
    return result


def sendmessage(dataframe, SMTP_SERVER, SMTP_PORT, SENDER_LOGIN, SENDER_PASSWORD, RECIEVER_EMAIL, SUBJECT, BEGIN_MESSAGE):
    """Sends the result excel file via email."""
    length = len(dataframe.index)
    if (length % 10) == 1 and (length % 100) != 11:
        finalofmessage = " строку."
    elif (length % 10) < 5 and (length % 10) > 1 and ((length % 100) >14 or (length % 100) < 11):
        finalofmessage = " строки."
    else:
        finalofmessage = " строк."
    MESSAGE_BODY = BEGIN_MESSAGE + str(length) + finalofmessage
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


if __name__ == '__main__':
    res = excel_wrapper(RESULTFILE, worksheetName, scrapper(web_page1), scrapper(web_page2))
    sendmessage(res, SMTP_SERVER, SMTP_PORT, SENDER_LOGIN, SENDER_PASSWORD, RECIEVER_EMAIL, SUBJECT, BEGIN_MESSAGE)
