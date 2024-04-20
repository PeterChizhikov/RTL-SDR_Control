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

