from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from clear_user_data import clear
from os.path import exists

app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def sms():
    def user_data(filetype, user):
        file = open(filetype, "w")
        file.write(user)

    def read_data(filetype):
        return open(filetype, "r").read()

    number = request.form['From']
    message_body = request.form['Body']
    resp = MessagingResponse()
    message = str(message_body)
    if message_body == "1234" and (not exists(number + "service_order.txt") or read_data(number + "service_order.txt") == "0"):
        user_data(number + "user_number.txt", str(number))
        user_data(number + "service_order.txt", "1")
        resp.message('Welcome to our Companion Cane Service\nWhat is your age? (message back with "age:(your age)"')
    elif not exists(number + "user_number.txt"):
        resp.message('Your number is not registered with our service')
    elif read_data(number + "user_number.txt") == str(number) and message[0:4] == "age:" and read_data(number + "service_order.txt") == "1":
        if not message[4:len(message)].isdigit():
            resp.message('Make sure to enter an integer for your age.')
        elif int(message[4:len(message)]) < 10 or int(message[4:len(message)]) > 130:
            resp.message('Make sure to enter an age is between 10 and 120')
        else:
            user_data(number + "user_age.txt", message[4:len(message)])
            resp.message('What is your gender? (message back with "gender:(gender)"')
            open(number + "service_order.txt", "w").write("2")
    elif read_data(number + "user_number.txt") == str(number) and message[0:7] == "gender:" and read_data(number + "service_order.txt") == "2":
        user_data(number + "user_gender.txt", message[7:len(message)])
        resp.message('What is your weight? (message back with "weight:(weight in lbs)"')
        open(number + "service_order.txt", "w").write("3")
    elif read_data(number + "user_number.txt") == str(number) and message[0:7] == "weight:" and read_data(number + "service_order.txt") == "3":
        try:
            float(message[7:len(message)])
            if float(message[7:len(message)]) > 40 and float(message[7:len(message)]) < 500:
                user_data(number + "user_weight.txt", message[7:len(message)])
                resp.message('What is the number of your emergency contact? (message back with "EC:(#))"')
                open(number + "service_order.txt", "w").write("4")
            else:
                resp.message('Make sure to enter your proper weight between 40 and 500 lbs.')
        except ValueError:
            resp.message('Make sure to enter a proper float value for your weight.')
    elif read_data(number + "user_number.txt") == str(number) and message[0:3] == "EC:" and read_data(number + "service_order.txt") == "4":
        try:
            int(message[3:len(message)])
            if len(message[3:len(message)]) == 11 or len(message[3:len(message)]) == 10:
                user_data(number + "emergency_contacts1.txt", message[3:len(message)])
                resp.message('What is the number of your physician? (message back with "PC:(#)"')
                open(number + "service_order.txt", "w").write("5")
            else:
                resp.message('Make sure to enter a proper 10 or 11 digit phone number.')
        except ValueError:
            resp.message('Make sure to enter only numbers for the phone number along with the "EC:".')
    elif read_data(number + "user_number.txt") == str(number) and message[0:3] == "PC:" and read_data(number + "service_order.txt") == "5":
        try:
            int(message[3:len(message)])
            if len(message[3:len(message)]) == 11 or len(message[3:len(message)]) == 10:
                user_data(number + "physician_contact.txt", message[3:len(message)])
                resp.message('What is the email of your physician? (message back with "email:(email)"')  
                open(number + "service_order.txt", "w").write("6")
            else:
                resp.message('Make sure to enter a proper 10 or 11 digit phone number.')
        except ValueError:
            resp.message('Make sure to enter only numbers for the phone number along with the "PC:".')
    elif read_data(number + "user_number.txt") == str(number) and message[0:6] == "email:" and read_data(number + "service_order.txt") == "6":
        if message.find("@") == -1:
            resp.message('Make sure to properly format the email with an @ symbol.')
        else:
            user_data(number + "physician_email.txt", message[6:len(message)])
            resp.message('Thank you, your information has been registered.\nIf you would like to prevent emergency calls, message back with "STOP". If you would like to reset your information message back with "reset"')
            open(number + "service_order.txt", "w").write("7")
    elif read_data(number + "user_number.txt") == str(number) and message[0:4] == "STOP" and read_data(number + "service_order.txt") == "7":
        user_data(number + "user_preference.txt", str(message))
        resp.message('Your emergency contact preferences have been updated')
        open(number + "service_order.txt", "w").write("8")
    elif read_data(number + "user_number.txt") == str(number) and message == "reset":
        clear(number)
        resp.message('Your information has been reset')
        open(number + "service_order.txt", "w").write("1")
    elif read_data(number + "user_number.txt") == str(number):
        resp.message('make sure you formatted your message correctly or that you provide information in the correct order. your message:' + message)
    return str(resp)


if __name__ == '__main__':    
    app.run()