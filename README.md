# RTL-SDR_Control

быстрый старт https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/



TCP команды от клиента разделяются на 2 типа: "system" и "settings":

TCP_PORT_SERVER = 5577

system - отвечает за начало и остановку передачи данных на клиент с примемника
{
    "type": "system"
    "action": "start"
}
or
{
    "type": "system"
    "action": "stop"
}
