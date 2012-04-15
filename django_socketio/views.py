
from django.http import HttpResponse

from django_socketio import events
from django_socketio.channels import SocketIOChannelNamespace
from django_socketio.clients import client_start, client_end
from django_socketio.utils import format_log

from socketio import socketio_manage

"""
from django.utils.importlib import import_module
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from django.contrib.auth.models import AnonymousUser

def manual_auth(session_key):
    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore(session_key)

    user_id = session.get(SESSION_KEY)
    backend = session[BACKEND_SESSION_KEY]

    django_auth_backend = load_backend(backend)
    return django_auth_backend.get_user(user_id) or AnonymousUser()
"""

def socketio(request):
    """
    Socket.IO handler - maintains the lifecycle of a Socket.IO
    request, sending the each of the events. Also handles
    adding/removing request/socket pairs to the CLIENTS dict
    which is used for sending on_finish events when the server
    stops.
    """
    print "Start"
    print request.user
    context = {}
    #print dir(request.environ["socketio"])
    try:
        socketio_manage(request.environ, {'': SocketIOChannelNamespace})
        """
        while False:
            message = socket.recieve()
            if not message and not socket.connected:
                events.on_disconnect.send(request, socket, context)
                break
            # Subscribe and unsubscribe messages are in two parts, the
            # name of either and the channel, so we use an iterator that
            # lets us jump a step in iteration to grab the channel name
            # for these.
            if not message: break
            if message['type'] == 'event':
                # Handle socket.emit(event, data) semantics from the client.
                if message['name'] == '__subscribe__':
                    # To subscribe on the client: socket.emit('__subscribe__', 'ch1', 'ch2')
                    for channel in message['args']:
                        socket.subscribe(channel)
                        events.on_subscribe.send(request, socket, context, channel)
                    log_message = format_log(request, 'subscribe', message['args'])
                elif message['name'] == '__unsubscribe__':
                    # To unsubscribe on the client: socket.emit('__unsubscribe__', 'ch1', 'ch2')
                    for channel in message['args']:
                        socket.unsubscribe(channel)
                        events.on_unsubscribe.send(request, socket, context, channel)
                    log_message = format_log(request, 'unsubscribe', message['args'])
                else:
                    events.on_message.send(request, socket, context, message)
                    log_message = format_log(request, '***Unkown Event***', message)
            elif message['type'] == 'message':
                # Handle WebSocket semantics using socket.send(data) on the client.
                events.on_message.send(request, socket, context, message['data'])
                log_message = format_log(request, message['type'], message['data'])
            else:
                print 'Unkown message type. Message = %s' % str(message)
                log_message = format_log(request, '***Unknown Type***', message)
            if log_message:
                socket.handler.server.log.write(log_message)

        """
    except Exception, exception:
        print "error"
        from traceback import print_exc
        print_exc()
        events.on_error.send(request, socket, context, exception)
    client_end(request, socket, context)
    return HttpResponse("")
