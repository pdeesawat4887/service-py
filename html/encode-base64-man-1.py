import base64
import bitmath

passEND1 = base64.b64encode("service_monitor")
passEND2 = base64.b64encode("p@ssword")

print passEND2

# print "Hello {fname} {lname} and today is my {condition}".format(fname='Peter', condition='BirthDay', lname='Parker')

# def convert_bps_to_mbps(num_of_bytes):
#     bit = bitmath.Bit(num_of_bytes)
#     return bit.to_Mib().value
#
#
# def convert_bps_to_mbps2(num_of_bytes):
#     bit = bitmath.Byte(num_of_bytes)
#     return bit.to_MiB().value
#
# print convert_bps_to_mbps(1234567899)
# print convert_bps_to_mbps2(1234567899)