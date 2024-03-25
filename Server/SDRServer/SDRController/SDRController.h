#pragma once
#include <QDebug>
#include "../libsdr/src/sdr.hh"
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <rtl-sdr.h>

class SDRController
{
public:
    SDRController();

    void testFunc();
private:
    void callback(unsigned char *buf, uint32_t len, void *ctx);
};

