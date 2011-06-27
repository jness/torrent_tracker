def send_email(toaddr, fromaddr, filenames, host):
    '''Sends a Email notification'''
    import smtplib
    from socket import error
    from config import get_config

    header = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n"
        % (fromaddr, toaddr, 'Torrent Tracker'))

    body = str()
    for f in filenames:
        body = body + '%s downloaded\n' % f
    msg = header + body

    try:
        server = smtplib.SMTP(host)
        server.set_debuglevel(0)

    except error:
        print "Unable to connect to SMTP server"

    else:
        server.sendmail(fromaddr, toaddr, msg)
        server.quit()

