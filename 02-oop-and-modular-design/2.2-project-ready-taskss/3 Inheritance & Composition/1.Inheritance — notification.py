class Notification:
    def send(self):
        print("Sending notification")


class EmailNotification(Notification):
    def send(self):
        print("Sending Email")


class SMSNotification(Notification):
    def send(self):
        print("Sending SMS")


EmailNotification().send()
SMSNotification().send()
