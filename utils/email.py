import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

EMAIL = "resilience.tt@gmail.com"
PASSWORD = "ResilienceTT2#"

coding = "latin-1"

def send_code_password(correo: str, nombre: str, numeros: str):
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(EMAIL, PASSWORD)
  
  subject = u"Recuperación de contraseña"
  
  bodyEmail = MIMEMultipart("alternative")
  bodyEmail['From'] = EMAIL
  bodyEmail['To'] = correo
  bodyEmail['Subject'] = Header(subject, coding)
  
  html = f'''
    <html>
      <body>
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #219653;border-radius:10px">
          <tr>
            <td width="15%" align="center" valign="top"></td>
            <td width="70%" align="center" valign="top">
              <div style="background-color:#FFFFFF;margin-top:50px;margin-bottom:50px;border-radius:10px;padding:10px">
                <div style="height:30px;width:10px"></div>
                <strong style="font-size: 1.6rem">
                  &iexcl;Hola {nombre}!
                </strong>
                <div style="height:1px;width:90%;background-color:#000000;margin-top:3px"></div>
                <div style="height:20px;width:10px"></div>
                <p style="font-size: 1.2rem">
                  Se ha solicitado la recuperaci&oacute;n de su contrase&ntilde;a en la aplicaci&oacute;n de Resilience.
                </p>
                <p style="font-size: 1.2rem">
                  Para llevar este procedimiento a cabo debe de ingresar los siguientes digitos en la aplicaci&oacute;n.
                </p>
                <strong style="font-size: 1.6rem">
                  {numeros[0:3]} {numeros[3:6]}
                </strong>
                <p style="font-size: 1.2rem">
                  Si se presenta alg&uacute;n error favor de mandar correo a {EMAIL} para dar soluci&oacute;n.
                </p>
                <p style="font-size: 1.2rem">
                  <em>
                    El equipo de Resilience le desea un excelente día.
                  </em>
                </p>
              </div>
            </td>
            <td width="15%" align="center" valign="top"></td>
          </tr>
        </table>
      </body>
    </html>
  '''
  
  part_html = MIMEText(html, "html")
  bodyEmail.attach(part_html)
  
  server.sendmail(EMAIL, correo, bodyEmail.as_string())
  server.quit()