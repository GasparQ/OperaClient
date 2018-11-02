from client import Client

phantom = Client(0)

# get the question in q variable
q = phantom.GetQuestion()

# send response OK from the lambda
phantom.SendResponse(lambda: 'Ok')

# print finish if the game is over
if phantom.IsGameOver():
    print('finish')
