package communication;

import org.zeromq.SocketType;
import org.zeromq.ZContext;
import org.zeromq.ZMQ;

/**
 * A channel between the graph generator and the graph visualizer component.
 * Connects the visualizer component (server) to the GA component through a TCP port, using ZMQ (jeroMQ).
 */

public class Channel {

    private final ZMQ.Socket socket;
    private String address;
    private String receivedMessage;
    private boolean isVerbose;

    public Channel(String address) {
        this.address = address;
        ZContext context = new ZContext();
        this.socket = context.createSocket(SocketType.REP);
        this.isVerbose = true;
    }

    public void setVerbose(boolean isVerbose) {
        this.isVerbose = isVerbose;
    }

//    public Channel() {
//        this.context = new ZContext();
//        this.socket = context.createSocket(SocketType.REP);
//    }

    public void bind() {
        this.socket.bind(this.address);
    }

    public void bind(String address) {
        this.address = address;
        this.socket.bind(this.address);
    }

    public void listenForMessage() {
        if(isVerbose) {
            System.out.println("Waiting for messages from clients");
        }
        byte[] messageFromClient = this.socket.recv(0);
        this.receivedMessage = new String(messageFromClient, ZMQ.CHARSET);

        if(isVerbose) {
            System.out.println("Received: " + this.receivedMessage);
        }
    }

    public void sendResponse(String response) {
        socket.send(response.getBytes(ZMQ.CHARSET), 0);

        if(isVerbose) {
            System.out.println("Response [" + response + "] was sent");
        }
    }

    public String getReceivedMessage() {
        return receivedMessage;
    }
}
