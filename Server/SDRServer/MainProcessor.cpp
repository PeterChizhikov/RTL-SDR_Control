#include "MainProcessor.h"

MainProcessor::MainProcessor(QObject *parent)
    : QObject{parent}
{
//    sdr::Queue::get(); --
    tcpProcessor = std::make_unique<TcpServerProcessor>();
    sdrController = std::make_unique<SDRController>();
}
