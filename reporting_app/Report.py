import openpyxl
wb = openpyxl.load_workbook('Pattern.xlsx')

sheet = wb.get_sheet_by_name('Sheet1')
sheet['B1'].value="weather condition ...."
wb.save('Report.xlsx')


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
msg = MIMEMultipart()
msg['from'] = 'fatum.michal@interia.pl'
msg['To'] = 'michal.kanarek@gmail.com'
msg['Subject'] = "Report"
body = "I've attached file with report"
msg.attach(MIMEText(body ,'plain'))

filename = 'Report.xlsx'
attachment = open(filename , "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename= '+filename)


msg.attach(part)
text = msg.as_string()
mail = smtplib.SMTP('poczta.interia.pl',587)
mail.ehlo()
mail.starttls()
mail.login('fatum.michal@interia.pl','#############')
mail.sendmail("fatum.michal@interia.pl" , "michal.kanarek@gmail.com",text)
mail.close()