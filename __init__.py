from emailKit import MailKit

campaign = {
    "name": "Test12979",
    "description": "description"
}

mailingList = {
    "name": "Dapppa",
    "description": "AAsasakskajskj"
}

email = {
    "email": "venkata.nestor@gmail.com",
    "subject": "Maikit Interview Assessment: Venkata Ramana P",
    "body": """<h1>MailKit Interview Assesment</h1>
                <hr>
                <table style='font-weight:bold;'>
                    <tr>
                        <td>Name: </td>
                        <td>Venkata Ramana P</td>
                    </tr>
                    <tr>
                        <td>Role: </td>
                        <td>Python Developer</td>
                    </tr>
                    <tr>
                        <td>Email: </td>
                        <td>pvrreddy155@gmail.com</td>
                    </tr>
                    <tr>
                        <td>Mobile: </td>
                        <td>9966350753</td>
                    </tr>
                </table>
                <hr>
                Please, click the below link for the assesment file.
                <br>
                https://drive.google.com/file/d/0B1xxML7ZMOl1STJGM3J5bDNyLUk/view?usp=sharing
            """
}

mailKit = MailKit()
mailKit.createCampaign(campaign['name'], campaign['description'])
mailKit.createMailingList(mailingList['name'], mailingList['description'])
mailKit.sendMail(email['email'], email['subject'], email['body'])
mailKit.deliveryReport()
