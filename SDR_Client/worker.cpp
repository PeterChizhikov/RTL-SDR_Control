#include "worker.h"
#include <QUdpSocket>
#include <ctime>

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

void Worker::updatePlot(double minF, double maxF, double minM, double maxM, const QVector<double>& xValues, const QVector<double>& yValues ) {

    std::lock_guard<std::mutex> lock(mtx);

    ui->customPlot->yAxis->blockSignals(true);
    ui->customPlot->xAxis->blockSignals(true);

    ui->customPlot->yAxis->setRange(minM, maxM);
    ui->customPlot->xAxis->setRange(minF, maxF);
    w->m_pColorMap->data()->setRange(QCPRange(minF,maxF),QCPRange(0,100));
    ui->customPlot->graph(0)->setData(xValues, yValues);
    ui->customPlot->replot();

    ui->customPlot->blockSignals(false);
    ui->customPlot->yAxis->blockSignals(false);
    ui->customPlot->xAxis->blockSignals(false);

    if(value_lofar.size()>99)
    {
        value_lofar.removeLast();
    }

    value_lofar.prepend(yValues);

    for (int i=0;i<value_lofar.size();i++)
    {
        for(int j=0;j<xValues.size();j++)
        {
            w->m_pColorMap->data()->setCell(j,i,value_lofar[i][j]);
        }
    }

    w->m_pColorMap->rescaleDataRange(true);
    w->m_pColorMap->data()->setSize(xValues.size()+1,100);
    w->fp3->rescaleAxes();
    ui->customPlot_2->replot();

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

    QUdpSocket* udpSocket = new QUdpSocket(w);
    udpSocket->bind(QHostAddress::Any, 6643);

    ui->customPlot->addGraph();
    ui->customPlot->xAxis->setLabel("frequency");
    ui->customPlot->yAxis->setLabel("magnitude");

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

            std::thread th(&Worker::updatePlot, this, gData.minFrequencyX, gData.maxFrequencyX, gData.minValueY, gData.maxValueY, gData.xValues, gData.yValues);

            th.join();
        }


//        QVector<QVector<double>> mock = generateMock();
//        QVector<double> xValues, yValues;

//        for(const auto& row : mock) {
//            xValues.push_back(row[0]);
//            yValues.push_back(row[1]);
//        }

//        std::thread th(&Worker::updatePlot, this, 0, 5, 0, 100, xValues, yValues);

//        th.join();

        QThread::msleep(500);
    }

    udpSocket->close();
    delete udpSocket;

}

