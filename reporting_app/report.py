import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from .models import Action, Profile
from .weather import Weather
class Report():

    @staticmethod
    def send_report():

        drivers_stats = [(Action.objects.filter(driver=x.user).last(),
                      i) for x, i in zip(Profile.objects.filter(is_driver=True),
                            range(1,1+len(Profile.objects.filter(is_driver=True))))]

        wb = openpyxl.load_workbook('Pattern.xlsx')

        sheet = wb.get_sheet_by_name('Sheet1')
        for action,index in drivers_stats:
            sheet[f'B{index}'].value = action.route
            active_message = "is active " if action.is_active else "is not active"
            sheet[f'C{index}'].value = active_message
        sheet["D1"] = Weather.get_temperature()
        wb.save('Report.xlsx')


        msg = MIMEMultipart()
        msg['from'] = 'fatum.michal@interia.pl'
        msg['To'] = 'michal.kanarek@gmail.com'
        msg['Subject'] = "Report"
        body = "I've attached file with report"
        msg.attach(MIMEText(body, 'plain'))



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
        mail.login('fatum.michal@interia.pl',"##")
        mail.sendmail("fatum.michal@interia.pl" , "michal.kanarek@gmail.com",text)
        mail.close()
        return "Report Send !"