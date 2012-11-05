#!/usr/bin/python2.6
import smtplib
import sys

from optparse import OptionParser


def setup_smtp_server(options):
	smtpserver = smtplib.SMTP(options.smtp_host, options.stmp_port)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo()
	smtpserver.login(options.gmail_user, options.gmail_pwd)
	return smtpserver

def create_header(options):
	header = 'To: %s\nFrom: %s\nSubject: %s\n\n'
	return header % (options.to_address, options.gmail_user,
		options.subject)

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option('-t', '--to', dest='to_address',
		default='richdel1991@gmail.com',
		help='address to send to.')
	parser.add_option('-u', '--user', dest='gmail_user',
		default='richdel1991@gmail.com', 
		help='gmail user to send mail as.')
	parser.add_option('-p', '--pwd', dest='gmail_pwd',
		default='Iin7sahZ', 
		help='gmail password')
	parser.add_option('--host', dest='smtp_host',
		default='smtp.gmail.com',
		help='gmail smtp hostname') 
	parser.add_option('--port', dest='stmp_port',
		default=587,
		help='gmail smtp port') 
	parser.add_option('--subject', dest='subject',
		help='gmail smtp port')
	(options, args) = parser.parse_args()
	if not options.subject:
		print "Message needs a subject"
		sys.exit(1)
	smtpserver = setup_smtp_server(options)
	header = create_header(options)
	body = sys.stdin.read()
	msg = header + body + "\n"
	smtpserver.sendmail(options.gmail_user, options.to_address, msg)
	smtpserver.close()
