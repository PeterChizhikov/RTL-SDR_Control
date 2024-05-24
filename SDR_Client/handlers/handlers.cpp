#include "handlers.h"
#include "../dto/DTO.h"
#include <QTcpSocket>
#include <chrono>
#include <thread>

using json = nlohmann::json;

bool handleResponse(MainWindow* w, Ui::MainWindow *ui, QString& response) {

    json resp = json::parse(response.toStdString());

    if(resp["answer"]!=200){
        ui->label_7->setText("Error occured...");
        return false;
    }

    return true;

}

void onStartClick(MainWindow* w, Ui::MainWindow *ui, bool& activityState) {

    QString response;

    json requestJSON;
    requestJSON["type"]="system";
    requestJSON["action"]="start";
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
                std::thread t([ui]() {

                    ui->label_7->setStyleSheet("color:green;");
                    ui->label_7->setText("Success");
                    std::this_thread::sleep_for(std::chrono::seconds(1));
                    ui->label_7->setStyleSheet("color:red;");
                    ui->label_7->setVisible(false);
                });
                activityState = !activityState;
                ui->pushButton_3->setText("Stop");
                w->worker.start();
                t.join();
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
    delete socket;
}

void onStopClick(MainWindow* w, Ui::MainWindow *ui, bool& activityState){
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

                std::thread t([ui]() {
                        ui->label_7->setStyleSheet("color:green;");
                        ui->label_7->setText("Success");
                        std::this_thread::sleep_for(std::chrono::seconds(1));
                        ui->label_7->setStyleSheet("color:red;");
                        ui->label_7->setVisible(false);
                    });

                activityState = !activityState;
                ui->pushButton_3->setText("Start");

                w->worker.stop();
                w->worker.wait();

                t.join();
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
    delete socket;
}

void onSetClick(MainWindow* w, Ui::MainWindow *ui, const bool& autoState) {
    const int sample_rate = ui->spinBox->value();
    const std::string center_frequency = std::to_string(ui->spinBox_2->value());

    if(sample_rate<2*ui->spinBox_2->value()){
        std::thread t([ui]() {
                ui->label_7->setVisible(true);
                ui->label_7->setStyleSheet("color:red;");
                ui->label_7->setText("Sample Rate must be at least 2 times more than Center Frequency");
            });
        t.detach();
        return;
    }

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

                std::thread t([ui]() {
                        ui->label_7->setStyleSheet("color:green;");
                        ui->label_7->setText("Success");
                        std::this_thread::sleep_for(std::chrono::seconds(1));
                        ui->label_7->setStyleSheet("color:red;");
                        ui->label_7->setVisible(false);
                    });

                t.join();
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
    delete socket;
}

void onExitClick(MainWindow* w){

    w->worker.stop();
    w->worker.wait();
    QApplication::exit();

}
