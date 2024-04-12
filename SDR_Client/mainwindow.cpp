#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <iostream>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButton_3_clicked()
{

ui->graphicsView->setScene(&sc);
sc.addLine(0, 0, 250, 0); // Ось X
sc.addLine(0, 0, 0, -250); // Ось Y


}

