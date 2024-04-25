#include "worker.h"
#include <QUdpSocket>
#include <ctime>

using json = nlohmann::json;

struct GraphData{
    double minFrequencyX;
    double maxFrequencyX;
    double maxValueY;
    double minValueY;
    QVector<double> xValues;
    QVector<double> yValues;
};

GraphData unmarshallGraphData(json& response){
    const double maxFrequencyX = response["max_frequency"];
    const double minFrequencyX = response["min_frequency"];
    const double maxValueY = response["max_magnitude"];
    const double minValueY = response["min_magnitude"];
    json dataArray = response["data"];
    QVector<double> xValues, yValues;


    if(dataArray.is_array()) {
        for(const auto& row : dataArray) {
            xValues.push_back(row[0]);
            yValues.push_back(row[1]);
        }
    }

    return {minFrequencyX, maxFrequencyX, maxValueY, minValueY, xValues, yValues};
}

void Worker::updatePlot(double minF, double maxF, double minM, double maxM, const QVector<double>& xValues, const QVector<double>& yValues ) {
    ui->customPlot->yAxis->blockSignals(true);
    ui->customPlot->xAxis->blockSignals(true);

    ui->customPlot->yAxis->setRange(minM, maxM);
    ui->customPlot->xAxis->setRange(minF, maxF);
    ui->customPlot->graph(0)->setData(xValues, yValues);
    ui->customPlot->replot();

    ui->customPlot->blockSignals(false);
    ui->customPlot->yAxis->blockSignals(false);
    ui->customPlot->xAxis->blockSignals(false);
}

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

            json response = json::parse(data.toStdString());

            //QVector<QVector<double>> mock = generateMock();

            GraphData gData = unmarshallGraphData(response);

            updatePlot(gData.minFrequencyX, gData.maxFrequencyX, gData.minValueY, gData.maxValueY, gData.xValues, gData.yValues);
        }


//        QVector<QVector<double>> mock = generateMock();
//        QVector<double> xValues, yValues;

//        for(const auto& row : mock) {
//            xValues.push_back(row[0]);
//            yValues.push_back(row[1]);
//        }

//        updatePlot(0, 5, 0, 100, xValues, yValues);
        QThread::msleep(100);

    }

    udpSocket->close();
    delete udpSocket;

}

