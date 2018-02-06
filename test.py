from authing import Authing

if __name__ == '__main__':

    clientId = '' 
    secret = ''

    authing = Authing(clientId, secret)

    def test_auth():
        result = authing.auth()
        print(result)

    test_auth()