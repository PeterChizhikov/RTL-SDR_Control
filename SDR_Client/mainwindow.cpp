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
    onExitClick();
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
