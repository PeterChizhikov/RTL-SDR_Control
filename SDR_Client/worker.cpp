#include "worker.h"
#include <QUdpSocket>
#include <ctime>
#include <float.h>

using json = nlohmann::json;

std::mutex mtx;

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

QVector<QVector<double>> generateMock(){

    srand(time(0));
    QVector<QVector<double>> values;

    for(double i = 0.0; i < 5.0; i+=0.01){
        QVector<double> tmp;
        tmp.append(i);
        if(i>2.0&&i<3.0)
        tmp.append(rand()%10+50);
        else
            tmp.append(rand()%20);
        values.append(tmp);
    }

    return values;
}

void Worker::run() {

    QUdpSocket* udpSocket = new QUdpSocket();
    udpSocket->bind(QHostAddress::Any, 6643);

    double yTop = DBL_MIN;
    double yBot = DBL_MAX;

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

            if (gData.minValueY < yBot){
                yBot = gData.minValueY;
            }

            if(gData.maxValueY > yTop) {
                yTop = gData.maxValueY;
            }

            emit DataRecieved(gData.minFrequencyX, gData.maxFrequencyX, yBot, yTop, gData.xValues, gData.yValues);

        }


//        QVector<QVector<double>> mock = generateMock();
//        QVector<double> xValues, yValues;

//        for(const auto& row : mock) {
//            xValues.push_back(row[0]);
//            yValues.push_back(row[1]);
//        }

//        emit DataRecieved( 0, 5, 0, 100, xValues, yValues);
    }

    udpSocket->close();
    delete udpSocket;

}
