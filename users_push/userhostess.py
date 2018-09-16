from users_push.userposter import send_message


class UserHostess:

    def greet_user(self, user_id):
        send_message("Hey !", user_id)

    def identification_user(self, user_id):
        send_message("Please follow the link and paste the code back to me !", user_id)

    def identification_completed_user(self, user_id):
        send_message("Hey everything is setup !", user_id)

    def something_gone_wrong(self, user_id):
        send_message("Outch !", user_id)
        send_message("Something gone wrong", user_id)
        send_message("I will keep you informed", user_id)

    def upload_succeeded(self, user_id):
        send_message("Hey niceJob !!", user_id)

    def request_not_understood(self, user_id):
        send_message("Hum, I dont understand", user_id)

    def user_identification_url(self, user_id, url):
        send_message(url, user_id)
