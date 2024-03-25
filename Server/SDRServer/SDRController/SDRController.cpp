#include "SDRController.h"
#include <stdio.h>
#include <stdlib.h>
#include <rtl-sdr.h>
#include <QDebug>

void callback(unsigned char *buf, uint32_t len, void *ctx) //обработка
{
    if (!ctx) {
        return;
    }
}

int main()
{
    rtlsdr_dev_t *dev = NULL;

    int r = rtlsdr_open(&dev, 0);
    if (r < 0) {
        qDebug() << "Failed to open rtlsdr device";
        return EXIT_FAILURE;
    }
    qDebug() << "Successfully opened rtlsdr device";

    rtlsdr_set_center_freq(dev, 100000000);
    qDebug() << "Center frequency set to 100 MHz";

    rtlsdr_set_sample_rate(dev, 2048000);
    qDebug() << "Sample rate set to 2048000 Hz";

    rtlsdr_read_async(dev, callback, NULL, 0, 0);
    qDebug() << "Started async read";

    rtlsdr_close(dev);
    qDebug() << "Closed rtlsdr device";

    return EXIT_SUCCESS;
}
