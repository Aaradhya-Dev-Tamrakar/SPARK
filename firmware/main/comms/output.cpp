// output.cpp -- stub bodies. No UART/BLE I/O, no serialization.
// Blocked on wire-format confirmation with user4 (this session's scope).

#include "comms/output.h"

namespace spark::comms {

SendStatus OutputTransport::Init() {
    // TODO: kSerial -> uart_driver_install(); kBle -> NimBLE GATT server
    // setup. Neither happens here -- stub always succeeds so app_main can
    // be built against this interface.
    initialized_ = true;
    return SendStatus::kOk;
}

SendStatus OutputTransport::SendFallEvent(const FallEvent& event) {
    if (!initialized_) {
        return SendStatus::kNotInitialized;
    }
    // TODO: serialize `event` per the confirmed wire format and write to
    // UART or notify over BLE. No encoding logic here yet -- deliberately,
    // per scope note (wire format wait).
    (void)event;
    return SendStatus::kOk;
}

}  // namespace spark::comms
