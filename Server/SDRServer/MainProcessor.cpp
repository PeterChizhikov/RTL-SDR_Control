#include "MainProcessor.h"

MainProcessor::MainProcessor(QObject *parent)
    : QObject{parent}
{

    tcpProcessor = std::make_unique<TcpServerProcessor>();

}
