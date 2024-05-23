#ifndef WORKER_H
#define WORKER_H

#include <QThread>
#include "./ui_mainwindow.h"
#include <nlohmann/json.hpp>

class Worker : public QThread
{

    Q_OBJECT

public:
    void run() override;
    void stop(){
        this->requestInterruption();
    }

signals:

    void DataRecieved(double _minF, double _maxF, double _minM, double _maxM, const QVector<double>& _xValues, const QVector<double>& _yValues);


};

#endif // WORKER_H


