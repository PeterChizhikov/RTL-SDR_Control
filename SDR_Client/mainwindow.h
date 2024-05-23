#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QGraphicsScene>
#include <nlohmann/json.hpp>
#include <./lib/qcustomplot/qcustomplot.h>
#include "worker.h"


QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void WaterfallInit();

    Worker worker;

    QCustomPlot * fp3;
    QCPColorMap * m_pColorMap;

private slots:
    void on_pushButton_3_clicked();

    void on_pushButton_5_clicked();

    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

    void onDataRecieved(double _minF, double _maxF, double _minM, double _maxM, const QVector<double>& _xValues, const QVector<double>& _yValues);


private:
    QList<QVector<double> > value_lofar;
    Ui::MainWindow *ui;
    bool activityState = false;
    bool autoState = false;

};
#endif // MAINWINDOW_H
