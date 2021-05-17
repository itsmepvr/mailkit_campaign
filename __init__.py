from emailKit import MailKit

campaign = {
    "name": "Email_Campaign_2021",
    "description": "An email campaign about the year 2021"
}

mailingList = {
    "name": "Itsmepvr",
    "description": "personal_list"
}

email = {
    "email": "hr@mailkit.in",
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
                Please, click the link for the assesment file - https://drive.google.com/drive/folders/1kAccinSSKaWo-NQq6muoL5Mt-6yyhcfV?usp=sharing
                <br>
                Link to the github repo - https://github.com/itsmepvr/mailkit_campaign
                <br><br>
                <strong>Thank you..</strong>
            """
}

mailKit = MailKit()
mailKit.createCampaign(campaign['name'], campaign['description'])
mailKit.createMailingList(mailingList['name'], mailingList['description'])
mailKit.sendMail(email['email'], email['subject'], email['body'])
mailKit.deliveryReport()
