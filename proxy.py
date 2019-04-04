from freeswitch import *

def fsapi( session, stream, env, args ):

    # You can review the SIP info before you answer
    print session
    print args
    handler(session, args)


def handler(session, args):

    # pickup the line
    session.answer()

    # wait a second for media channels to sync
    session.sleep(1000)

    # play a beep
    session.streamFile("/usr/local/freeswitch/scripts/easy/audio/beep.wav")

    # get some digits: max 2sec btwn keys, # is optional terminator
    digits = session.getDigits( 4, '#', 2000, 5000)

    # did we get the secret code?
    if digits == '1234':
        # We're in! Do some cool stuff.
        session.streamFile("/usr/local/freeswitch/scripts/easy/audio/authorized.wav")

    # play goodbye
    session.streamFile("/usr/local/freeswitch/scripts/easy/audio/goodbye.wav")

    # hangup the SIP session
    session.hangup()

    # end the session in freeswitch
    session.destroy()
