#include <Pixy2UART.h>
Pixy2UART pixy;

#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>

EthernetUDP Udp;
byte mac[] = {0x90, 0xA2, 0xDA, 0x0D, 0x5C, 0x18};
IPAddress ip(192,168,250,123);
unsigned int localport = 8888;

IPAddress remoteIP(192,168,250,1);
unsigned int remotePort = 9600;

byte sendPacket[] =
  {
      // Full UDP packet: 80 00 02 00 00 00 00 05 00 19 01 02 82 00 64 00 00 01 00 01
  
      // Header
      0x80, //0.(ICF) Display frame information: 1000 0001
      0x00, //1.(RSV) Reserved by system: (hex)00
      0x02, //2.(GCT) Permissible number of gateways: (hex)02
      0x00, //3.(DNA) Destination network address: (hex)00, local network
      0x00, //4.(DA1) Destination node address: (hex)00, local PLC unit
      0x00, //5.(DA2) Destination unit address: (hex)00, PLC
      0x00, //6.(SNA) Source network address: (hex)00, local network
      0x05, //7.(SA1) Source node address: (hex)05, PC's IP is 192.168.250.5
      0x00, //8.(SA2) Source unit address: (hex)00, PC only has one ethernet
      0x19, //9.(SID) Service ID: just give a random number 19
  
      // Command
      0x01, //10.(MRC) Main request code: 01, memory area write
      0x02, //11.(SRC) Sub-request code: 02, memory area write
  
      // PLC Memory Area
      0x82, //12.Memory area code (1 byte): 82(DM)
  
      // Address information
      0x00, //13.Write start address (2 bytes): D30
      0x1E, 
      0x00, //15.Bit address (1 byte): Default 0
      0x00, //16.No. of items (2 bytes): only one address which is D100
      0x01,
  
      // Write Data
      0x00, //18.Data to write (2 bytes): prodNum is 1
      0x01,
  };



  


void setup(){
 pixy.init();
 Serial.begin(9600);
 Serial.println("****************");
 Serial.println("Serial port OK");
 Ethernet.begin(mac,ip);
 Serial.print("IP : ");
 Serial.println(Ethernet.localIP());
 Udp.begin(localport);
}


byte memmoryAdr = 0x1F; //D31
byte prodNum = 0x00;
bool pres = false;
void loop(){

  // grab blocks!
  pixy.line.getAllFeatures();


  // If there are detect blocks, print them!
  if (pixy.line.numBarcodes)
  {
    pres = true;
    Serial.print("Detected ");
    Serial.println(pixy.line.barcodes[0].m_code);
    if (prodNum <= 10)
      prodNum = pixy.line.barcodes[0].m_code;
      else
      prodNum = 0;
  } 
  else
  {
     pres = false;
     prodNum = 0;
  }

// Send Presence
  sendPacket[14] = 0x1E;
  sendPacket[19] = pres;
  
 Udp.beginPacket(remoteIP, remotePort);
 Udp.write((byte*)sendPacket, sizeof(sendPacket));
 Serial.println("Mensagem enviada para o automato");
 Udp.endPacket();



// Send Product
 sendPacket[14] = memmoryAdr;
 sendPacket[19] = prodNum;
   
 Udp.beginPacket(remoteIP, remotePort);
 Udp.write((byte*)sendPacket, sizeof(sendPacket));
 Serial.println("Mensagem enviada para o automato");
 Udp.endPacket();
 
 delay(200);
}
