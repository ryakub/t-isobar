import imaplib
import email


def email_download_report(email_user, email_pass, email_from, host='imap.yandex.ru', port=993):
    mail = imaplib.IMAP4_SSL(host, int(port))
    mail.login(email_user, email_pass)

    mail.select('INBOX')
    status_search, search_result = mail.search(None, 'FROM', email_from)

    list_of_mail_id = search_result[0].decode('utf-8').split(' ')

    status_fetch, fetch_result = mail.fetch(list_of_mail_id[-1], '(RFC822)')
    raw_email = fetch_result[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    list_of_file_names = []
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        file_name = part.get_filename()
        fp = open(file_name, 'wb')
        fp.write(part.get_payload(decode=True))
        fp.close()
        list_of_file_names.append(file_name)
    mail.close()
    return list_of_file_names
