#pragma once
#include <QDebug>
#include <QObject>
#include "TcpServerProcessor.h"
#include "SDRController.h"

class MainProcessor : public QObject
{
    Q_OBJECT
public:
    explicit MainProcessor(QObject *parent = nullptr);

private:
    std::unique_ptr<TcpServerProcessor> tcpProcessor;
    std::unique_ptr<SDRController> sdrController;
signals:

};

