# resistbotca
A Canadian version of resistbot. It's an SMS bot that helps you find and contact
your local Member of Parliament.

Currently, it supports phoning, faxing, and emailing your representative.



## Requirements
ResistbotCA uses Twilio for SMS and phoning functions, SRfax for faxing, and any arbitrary SMTP server
for emails. It should be fairly easy to replace those with your service of choice if you'd like.

It also requires a web-facing server (for Twilio callbacks, though there is no web UI) and
a mySQL database.

It's written in Django.

You could also update the project to use Twilio for faxes -- we built this before Twilio supported fax,
but it'd be a good thing to consolidate (and get rid of the srfax account). Do this, send me
a pull request, and I'll buy you a beer. =)



## Installation

### Python setup
Python virtual environments are strongly recommended.

In your virutal environment, all you need to do to instal dependencies is
pip install -r requirements.txt

All configuration settings should be placed in a new local_settings.py file
(and that file should be excluded from all repositories).

You can use settings.py as a template for your local_settings.py, but don't copy
over the last code block that imports local_settings

### Server setup
The _scripts/restart.sh_ file can be used to start/restart the project if running as
a gunicorn service (personally I do this, with Apache ProxyPass configuration for the frontend,
but it's really up to you)

You'll also need to add _scripts/send_mail.sh_ to your server's crontab in order for emails/faxes
to be actually sent. I usually have it run every minute.
(or, don't do that to leave the project in testing mode, and manually remove messages
from the database's django_mailer table before turning it back on).

### Twilio setup
You'll need a Twilio account and a phone number.  Set the messaging webhook to your server's URL,
ie, _https://resistbot.mydomain.com/rbot/_

You don't need to handle incoming voice calls if you don't want, though it may be helpful to read
out a generic script explaining what this service is.

Make sure you also put your Twilio account id, key, and phone number in local_settings.py

### SRfax setup
To use faxes, you'll need a SRfax account. Make sure you set FAX\_FROM\_EMAIL in local_settings.py
to the email address in your SRfax account.

(bonus TODO: rewrite a fax module that uses Twilio's new faxing features!)



## Customizing the bot's responses and conversations
Unfortunately, the conversations are currently hardcoded, so you'll need to edit the code
if you want to change how the bot behaves or what it says.

Fortunately, this is not hardcoded into obscure places in the code: it's abstracted into a 
series of "stages". An active conversation can only be in one stage, and each stage can define
a number of responses, actions, and ways to move to another stage. Think of a finite state machine,
from way back in compsci classes.

These stages are coded in _rbot/stages_.

Each Stage object must define a _name_ field, which should be the name of the file.
It can also have an optional _no_easter_eggs_ field (set to True to disable global easter-egg messages
and help keywords during this stage).

Each Stage object must also define two methods:
* get_messages(self, conversation)

  This is called once a user lands on this stage. It should return a list of strings, each string
  being a message that is sent to the user.

* respond(self, conversation, message)

  If/when the user responds to the messages in _get\_messages()_, this is called. The _messsages_
  parameter contains the user's response.
  
  It returns a two-tuple.  The first value in the tuple is a Stage object (possibly _self_) which
  the user will be moved to. The second value is a string, which is a message sent to the user.
  Either (or both) of these values can be None. If stage is None, it indicates the end of a conversation.
  If the response message is None, then no response will be sent, but the user will still be moved
  to the next stage (and the _get\_messages()_ from the next stage will be sent).
  
There is one additional optional method:
* do_action(self, conversation, response)

  This code is executed right after _get\_messages()_, before waiting for a response.
  The return is ignored.
  
This handled in code, rather than through an administrative user interface, to allow for
complex branching logic in _respond_ (it's just python code after all), as well as arbitrary
coded actions in _respond_ (ie send an email, send a fax, initiate a phone call, generate a MMS preview).

### Global keywords
There are three sets of global keywords, that exist outside the normal conversation flow.

Restart keywords (defined in rbot.view.START_KEYWORDS) will always restart the conversation
flow on the first stage.

Help keywords (defind in rbot.views.HELP_KEYWORDS) will trigger a pre-defined help message, currently
hardcoded at rbot.views:54

Easter egg keywords (defined in rbot.easter_eggs) will respond with the associated response.

In all three cases, the user will _not_ be advanced to a new stage. The bot will continue
listening and pass the next message to the stage's _respond_ method.


## Postal code and MP lookups
The project uses Open North to translate postal codes into ridings and representatives. This code lives
in the _ridings_ app, which includes caching of postal codes and ridings to avoid excessive Open North
lookups. This means if any data changes (riding boundaries are redrawn, a byelection occurs, etc), you'll
need to clear the cache.

Currently there is no way command or UI for that; just delete the database row. (it'd be a nice
enhancement to build a Django management command or UI for this...!)


## Contact methods
Emails and faxes are stored in the _emailfax_ app (since sending a fax is just sending a
specially-formatted email to the SRfax address). It relies on some security-by-obscurity at the moment
when generating and returning MMS previews, which we should fix.

The _phonecall_ app provides logging models and views to handle Twilio click-to-call style phone calls.

Want to add more contact methods? Create a similar app, and then modify the conversation flow
to recognize it!


## Testing
There are some settings variables to put the project in testing mode.  In particular:

* TESTING_PHONE: if set, all phone calls will go to this number instead of the MP's number
* TESTING_EMAIL: if set, all emails will go to this address instead of the MP's email
* TESTING_FAX: if set, all faxes will go to this number instead of the MP's fax


## License

This project is licensed under the terms of the GNU GPL v3, a copy of which is included in LICENSE.md

Copyright (c) 2017 franciskung.com consulting ltd.

