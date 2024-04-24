#ifndef DTO_H
#define DTO_H

#include <nlohmann/json.hpp>
#include <QVector>

using json = nlohmann::json;

struct Options {
    int sampleRate;
    std::string centerFrequency;
    std::string frequencyCorrection;
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
    double minFrequencyX;
    double maxFrequencyX;
    double maxValueY;
    QVector<double> xValues;
    QVector<double> yValues;
};

GraphData unmarshallGraphData(json& response){
    const double maxFrequencyX = response["max_frequency"];
    const double minFrequencyX = response["min_frequency"];
    const double maxValueY = response["max_value"];
    json dataArray = response["data"];
    QVector<double> xValues, yValues;


    if(dataArray.is_array()) {
        for(const auto& row : dataArray) {
            xValues.push_back(row[0]);
            yValues.push_back(row[1]);
        }
    }

    return {minFrequencyX, maxFrequencyX, maxValueY, xValues, yValues};
}

#endif // DTO_H
