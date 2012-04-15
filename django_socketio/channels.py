
from collections import defaultdict
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

from django_socketio import events

# Mapping of channels to lists of socket session IDs subscribed.
CHANNELS = defaultdict(list)


class SocketIOChannelNamespace(BaseNamespace):
    """
    Proxy object for SocketIOProtocol that adds channel subscription
    and broadcast.
    """

    def __init__(self, *args, **kwargs):
        """
        Add Channels
        """
        print "init"
        super(SocketIOChannelNamespace, self).__init__(*args, **kwargs)
        if not hasattr(self.socket, 'channels'):
            self.socket.channels = [] # store our subscribed channels for faster lookup.
        print dir(self)

    def subscribe(self, channel):
        """
        Add the channel to this socket's channels, and to the list of
        subscribed session IDs for the channel. Return False if
        already subscribed, otherwise True.
        """
        print "sub"
        if channel in self.channels:
            return False
        CHANNELS[channel].append(self.socket.sessid)
        self.channels.append(channel)
        return True

    def unsubscribe(self, channel):
        """
        Remove the channel from this socket's channels, and from the
        list of subscribed session IDs for the channel. Return False
        if not subscribed, otherwise True.
        """
        print "unsub"
        try:
            CHANNELS[channel].remove(self.socket.sessid)
            self.channels.remove(channel)
        except ValueError:
            return False
        return True

    def broadcast_channel(self, event, channel=None, *args, **kwargs):
        """
        Send the given event to all subscribers for the channel
        given. If no channel is given, send to the subscribers for
        all the channels that this socket is subscribed to.
        """
        print "brch"
        if channel is None:
            channels = self.channels
        else:
            channels = [channel]

        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)

        for sessid, socket in self.socket.server.sockets.iteritems():
            if sessid == self.socket.sessid:
                continue
            if not hasattr(socket, 'channels'):
                continue
            for channel in channels:
                if channel in socket.channels:
                    socket.send_packet(pkt)

    def send_and_broadcast(self, event, *args, **kwargs):
        """
        Shortcut for a socket to broadcast to all sockets itself.
        """
        print "sbrch"
        self.emit(event, *args)
        self.broadcast(event, *args, **kwargs)

    def send_and_broadcast_channel(self, event, channel=None, *args, **kwargs):
        """
        Shortcut for a socket to broadcast to all sockets subscribed
        to a channel, and itself.
        """
        print "sabrch"
        self.emit(event, *args)
        self.broadcast_channel(event, channel, *args, **kwargs)

    def __getattr__(self, name):
        """
        Proxy missing attributes to the socket.
        """
        print "  get %s" % name
        return getattr(self.socket, name)

    def on_user_message(self, msg):
        print 'Message = %s' % str(msg)
        #print "========================"
        #print "sreq", self.socket.request
        #print "req", self.request
        #print "env", self.environ
        #print "socketio", dir(self.environ["socketio"])
        #print "websocket", dir(self.environ["wsgi.websocket"])
        #print "environ", dir(self.environ)
        #print "socket", dir(self.socket)
        #print "namespace", dir(self)
        #print "========================"
        events.on_message.send(self.socket.request, self, {}, msg)
        #self.socket(msg)

    def recv_message(self, message):
        # Handle WebSocket semantics using socket.send(data) on the client.
        print 'Message = %s' % str(message)
        events.on_message.send(request, self, context, message['data'])
        log_message = format_log(request, message['type'], message['data'])

    def recv_json(self, message):
        # Handle WebSocket semantics using socket.send(data) on the client.
        events.on_message.send(request, self, context, message['data'])
        log_message = format_log(request, message['type'], message['data'])

    def recv_connect(self):
        print "Connected !"
        events.on_connect.send(request, self, context)
