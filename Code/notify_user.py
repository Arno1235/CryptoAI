# TODO: Log everything in an excel file (maybe calculate the predicted profit vs the actual profit)

from discord import Webhook, RequestsWebhookAdapter

def notifyUser(message):
    webhook = Webhook.from_url(getDiscordURL(), adapter=RequestsWebhookAdapter())
    webhook.send(message)

def getDiscordURL():
    with open ("secret.txt", "r") as myfile:
        data = myfile.read().splitlines()
        return data[2]

if __name__ == "__main__":
    print("running notify_user")

    notifyUser("Test")