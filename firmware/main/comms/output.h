// output.h -- Serial/BLE output, wire format LOCKED per
// docs/WIRE_FORMAT_v1.md (task_2026-08-05_005). BLE is primary transport,
// Serial is the dev/debug fallback -- same JSON schema, no BLE framing.
//
// GATT UUIDs and BLE chunking/MTU handling remain open (WIRE_FORMAT_v1.md
// §Transport) but don't block this file: device is single-producer,
// one event at a time, and the payload fits well under typical MTU
// (~250-350 bytes typical per WIRE_FORMAT_v1.md §Size note) -- no
// chunking protocol implemented here, matches the doc's v1 scope.

#pragma once

#include <cstddef>
#include <cstdint>
#include <string>

#include "layer1/gate.h"
#include "comms/peak_features.h"
#include "tflite/inference.h"

namespace spark::comms {

enum class OutputChannel {
    kSerial,
    kBle,
};

enum class SendStatus {
    kOk,
    kNotConnected,
    kNotInitialized,
};

// One CONFIRMED_FALL event, gateway-bound. Field set matches
// WIRE_FORMAT_v1.md's JSON payload exactly:
//   event_id, device_id, firmware_version, timestamp_ms, confidence,
//   peak_features (a_x,a_y,a_z,w_x,w_y,w_z)
// `confidence` is class_probs[1] only (P(FALL)) -- class_probs[0] stays
// internal to InferenceOutput and is dropped at the transport boundary
// (Resolution #1, WIRE_FORMAT_v1.md). No raw_window in v1 (Resolution #2).
//
// event_id/device_id/firmware_version are strings the caller (app_main)
// supplies -- generation strategy (UUID vs seq counter, MAC vs
// provisioned ID) is not this file's concern; SendFallEvent only encodes
// whatever it's given.
struct FallEvent {
    std::string event_id;
    std::string device_id;
    std::string firmware_version;
    uint32_t timestamp_ms;
    layer1::GateDecision gate_decision;  // not sent on wire; local bookkeeping only
    tflite_stub::InferenceOutput inference;
    PeakFeatures peak_features;
};

// Transport interface. Encodes FallEvent to the WIRE_FORMAT_v1.md JSON
// shape and writes it out. Actual UART/BLE I/O calls remain stubbed
// (ESP-IDF driver wiring is separate scope -- this task covers encoding
// + the call path, not `uart_driver_install`/NimBLE GATT server setup).
class OutputTransport {
public:
    explicit OutputTransport(OutputChannel channel) : channel_(channel) {}

    SendStatus Init();

    // Encodes `event` per WIRE_FORMAT_v1.md and sends it on `channel_`.
    SendStatus SendFallEvent(const FallEvent& event);

    OutputChannel channel() const { return channel_; }

private:
    OutputChannel channel_;
    bool initialized_ = false;
};

// Encodes a FallEvent to the WIRE_FORMAT_v1.md JSON string. Exposed
// standalone (not just as a SendFallEvent implementation detail) so it's
// independently host-testable without a transport/hardware dependency --
// same host-testable pattern as layer1/gate.h.
std::string EncodeFallEventJson(const FallEvent& event);

}  // namespace spark::comms
