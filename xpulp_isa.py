import pandas as pd
#ISA = pd.read_excel('XpulpNN_SPECS.xlsx')
ISA = pd.read_csv('XpulpNN_SPECS_msdos.csv')
final_hex = []
for index, row in ISA.iterrows():
    hex = ''
    for i in range(len(row['HEX.2'])):
        # Now let rd = x7, rs1 = x8 and rs2 = x9:
        if i == 4:
            hex = hex + '9'
        elif i == 5:
            hex = hex + '4'
        elif i == 7:
            hex = hex + '7'
        else:  
            if row['HEX.1'][i] == '0':
                hex = hex + row['HEX.2'][i]
            elif i == 3:
                if row['HEX.2'][i] == '0':
                    hex = hex + row['HEX.1'][i]
                else:
                    hex = hex + 'A' # Because (assuming rs2 = 00) that means that, since row['HEX.2'][i] != '0', there is 2 contribution from it from instr[25] bit. If row['HEX.1'][i] != '0', there is 8 contribution from it from instr[27] bit (F bit, which is instr[26]
                                             # bit, is always 0). 8+2=A
            else:
                hex = hex + row['HEX.1'][i]
    final_hex.append(hex)
ISA['HEX_FINAL'] = final_hex
ISA.to_csv ('XpulpNN_TEST.csv', index = False, header=True)
# Preparing a test program for each single instruction
prog_first_part = '@00000000\n6F 00 40 27\n@00000180\n17 03 00 00\n67 00 83 00 \n13 04 a0 00 \n93 04 c0 00 \nb7 27 d3 75 \n93 87 67 1f \n63 c8 07 00 \n13 07 30 01 \n63 44 94 00 \n93 06 f0 00\n'
prog_last_part = '13 08 20 17\n23 20 78 00\n13 05 a0 00\n37 09 00 20\nb7 d9 5b 07\n93 89 59 d1\n23 20 39 01'
for index, row in ISA.iterrows():
    file_name = row['mnemonic'].split(' ')[0] + '.hex'
    with open(file_name, 'w') as f:
        f.write("%s%s %s %s %s\n%s" % (prog_first_part, row['HEX_FINAL'][8:10], row['HEX_FINAL'][6:8], row['HEX_FINAL'][4:6], row['HEX_FINAL'][2:4], prog_last_part))
# Newest Version ISA & TPs:
ISA_new = pd.read_csv('XpulpNN_sheet2.csv')
print(ISA_new)
make_add2 = ''
for index, row in ISA_new.iterrows():
    prefix2 = row['Mnemonic']
    file_name2 = prefix2 + '.hex'
    phony2 = prefix2 + '-vsim-run-gui'
    with open(file_name2, 'w') as f3:
        f3.write("%s%s %s %s %s\n%s" % (prog_first_part, row['HEX_FINAL'][8:10], row['HEX_FINAL'][6:8], row['HEX_FINAL'][4:6], row['HEX_FINAL'][2:4], prog_last_part))
    make_add2 = make_add2 + "\n.PHONY: %s\n%s: vsim-all xpulp_tests/%s\n%s: ALL_VSIM_FLAGS += \"+firmware=xpulp_tests/%s\"\n%s: vsim-run-gui\n" % (phony2, phony2, file_name2, phony2, file_name2, phony2)
with open('make_add2.txt', 'w') as f4:
    f4.write(make_add2)
