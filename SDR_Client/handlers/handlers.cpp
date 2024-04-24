#include "handlers.h"
#include "dto/DTO.h"
#include <QTcpSocket>
#include <nlohmann/json.hpp>
#include <future>
#include <chrono>
#include <thread>

using json = nlohmann::json;

Worker* worker;

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

    std::future<void> handleSuccess;

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
                handleSuccess = std::async(std::launch::async, [ui]() {
                        ui->label_7->setStyleSheet("color:green;");
                        ui->label_7->setText("Success");
                        std::this_thread::sleep_for(std::chrono::seconds(1));
                        ui->label_7->setStyleSheet("color:red;");
                        ui->label_7->setVisible(false);
                    });
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

    handleSuccess.wait();
    socket->close();
}

void onStopClick(MainWindow* w, Ui::MainWindow *ui, bool& activityState){
    worker->stop();
    QString response;

    json requestJSON;
    requestJSON["type"]="system";
    requestJSON["action"]="stop";

    std::future<void> handleSuccess;

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

                handleSuccess = std::async(std::launch::async, [ui]() {
                        ui->label_7->setStyleSheet("color:green;");
                        ui->label_7->setText("Success");
                        std::this_thread::sleep_for(std::chrono::seconds(1));
                        ui->label_7->setStyleSheet("color:red;");
                        ui->label_7->setVisible(false);
                    });

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

    handleSuccess.wait();
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

    std::future<void> handleSuccess;

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

                handleSuccess = std::async(std::launch::async, [ui]() {
                        ui->label_7->setStyleSheet("color:green;");
                        ui->label_7->setText("Success");
                        std::this_thread::sleep_for(std::chrono::seconds(1));
                        ui->label_7->setStyleSheet("color:red;");
                        ui->label_7->setVisible(false);
                    });

            }


        }
        else {
            ui->label_7->setText("Error reading response...");
        }

    }
    else {
        ui->label_7->setText("Error while connecting to server...");
    }

    handleSuccess.wait();
    socket->close();
}

void onExitClick(){

    worker->stop();
    worker->wait();
    QApplication::exit();
}
