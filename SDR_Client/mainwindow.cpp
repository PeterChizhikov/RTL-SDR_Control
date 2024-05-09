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
}



void MainWindow::on_pushButton_2_clicked()
{
    onExitClick();
}

void MainWindow::WaterfallInit()
{
    fp3 = ui->customPlot_2; //创建一个画图指针
    fp3->setInteractions(QCP::iRangeDrag|QCP::iRangeZoom);//可拖拽+可滚轮缩放
    m_pColorMap = new QCPColorMap(fp3->xAxis,fp3->yAxis);
    m_pColorMap->data()->setSize(1000+1,51);//设置整个图（x,y）点数
    m_pColorMap->data()->setRange(QCPRange(0,1000),QCPRange(0,100));//setRange是设置X轴以及Y轴的范围
    m_pColorMap->setGradient(QCPColorGradient::gpJet);//设置默认渐进色变化（可在QCPColorGradient中查看）
    m_pColorMap->rescaleDataRange(true);
   // 立即刷新图像
    fp3->rescaleAxes();//自适应大小
   // ui->widget->replot();
}
