from scapy.all import sniff


class PacketCapture:
    def __init__(self, interface: str, packet_callback):
        self.interface = interface
        self.packet_callback = packet_callback

    def start(self):
        if self.interface:
            print(f"[INFO] Capturando tráfico en interfaz: {self.interface}")
            sniff(iface=self.interface, prn=self.packet_callback, store=False)
        else:
            print("[INFO] Capturando tráfico en interfaz por defecto")
            sniff(prn=self.packet_callback, store=False)
