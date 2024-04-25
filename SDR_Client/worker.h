#ifndef WORKER_H
#define WORKER_H

#include <QThread>
#include "mainwindow.h"
#include "./ui_mainwindow.h"


class Worker : public QThread
{

    QMainWindow* w;
    Ui::MainWindow *ui;

public:
    void run() override;
    Worker(QMainWindow* _w, Ui::MainWindow* _ui) : w(_w), ui(_ui){}
    Worker(const Worker& other) : w(other.w), ui(other.ui) {}
    Worker(Worker&& other) : w(other.w), ui(other.ui) {
        other.w = nullptr;
        other.ui = nullptr;
    }
    void stop(){
        this->requestInterruption();
    }

public slots:

    void updatePlot(double minF, double maxF, double minM, double maxM, const QVector<double>& xValues, const QVector<double>& yValues );
};

#endif // WORKER_H


