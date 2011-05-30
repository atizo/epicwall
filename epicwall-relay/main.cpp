#include <WProgram.h>
#include <WiShield.h>
#include <avr/interrupt.h>
#include "HardwareSerial.h"
#include "epicwall.h"

extern "C" void __cxa_pure_virtual(void);
void __cxa_pure_virtual(void) {}

#define WIRELESS_MODE_INFRA 1
#define WIRELESS_MODE_ADHOC 2

// Wireless configuration parameters ----------------------------------------
extern U8 local_ip[] = {192,168,1,2};   // IP address of WiShield
extern U8 gateway_ip[] = {192,168,1,1}; // router or gateway IP address
extern U8 subnet_mask[] = {255,255,255,0};  // subnet mask for the local network
extern const prog_char ssid[] PROGMEM = {"epicwall"};     // max 32 bytes

extern U8 security_type = 0;    // 0 - open; 1 - WEP; 2 - WPA; 3 - WPA2


// WPA/WPA2 passphrase
extern const prog_char security_passphrase[] PROGMEM = {"12345678"};   // max 64 characters

// WEP 128-bit keys
// sample HEX keys
extern prog_uchar wep_keys[] PROGMEM = {   0x0e, 0x09, 0x01, 0x0c, 0x03, 0x0a, 0x01, 0x01, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e,   // Key 0 (e91c3a11abcde)
                                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,   // Key 1
                                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,   // Key 2
                                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00    // Key 3
                                };

// setup the wireless mode
// infrastructure - connect to AP
// adhoc - connect to another WiFi device
unsigned char wireless_mode = WIRELESS_MODE_ADHOC;

unsigned char ssid_len;
unsigned char security_passphrase_len;
//---------------------------------------------------------------------------

char previous_pixelbuffer[PIXEL_LEN];

void setup()
{
    WiFi.init();
    Serial.begin(115200);
    Serial.write("fdgfsdgsdg");

    memset(previous_pixelbuffer, 0x00, PIXEL_LEN);
}

void loop()
{
    uint8_t sreg_local; // Lokale Sicherungskopie von SREG

    WiFi.run();

    sreg_local = SREG;
    cli();

    if (strcmp((char*)pixelbuffer, previous_pixelbuffer) != 0) {
        Serial.write((char*)pixelbuffer);
        Serial.write(0xff);
        memcpy(previous_pixelbuffer, (char*)pixelbuffer, PIXEL_LEN);
    }

    SREG = sreg_local;
}

int main(void)
{
    init();

    setup();

    for (;;) {
        loop();
    }
}
