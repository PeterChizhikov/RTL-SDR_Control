#include "MainProcessor.h"

MainProcessor::MainProcessor(QObject *parent)
    : QObject{parent}
{
    tcpProcessor = std::make_unique<TcpServerProcessor>();
    udpProcessor = std::make_unique<UdpServerProcessor>();
}
