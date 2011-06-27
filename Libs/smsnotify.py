def send_sms(username, password, cellnumber, filename):
    '''Sends a SMS message to cellnumber via PyGoogleVoice'''

    from googlevoice import Voice

    voice = Voice()
    voice.login(username, password)
    text = '%s downloaded' % filename
    voice.send_sms(cellnumber, text)
    return
