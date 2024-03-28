#include "UdpServerProcessor.h"

UdpServerProcessor::UdpServerProcessor(QObject *parent):QObject{parent}
{
    udpServerSocket = std::make_unique<QUdpSocket>();

    if(udpServerSocket->bind(QHostAddress::LocalHost, udpPort))
    {
        qDebug() << "udpServerSocket started on port " << udpPort << "\n";
        connect(udpServerSocket.get(), &QUdpSocket::readyRead,
                this, &UdpServerProcessor::readMessage);
        //test, emitted from constructor
        connect(this, SIGNAL(startWork(QByteArray &)),
                this, SLOT(sendData(QByteArray &)));
    }else {
        qDebug() << "udpServerSocket not started";
    }


}

void UdpServerProcessor::readMessage()
{

}

void UdpServerProcessor::sendData(QByteArray &data)
{
//    int num = 0;
//    for(;;)
//    {
//        qDebug("sendData from udp");
//        QString temp =  "Num: " + QString::number(num) + "\n";
//        QByteArray arr = temp.toUtf8();
//        arr.append(arr);
//        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
//        udpServerSocket->writeDatagram(arr, QHostAddress::LocalHost, 2525);
//        num++;
//    }
}


