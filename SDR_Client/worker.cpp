#include "worker.h"
#include <QUdpSocket>
#include <ctime>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

QVector<QVector<double>>  generateMock(){

    srand(time(0));
    QVector<QVector<double>> values;

    for(double i = 0.0; i < 5.0 ; i+=0.01){
        QVector<double> tmp;
        tmp.append(i);
        tmp.append(rand()%100);
        values.append(tmp);
    }

    return values;
}

void Worker::run() {

    QUdpSocket* udpSocket = new QUdpSocket(w);
    udpSocket->bind(QHostAddress::Any, 6643);

    ui->customPlot->addGraph();
    ui->customPlot->xAxis->setLabel("f");
    ui->customPlot->yAxis->setLabel("S(f)");

    while(!isInterruptionRequested()){

        if(udpSocket->hasPendingDatagrams()){
            QByteArray datagram;
            QString data;

            datagram.resize(udpSocket->pendingDatagramSize());

            udpSocket->readDatagram(datagram.data(), datagram.size());

            data = QString::fromUtf8(datagram);

            json response(data.toStdString());

            //QVector<QVector<double>> mock = generateMock();

            QVector<QVector<double>> points = response["data"];

            QVector<double> xAxis, yAxis;

            for(auto& v : points){
                xAxis.append(v[0]);
                yAxis.append(v[1]);
            }

            ui->customPlot->yAxis->setRange(0, response["max_y"]);
            ui->customPlot->xAxis->setRange(response["min_x"], response["max_x"]);
            ui->customPlot->graph(0)->setData(xAxis, yAxis);
            ui->customPlot->replot();
        }

    }

    udpSocket->close();

}

