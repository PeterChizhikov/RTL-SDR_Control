#ifndef HANDLERS_H
#define HANDLERS_H

#include "mainwindow.h"
#include "./ui_mainwindow.h"

void onStartClick(MainWindow* w, Ui::MainWindow *ui, bool& activityState);

void onStopClick(MainWindow* w, Ui::MainWindow *ui, bool& activityState);

#endif // HANDLERS_H
