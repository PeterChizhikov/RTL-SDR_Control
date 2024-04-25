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

#endif // DTO_H
