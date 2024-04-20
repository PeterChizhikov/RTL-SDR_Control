#ifndef WORKER_H
#define WORKER_H

#include <QThread>
#include "../mainwindow.h"


class Worker : public QThread
{

    QMainWindow* w;
    Ui::MainWindow *ui;

public:
    void run() override;
    void SetContext(QMainWindow* _w, Ui::MainWindow * _ui){
        w=_w;
        ui=_ui;
    }
    void stop(){
        this->requestInterruption();
    }
};

#endif // WORKER_H
