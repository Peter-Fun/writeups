import binascii
vals = """       local_38 = 0xa2;
  local_37 = 0xa8;
  local_36 = 0xa5;
  local_35 = 0xa3;
  local_34 = 0x9b;
  local_33 = 0xbf;
  local_32 = 0xfd;
  local_31 = 0xf0;
  local_30 = 0xfd;
  local_2f = 0xa6;
  local_2e = 0xfd;
  local_2d = 0xf5;
  local_2c = 0xf5;
  local_2b = 0xa0;
  local_2a = 0xf3;
  local_29 = 0xa7;
  local_28 = 0xa2;
  local_27 = 0xf4;
  local_26 = 0xf0;
  local_25 = 0xf7;
  local_24 = 0xfd;
  local_23 = 0xa0;
  local_22 = 0xa5;
  local_21 = 0xf4;
  local_20 = 0xf5;
  local_1f = 0xf0;
  local_1e = 0xa6;
  local_1d = 0xa6;
  local_1c = 0xfc;
  local_1b = 0xfd;
  local_1a = 0xf3;
  local_19 = 0xa0;
  local_18 = 0xf2;
  local_17 = 0xfc;
  local_16 = 0xa7;
  local_15 = 0xa6;
  local_14 = 0xf0;
  local_13 = 0xf1;
  local_12 = 0xb9;
"""

vals = vals.split("\n")
for i in range(len(vals)):
    vals[i] = vals[i][-3:-1]
vals = "".join(vals)
xorchain = "c4" * (len(vals)//2)
print(xorchain)
print(vals, len(vals))
flag = hex(int(xorchain,16) ^ int(vals,16))[2:]
print(flag)
flag = binascii.unhexlify(flag)
print(flag)