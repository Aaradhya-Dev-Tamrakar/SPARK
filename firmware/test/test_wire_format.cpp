// test_wire_format.cpp -- host-testable unit tests for comms/output.h's
// EncodeFallEventJson and comms/peak_features.h's ComputePeakFeatures.
// No hardware, no ESP-IDF headers, no I2C -- same host-testable pattern
// as test_gate.cpp.
//
// Build (no ESP-IDF needed):
//   g++ -std=c++17 -I../main test_wire_format.cpp ../main/comms/output.cpp
//       ../main/comms/peak_features.cpp -o test_wire_format
//   ./test_wire_format
//
// Validates against WIRE_FORMAT_v1.md's locked JSON shape: field
// presence, confidence = class_probs[1] only (class_probs[0] dropped),
// peak_features six-channel structure, no raw_window key.

#include <cstdio>
#include <cstring>
#include <string>

#include "comms/output.h"
#include "comms/peak_features.h"
#include "layer1/gate.h"
#include "tflite/inference.h"

using spark::comms::ComputePeakFeatures;
using spark::comms::EncodeFallEventJson;
using spark::comms::FallEvent;
using spark::comms::PeakFeatures;
using spark::layer1::GateDecision;
using spark::tflite_stub::InferenceInput;
using spark::tflite_stub::InferenceOutput;

namespace {

int g_failures = 0;
int g_checks = 0;

void Check(bool condition, const char* description) {
    ++g_checks;
    if (!condition) {
        ++g_failures;
        std::fprintf(stderr, "FAIL: %s\n", description);
    }
}

bool Contains(const std::string& haystack, const std::string& needle) {
    return haystack.find(needle) != std::string::npos;
}

FallEvent MakeSampleEvent() {
    InferenceOutput inference{};
    inference.class_probs[0] = 0.12f;  // P(NON_FALL) -- must NOT appear on wire
    inference.class_probs[1] = 0.88f;  // P(FALL) -- must appear as "confidence"

    PeakFeatures peaks{1.5f, -2.1f, 9.8f, 45.0f, -12.3f, 3.3f};

    return FallEvent{
        .event_id = "evt-0001",
        .device_id = "AA:BB:CC:DD:EE:FF",
        .firmware_version = "0.1.0-skeleton",
        .timestamp_ms = 123456,
        .gate_decision = GateDecision::kTriggerCnn,
        .inference = inference,
        .peak_features = peaks,
    };
}

void TestEncodeFallEventJson_ContainsAllLockedFields() {
    const std::string json = EncodeFallEventJson(MakeSampleEvent());

    Check(Contains(json, "\"event_id\":\"evt-0001\""),
          "JSON: event_id field present with correct value");
    Check(Contains(json, "\"device_id\":\"AA:BB:CC:DD:EE:FF\""),
          "JSON: device_id field present with correct value");
    Check(Contains(json, "\"firmware_version\":\"0.1.0-skeleton\""),
          "JSON: firmware_version field present with correct value");
    Check(Contains(json, "\"timestamp_ms\":123456"),
          "JSON: timestamp_ms field present with correct value");
    Check(Contains(json, "\"peak_features\":{"),
          "JSON: peak_features object present");
    for (const char* key : {"a_x", "a_y", "a_z", "w_x", "w_y", "w_z"}) {
        Check(Contains(json, std::string("\"") + key + "\":"),
              (std::string("JSON: peak_features contains key ") + key).c_str());
    }
}

void TestEncodeFallEventJson_ConfidenceIsClassProbsOneOnly() {
    const std::string json = EncodeFallEventJson(MakeSampleEvent());

    Check(Contains(json, "\"confidence\":0.88"),
          "JSON: confidence equals class_probs[1] (0.88)");
    Check(!Contains(json, "0.12"),
          "JSON: class_probs[0] (0.12, P(NON_FALL)) does not appear anywhere "
          "on the wire -- Resolution #1, WIRE_FORMAT_v1.md");
}

void TestEncodeFallEventJson_NoRawWindowKey() {
    const std::string json = EncodeFallEventJson(MakeSampleEvent());
    Check(!Contains(json, "raw_window"),
          "JSON: raw_window key absent -- Resolution #2, deferred to v2");
}

void TestEncodeFallEventJson_ValidJsonBraceBalance() {
    const std::string json = EncodeFallEventJson(MakeSampleEvent());
    int depth = 0;
    bool balanced = true;
    for (const char c : json) {
        if (c == '{') ++depth;
        if (c == '}') --depth;
        if (depth < 0) balanced = false;
    }
    Check(balanced && depth == 0, "JSON: brace-balanced, well-formed structure");
}

void TestComputePeakFeatures_PicksMaxAbsPerChannel() {
    InferenceInput window{};
    // Zero everything, then inject one large value per channel at
    // different sample indices -- peak extraction must be independent
    // of *which* sample position the peak occurs at.
    const int channels = spark::tflite_stub::kChannelsPerSample;
    window.data[0 * channels + 0] = 2.5f;    // a_x peak at sample 0
    window.data[50 * channels + 1] = -3.7f;  // a_y peak (negative) at sample 50
    window.data[199 * channels + 2] = 9.8f;  // a_z peak at last sample
    window.data[10 * channels + 3] = 120.0f; // w_x peak
    window.data[10 * channels + 4] = -45.5f; // w_y peak (negative)
    window.data[10 * channels + 5] = 0.5f;   // w_z peak (small)

    const PeakFeatures peaks = ComputePeakFeatures(window);

    Check(peaks.a_x == 2.5f, "PeakFeatures: a_x picks the injected peak");
    Check(peaks.a_y == -3.7f,
          "PeakFeatures: a_y picks negative peak by magnitude, keeps sign");
    Check(peaks.a_z == 9.8f, "PeakFeatures: a_z picks peak at last sample index");
    Check(peaks.w_x == 120.0f, "PeakFeatures: w_x picks the injected peak");
    Check(peaks.w_y == -45.5f, "PeakFeatures: w_y picks negative peak, keeps sign");
    Check(peaks.w_z == 0.5f, "PeakFeatures: w_z picks the only nonzero value");
}

void TestComputePeakFeatures_AllZeroWindowGivesAllZeroPeaks() {
    InferenceInput window{};  // zero-initialized
    const PeakFeatures peaks = ComputePeakFeatures(window);
    Check(peaks.a_x == 0.0f && peaks.a_y == 0.0f && peaks.a_z == 0.0f &&
              peaks.w_x == 0.0f && peaks.w_y == 0.0f && peaks.w_z == 0.0f,
          "PeakFeatures: all-zero window gives all-zero peaks");
}

}  // namespace

int main() {
    TestEncodeFallEventJson_ContainsAllLockedFields();
    TestEncodeFallEventJson_ConfidenceIsClassProbsOneOnly();
    TestEncodeFallEventJson_NoRawWindowKey();
    TestEncodeFallEventJson_ValidJsonBraceBalance();
    TestComputePeakFeatures_PicksMaxAbsPerChannel();
    TestComputePeakFeatures_AllZeroWindowGivesAllZeroPeaks();

    std::printf("%d/%d checks passed\n", g_checks - g_failures, g_checks);
    return g_failures == 0 ? 0 : 1;
}
