#ifndef HANDLERS_H
#define HANDLERS_H

#include "../mainwindow.h"

void onStartClick(MainWindow* w, Ui::MainWindow *ui, bool& activityState);

void onStopClick(MainWindow* w, Ui::MainWindow *ui, bool& activityState);

void onSetClick(MainWindow* w, Ui::MainWindow *ui, const bool& autoState);

#endif // HANDLERS_H
