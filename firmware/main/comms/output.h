// output.h -- Serial/BLE output stub.
//
// WIRE FORMAT NOT DECIDED. Waiting on confirmation with user4 (per this
// session's scope) before locking a schema -- JSON per proposal §2.1
// ("Output: local JSON + clinical PDF...") is the likely target, but
// field names/framing/BLE-vs-serial-first are unconfirmed. This header
// only fixes the *transport-agnostic call shape* (send a fall event,
// get a status back) so app_main.cpp has something to call without
// blocking on that decision.
//
// Do not add JSON field definitions, BLE GATT characteristic UUIDs, or
// packet framing here until the format is confirmed -- this file should
// stay format-opaque.

#pragma once

#include <cstddef>
#include <cstdint>

#include "layer1/gate.h"
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

// Everything downstream (gateway JSON, SHAP, PDF) needs about one fall
// event. Deliberately just the fields already locked elsewhere in the
// pipeline (gate decision + CNN output + timestamp) -- no serialization
// format applied to it yet. Field list may grow once wire format is
// confirmed with user4.
struct FallEvent {
    uint32_t timestamp_ms;
    layer1::GateDecision gate_decision;
    tflite_stub::InferenceOutput inference;
};

// Transport interface. Both channels stubbed -- no UART writes, no BLE
// GATT notify calls. Real bodies are blocked on wire-format confirmation.
class OutputTransport {
public:
    explicit OutputTransport(OutputChannel channel) : channel_(channel) {}

    SendStatus Init();

    // Serialization format TBD -- stub does not encode `event` to bytes
    // yet. Signature is stable so app_main can call this once per
    // Layer-2-triggered event without knowing the eventual wire format.
    SendStatus SendFallEvent(const FallEvent& event);

    OutputChannel channel() const { return channel_; }

private:
    OutputChannel channel_;
    bool initialized_ = false;
};

}  // namespace spark::comms
