import random
import smtplib

from email.mime.text import MIMEText
from django.conf import settings

from api.helpers import r1
from comic.celery import app

"""
TEMPLLATES = {"001": u"<html><div>尊敬的XXX漫画用户:</div><br>" \
                    "<div>您的验证码为:</div>" \
                    "<div style='text-align:center'><font size='10' color='#0066FF'>%s</font></div><br>" \
                     "<div>此电子邮件用于注册XXXX漫画帐号。如果是您本人操作,为保障您的帐号安全，请在2分钟内,请输入上方显示的数字验证码。</div><br>" \
                     "<div>若您没有申请过验证邮箱 ，请您忽略此邮件，由此给您带来的不便请谅解。</div><br>" \
                     "<div>此致</div>" \
                     "<div>XXX漫画团队敬上</div>"
                     "</html>",
              "002":u"<html><div>尊敬的XXX漫画用户:</div><br>" \
                    "<div>您的验证码为:</div>" \
                    "<div style='text-align:center'><font size='10' color='#0066FF'>%s</font></div><br>" \
                     "<div>此电子邮件用于更改XXXX漫画帐号。如果是您本人操作,为保障您的帐号安全，请在2分钟内,请输入上方显示的数字验证码。</div><br>" \
                     "<div>若您没有申请过验证邮箱 ，请您忽略此邮件，由此给您带来的不便请谅解。</div><br>" \
                     "<div>此致</div>" \
                     "<div>XXX漫画团队敬上</div>"
                     "</html>",
              }
"""
TEMPLLATES = {"001": u"<html>" \
                     "<div>Your Verification Code:</div>" \
                     "<div style='text-align:center'><font size='10' color='#0066FF'>%s</font></div><br>" \
                     "<div>This email address is being used to register %s. If you initiated this process, it is asking you to enter the numeric verification code that appears above within 2 minutes.</div><br>" \
                     "<div>if you did not initiate an account register/log in process. It is possible that someone else is trying to use %s via your account. Do not forward or give this code to anyone.</div><br>" \
                     "<div>Your sincerely</div>" \
                     "<div>The Burger Clerk :) </div>"
                     "</html>" % ("%s", settings.APP_TITLE, settings.APP_TITLE),
              }

sender = 'mangaburger@entermedia.cn'  # todo 更换邮箱
subject = u'%s verification' % settings.APP_TITLE
smtpserver = 'hwsmtp.exmail.qq.com'  # 163网易提供给用户的服务器
username = 'mangaburger@entermedia.cn'  # todo 更换邮箱r
password = 'Comicdingyu@906'  # todo 更换邮箱


@app.task  # todo 处理退还邮箱bind=True, default_retry_delay=20, max_retries=3
def send_email(email, template):
    # time_begin = datetime.datetime.now()
    PIN = str(random.randint(100000, 999999))
    content = TEMPLLATES[template] % (PIN)
    r1.setex("%s_PIN" % email, PIN, 60 * 5)
    try:
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = email
        smtp = smtplib.SMTP_SSL(smtpserver)
        # smtp.connect(host=smtpserver, port=port)
        smtp.login(username, password)
        smtp.sendmail(sender, email, msg.as_string())
        smtp.quit()
        return True
    except Exception as e:
        print(e)
        return False
    # except Exception as exc:
    #     retries = self.request.retries
    #     r1.zincrby("email_list", email, 1)
    #     print("没发送成功")
    #     if retries < self.max_retries:
    #         delta_second = (datetime.datetime.now() - time_begin).seconds
    #         if delta_second < 5:
    #             return self.retry(exc=exc, countdown=15 - delta_second)
    #         else:
    #             return self.retry(exc=exc, countdown=0)
