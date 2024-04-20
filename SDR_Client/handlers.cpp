#include "handlers.h"
#include "DTO.h"
#include <QTcpSocket>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

void onStartClick(MainWindow* w, Ui::MainWindow *ui, bool& activityState) {

    const int sample_rate = ui->spinBox->value();
    const double center_frequency = ui->spinBox_2->value();
    const double frequency_correction = ui->spinBox_3->value();
    const double gain = ui->spinBox_4->value();
    const Options opts = {sample_rate, center_frequency, frequency_correction, gain};
    QString response;

    QTcpSocket* socket = new QTcpSocket(w);

    socket->connectToHost("127.0.0.1", 5577);

    ui->label_7->setVisible(true);
    ui->label_7->setText("Loading...");

    if(socket->waitForConnected()){

        QString message = "hi";
        socket->write(message.toUtf8());
        socket->waitForBytesWritten();

        if(socket->waitForReadyRead()){

            QByteArray temp = socket->readAll();
            response = QString::fromUtf8(temp);

            ui->label_7->setVisible(false);

            activityState = !activityState;
            ui->pushButton_3->setText("Stop");

        }
        else {
            ui->label_7->setText("Error reading response...");
        }

    }
    else {
        ui->label_7->setText("Error while connecting to server...");
    }

    socket->close();
}

void onStopClick(MainWindow* w, Ui::MainWindow *ui, bool& activityState){}
