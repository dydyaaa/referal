from app import mail
from celery import shared_task
from flask import render_template_string
from flask_mail import Message


@shared_task
def send_password(email, password):
    html_template = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                padding: 20px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #007BFF;
            }
            .password {
                font-size: 18px;
                font-weight: bold;
                color: #28a745;
                background: #e9ecef;
                padding: 10px;
                border-radius: 4px;
                text-align: center;
                margin: 20px 0;
            }
            .footer {
                margin-top: 20px;
                font-size: 12px;
                color: #666;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Сброс пароля</h1>
            <p>Здравствуйте!</p>
            <p>Ваш новый пароль для доступа к системе:</p>
            <div class="password">{{ password }}</div>
            <p>Пожалуйста, измените пароль после входа в систему.</p>
            <div class="footer">
                <p>Это письмо отправлено автоматически. Пожалуйста, не отвечайте на него.</p>
            </div>
        </div>
    </body>
    </html>
    """
    print('task started')
    # with current_app.app_context():
   
    html_body = render_template_string(html_template, password=password)

    msg = Message(
        subject="Сброс пароля",
        sender="flask_sender@mail.ru",
        recipients=[email]
    )
    msg.html = html_body

    mail.send(msg)
        