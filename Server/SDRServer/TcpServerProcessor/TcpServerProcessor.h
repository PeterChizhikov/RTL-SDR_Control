#pragma once
#include <QDebug>
#include <QTcpServer>
#include <QTcpSocket>
#include <vector>

class TcpServerProcessor : public QTcpServer
{
    Q_OBJECT
public:
    TcpServerProcessor(QObject *parent = 0);


private:
    std::list<std::shared_ptr<QTcpSocket>> sockets;
    QByteArray Data;
    int16_t portForListen = 2323;
    std::unique_ptr<QTcpServer> tcpServer;


    void SendToClient(QByteArray data);


public slots:
//    qintptr Этот тип гарантирует, что будет тем же размером как указатель на всех платформах, поддерживаемых QT.
//    В системе с 32-разрядными указателями qintptr является определением типа для qint32;
//    в системе с 64-разрядными указателями qintptr является определением типа для qint64.
    void newConnection();
    void processMessage();
    void socketDisconnected();
};

