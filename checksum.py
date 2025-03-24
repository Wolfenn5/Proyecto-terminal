### Script original obtenido de: https://www.geeksforgeeks.org/implementing-checksum-using-python/


# Se redujo una parte del script original para utilizar en firma_eliptica_hash.py e importarlo

def findChecksum(sent_message, k):
    # dividir el mensaje en bloques de k bits
    packets = [sent_message[i:i+k] for i in range(0, len(sent_message), k)]
    # sumar los bloques binarios
    sum_bin = bin(sum(int(packet, 2) for packet in packets))[2:]
    # controlar el desbordamiento
    while len(sum_bin) > k:
        x = len(sum_bin) - k
        sum_bin = bin(int(sum_bin[0:x], 2) + int(sum_bin[x:], 2))[2:]
    # ajustar la longitud del resultado
    sum_bin = sum_bin.zfill(k)
    # calcular el complemento
    checksum = ''.join('0' if bit == '1' else '1' for bit in sum_bin)
    return checksum




def checkReceiverChecksum(received_message, k, checksum):
    # dividir el mensaje en bloques de k bits
    packets = [received_message[i:i+k] for i in range(0, len(received_message), k)]
    # sumar los bloques binarios y el checksum
    sum_bin = bin(sum(int(packet, 2) for packet in packets) + int(checksum, 2))[2:]
    # controlar el desbordamiento
    while len(sum_bin) > k:
        x = len(sum_bin) - k
        sum_bin = bin(int(sum_bin[0:x], 2) + int(sum_bin[x:], 2))[2:]
    # calcular el complemento
    receiver_checksum = ''.join('0' if bit == '1' else '1' for bit in sum_bin)
    return receiver_checksum
