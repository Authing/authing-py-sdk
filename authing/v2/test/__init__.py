from ..management import ManagementClientOptions
from ..management.authing import ManagementClient
from dotenv import load_dotenv
import os
load_dotenv()

management = ManagementClient(ManagementClientOptions(
    userPoolId=os.getenv('AUTHING_USERPOOL_ID'),
    secret=os.getenv('AUTHING_USERPOOL_SECRET'),
    host=os.getenv('AUTHING_SERVER')
))
