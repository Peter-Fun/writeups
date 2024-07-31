differences = [0.083,0.073,0.086,0.085,0.083,0.067,0.071,0.123,0.084,0.049,0.109,0.049,0.110,0.057,0.095,0.049,0.053,0.095,0.051,0.118,0.051,0.114,0.121,0.116,0.104,0.049,0.110,0.057,0.125]
differences = [int(i * 1000) for i in differences] 
print(differences)
print("".join(chr(i) for i in differences))