#include <QCoreApplication>
#include "MainProcessor.h"


int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    std::unique_ptr<MainProcessor> mainProc = std::make_unique<MainProcessor>();


    return a.exec();
}
