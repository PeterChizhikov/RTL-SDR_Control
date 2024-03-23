#include "TcpServerProcessor.h"

TcpServerProcessor::TcpServerProcessor(QObject *parent)
{
    tcpServer = std::make_unique<QTcpServer>();
    if(tcpServer->listen(QHostAddress::Any, portForListen))
    {
        qDebug() << "TcpServerProcessor started on port " << portForListen << "\n";
        connect(tcpServer.get(), &QTcpServer::newConnection,
                this, &TcpServerProcessor::newConnection);
    }else {
        qDebug() << "TcpServerProcessor not started";
    }
}

void TcpServerProcessor::SendToClient(QByteArray data)
{
    if (sockets.empty()) return;
    for (auto socket : sockets)
    {
        socket->write(data);
        socket->flush();
    }

}

void TcpServerProcessor::newConnection()
{
    //Возвращается объект клиента?
    auto newSocket = std::shared_ptr<QTcpSocket>(tcpServer->nextPendingConnection());
    qDebug() << "tcp client connected: " << newSocket->peerAddress().toString() << "on port: " << QString::number(newSocket->peerPort());

    connect(newSocket.get(), &QTcpSocket::readyRead, this, &TcpServerProcessor::processMessage, Qt::QueuedConnection);
    connect(newSocket.get(), &QTcpSocket::disconnected, this, &TcpServerProcessor::socketDisconnected, Qt::QueuedConnection);

    sockets.push_back(newSocket);

    //message after Connect
    QString clientConnectedStatus = "Client connected";
    newSocket->write(QByteArray::fromStdString(clientConnectedStatus.toStdString()));
    newSocket->flush();
}

void TcpServerProcessor::socketDisconnected()
{
    auto senderClient = std::dynamic_pointer_cast<QTcpSocket>(std::shared_ptr<QObject>(sender(),[](QObject* obj){}));
    if(senderClient)
    {
        disconnect(senderClient.get(), &QTcpSocket::readyRead, this, &TcpServerProcessor::processMessage);
        disconnect(senderClient.get(), &QTcpSocket::disconnected, this, &TcpServerProcessor::socketDisconnected);
        sockets.remove(senderClient);
    }
}

void TcpServerProcessor::processMessage()
{
    auto senderClient = std::dynamic_pointer_cast<QTcpSocket>(std::shared_ptr<QObject>(sender(),[](QObject* obj){}));
    QByteArray data = senderClient->readAll();
    qDebug() << "Your message: " <<  QString::fromUtf8(data);
}
