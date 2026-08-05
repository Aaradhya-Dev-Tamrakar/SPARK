// output.cpp -- encodes FallEvent per WIRE_FORMAT_v1.md and sends it.
// UART/BLE driver init and the actual write/notify call remain stubbed
// (ESP-IDF peripheral wiring is out of this task's scope -- see gate.h-
// style scope notes elsewhere in this repo); encoding is real.

#include "comms/output.h"

#include <cstdio>

namespace spark::comms {

namespace {

// Minimal dependency-free JSON string escaping -- WIRE_FORMAT_v1.md's
// string fields (event_id, device_id, firmware_version) are expected to
// be simple identifiers/semver strings, but escape defensively rather
// than assume no caller ever passes a quote or backslash.
void AppendEscapedJsonString(std::string* out, const std::string& value) {
    out->push_back('"');
    for (const char c : value) {
        switch (c) {
            case '"':
                out->append("\\\"");
                break;
            case '\\':
                out->append("\\\\");
                break;
            case '\n':
                out->append("\\n");
                break;
            default:
                out->push_back(c);
        }
    }
    out->push_back('"');
}

// %g-style float formatting -- compact, matches typical JSON float
// output. No fixed decimal-place requirement in WIRE_FORMAT_v1.md.
std::string FormatFloat(float value) {
    char buf[32];
    std::snprintf(buf, sizeof(buf), "%g", static_cast<double>(value));
    return std::string(buf);
}

}  // namespace

std::string EncodeFallEventJson(const FallEvent& event) {
    std::string json;
    json.reserve(320);  // WIRE_FORMAT_v1.md §Size note: ~250-350 bytes typical

    json.append("{");

    json.append("\"event_id\":");
    AppendEscapedJsonString(&json, event.event_id);
    json.append(",");

    json.append("\"device_id\":");
    AppendEscapedJsonString(&json, event.device_id);
    json.append(",");

    json.append("\"firmware_version\":");
    AppendEscapedJsonString(&json, event.firmware_version);
    json.append(",");

    json.append("\"timestamp_ms\":");
    json.append(std::to_string(event.timestamp_ms));
    json.append(",");

    // Resolution #1 (WIRE_FORMAT_v1.md): confidence = class_probs[1]
    // (P(FALL)) only. class_probs[0] stays internal to InferenceOutput,
    // dropped here at the transport boundary.
    json.append("\"confidence\":");
    json.append(FormatFloat(event.inference.class_probs[1]));
    json.append(",");

    json.append("\"peak_features\":{");
    json.append("\"a_x\":");
    json.append(FormatFloat(event.peak_features.a_x));
    json.append(",\"a_y\":");
    json.append(FormatFloat(event.peak_features.a_y));
    json.append(",\"a_z\":");
    json.append(FormatFloat(event.peak_features.a_z));
    json.append(",\"w_x\":");
    json.append(FormatFloat(event.peak_features.w_x));
    json.append(",\"w_y\":");
    json.append(FormatFloat(event.peak_features.w_y));
    json.append(",\"w_z\":");
    json.append(FormatFloat(event.peak_features.w_z));
    json.append("}");
    // No raw_window key -- Resolution #2 (WIRE_FORMAT_v1.md): deferred to v2.

    json.append("}");
    return json;
}

SendStatus OutputTransport::Init() {
    // TODO: kSerial -> uart_driver_install(); kBle -> NimBLE GATT server
    // setup + service/characteristic registration (UUIDs still open per
    // WIRE_FORMAT_v1.md §Transport). Neither happens here -- init always
    // succeeds so app_main can be built against this interface; encoding
    // (the actual scope of this task) is real and testable independent
    // of this peripheral wiring.
    initialized_ = true;
    return SendStatus::kOk;
}

SendStatus OutputTransport::SendFallEvent(const FallEvent& event) {
    if (!initialized_) {
        return SendStatus::kNotInitialized;
    }
    const std::string payload = EncodeFallEventJson(event);
    // TODO: kSerial -> uart_write_bytes(); kBle -> GATT characteristic
    // notify with `payload`. Both are peripheral-driver calls, not
    // encoding logic -- out of this task's scope (see Init() note).
    // Payload fits in 2-3 BLE packets at MTU 185+ per WIRE_FORMAT_v1.md
    // §Size note; no chunking needed for v1.
    (void)payload;
    return SendStatus::kOk;
}

}  // namespace spark::comms
