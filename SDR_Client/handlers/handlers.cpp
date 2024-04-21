#include "handlers.h"
#include "dto/DTO.h"
#include <QTcpSocket>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

Worker* worker;

bool handleResponse(MainWindow* w, Ui::MainWindow *ui, QString& response) {

    json resp = json::parse(response.toStdString());

    if(resp["answer"]!=200){
        ui->label_7->setText("Error occured...");
        return true;
    }

    return false;

}

void onStartClick(MainWindow* w, Ui::MainWindow *ui, bool& activityState) {

    QString response;

    json requestJSON;
    requestJSON["type"]="system";
    requestJSON["action"]="start";

    worker = new Worker(w, ui);
    worker->start();

    QTcpSocket* socket = new QTcpSocket(w);

    socket->connectToHost("127.0.0.1", 5577);

    ui->label_7->setVisible(true);
    ui->label_7->setText("Loading...");

    if(socket->waitForConnected()){
        QString message = QString::fromStdString(requestJSON.dump());
        socket->write(message.toUtf8());
        socket->waitForBytesWritten();

        if(socket->waitForReadyRead()){

            QByteArray temp = socket->readAll();
            response = QString::fromUtf8(temp);

            if(handleResponse(w, ui, response))
            {
                ui->label_7->setVisible(false);

                activityState = !activityState;
                ui->pushButton_3->setText("Stop");

            }

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

void onStopClick(MainWindow* w, Ui::MainWindow *ui, bool& activityState){
    worker->stop();
    QString response;

    json requestJSON;
    requestJSON["type"]="system";
    requestJSON["action"]="stop";

    QTcpSocket* socket = new QTcpSocket(w);

    socket->connectToHost("127.0.0.1", 5577);

    ui->label_7->setVisible(true);
    ui->label_7->setText("Loading...");

    if(socket->waitForConnected()){
        QString message = QString::fromStdString(requestJSON.dump());
        socket->write(message.toUtf8());
        socket->waitForBytesWritten();

        if(socket->waitForReadyRead()){

            QByteArray temp = socket->readAll();
            response = QString::fromUtf8(temp);
            if(handleResponse(w, ui, response)) {

                worker->wait();

                ui->label_7->setVisible(false);

                activityState = !activityState;
                ui->pushButton_3->setText("Start");

            }


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

void onSetClick(MainWindow* w, Ui::MainWindow *ui, const bool& autoState) {
    const int sample_rate = ui->spinBox->value();
    const std::string center_frequency = std::to_string(ui->spinBox_2->value());
    const std::string frequency_correction = std::to_string(ui->spinBox_3->value());
    const std::string gain =  autoState ? "auto" : std::to_string(ui->spinBox_4->value());
    const Options opts = {sample_rate, center_frequency, frequency_correction, gain};
    QString response;

    json request = marshall(opts);
    request["type"] = "settings";

    QTcpSocket* socket = new QTcpSocket(w);

    socket->connectToHost("127.0.0.1", 5577);

    ui->label_7->setVisible(true);
    ui->label_7->setText("Loading...");

    if(socket->waitForConnected()){
        QString message = QString::fromStdString(request.dump());
        socket->write(message.toUtf8());
        socket->waitForBytesWritten();

        if(socket->waitForReadyRead()){

            QByteArray temp = socket->readAll();
            response = QString::fromUtf8(temp);
            if(handleResponse(w, ui, response)) {

                ui->label_7->setVisible(false);
            }


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

void onExitClick(){

    worker->stop();
    worker->wait();
    QApplication::exit();
}
