import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi_boot.core import Service
from redis import Redis

from constants import CacheConstant, EmailConstant
from domain.config import ProjConfig
from exception import BusinessException


@Service
class EmailService:
    def __init__(self, cfg: ProjConfig, redis: Redis):
        self.config = cfg.email
        self.redis = redis

    def send_email_code(self, to: str, code: str):
        """
        发送注册邮箱验证码
        """
        msg = MIMEMultipart()
        msg["from"] = self.config.host
        msg["To"] = to
        msg["Subject"] = "欢迎使用h-TrackPoint埋点平台"
        # 正文
        minutes = int(CacheConstant.EXPIRES / 60)
        with open("./resource/regiater_email_template.html", "r", encoding="utf-8") as f:
            content = f.read()\
                .replace(EmailConstant.TEMPLATE_CODE_PLACEHOLDER, code)\
                .replace(EmailConstant.TEMPLATE_MINUTE_PLACEHOLDER, str(minutes))
            msg.attach(MIMEText(content, 'html'))
        try:
            # 连接
            server = smtplib.SMTP(self.config.host)
            server.starttls()
            server.login(self.config.username, self.config.password)
            # 发送
            server.sendmail(self.config.username, to, msg.as_string())
        except:
            raise BusinessException(detail="验证码发送失败")
