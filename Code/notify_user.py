# Discord and Excel libraries
from discord import Webhook, RequestsWebhookAdapter



# Sends a message to the user over on Discord
def notifyUser(message):
    webhook = Webhook.from_url(getDiscordURL(), adapter=RequestsWebhookAdapter())
    webhook.send(message)

# Returns the discord url from the secret.txt file
def getDiscordURL():
    with open ("secret.txt", "r") as myfile:
        data = myfile.read().splitlines()
        return data[2]



if __name__ == "__main__":
    print("running notify_user")

    notifyUser("Test")