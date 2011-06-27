def send_sms(username, password, cellnumber, filenames):
    '''Sends a SMS message to cellnumber via PyGoogleVoice'''

    from googlevoice import Voice

    voice = Voice()
    voice.login(username, password)
    
    text = str()
    for f in filenames:
        text = text + '%s downloaded\n' % f
    voice.send_sms(cellnumber, text)
    return
