#!/usr/bin/env python3
"""Przydział pinów STM32G474VET3 (LQFP100) — sprawdzenie jednoczesnej dostępności funkcji (O-028).

Dane pinów: repozytorium producenta https://github.com/STMicroelectronics/STM32_open_pin_data
(plik mcu/STM32G474V(B-C-E)Tx.xml — baza narzędzia CubeMX).
Użycie: python3 scripts/piny_mcu.py <ścieżka do STM32G474V(B-C-E)Tx.xml>
Ograniczenia: zapłon i oba wtryskiwacze na różnych jednostkach czasowych HRTIM; PB8-BOOT0 i NRST nieużywane.
"""
import json,re,sys
import xml.etree.ElementTree as ET
_r=ET.parse(sys.argv[1]).getroot(); _ns=_r.tag.split('}')[0]+'}'
pins={p.get('Name'):(p.get('Position'),[x.get('Name') for x in p.findall(_ns+'Signal')]) for p in _r.findall(_ns+'Pin') if p.get('Type') in ('I/O','MonoIO')}
EXCL={'PB8-BOOT0','PG10-NRST'}|{n for n,(pos,s) in pins.items() if 'GPIO' not in s}
def cand(pat):
    return [n for n,(pos,s) in pins.items() if n not in EXCL and any(re.fullmatch(pat,x) for x in s)]
adc=lambda: cand(r'ADC\d_IN\d+')
# (name, candidates, group)
S=[]
def add(name,pat=None,pins_=None,grp=''):
    S.append((name, pins_ if pins_ else cand(pat), grp))
add('SWDIO',pins_=['PA13'],grp='system'); add('SWCLK',pins_=['PA14'],grp='system')
add('HSE_IN',pins_=['PF0-OSC_IN'],grp='system'); add('HSE_OUT',pins_=['PF1-OSC_OUT'],grp='system')
add('LSE_IN',pins_=['PC14-OSC32_IN'],grp='system'); add('LSE_OUT',pins_=['PC15-OSC32_OUT'],grp='system')
add('USB_DM',pins_=['PA11'],grp='system'); add('USB_DP',pins_=['PA12'],grp='system')
add('CAN_RX',r'FDCAN1_RX',grp='CAN'); add('CAN_TX',r'FDCAN1_TX',grp='CAN')
add('IGN_OUT',r'HRTIM1_CH[A-F][12]',grp='zapłon')
add('INJ1_IN',r'HRTIM1_CH[A-F][12]',grp='wtrysk B/C'); add('INJ2_IN',r'HRTIM1_CH[A-F][12]',grp='wtrysk B/C')
add('CRANK_EEV',r'HRTIM1_EEV(6|7|8|9|10)',grp='zapłon')
add('SCR_CAPTURE_EEV',r'HRTIM1_EEV\d+',grp='zapłon')
add('CAM_EEV',r'HRTIM1_EEV\d+|TIM(2|3|4|5|8|15|20)_CH\d',grp='rezerwa 4T')
add('WHEEL_CAP',r'TIM(2|3|4|5|15|16|17|20)_CH\d',grp='czujniki')
for b,g in [('SPI1','pamięć'),('SPI2','czujniki'),('SPI3','PMIC')]:
    for f in ['SCK','MISO','MOSI']: add(f'{b}_{f}',rf'{b}_{f}',grp=g)
for a in ['ADC_EXCITER','ADC_CAP','ADC_KILL','ADC_IS1','ADC_IS2','ADC_IS3','ADC_COOLANT','ADC_AIR','ADC_GEAR','ADC_TPS','ADC_O060','ADC_VBAT','ADC_VDD5','ADC_VSOUT1','ADC_NTC1','ADC_NTC2','ADC_PMIC_DIAG']:
    S.append((a,adc(),'ADC'))
gpio=['CS_FLASH','CS_AIS2IH','CS_KP464','CS_TLE9104','CS_PMIC','AIS2IH_INT','PMIC_WDI','PMIC_ENDRV_RB','COMP_RB','THR_RB','START_IN','TJA_STB','TJA_EN','TJA_ERRN','PROF_IN1','PROF_IN2','PROF_IN3','PROF_IN4','PROF_IN5','PROF_IN6','PROF_DEN1','PROF_DEN2','PROF_DEN3','PROF_DSEL','TLE_EN_REQ','WHEEL_PU','HMI_PWR_OFF']
order=sorted(range(len(S)),key=lambda i:len(S[i][1]))
used={}; res={}; units={}; HR={'IGN_OUT','INJ1_IN','INJ2_IN'}
def bt(k):
    if k==len(order): return True
    i=order[k]; name,c,g=S[i]
    # prefer pins with fewest special capabilities (keep scarce pins free)
    for p in sorted(c,key=lambda n:len(pins[n][1])):
        if p in used: continue
        if name in HR:
            u=[x[9] for x in pins[p][1] if re.fullmatch(r'HRTIM1_CH[A-F][12]',x)][0]
            if u in units.values(): continue
            units[name]=u
        used[p]=name; res[name]=p
        if bt(k+1): return True
        del used[p]; del res[name]
        units.pop(name,None)
    return False
ok=bt(0)
print('constrained OK' if ok else 'FAIL', 'HRTIM units:',units)
free=[n for n in pins if n not in used and n not in EXCL]
# prefer plain pins for gpio; avoid PC13 for outputs
outs={'CS_FLASH','CS_AIS2IH','CS_KP464','CS_TLE9104','CS_PMIC','PMIC_WDI','TJA_STB','TJA_EN','PROF_IN1','PROF_IN2','PROF_IN3','PROF_IN4','PROF_IN5','PROF_IN6','PROF_DEN1','PROF_DEN2','PROF_DEN3','PROF_DSEL','TLE_EN_REQ','WHEEL_PU','HMI_PWR_OFF'}
free_sorted=sorted(free,key=lambda n:(n=='PC13',len(pins[n][1])))
g_assign={}
for g in gpio:
    for p in free_sorted:
        if p in used: continue
        if g in outs and p=='PC13': continue
        used[p]=g; g_assign[g]=p; break
    else: print('NO PIN for',g)
tot=len(S)+len(gpio)
left=[n for n in pins if n not in used and n not in EXCL]
print('signals',tot,'I/O total',len(pins),'excluded',len(EXCL),'spare',len(left))
for n,_,g in S: print(f'{n:16s} {res.get(n)}  [{g}]')
for g in gpio: print(f'{g:16s} {g_assign.get(g)}  [GPIO]')
print('spare:',left)
