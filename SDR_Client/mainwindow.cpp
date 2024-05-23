#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <iostream>
#include <QTcpSocket>
#include "handlers/handlers.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->label_7->setVisible(false);
    WaterfallInit();

    connect(&worker, &Worker::DataRecieved, this, &MainWindow::onDataRecieved);

    ui->customPlot->addGraph();
    ui->customPlot->xAxis->setLabel("frequency");
    ui->customPlot->yAxis->setLabel("magnitude");
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButton_3_clicked()
{

    if(!activityState){
        onStartClick(this, ui, activityState);
    }
    else {
        onStopClick(this, ui, activityState);
    }

}


void MainWindow::on_pushButton_5_clicked()
{
    onSetClick(this, ui, autoState);
}

void MainWindow::on_pushButton_clicked()
{
    autoState = !autoState;

    autoState ? ui->pushButton->setStyleSheet("background-color:green; border-radius: 5px; color: white; border: 1px solid white;") : ui->pushButton->setStyleSheet("background-color:blue; border-radius: 5px; color: white; border: 1px solid white;");

    ui->spinBox_4->setEnabled(!autoState);
}



void MainWindow::on_pushButton_2_clicked()
{
    onExitClick(this);
}

void MainWindow::WaterfallInit()
{
    fp3 = ui->customPlot_2;
    fp3->setInteractions(QCP::iRangeDrag|QCP::iRangeZoom);
    m_pColorMap = new QCPColorMap(fp3->xAxis,fp3->yAxis);
    m_pColorMap->data()->setSize(1024,100);
    m_pColorMap->data()->setRange(QCPRange(0,100),QCPRange(0,100));
    m_pColorMap->setGradient(QCPColorGradient::gpJet);
//    m_pColorMap->rescaleDataRange(true);

    fp3->rescaleAxes();
   // ui->widget->replot();
}

void MainWindow::onDataRecieved(double _minF, double _maxF, double _minM, double _maxM, const QVector<double>& _xValues, const QVector<double>& _yValues)
{
    ui->customPlot->yAxis->blockSignals(true);
    ui->customPlot->xAxis->blockSignals(true);

    ui->customPlot->yAxis->setRange(_minM, _maxM);
    ui->customPlot->xAxis->setRange(_minF, _maxF);
    m_pColorMap->data()->setRange(QCPRange(_minF, _maxF),QCPRange(0,100));
    ui->customPlot->graph(0)->setData(_xValues, _yValues);
    ui->customPlot->replot();

    ui->customPlot->blockSignals(false);
    ui->customPlot->yAxis->blockSignals(false);
    ui->customPlot->xAxis->blockSignals(false);

    if(value_lofar.size()>99)
    {
        value_lofar.removeLast();
    }

    value_lofar.prepend(_yValues);

    for (int i=0;i<value_lofar.size();i++)
    {
        for(int j=0;j<_xValues.size();j++)
        {
            m_pColorMap->data()->setCell(j,i,value_lofar[i][j]);
        }
    }

    m_pColorMap->rescaleDataRange(true);
    m_pColorMap->data()->setSize(_xValues.size()+1,100);
    fp3->rescaleAxes();
    ui->customPlot_2->replot();
}
