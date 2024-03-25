#include "MainProcessor.h"

MainProcessor::MainProcessor(QObject *parent)
    : QObject{parent}
{

    tcpProcessor = std::make_unique<TcpServerProcessor>();
    sdrController = std::make_unique<SDRController>();
}
