#ifndef DTO_H
#define DTO_H

#include <nlohmann/json.hpp>
#include <QVector>

using json = nlohmann::json;

struct Options {
    int sampleRate;
    double centerFrequency;
    double frequencyCorrection;
    std::string gain;
};

json marshall(const Options& opts){
    return {
        {"sample_rate", opts.sampleRate},
        {"center_frequency", opts.centerFrequency},
        {"frequency_correction", opts.frequencyCorrection},
        {"gain", opts.gain}
    };
}

struct GraphData{
    double minFrequency;
    double maxFrequency;
    QVector<QVector<double>> values;
};

GraphData unmarshallGraphData(json& response){
    const double maxFrequency = response["max_frequency"];
    const double minFrequency = response["min_frequency"];
    json dataArray = response["data"];
    QVector<QVector<double>> values;

    if(dataArray.is_array()) {
        for(const auto& row : dataArray) {
            QVector<double> tmpRow;
            for(const auto& el : row){
                tmpRow.push_back(el);
            }
            values.push_back(tmpRow);
        }
    }

    return {minFrequency, maxFrequency, values};
}

#endif // DTO_H
