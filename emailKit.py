import os
import requests
import json
import base64
from dotenv import load_dotenv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# Insecurity Warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

load_dotenv()  # take environment variables from .env.

class MailKit:
    """Class for MailKit to create campaign, send mail and deliver report back. """

    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_md5 = os.getenv('CLIENT_MD5')
        self.api = os.getenv('API_URL')
        self.campaign_id = None
        self.mailing_list_id = None
    
    def dataToBase64(self, data=''):
        """Convert string to base64 literal

        Parameters
        ----------
        data : str
            The input string default is empty

        Returns
        -------
        str
            an str which is encoded to base64-ascii
        """
        return base64.b64encode(bytes(str(data), 'ascii')).decode('utf-8')

    def getProfileEmailsList(self):
        """Get User Profile Emails as list 

        Returns
        -------
        json
            Response from api with list of emails in user profile
        """

        data = {
            "function":"mailkit.profile.emails.list",
            "id":self.client_id,
            "md5":self.client_md5,
        }
        return self.postToAPI(data)
    
    def getCampaignList(self):
        """Get list of campaigns

        Returns
        -------
        json
            Response from api with list of campaigns
        """

        data = {
            "function":"mailkit.campaigns.list",
            "id":self.client_id,
            "md5":self.client_md5,
        }
        return self.postToAPI(data)

    def checkIfCampaignExists(self, name):
        """Checks if campaign exists for given client. If exists returns campaign Id

        Parameters
        ----------
        name : str
            Name of the campaign cannot be empty

        Returns
        -------
        str/Boolean
            returns str with campaign id if campaign exists, else returns False
        """

        campaignList = self.getCampaignList()
        for campaign in campaignList:
            if campaign['NAME'] == name:
                return campaign['ID_MESSAGE']
                break
        return False

    def createCampaign(self, name, description=''):
        """Creates a campaign if not exists. If exists reuse campaign id.

        Parameters
        ----------
        name : name
            Name of the campaign cannot be empty
        description: str
            Description of the campaign cannot be empty

        Returns
        -------
        json/str
            Response from api with status code and result or campaign id if campaign exists
        """

        self.campaign_id = self.checkIfCampaignExists(name)
        if self.campaign_id:
            print("Campaign '%s' already exists. Id: %s" % (name, self.campaign_id))
            return self.campaign_id
        profileEmailsList = self.getProfileEmailsList()['emails'][0]
        data = {
	        "function": "mailkit.campaigns.create",
	        "id": self.client_id,
	        "md5": self.client_md5,
	        "parameters": {
	        	"name": self.dataToBase64(name),
                "subject": self.dataToBase64(description),
                "ID_allow_email": self.dataToBase64(profileEmailsList['ID_ALLOW_EMAIL'])
	        }
        }
        res = self.postToAPI(data)
        if 'error' in res:
            print('Error: %s' % res['error'])
            return res
        self.campaign_id = res['ID_message']
        print('New campaign %s with Id %s created.' % (name, self.campaign_id))
        return res
    
    def createMailingList(self, name='', description=''):
        """Creates a mailing list for email campaign

        Parameters
        ----------
        name : str
            Name of the mailing list cannot be empty
        description: str
            Description of the mailing list can be empty

        Returns
        -------
        json
            Response from api with status code and result
        """

        mailingList = self.getMailingList()
        for mail in mailingList:
            if mail['NAME'] == name:
                print("Mailing list already exists. Id: %s"%mail['ID_USER_LIST'])
                self.mailing_list_id = mail['ID_USER_LIST']
                return self.mailing_list_id
                break

        data = {  
            "function":"mailkit.mailinglist.create",
            "id":self.client_id,
            "md5":self.client_md5,
            "parameters":{  
                "name":name,
                "description":description
            }
        }
        res = self.postToAPI(data)
        print(res)
        if 'error' in res:
            print("Error: %s"%res['error'])
            return
        self.mailing_list_id = res['data']
        print("Mailing list with name '%s' and id '%s' created." % (name, self.mailing_list_id))
        return res

    def getMailingList(self):
        """Get list of mailing list

        Returns
        -------
        json
            Response from api with list of emails
        """

        data = {
            "function":"mailkit.mailinglist.list",
            "id":self.client_id,
            "md5":self.client_md5,
        }
        return self.postToAPI(data)

    def sendMail(self, email, subject='', body=''):
        """Send message from campaign with custom email and subject

        Parameters
        ----------
        email : str
            Email id of the receipent
        subject: str
            Subject for the email
        body: str:
            Message body for the email

        Returns
        -------
        json/str
            Response from api with status code and result
        """

        if not email:
            return "Error: Email cannot be empty"

        mailinglist_id = self.getMailingList()[2]['ID_USER_LIST']
        mailinglist_id = '82239'
        data = {
          "function": "mailkit.sendmail",
          "id": self.client_id,
          "md5": self.client_md5,
          "parameters": {
            "mailinglist_id": self.mailing_list_id,
            "campaign_id": self.campaign_id,
            "main": {
                "send_to": email,
                "subject": subject,
                "message_data": self.dataToBase64(body)
            }
          }
        }
        res = self.postToAPI(data)
        print(res)
        return res

    def deliveryReport(self):
        """Delivery report for the email sent

        Returns
        -------
        json/str
            Response from api with status code and result
        """

        data = {
           "function":"mailkit.report.campaign",
           "id":self.client_id,
           "md5":self.client_md5,
           "parameters":{
              "range_from":"",
              "range_to":"",
              "ID_message": self.campaign_id
           }
        }
        res = self.postToAPI(data)
        print("Delivery report: %s" % json.dumps(res, indent=2))
        return res

    def postToAPI(self, data={}):
        """Perform POST request to API

        Parameters
        ----------
        data : json
            json data to post to api

        Returns
        -------
        json/str
            Response from api with status code and result
        """

        if not data:
            data = {
                "id": self.client_id,
                "md5": self.client_md5
            }
        res = requests.post(self.api, headers={"content-type":"application/json"}, json=data, verify=False)
        return res.json()

