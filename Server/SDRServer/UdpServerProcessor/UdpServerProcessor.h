#pragma once
#include <QDebug>
#include <QUdpSocket>
#include <QHostAddress>
#include <thread>
#include <chrono>


class UdpServerProcessor : public QObject
{
    Q_OBJECT
public:
    UdpServerProcessor(QObject *parent = 0);


private:
    std::unique_ptr<QUdpSocket> udpServerSocket;
    void readMessage();
    int16_t udpPort = 2424;

public slots:
    void sendData(QByteArray &data);

signals:
    void startWork(QByteArray &data);
};

