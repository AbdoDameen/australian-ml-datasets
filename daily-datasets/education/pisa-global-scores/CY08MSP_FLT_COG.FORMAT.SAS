%let DataFile=CY08MSP_FLT_COG;
libname DataLib '.';

proc format;
     value ADMINMODEF
     	1  = "Paper"
     	2  = "Computer"
     ;
     value BOOKIDF
     	1  = "Form 1"
     	2  = "Form 2"
     	3  = "Form 3"
     	4  = "Form 4"
     	5  = "Form 5"
     	6  = "Form 6"
     	7  = "Form 7"
     	8  = "Form 8"
     	9  = "Form 9"
     	10  = "Form 10"
     	11  = "Form 11"
     	12  = "Form 12"
     	13  = "Form 13"
     	14  = "Form 14"
     	15  = "Form 15"
     	16  = "Form 16"
     	17  = "Form 17"
     	18  = "Form 18"
     	19  = "Form 19"
     	20  = "Form 20"
     	21  = "Form 21"
     	22  = "Form 22"
     	23  = "Form 23"
     	24  = "Form 24"
     	25  = "Form 25"
     	26  = "Form 26"
     	27  = "Form 27"
     	28  = "Form 28"
     	29  = "Form 29"
     	30  = "Form 30"
     	31  = "Form 31"
     	32  = "Form 32"
     	33  = "Form 33"
     	34  = "Form 34"
     	35  = "Form 35"
     	36  = "Form 36"
     	37  = "Form 37"
     	38  = "Form 38"
     	39  = "Form 39"
     	40  = "Form 40"
     	41  = "Form 41"
     	42  = "Form 42"
     	43  = "Form 43"
     	44  = "Form 44"
     	45  = "Form 45"
     	46  = "Form 46"
     	47  = "Form 47"
     	48  = "Form 48"
     	49  = "Form 49"
     	50  = "Form 50"
     	51  = "Form 51"
     	52  = "Form 52"
     	53  = "Form 53"
     	54  = "Form 54"
     	55  = "Form 55"
     	56  = "Form 56"
     	57  = "Form 57"
     	58  = "Form 58"
     	59  = "Form 59"
     	60  = "Form 60"
     	61  = "Form 61"
     	62  = "Form 62"
     	63  = "Form 63"
     	64  = "Form 64"
     	65  = "Form 65"
     	66  = "Form 66"
     	67  = "Form 67"
     	68  = "Form 68"
     	69  = "Form 69"
     	70  = "Form 70"
     	71  = "Form 71"
     	72  = "Form 72"
     	73  = "Form 73"
     	74  = "Form 74"
     	99  = "UH Form"
     	201  = "PBA Trend Booklet 1"
     	202  = "PBA Trend Booklet 2"
     	203  = "PBA Trend Booklet 3"
     	204  = "PBA Trend Booklet 4"
     	205  = "PBA Trend Booklet 5"
     	206  = "PBA Trend Booklet 6"
     	207  = "PBA Trend Booklet 7"
     	208  = "PBA Trend Booklet 8"
     	209  = "PBA Trend Booklet 9"
     	210  = "PBA Trend Booklet 10"
     	211  = "PBA Trend Booklet 11"
     	212  = "PBA Trend Booklet 12"
     	213  = "PBA Trend Booklet 13"
     	214  = "PBA Trend Booklet 14"
     	215  = "PBA Trend Booklet 15"
     	216  = "PBA Trend Booklet 16"
     	217  = "PBA Trend Booklet 17"
     	218  = "PBA Trend Booklet 18"
     	301  = "PBA New Booklet 1"
     	302  = "PBA New Booklet 2"
     	303  = "PBA New Booklet 3"
     	304  = "PBA New Booklet 4"
     	305  = "PBA New Booklet 5"
     	306  = "PBA New Booklet 6"
     	307  = "PBA New Booklet 7"
     	308  = "PBA New Booklet 8"
     	309  = "PBA New Booklet 9"
     	310  = "PBA New Booklet 10"
     	311  = "PBA New Booklet 11"
     	312  = "PBA New Booklet 12"
     ;
     value CF303Q01WF
     	0  = "Incorrect"
     	1  = "Correct"
     ;
     value CMA112Q02WDF
     	.  = "Missing"
     	9996  = "Not Reached"
     	.R  = "Not Reached"
     	9997  = "Not Applicable"
     	.N  = "Not Applicable"
     	9998  = "Invalid"
     	.I  = "Invalid"
     	9999  = "No Response"
     	.M  = "No Response"
     ;
     value CMA116Q02SF
     	0  = "00 - No credit"
     	11  = "11 - Partial credit"
     	12  = "12 - Partial credit"
     	13  = "13 - Partial credit"
     	14  = "14 - Partial credit"
     	21  = "21 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value CMA125Q01SF
     	0  = "00 - No credit"
     	11  = "11 - Full credit"
     	12  = "12 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value CMA125Q02SF
     	0  = "00 - No credit"
     	11  = "11 - Partial credit"
     	12  = "12 - Partial credit"
     	21  = "21 - Full credit"
     	22  = "22 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value CMA129Q02SF
     	0  = "0 - No credit"
     	11  = "11 - Partial credit"
     	21  = "21 - Full credit"
     	22  = "22 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value CMA133Q02SF
     	0  = "00 - No credit"
     	11  = "11 - Partial credit"
     	12  = "12 - Partial credit"
     	13  = "13 - Partial credit"
     	21  = "21 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value CMA152Q02SF
     	0  = "00 - No credit"
     	11  = "11 - Partial credit"
     	12  = "12 - Partial credit"
     	21  = "21 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value CMA157Q01SF
     	0  = "00 - No credit"
     	11  = "11 - Partial credit"
     	21  = "21 - Full credit"
     	22  = "22 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value $ CNTF
     	'ALB'  = "Albania"
     	'ARE'  = "United Arab Emirates"
     	'ARG'  = "Argentina"
     	'AUS'  = "Australia"
     	'AUT'  = "Austria"
     	'BEL'  = "Belgium"
     	'BGR'  = "Bulgaria"
     	'BRA'  = "Brazil"
     	'BRN'  = "Brunei Darussalam"
     	'CAN'  = "Canada"
     	'CHE'  = "Switzerland"
     	'CHL'  = "Chile"
     	'COL'  = "Colombia"
     	'CRI'  = "Costa Rica"
     	'CZE'  = "Czech Republic"
     	'DEU'  = "Germany"
     	'DNK'  = "Denmark"
     	'DOM'  = "Dominican Republic"
     	'ESP'  = "Spain"
     	'EST'  = "Estonia"
     	'FIN'  = "Finland"
     	'FRA'  = "France"
     	'GBR'  = "United Kingdom"
     	'GEO'  = "Georgia"
     	'GRC'  = "Greece"
     	'GTM'  = "Guatemala"
     	'HKG'  = "Hong Kong (China)"
     	'HRV'  = "Croatia"
     	'HUN'  = "Hungary"
     	'IDN'  = "Indonesia"
     	'IRL'  = "Ireland"
     	'ISL'  = "Iceland"
     	'ISR'  = "Israel"
     	'ITA'  = "Italy"
     	'JAM'  = "Jamaica"
     	'JOR'  = "Jordan"
     	'JPN'  = "Japan"
     	'KAZ'  = "Kazakhstan"
     	'KHM'  = "Cambodia"
     	'KOR'  = "Korea"
     	'KSV'  = "Kosovo"
     	'LTU'  = "Lithuania"
     	'LVA'  = "Latvia"
     	'MAC'  = "Macao (China)"
     	'MAR'  = "Morocco"
     	'MDA'  = "Republic of Moldova"
     	'MEX'  = "Mexico"
     	'MKD'  = "North Macedonia"
     	'MLT'  = "Malta"
     	'MNE'  = "Montenegro"
     	'MNG'  = "Mongolia"
     	'MYS'  = "Malaysia"
     	'NLD'  = "Netherlands"
     	'NOR'  = "Norway"
     	'NZL'  = "New Zealand"
     	'PAN'  = "Panama"
     	'PER'  = "Peru"
     	'PHL'  = "Philippines"
     	'POL'  = "Poland"
     	'PRT'  = "Portugal"
     	'PRY'  = "Paraguay"
     	'PSE'  = "Palestinian Authority"
     	'QAT'  = "Qatar"
     	'QAZ'  = "Baku (Azerbaijan)"
     	'QCY'  = "Cyprus"
     	'QUR'  = "Ukrainian regions (18 of 27)"
     	'ROU'  = "Romania"
     	'SAU'  = "Saudi Arabia"
     	'SGP'  = "Singapore"
     	'SLV'  = "El Salvador"
     	'SRB'  = "Serbia"
     	'SVK'  = "Slovak Republic"
     	'SVN'  = "Slovenia"
     	'SWE'  = "Sweden"
     	'TAP'  = "Chinese Taipei"
     	'THA'  = "Thailand"
     	'TUR'  = "Türkiye"
     	'URY'  = "Uruguay"
     	'USA'  = "United States"
     	'UZB'  = "Uzbekistan"
     	'VNM'  = "Viet Nam"
     ;
     value CNTRYIDF
     	8  = "Albania"
     	31  = "Baku (Azerbaijan)"
     	32  = "Argentina"
     	36  = "Australia"
     	40  = "Austria"
     	56  = "Belgium"
     	76  = "Brazil"
     	96  = "Brunei Darussalam"
     	100  = "Bulgaria"
     	116  = "Cambodia"
     	124  = "Canada"
     	152  = "Chile"
     	158  = "Chinese Taipei"
     	170  = "Colombia"
     	188  = "Costa Rica"
     	191  = "Croatia"
     	196  = "Cyprus"
     	203  = "Czech Republic"
     	208  = "Denmark"
     	214  = "Dominican Republic"
     	222  = "El Salvador"
     	233  = "Estonia"
     	246  = "Finland"
     	250  = "France"
     	268  = "Georgia"
     	275  = "Palestinian Authority"
     	276  = "Germany"
     	300  = "Greece"
     	320  = "Guatemala"
     	344  = "Hong Kong (China)"
     	348  = "Hungary"
     	352  = "Iceland"
     	360  = "Indonesia"
     	372  = "Ireland"
     	376  = "Israel"
     	380  = "Italy"
     	383  = "Kosovo"
     	388  = "Jamaica"
     	392  = "Japan"
     	398  = "Kazakhstan"
     	400  = "Jordan"
     	410  = "Korea"
     	428  = "Latvia"
     	440  = "Lithuania"
     	446  = "Macao (China)"
     	458  = "Malaysia"
     	470  = "Malta"
     	484  = "Mexico"
     	496  = "Mongolia"
     	498  = "Republic of Moldova"
     	499  = "Montenegro"
     	504  = "Morocco"
     	528  = "Netherlands"
     	554  = "New Zealand"
     	578  = "Norway"
     	591  = "Panama"
     	600  = "Paraguay"
     	604  = "Peru"
     	608  = "Philippines"
     	616  = "Poland"
     	620  = "Portugal"
     	634  = "Qatar"
     	642  = "Romania"
     	682  = "Saudi Arabia"
     	688  = "Serbia"
     	702  = "Singapore"
     	703  = "Slovak Republic"
     	704  = "Viet Nam"
     	705  = "Slovenia"
     	724  = "Spain"
     	752  = "Sweden"
     	756  = "Switzerland"
     	764  = "Thailand"
     	784  = "United Arab Emirates"
     	792  = "Türkiye"
     	807  = "North Macedonia"
     	826  = "United Kingdom"
     	840  = "United States"
     	858  = "Uruguay"
     	860  = "Uzbekistan"
     	901  = "Ukrainian regions (18 of 27)"
     ;
     value CR561Q06SF
     	0  = "0 - No credit"
     	11  = "11 - Partial credit"
     	12  = "12 - Partial credit"
     	13  = "13 - Partial credit"
     	21  = "21 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value CR570Q04SDF
     	0  = "Incorrect"
     	1  = "Correct"
     	.  = "Missing"
     	6  = "Not Reached"
     	.R  = "Not Reached"
     	7  = "Not Applicable"
     	.N  = "Not Applicable"
     	8  = "Invalid"
     	.I  = "Invalid"
     	9  = "No Response"
     	.M  = "No Response"
     ;
     value CR570Q10VSF
     	.  = "Missing"
     	9996  = "Not Reached"
     	.R  = "Not Reached"
     	9997  = "Not Applicable"
     	.N  = "Not Applicable"
     	9998  = "Invalid"
     	.I  = "Invalid"
     	9999  = "No Response"
     	.M  = "No Response"
     ;
     value CR590Q66SF
     	0  = "0 - No credit"
     	1  = "1 - Full credit"
     	.  = "Missing"
     	6  = "Not Reached"
     	.R  = "Not Reached"
     	7  = "Not Applicable"
     	.N  = "Not Applicable"
     	8  = "Invalid"
     	.I  = "Invalid"
     	9  = "No Response"
     	.M  = "No Response"
     ;
     value CR590Q66TTF
     	.  = "Missing"
     	99999996  = "Not Reached"
     	.R  = "Not Reached"
     	99999997  = "Not Applicable"
     	.N  = "Not Applicable"
     	99999998  = "Invalid"
     	.I  = "Invalid"
     	99999999  = "No Response"
     	.M  = "No Response"
     ;
     value DF024Q02CF
     	0  = "00 - No credit"
     	11  = "11 - Full credit"
     	12  = "12 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DF201Q01CF
     	0  = "00 - No credit"
     	11  = "11 - Full credit"
     	12  = "12 - Full credit"
     	13  = "13 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DM155Q02CF
     	0  = "00 - No credit"
     	11  = "11 - Partial credit"
     	12  = "12 - Partial credit"
     	13  = "13 - Partial credit"
     	21  = "21 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DM192Q01RCF
     	1  = "A"
     	2  = "B"
     	3  = "C"
     	4  = "D"
     	5  = "E"
     	6  = "F"
     	7  = "G"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DM462Q01CF
     	1  = "01 - No credit"
     	2  = "02 - No credit"
     	11  = "11 - Partial credit"
     	12  = "12 - Partial credit"
     	21  = "21 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DM474Q01RF
     	1  = "A"
     	2  = "B"
     	3  = "C"
     	4  = "D"
     	5  = "E"
     	6  = "F"
     	7  = "G"
     	8  = "H"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DM906Q01RF
     	1  = "A"
     	2  = "B"
     	3  = "C"
     	4  = "D"
     	5  = "E"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DM936Q02CF
     	0  = "0 - No credit"
     	1  = "1 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DM949Q03CF
     	0  = "0 - No credit"
     	1  = "1 - Partial credit"
     	2  = "2 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DM953Q04CF
     	0  = "00 - No credit"
     	11  = "11 - Partial credit"
     	12  = "12 - Partial credit"
     	21  = "21 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DM998Q02CF
     	0  = "0 - No credit"
     	1  = "1 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DMA103Q05RAF
     	1  = "Equal To"
     	2  = "Greater Than"
     	3  = "Less Than"
     	4  = "Greater Than or Equal To"
     	5  = "Less Than or Equal To"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DMA119Q03CF
     	0  = "0 - No credit"
     	1  = "1 - Partial credit"
     	2  = "2 - Full credit"
     	.  = "Missing"
     	6  = "Not Reached"
     	.R  = "Not Reached"
     	7  = "Not Applicable"
     	.N  = "Not Applicable"
     	8  = "Invalid"
     	.I  = "Invalid"
     	9  = "No Response"
     	.M  = "No Response"
     ;
     value DMA128Q03RCF
     	1  = "True"
     	2  = "False"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DMA136Q02CF
     	0  = "00 - No credit"
     	11  = "11 - Partial credit"
     	21  = "21 - Full credit"
     	22  = "22 - Full credit"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DMA146Q03CF
     	0  = "0 - No credit"
     	1  = "1 - Partial credit"
     	2  = "2 - Full credit"
     	.  = "Missing"
     	6  = "Not Reached"
     	.R  = "Not Reached"
     	7  = "Not Applicable"
     	.N  = "Not Applicable"
     	8  = "Invalid"
     	.I  = "Invalid"
     	9  = "No Response"
     	.M  = "No Response"
     ;
     value DMA152Q02RAF
     	0  = "No Selection Made"
     	1  = "Less Than"
     	2  = "Less Than or Equal To"
     	3  = "Equal To"
     	4  = "Greater Than or Equal To"
     	5  = "Greater Than"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DMA161Q04CF
     	0  = "0 - No credit"
     	1  = "1 - Full credit"
     	2  = "2 - Full credit"
     	.  = "Missing"
     	6  = "Not Reached"
     	.R  = "Not Reached"
     	7  = "Not Applicable"
     	.N  = "Not Applicable"
     	8  = "Invalid"
     	.I  = "Invalid"
     	9  = "No Response"
     	.M  = "No Response"
     ;
     value DMA162Q02RCF
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DR055Q03CF
     	0  = "0 - No credit"
     	1  = "1 - No credit"
     	2  = "2 - Full credit"
     	.  = "Missing"
     	6  = "Not Reached"
     	.R  = "Not Reached"
     	7  = "Not Applicable"
     	.N  = "Not Applicable"
     	8  = "Invalid"
     	.I  = "Invalid"
     	9  = "No Response"
     	.M  = "No Response"
     ;
     value DR466Q02CF
     	0  = "0 - No credit"
     	1  = "1 - Full credit"
     	.  = "Missing"
     	6  = "Not Reached"
     	.R  = "Not Reached"
     	7  = "Not Applicable"
     	.N  = "Not Applicable"
     	8  = "Invalid"
     	.I  = "Invalid"
     	9  = "No Response"
     	.M  = "No Response"
     ;
     value DR556Q12RDF
     	1  = "A"
     	2  = "B"
     	3  = "C"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DR562Q06CF
     	0  = "0 - No credit"
     	1  = "1 - Partial credit"
     	2  = "2 - Full credit"
     	.  = "Missing"
     	6  = "Not Reached"
     	.R  = "Not Reached"
     	7  = "Not Applicable"
     	.N  = "Not Applicable"
     	8  = "Invalid"
     	.I  = "Invalid"
     	9  = "No Response"
     	.M  = "No Response"
     ;
     value DR566Q09REF
     	1  = "Checked"
     	2  = "Not Checked"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DR570Q04RDF
     	1  = "A"
     	2  = "B"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DR570Q08RF
     	1  = "A"
     	2  = "B"
     	3  = "C"
     	4  = "D"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value DR570Q10CF
     	0  = "0 - No credit"
     	1  = "1 - Full credit"
     	.  = "Missing"
     	6  = "Not Reached"
     	.R  = "Not Reached"
     	7  = "Not Applicable"
     	.N  = "Not Applicable"
     	8  = "Invalid"
     	.I  = "Invalid"
     	9  = "No Response"
     	.M  = "No Response"
     ;
     value DR590Q66RF
     	1  = "Yes"
     	2  = "No"
     	.  = "Missing"
     	96  = "Not Reached"
     	.R  = "Not Reached"
     	97  = "Not Applicable"
     	.N  = "Not Applicable"
     	98  = "Invalid"
     	.I  = "Invalid"
     	99  = "No Response"
     	.M  = "No Response"
     ;
     value LANGTEST_COGF
     	113  = "Indonesian"
     	118  = "Romanian"
     	121  = "Estonian"
     	130  = "Georgian"
     	140  = "Albanian"
     	141  = "Bokmal"
     	148  = "German"
     	149  = "Maltese"
     	156  = "Spanish"
     	160  = "Catalan"
     	170  = "Slovak"
     	192  = "Bosnian"
     	200  = "Italian"
     	202  = "Mongolian"
     	204  = "Malay"
     	232  = "Portuguese"
     	244  = "Czech"
     	264  = "Danish"
     	265  = "Faroese"
     	266  = "Croatian"
     	273  = "Polish"
     	275  = "Kazakh"
     	286  = "Japanese"
     	301  = "Korean"
     	313  = "English"
     	316  = "Chinese"
     	317  = "Serbian"
     	322  = "Dutch"
     	325  = "Latvian"
     	329  = "Vietnamese"
     	344  = "Turkish"
     	351  = "Bulgarian"
     	363  = "Kyrgyz"
     	369  = "Azerbaijani"
     	375  = "Lithuanian"
     	379  = "Welsh"
     	415  = "Hindi"
     	420  = "Finnish"
     	422  = "Hebrew"
     	428  = "Belarusian"
     	434  = "Irish"
     	442  = "Slovenian"
     	449  = "Greek"
     	451  = "Basque"
     	467  = "Icelandic"
     	471  = "Uzbek"
     	472  = "Karakalpak"
     	474  = "Galician"
     	492  = "Macedonian"
     	493  = "French"
     	494  = "Swedish"
     	495  = "Russian"
     	496  = "Hungarian"
     	500  = "Arabic"
     	507  = "Luxembourgish"
     	513  = "Nynorsk"
     	514  = "Ukranian"
     	520  = "Khmer"
     	547  = "Armenian"
     	555  = "Thai"
     	608  = "Valencian"
     	622  = "Montenegrin"
     	632  = "Chinese (Taiwan dialect)"
     	803  = "Azeri"
     	915  = "Hindi/English"
     	922  = "Hebrew (Ultra Orthodox)"
     	979  = "Welsh-M,R, English-S"
     	991  = "Arabic-R, English-M,S"
     	993  = "English schools in Panama"
     	994  = "Slovenian ISCED2"
     	998  = "Invalid"
     ;
     value MPATHF
     	0  = "Not used"
     	1  = "Linear"
     	2  = "Adaptive"
     ;
     value MS1_LEVF
     	0  = "Not used"
     	1  = "Low"
     	2  = "High"
     	3  = "Linear"
     ;
     value MS2_ItemSetF
     	0  = "Not used"
     	1  = "A"
     	2  = "B"
     	3  = "C"
     ;
     value MS2_LEVF
     	0  = "Not used"
     	1  = "Low"
     	2  = "Medium"
     	3  = "High"
     	4  = "Linear"
     ;
     value MS2_TESTF
     	0  = "Not used"
     	1  = "Testlet 1"
     	2  = "Testlet 2"
     	3  = "Testlet 3"
     	4  = "Testlet 4"
     	5  = "Testlet 5"
     	6  = "Testlet 6"
     	7  = "Testlet 7"
     	8  = "Testlet 8"
     	9  = "Testlet 9"
     	10  = "Testlet 10"
     	11  = "Testlet 11"
     	12  = "Testlet 12"
     	13  = "Testlet 13"
     	14  = "Testlet 14"
     	15  = "Testlet 15"
     	16  = "Testlet 16"
     ;
     value $ NatCenF
     	'000800'  = "Albania"
     	'003100'  = "Baku (Azerbaijan)"
     	'003200'  = "Argentina"
     	'003600'  = "Australia"
     	'004000'  = "Austria"
     	'005601'  = "Belgium: Flemish"
     	'005602'  = "Belgium: French"
     	'007600'  = "Brazil"
     	'009600'  = "Brunei Darussalam"
     	'010000'  = "Bulgaria"
     	'011600'  = "Cambodia"
     	'012400'  = "Canada"
     	'015200'  = "Chile"
     	'015800'  = "Chinese Taipei"
     	'017000'  = "Colombia"
     	'018800'  = "Costa Rica"
     	'019100'  = "Croatia"
     	'019600'  = "Cyprus"
     	'020300'  = "Czech Republic"
     	'020800'  = "Denmark"
     	'021400'  = "Dominican Republic"
     	'022200'  = "El Salvador"
     	'023300'  = "Estonia"
     	'024600'  = "Finland"
     	'025000'  = "France"
     	'026800'  = "Georgia"
     	'027500'  = "Palestinian Authority"
     	'027600'  = "Germany"
     	'030000'  = "Greece"
     	'032000'  = "Guatemala"
     	'034400'  = "Hong Kong"
     	'034800'  = "Hungary"
     	'035200'  = "Iceland"
     	'036000'  = "Indonesia"
     	'037200'  = "Ireland"
     	'037600'  = "Israel"
     	'038000'  = "Italy"
     	'038300'  = "Kosovo"
     	'038800'  = "Jamaica"
     	'039200'  = "Japan"
     	'039800'  = "Kazakhstan"
     	'040000'  = "Jordan"
     	'041000'  = "Korea"
     	'042800'  = "Latvia"
     	'044000'  = "Lithuania"
     	'044600'  = "Macao"
     	'045800'  = "Malaysia"
     	'047000'  = "Malta"
     	'048400'  = "Mexico"
     	'049600'  = "Mongolia"
     	'049800'  = "Moldova"
     	'049900'  = "Montenegro"
     	'050400'  = "Morocco"
     	'052800'  = "Netherlands"
     	'055400'  = "New Zealand"
     	'057800'  = "Norway"
     	'059100'  = "Panama"
     	'060000'  = "Paraguay"
     	'060400'  = "Peru"
     	'060800'  = "Philippines"
     	'061600'  = "Poland"
     	'062000'  = "Portugal"
     	'063400'  = "Qatar"
     	'064200'  = "Romania"
     	'068200'  = "Saudi Arabia"
     	'068800'  = "Serbia"
     	'070200'  = "Singapore"
     	'070300'  = "Slovak Republic"
     	'070400'  = "Vietnam"
     	'070500'  = "Slovenia"
     	'072400'  = "Spain"
     	'075200'  = "Sweden"
     	'075600'  = "Switzerland"
     	'076400'  = "Thailand"
     	'078401'  = "United Arab Emirates: excl. private schools in Abu Dhabi and Dubai"
     	'078402'  = "United Arab Emirates: Abu Dhabi private schools"
     	'078403'  = "United Arab Emirates: Dubai private schools"
     	'079200'  = "Türkiye"
     	'080400'  = "Ukraine"
     	'080700'  = "North Macedonia"
     	'082700'  = "United Kingdom: excl. Scotland"
     	'082800'  = "United Kingdom: Scotland"
     	'084000'  = "United States"
     	'085800'  = "Uruguay"
     	'086000'  = "Uzbekistan"
     ;
     value Option_UHF
     	0  = "No"
     	1  = "Yes"
     ;
     value RCORE_PERFF
     	0  = "Not used"
     	1  = "Low Level"
     	2  = "Medium Level"
     	3  = "High Level"
     ;
     value RCORE_TESTF
     	0  = "Not used"
     	1  = "Testlet 1"
     	2  = "Testlet 2"
     	3  = "Testlet 3"
     	4  = "Testlet 4"
     	5  = "Testlet 5"
     	6  = "Testlet 6"
     ;
     value RDESIGNF
     	0  = "Not used"
     	1  = "Design A (Stage1 then Stage2)"
     	2  = "Design B (Stage2 then Stage1)"
     ;
     value REGIONF
     	800  = "Albania"
     	3100  = "Baku (Azerbaijan)"
     	3200  = "Argentina"
     	3600  = "Australia"
     	4000  = "Austria"
     	5600  = "Belgium: Rest of the country"
     	5601  = "Belgium: Flemish community"
     	5602  = "Belgium: French community"
     	5603  = "Belgium: German community"
     	7600  = "Brazil: Rest of the country"
     	7601  = "Brazil: North"
     	7602  = "Brazil: Northeast"
     	7603  = "Brazil: South"
     	7604  = "Brazil: Southeast"
     	7605  = "Brazil: Middle-West"
     	9600  = "Brunei Darussalam"
     	10000  = "Bulgaria"
     	11600  = "Cambodia"
     	12400  = "Canada: Rest of the country"
     	12401  = "Canada: Newfoundland and Labrador"
     	12402  = "Canada: Prince Edward Island"
     	12403  = "Canada: Nova Scotia"
     	12404  = "Canada: New Brunswick"
     	12405  = "Canada: Quebec"
     	12406  = "Canada: Ontario"
     	12407  = "Canada: Manitoba"
     	12408  = "Canada: Saskatchewan"
     	12409  = "Canada: Alberta"
     	12410  = "Canada: British Columbia"
     	15200  = "Chile"
     	15800  = "Chinese Taipei"
     	17000  = "Colombia: Rest of the country"
     	17001  = "Colombia: Bogota"
     	18800  = "Costa Rica"
     	19100  = "Croatia"
     	19600  = "Cyprus"
     	20300  = "Czech Republic"
     	20800  = "Denmark"
     	21400  = "Dominican Republic"
     	22200  = "El Salvador"
     	23300  = "Estonia"
     	24600  = "Finland"
     	25000  = "France"
     	26800  = "Georgia"
     	27500  = "Palestinian Authority"
     	27600  = "Germany"
     	30000  = "Greece"
     	32000  = "Guatemala"
     	34400  = "Hong Kong (China)"
     	34800  = "Hungary"
     	35200  = "Iceland"
     	36000  = "Indonesia"
     	37200  = "Ireland"
     	37600  = "Israel"
     	38000  = "Italy"
     	38300  = "Kosovo"
     	38800  = "Jamaica"
     	39200  = "Japan"
     	39800  = "Kazakhstan: Rest of the country"
     	39801  = "Kazakhstan: Astana"
     	39802  = "Kazakhstan: Almaty"
     	39803  = "Kazakhstan: Akmola region"
     	39804  = "Kazakhstan: Aktobe region"
     	39805  = "Kazakhstan: Almaty region"
     	39806  = "Kazakhstan: Atyrau region"
     	39807  = "Kazakhstan: West-Kazakhstan region"
     	39808  = "Kazakhstan: Zhambyl region"
     	39809  = "Kazakhstan: Karagandy region"
     	39810  = "Kazakhstan: Kostanay region"
     	39811  = "Kazakhstan: Kyzyl-Orda region"
     	39812  = "Kazakhstan: Mangistau region"
     	39813  = "Kazakhstan: Turkestan region"
     	39814  = "Kazakhstan: Pavlodar region"
     	39815  = "Kazakhstan: North-Kazakhstan region"
     	39816  = "Kazakhstan: East-Kazakhstan region"
     	39817  = "Kazakhstan: Shymkent"
     	40000  = "Jordan"
     	41000  = "Korea"
     	42800  = "Latvia"
     	44000  = "Lithuania"
     	44600  = "Macao (China)"
     	45800  = "Malaysia"
     	47000  = "Malta"
     	48400  = "Mexico"
     	49600  = "Mongolia: Rest of the country"
     	49601  = "Mongolia: Central"
     	49602  = "Mongolia: Khangai"
     	49603  = "Mongolia: Western"
     	49800  = "Republic of Moldova"
     	49900  = "Montenegro"
     	50400  = "Morocco"
     	52800  = "Netherlands"
     	55400  = "New Zealand"
     	57800  = "Norway"
     	59100  = "Panama"
     	60000  = "Paraguay"
     	60400  = "Peru"
     	60800  = "Philippines"
     	61600  = "Poland"
     	62000  = "Portugal"
     	63400  = "Qatar"
     	64200  = "Romania"
     	68200  = "Saudi Arabia"
     	68800  = "Serbia"
     	70200  = "Singapore"
     	70300  = "Slovak Republic"
     	70400  = "Viet Nam: Rest of the country"
     	70401  = "Viet Nam: Northern Vietnam"
     	70402  = "Viet Nam: Central Vietnam"
     	70403  = "Viet Nam: Southern Vietnam"
     	70500  = "Slovenia"
     	72400  = "Spain: Rest of the country"
     	72401  = "Spain: Andalusia"
     	72402  = "Spain: Aragon"
     	72403  = "Spain: Asturias"
     	72404  = "Spain: Balearic Islands"
     	72405  = "Spain: Canary Islands"
     	72406  = "Spain: Cantabria"
     	72407  = "Spain: Castile and Leon"
     	72408  = "Spain: Castile-La Mancha"
     	72409  = "Spain: Catalonia"
     	72410  = "Spain: Extremadura"
     	72411  = "Spain: Galicia"
     	72412  = "Spain: La Rioja"
     	72413  = "Spain: Madrid"
     	72414  = "Spain: Murcia"
     	72415  = "Spain: Navarre"
     	72416  = "Spain: Basque Country"
     	72417  = "Spain: Comunidad Valenciana"
     	72418  = "Spain: Ceuta"
     	72419  = "Spain: Melilla"
     	75200  = "Sweden"
     	75600  = "Switzerland"
     	76400  = "Thailand"
     	78400  = "United Arab Emirates"
     	79200  = "Türkiye"
     	80700  = "North Macedonia"
     	82611  = "Great Britain: England"
     	82612  = "Great Britain: Northern Ireland"
     	82613  = "Great Britain: Wales"
     	82620  = "Great Britain: Scotland"
     	84000  = "United States"
     	85800  = "Uruguay"
     	86000  = "Uzbekistan"
     	90100  = "Ukraine"
     ;
     value RS1_TESTF
     	0  = "Not used"
     	11  = "Testlet 11"
     	12  = "Testlet 12"
     	13  = "Testlet 13"
     	14  = "Testlet 14"
     	15  = "Testlet 15"
     	16  = "Testlet 16"
     ;
     value RS2_LEVF
     	0  = "Not used"
     	1  = "Low"
     	2  = "High"
     ;
     value RS2_TESTF
     	0  = "Not used"
     	21  = "Testlet 21"
     	22  = "Testlet 22"
     	23  = "Testlet 23"
     	24  = "Testlet 24"
     	25  = "Testlet 25"
     	26  = "Testlet 26"
     ;
     value $ STRATUMF
     	'ALB01'  = "ALB - stratum 01: Urban / North / Public"
     	'ALB02'  = "ALB - stratum 02: Urban / North / Private"
     	'ALB03'  = "ALB - stratum 03: Urban / Center / Public"
     	'ALB04'  = "ALB - stratum 04: Urban / Center / Private"
     	'ALB05'  = "ALB - stratum 05: Urban / South / Public"
     	'ALB06'  = "ALB - stratum 06: Urban / South / Private"
     	'ALB07'  = "ALB - stratum 07: Rural / North / Public and Private"
     	'ALB08'  = "ALB - stratum 08: Rural / Center / Public"
     	'ALB09'  = "ALB - stratum 09: Rural / Center / Private"
     	'ALB10'  = "ALB - stratum 10: Rural / South / Public"
     	'ALB11'  = "ALB - stratum 11: Rural / South / Private"
     	'ALB97'  = "Undisclosed STRATUM - Albania"
     	'ARE01'  = "ARE - stratum 01: Abu Dhabi,Public,MOE"
     	'ARE05'  = "ARE - stratum 05: Abu Dhabi,Public,Other"
     	'ARE06'  = "ARE - stratum 06: Abu Dhabi,Private,MOE"
     	'ARE07'  = "ARE - stratum 07: Abu Dhabi,Private,US"
     	'ARE08'  = "ARE - stratum 08: Abu Dhabi,Private,UK"
     	'ARE09'  = "ARE - stratum 09: Abu Dhabi,Private,Indian"
     	'ARE10'  = "ARE - stratum 10: Abu Dhabi,Private,Other"
     	'ARE11'  = "ARE - stratum 11: Dubai,Public,MOE"
     	'ARE15'  = "ARE - stratum 15: Dubai,Public,Other"
     	'ARE16'  = "ARE - stratum 16: Dubai,Private,MOE"
     	'ARE17'  = "ARE - stratum 17: Dubai,Private,US"
     	'ARE18'  = "ARE - stratum 18: Dubai,Private,UK"
     	'ARE19'  = "ARE - stratum 19: Dubai,Private,Indian"
     	'ARE20'  = "ARE - stratum 20: Dubai,Private,Other"
     	'ARE21'  = "ARE - stratum 21: Sharjah,Public,MOE"
     	'ARE25'  = "ARE - stratum 25: Sharjah,Public,Other"
     	'ARE26'  = "ARE - stratum 26: Sharjah,Private,MOE"
     	'ARE27'  = "ARE - stratum 27: Sharjah,Private,US"
     	'ARE28'  = "ARE - stratum 28: Sharjah,Private,UK"
     	'ARE29'  = "ARE - stratum 29: Sharjah,Private,Indian"
     	'ARE30'  = "ARE - stratum 30: Sharjah,Private,Other"
     	'ARE31'  = "ARE - stratum 31: Ajman,Public,MOE"
     	'ARE35'  = "ARE - stratum 35: Ajman,Public,Other"
     	'ARE36'  = "ARE - stratum 36: Ajman,Private,MOE"
     	'ARE37'  = "ARE - stratum 37: Ajman,Private,US"
     	'ARE38'  = "ARE - stratum 38: Ajman,Private,UK"
     	'ARE39'  = "ARE - stratum 39: Ajman,Private,Indian"
     	'ARE40'  = "ARE - stratum 40: Ajman,Private,Other"
     	'ARE41'  = "ARE - stratum 41: Umm Al quwain,Public,MOE"
     	'ARE45'  = "ARE - stratum 45: Umm Al quwain,Public,Other"
     	'ARE46'  = "ARE - stratum 46: Umm Al quwain,Private,MOE"
     	'ARE47'  = "ARE - stratum 47: Umm Al quwain,Private,US"
     	'ARE49'  = "ARE - stratum 49: Umm Al quwain,Private,Indian"
     	'ARE50'  = "ARE - stratum 50: Umm Al quwain,Private,Other"
     	'ARE51'  = "ARE - stratum 51: Ras Al khaimah,Public,MOE"
     	'ARE55'  = "ARE - stratum 55: Ras Al khaimah,Public,Other"
     	'ARE56'  = "ARE - stratum 56: Ras Al khaimah,Private,MOE"
     	'ARE57'  = "ARE - stratum 57: Ras Al khaimah,Private,US"
     	'ARE58'  = "ARE - stratum 58: Ras Al khaimah,Private,UK"
     	'ARE59'  = "ARE - stratum 59: Ras Al khaimah,Private,Indian"
     	'ARE60'  = "ARE - stratum 60: Ras Al khaimah,Private,Other"
     	'ARE61'  = "ARE - stratum 61: Fujairah,Public,MOE"
     	'ARE65'  = "ARE - stratum 65: Fujairah,Public,Other"
     	'ARE66'  = "ARE - stratum 66: Fujairah,Private,MOE"
     	'ARE67'  = "ARE - stratum 67: Fujairah,Private,US"
     	'ARE68'  = "ARE - stratum 68: Fujairah,Private,UK"
     	'ARE70'  = "ARE - stratum 70: Fujairah,Private,Other"
     	'ARE97'  = "Undisclosed STRATUM - United Arab Emirates"
     	'ARG01'  = "ARG - stratum 01: CABA/Public"
     	'ARG02'  = "ARG - stratum 02: CABA/Private"
     	'ARG03'  = "ARG - stratum 03: Buenos Aires province/Public"
     	'ARG04'  = "ARG - stratum 04: Buenos Aires province/Private"
     	'ARG05'  = "ARG - stratum 05: Tucumán/Public"
     	'ARG06'  = "ARG - stratum 06: Tucumán/Private"
     	'ARG07'  = "ARG - stratum 07: Córdoba/Public"
     	'ARG08'  = "ARG - stratum 08: Córdoba/Private"
     	'ARG09'  = "ARG - stratum 09: Santa Fe/Public"
     	'ARG10'  = "ARG - stratum 10: Santa Fe/Private"
     	'ARG11'  = "ARG - stratum 11: NEA/Public"
     	'ARG12'  = "ARG - stratum 12: NEA/Private"
     	'ARG13'  = "ARG - stratum 13: NOA/Public"
     	'ARG14'  = "ARG - stratum 14: NOA/Private"
     	'ARG15'  = "ARG - stratum 15: Cuyo/Public"
     	'ARG16'  = "ARG - stratum 16: Cuyo/Private"
     	'ARG17'  = "ARG - stratum 17: Patagonia/Public"
     	'ARG18'  = "ARG - stratum 18: Patagonia/Private"
     	'ARG19'  = "ARG - stratum 19: Mendoza/Public"
     	'ARG20'  = "ARG - stratum 20: Mendoza/Private"
     	'ARG97'  = "Undisclosed STRATUM - Argentina"
     	'AUS01'  = "AUS - stratum 01: ACT-Catholic"
     	'AUS02'  = "AUS - stratum 02: ACT-Government"
     	'AUS03'  = "AUS - stratum 03: ACT-Independent"
     	'AUS04'  = "AUS - stratum 04: NSW-Catholic"
     	'AUS05'  = "AUS - stratum 05: NSW-Government"
     	'AUS06'  = "AUS - stratum 06: NSW-Independent"
     	'AUS07'  = "AUS - stratum 07: VIC-Catholic"
     	'AUS08'  = "AUS - stratum 08: VIC-Government"
     	'AUS09'  = "AUS - stratum 09: VIC-Independent"
     	'AUS10'  = "AUS - stratum 10: QLD-Catholic"
     	'AUS11'  = "AUS - stratum 11: QLD-Government"
     	'AUS12'  = "AUS - stratum 12: QLD-Independent"
     	'AUS13'  = "AUS - stratum 13: SA-Catholic"
     	'AUS14'  = "AUS - stratum 14: SA-Government"
     	'AUS15'  = "AUS - stratum 15: SA-Independent"
     	'AUS16'  = "AUS - stratum 16: WA-Catholic"
     	'AUS17'  = "AUS - stratum 17: WA-Government"
     	'AUS18'  = "AUS - stratum 18: WA-Independent"
     	'AUS19'  = "AUS - stratum 19: TAS-Catholic"
     	'AUS20'  = "AUS - stratum 20: TAS-Government"
     	'AUS21'  = "AUS - stratum 21: TAS-Independent"
     	'AUS22'  = "AUS - stratum 22: NT-Catholic"
     	'AUS23'  = "AUS - stratum 23: NT-Government"
     	'AUS24'  = "AUS - stratum 24: NT-Independent"
     	'AUS97'  = "Undisclosed STRATUM - Australia"
     	'AUT01'  = "AUT - stratum 01: 1a NMS"
     	'AUT02'  = "AUT - stratum 02: 1b ASO"
     	'AUT03'  = "AUT - stratum 03: 2 Polytechnische Schulen"
     	'AUT04'  = "AUT - stratum 04: 3 AHS-Langform"
     	'AUT05'  = "AUT - stratum 05: 4 AHS-Kurzform"
     	'AUT06'  = "AUT - stratum 06: 5 Schulen mit Statut"
     	'AUT07'  = "AUT - stratum 07: 7 Berufsschulen kaufmaennisch&gewerblich"
     	'AUT08'  = "AUT - stratum 08: 8 Berufsschulen landwirtschaftlich"
     	'AUT09'  = "AUT - stratum 09: 9 BMS gewerblich"
     	'AUT10'  = "AUT - stratum 10: 10 BMS kaufmaennisch"
     	'AUT11'  = "AUT - stratum 11: 11 BMS wirtschaftlich"
     	'AUT12'  = "AUT - stratum 12: 12 BMS landwirtschaftlich"
     	'AUT13'  = "AUT - stratum 13: 13 BHS gewerblich"
     	'AUT14'  = "AUT - stratum 14: 14 BHS kaufmaennisch"
     	'AUT15'  = "AUT - stratum 15: 15 BHS wirtschaftlich"
     	'AUT16'  = "AUT - stratum 16: 16 BHS landwirtschaftlich"
     	'AUT17'  = "AUT - stratum 17: 17 BAfEP/BASOP"
     	'AUT97'  = "Undisclosed STRATUM - Austria"
     	'BEL01'  = "BEL - stratum 01: Flanders/Gen Ed only/private subsidized/ISCED2"
     	'BEL02'  = "BEL - stratum 02: Flanders/Gen Ed only/private subsidized/ISCED3"
     	'BEL03'  = "BEL - stratum 03: Flanders/Gen Ed only/private subsidized/Mixed ISCED"
     	'BEL04'  = "BEL - stratum 04: Flanders/Gen Ed only/community/ISCED2"
     	'BEL05'  = "BEL - stratum 05: Flanders/Gen Ed only/community/ISCED3"
     	'BEL06'  = "BEL - stratum 06: Flanders/Gen Ed only/community/Mixed ISCED"
     	'BEL07'  = "BEL - stratum 07: Flanders/Gen Ed and other type/private subsidized/ISCED2"
     	'BEL08'  = "BEL - stratum 08: Flanders/Gen Ed and other type/private subsidized /ISCED3"
     	'BEL09'  = "BEL - stratum 09: Flanders/Gen Ed and other type/private subsidized /Mixed ISCED"
     	'BEL10'  = "BEL - stratum 10: Flanders/Gen Ed and other type/community/ISCED2"
     	'BEL11'  = "BEL - stratum 11: Flanders/Gen Ed and other type/community/ISCED3"
     	'BEL12'  = "BEL - stratum 12: Flanders/Gen Ed and other type/community/Mixed ISCED"
     	'BEL13'  = "BEL - stratum 13: Flanders/Tech or Voc/private subsidized/ISCED2"
     	'BEL14'  = "BEL - stratum 14: Flanders/Tech or Voc/private subsidized/ISCED3"
     	'BEL15'  = "BEL - stratum 15: Flanders/Tech or Voc/private subsidized/Mixed ISCED"
     	'BEL16'  = "BEL - stratum 16: Flanders/Tech or Voc/community/ISCED2"
     	'BEL17'  = "BEL - stratum 17: Flanders/Tech or Voc/community/ISCED3"
     	'BEL18'  = "BEL - stratum 18: Flanders/Tech or Voc/community/Mixed ISCED"
     	'BEL19'  = "BEL - stratum 19: Flanders/Special Ed/private subsidized"
     	'BEL20'  = "BEL - stratum 20: Flanders/Special Ed/community"
     	'BEL21'  = "BEL - stratum 21: Flanders/Part-time Vocational Ed"
     	'BEL22'  = "BEL - stratum 22: French com/Regular/ISCED2"
     	'BEL23'  = "BEL - stratum 23: French com/Regular/ISCED3/Academic only"
     	'BEL24'  = "BEL - stratum 24: French com/Regular/ISCED3/Mixed"
     	'BEL25'  = "BEL - stratum 25: French com/Regular/ISCED3/Vocational only"
     	'BEL26'  = "BEL - stratum 26: French com/Regular/ Mixed ISCED/Academic only"
     	'BEL27'  = "BEL - stratum 27: French com/Regular/ Mixed ISCED/Mixed"
     	'BEL28'  = "BEL - stratum 28: French com/Special Ed"
     	'BEL29'  = "BEL - stratum 29: French com/Part-time Vocational Ed"
     	'BEL30'  = "BEL - stratum 30: German com/Regular"
     	'BEL31'  = "BEL - stratum 31: German com/Special Ed"
     	'BEL97'  = "Undisclosed STRATUM - Belgium"
     	'BGR01'  = "BGR - stratum 01: Capital"
     	'BGR02'  = "BGR - stratum 02: Large City"
     	'BGR03'  = "BGR - stratum 03: Other Location"
     	'BGR97'  = "Undisclosed STRATUM - Bulgaria"
     	'BRA01'  = "BRA - stratum 01: Norte / Public Federal"
     	'BRA02'  = "BRA - stratum 02: Norte / Public State"
     	'BRA03'  = "BRA - stratum 03: Norte / Public Municipal"
     	'BRA04'  = "BRA - stratum 04: Norte / Private"
     	'BRA05'  = "BRA - stratum 05: Nordeste / Public Federal"
     	'BRA06'  = "BRA - stratum 06: Nordeste / Public State"
     	'BRA07'  = "BRA - stratum 07: Nordeste / Public Municipal"
     	'BRA08'  = "BRA - stratum 08: Nordeste / Private"
     	'BRA09'  = "BRA - stratum 09: Sul / Public Federal"
     	'BRA10'  = "BRA - stratum 10: Sul / Public State"
     	'BRA11'  = "BRA - stratum 11: Sul / Public Municipal"
     	'BRA12'  = "BRA - stratum 12: Sul / Private"
     	'BRA13'  = "BRA - stratum 13: Sudeste / Public Federal"
     	'BRA14'  = "BRA - stratum 14: Sudeste / Public State"
     	'BRA15'  = "BRA - stratum 15: Sudeste / Public Municipal"
     	'BRA16'  = "BRA - stratum 16: Sudeste / Private"
     	'BRA17'  = "BRA - stratum 17: Centro-Oeste / Public Federal"
     	'BRA18'  = "BRA - stratum 18: Centro-Oeste / Public State"
     	'BRA19'  = "BRA - stratum 19: Centro-Oeste / Public Municipal"
     	'BRA20'  = "BRA - stratum 20: Centro-Oeste / Private"
     	'BRA97'  = "Undisclosed STRATUM - Brazil"
     	'BRN02'  = "BRN - stratum 02: Ministry of Education,Mixed ISCED (Lower & Upper Secondary to Sixth Form)"
     	'BRN03'  = "BRN - stratum 03: Ministry of Education,ISCED 3 ONLY"
     	'BRN04'  = "BRN - stratum 04: Ministry of Religious Affair,ISCED 2 ONLY (Lower Secondary)"
     	'BRN05'  = "BRN - stratum 05: Ministry of Religious Affair,Mixed ISCED (Lower & Upper Secondary to Sixth Form)"
     	'BRN06'  = "BRN - stratum 06: Ministry of Religious Affair,ISCED 3 ONLY"
     	'BRN08'  = "BRN - stratum 08: Private Schools,Mixed ISCED (Lower & Upper Secondary to Sixth Form)"
     	'BRN10'  = "BRN - stratum 10: International Schools,ISCED 2 ONLY (Lower Secondary)"
     	'BRN11'  = "BRN - stratum 11: International Schools,Mixed ISCED (Lower & Upper Secondary to Sixth Form)"
     	'BRN97'  = "Undisclosed STRATUM - Brunei Darussalam"
     	'CAN01'  = "CAN - stratum 01: Province 10 / Fren, Engl / 000 to 002"
     	'CAN02'  = "CAN - stratum 02: Province 10 / Fren, Engl / 003 to 021"
     	'CAN03'  = "CAN - stratum 03: Province 10 / Engl / 022 to 041"
     	'CAN04'  = "CAN - stratum 04: Province 10 / Engl / 042 to …"
     	'CAN11'  = "CAN - stratum 11: Province 11 / Engl / 000 to 002"
     	'CAN12'  = "CAN - stratum 12: Province 11 / Fren, Engl / 003 to 021"
     	'CAN13'  = "CAN - stratum 13: Province 11 / Engl / 022 to 041"
     	'CAN14'  = "CAN - stratum 14: Province 11 / Engl / 042 to …"
     	'CAN21'  = "CAN - stratum 21: Province 12 / Engl / 000 to 002"
     	'CAN22'  = "CAN - stratum 22: Province 12 / Engl / 003 to 021"
     	'CAN23'  = "CAN - stratum 23: Province 12 / Engl / 022 to 041"
     	'CAN24'  = "CAN - stratum 24: Province 12 / Engl / 042 to …"
     	'CAN25'  = "CAN - stratum 25: Province 12 / Fren / 000 to 002"
     	'CAN26'  = "CAN - stratum 26: Province 12 / Fren / 003 to 021"
     	'CAN27'  = "CAN - stratum 27: Province 12 / Fren / 022 to 041"
     	'CAN28'  = "CAN - stratum 28: Province 12 / Fren / 042 to …"
     	'CAN31'  = "CAN - stratum 31: Province 13 / Engl / 000 to 002"
     	'CAN32'  = "CAN - stratum 32: Province 13 / Engl / 003 to 021"
     	'CAN33'  = "CAN - stratum 33: Province 13 / Engl / 022 to 041"
     	'CAN34'  = "CAN - stratum 34: Province 13 / Engl / 042 to …"
     	'CAN35'  = "CAN - stratum 35: Province 13 / Fren / 000 to 002"
     	'CAN36'  = "CAN - stratum 36: Province 13 / Fren, Fren / 003 to 041"
     	'CAN37'  = "CAN - stratum 37: Province 13 / Fren / 042 to …"
     	'CAN41'  = "CAN - stratum 41: Province 24 / Engl / 000 to 002"
     	'CAN42'  = "CAN - stratum 42: Province 24 / Engl / 003 to 021"
     	'CAN43'  = "CAN - stratum 43: Province 24 / Engl / 022 to 041"
     	'CAN44'  = "CAN - stratum 44: Province 24 / Engl / 042 to …"
     	'CAN45'  = "CAN - stratum 45: Province 24 / Fren, Fren / 000  to 021"
     	'CAN46'  = "CAN - stratum 46: Province 24 / Fren / 022 to 041"
     	'CAN47'  = "CAN - stratum 47: Province 24 / Fren / 042 to …"
     	'CAN51'  = "CAN - stratum 51: Province 35 / Engl, Engl / 000 to 021"
     	'CAN52'  = "CAN - stratum 52: Province 35 / Engl / 022 to 041"
     	'CAN53'  = "CAN - stratum 53: Province 35 / Engl / 042 to …"
     	'CAN54'  = "CAN - stratum 54: Province 35 / Fren, Fren / 000 to 021"
     	'CAN55'  = "CAN - stratum 55: Province 35 / Fren / 022 to 041"
     	'CAN56'  = "CAN - stratum 56: Province 35 / Fren / 042 to …"
     	'CAN61'  = "CAN - stratum 61: Province 46 / Engl / 000 to 002"
     	'CAN62'  = "CAN - stratum 62: Province 46 / Engl / 003 to 021"
     	'CAN63'  = "CAN - stratum 63: Province 46 / Engl / 022 to 041"
     	'CAN64'  = "CAN - stratum 64: Province 46 / Engl / 042 to …"
     	'CAN65'  = "CAN - stratum 65: Province 46 / Fren / 000 to 002"
     	'CAN66'  = "CAN - stratum 66: Province 46 / Fren / 003 to 021"
     	'CAN67'  = "CAN - stratum 67: Province 46 / Fren / 022 to 041"
     	'CAN68'  = "CAN - stratum 68: Province 46 / Fren / 042 to …"
     	'CAN71'  = "CAN - stratum 71: Province 47 / Engl / 000 to 002"
     	'CAN72'  = "CAN - stratum 72: Province 47 / Engl / 003 to 021"
     	'CAN73'  = "CAN - stratum 73: Province 47 / Engl / 022 to 041"
     	'CAN74'  = "CAN - stratum 74: Province 47 / Engl / 042 to …"
     	'CAN75'  = "CAN - stratum 75: Province 47 / Fren / 000 to 002"
     	'CAN76'  = "CAN - stratum 76: Province 47 / Fren / 003 to 021"
     	'CAN81'  = "CAN - stratum 81: Province 48 / Engl / 000 to 002"
     	'CAN82'  = "CAN - stratum 82: Province 48 / Engl / 003 to 021"
     	'CAN83'  = "CAN - stratum 83: Province 48 / Engl / 022 to 041"
     	'CAN84'  = "CAN - stratum 84: Province 48 / Engl / 042 to …"
     	'CAN85'  = "CAN - stratum 85: Province 48 / Fren / 000 to 002"
     	'CAN86'  = "CAN - stratum 86: Province 48 / Fren / 003 to 021"
     	'CAN87'  = "CAN - stratum 87: Province 48 / Fren / 022 to 041"
     	'CAN88'  = "CAN - stratum 88: Province 48 / Fren / 042 to …"
     	'CAN91'  = "CAN - stratum 91: Province 59 / Engl / 000 to 002"
     	'CAN92'  = "CAN - stratum 92: Province 59 / Engl / 003 to 021"
     	'CAN93'  = "CAN - stratum 93: Province 59 / Engl / 022 to 041"
     	'CAN94'  = "CAN - stratum 94: Province 59 / Engl / 042 to …"
     	'CAN95'  = "CAN - stratum 95: Province 59 / Fren / 000 to 002"
     	'CAN96'  = "CAN - stratum 96: Province 59 / Fren / 003 to 021"
     	'CAN97'  = "CAN - stratum 97: Province 59 / Fren / 022 to 041"
     	'CAN98'  = "CAN - stratum 98: Province 59 / Fren / 042 to …"
     	'CAN99'  = "Undisclosed STRATUM - Canada"
     	'CHE01'  = "CHE - stratum 01: German, ISCED 2, Urban Core Area"
     	'CHE02'  = "CHE - stratum 02: German, ISCED 2, Non-Urban"
     	'CHE03'  = "CHE - stratum 03: German, Mixed, Urban Core Area"
     	'CHE04'  = "CHE - stratum 04: German, Mixed, Non-Urban"
     	'CHE05'  = "CHE - stratum 05: German, ISCED 3, Urban Core Area"
     	'CHE06'  = "CHE - stratum 06: German, ISCED 3, Non-Urban"
     	'CHE07'  = "CHE - stratum 07: French, ISCED 2, Urban Core Area"
     	'CHE08'  = "CHE - stratum 08: French, ISCED 2, Non-Urban"
     	'CHE09'  = "CHE - stratum 09: French, Mixed, Urban Core Area"
     	'CHE10'  = "CHE - stratum 10: French, ISCED 3, Urban Core Area"
     	'CHE11'  = "CHE - stratum 11: French, ISCED 3, Non-Urban"
     	'CHE12'  = "CHE - stratum 12: Italian, ISCED 2, Urban Core Area"
     	'CHE13'  = "CHE - stratum 13: Italian, ISCED 2, Non-Urban"
     	'CHE14'  = "CHE - stratum 14: Italian, ISCED 3, Urban Core Area"
     	'CHE15'  = "CHE - stratum 15: Italian, ISCED 3, Non-Urban"
     	'CHE97'  = "Undisclosed STRATUM - Switzerland"
     	'CHL01'  = "CHL - stratum 01: PRIMARY ONLY"
     	'CHL02'  = "CHL - stratum 02: MUNICIPAL / PRIMARY & SECONDARY / HS"
     	'CHL03'  = "CHL - stratum 03: MUNICIPAL / PRIMARY & SECONDARY / HS & TP"
     	'CHL04'  = "CHL - stratum 04: MUNICIPAL / PRIMARY & SECONDARY / TP"
     	'CHL05'  = "CHL - stratum 05: MUNICIPAL / SECONDARY / HS"
     	'CHL06'  = "CHL - stratum 06: MUNICIPAL / SECONDARY / HS & TP"
     	'CHL07'  = "CHL - stratum 07: MUNICIPAL / SECONDARY / TP"
     	'CHL08'  = "CHL - stratum 08: SUBSIDIZED / PRIMARY & SECONDARY / HS"
     	'CHL09'  = "CHL - stratum 09: SUBSIDIZED / PRIMARY & SECONDARY / HS & TP"
     	'CHL10'  = "CHL - stratum 10: SUBSIDIZED / PRIMARY & SECONDARY / TP"
     	'CHL11'  = "CHL - stratum 11: SUBSIDIZED / SECONDARY / HS"
     	'CHL12'  = "CHL - stratum 12: SUBSIDIZED / SECONDARY / HS & TP"
     	'CHL13'  = "CHL - stratum 13: SUBSIDIZED / SECONDARY / TP"
     	'CHL14'  = "CHL - stratum 14: PRIVATE / ALL CATEGORIES"
     	'CHL97'  = "Undisclosed STRATUM - Chile"
     	'COL01'  = "COL - stratum 01: Bogota,Urban-Public"
     	'COL02'  = "COL - stratum 02: Bogota,Rural-public"
     	'COL03'  = "COL - stratum 03: Bogota,Private"
     	'COL04'  = "COL - stratum 04: Rest of the country,Urban-Public"
     	'COL05'  = "COL - stratum 05: Rest of the country,Rural-public"
     	'COL06'  = "COL - stratum 06: Rest of the country,Private"
     	'COL97'  = "Undisclosed STRATUM - Colombia"
     	'CRI01'  = "CRI - stratum 01: Urban public academic"
     	'CRI02'  = "CRI - stratum 02: Rural public academic"
     	'CRI03'  = "CRI - stratum 03: Urban public technical"
     	'CRI04'  = "CRI - stratum 04: Rural public technical"
     	'CRI05'  = "CRI - stratum 05: Private"
     	'CRI97'  = "Undisclosed STRATUM - Costa Rica"
     	'CZE01'  = "CZE - stratum 01: Basic/Region1"
     	'CZE02'  = "CZE - stratum 02: Basic/Region2"
     	'CZE03'  = "CZE - stratum 03: Basic/Region3"
     	'CZE04'  = "CZE - stratum 04: Basic/Region4"
     	'CZE05'  = "CZE - stratum 05: Basic/Region5"
     	'CZE06'  = "CZE - stratum 06: Basic/Region6"
     	'CZE07'  = "CZE - stratum 07: Basic/Region7"
     	'CZE08'  = "CZE - stratum 08: Basic/Region8"
     	'CZE09'  = "CZE - stratum 09: Basic/Region9"
     	'CZE10'  = "CZE - stratum 10: Basic/Region10"
     	'CZE11'  = "CZE - stratum 11: Basic/Region11"
     	'CZE12'  = "CZE - stratum 12: Basic/Region12"
     	'CZE13'  = "CZE - stratum 13: Basic/Region13"
     	'CZE14'  = "CZE - stratum 14: Basic/Region14"
     	'CZE15'  = "CZE - stratum 15: 6-8yrGym/Region1"
     	'CZE16'  = "CZE - stratum 16: 6-8yrGym/Region2"
     	'CZE17'  = "CZE - stratum 17: 6-8yrGym/Region3"
     	'CZE18'  = "CZE - stratum 18: 6-8yrGym/Region4"
     	'CZE19'  = "CZE - stratum 19: 6-8yrGym/Region5"
     	'CZE20'  = "CZE - stratum 20: 6-8yrGym/Region6"
     	'CZE21'  = "CZE - stratum 21: 6-8yrGym/Region7"
     	'CZE22'  = "CZE - stratum 22: 6-8yrGym/Region8"
     	'CZE23'  = "CZE - stratum 23: 6-8yrGym/Region9"
     	'CZE24'  = "CZE - stratum 24: 6-8yrGym/Region10"
     	'CZE25'  = "CZE - stratum 25: 6-8yrGym/Region11"
     	'CZE26'  = "CZE - stratum 26: 6-8yrGym/Region12"
     	'CZE27'  = "CZE - stratum 27: 6-8yrGym/Region13"
     	'CZE28'  = "CZE - stratum 28: 6-8yrGym/Region14"
     	'CZE29'  = "CZE - stratum 29: 4yr Gym"
     	'CZE30'  = "CZE - stratum 30: Voc-Tech-Conservatory with maturate"
     	'CZE31'  = "CZE - stratum 31: Voc-Tech Secondary without maturate"
     	'CZE32'  = "CZE - stratum 32: Special & practical"
     	'CZE97'  = "Undisclosed STRATUM - Czech Republic"
     	'DEU01'  = "DEU - stratum 01: NOR/Baden-Württemberg (BW)"
     	'DEU02'  = "DEU - stratum 02: NOR/Bayern (BY)"
     	'DEU03'  = "DEU - stratum 03: NOR/Berlin (BE)"
     	'DEU04'  = "DEU - stratum 04: NOR/Brandenburg (BB)"
     	'DEU05'  = "DEU - stratum 05: NOR/Bremen (HB)"
     	'DEU06'  = "DEU - stratum 06: NOR/Hamburg (HH)"
     	'DEU07'  = "DEU - stratum 07: NOR/Hessen (HE)"
     	'DEU08'  = "DEU - stratum 08: NOR/Mecklenburg-Vorpommern (MV)"
     	'DEU09'  = "DEU - stratum 09: NOR/Niedersachsen (NI)"
     	'DEU10'  = "DEU - stratum 10: NOR/Nordrhein-Westfalen (NW)"
     	'DEU11'  = "DEU - stratum 11: NOR/Rheinland-Pfalz (RP)"
     	'DEU12'  = "DEU - stratum 12: NOR/Saarland (SL)"
     	'DEU13'  = "DEU - stratum 13: NOR/Sachsen (SN)"
     	'DEU14'  = "DEU - stratum 14: NOR/Sachsen-Anhalt (ST)"
     	'DEU15'  = "DEU - stratum 15: NOR/Schleswig-Holstein (SH)"
     	'DEU16'  = "DEU - stratum 16: NOR/Thüringen (TH)"
     	'DEU17'  = "DEU - stratum 17: SEN schools"
     	'DEU18'  = "DEU - stratum 18: Vocational Schools"
     	'DEU97'  = "Undisclosed STRATUM - Germany"
     	'DNK01'  = "DNK - stratum 01: High Minority"
     	'DNK02'  = "DNK - stratum 02: Mid Minority"
     	'DNK03'  = "DNK - stratum 03: Low Minority"
     	'DNK04'  = "DNK - stratum 04: No Minority"
     	'DNK05'  = "DNK - stratum 05: Faroe Island"
     	'DNK97'  = "Undisclosed STRATUM - Denmark"
     	'DOM01'  = "DOM - stratum 01: Public/Urban/ISCED2"
     	'DOM02'  = "DOM - stratum 02: Public/Urban/ISCED3"
     	'DOM03'  = "DOM - stratum 03: Public/Urban/Mixed"
     	'DOM04'  = "DOM - stratum 04: Public/Rural/ISCED2"
     	'DOM05'  = "DOM - stratum 05: Public/Rural/ISCED3"
     	'DOM06'  = "DOM - stratum 06: Public/Rural/Mixed"
     	'DOM07'  = "DOM - stratum 07: Private/Urban/ISCED2"
     	'DOM08'  = "DOM - stratum 08: Private/Urban/ISCED3 & Mixed"
     	'DOM09'  = "DOM - stratum 09: Private/Rural/ISCED2"
     	'DOM10'  = "DOM - stratum 10: Private/Rural/Mixed"
     	'DOM97'  = "Undisclosed STRATUM - Dominican Republic"
     	'ESP01'  = "ESP - stratum 01: Andalucía,Public"
     	'ESP02'  = "ESP - stratum 02: Andalucía,Private"
     	'ESP03'  = "ESP - stratum 03: Aragón,Public"
     	'ESP04'  = "ESP - stratum 04: Aragón,Private"
     	'ESP05'  = "ESP - stratum 05: Asturias,Public"
     	'ESP06'  = "ESP - stratum 06: Asturias,Private"
     	'ESP07'  = "ESP - stratum 07: Baleares,Public"
     	'ESP08'  = "ESP - stratum 08: Baleares,Private"
     	'ESP09'  = "ESP - stratum 09: Canarias,Public"
     	'ESP10'  = "ESP - stratum 10: Canarias,Private"
     	'ESP11'  = "ESP - stratum 11: Cantabria,Public"
     	'ESP12'  = "ESP - stratum 12: Cantabria,Private"
     	'ESP13'  = "ESP - stratum 13: Castilla y León,Public"
     	'ESP14'  = "ESP - stratum 14: Castilla y León,Private"
     	'ESP15'  = "ESP - stratum 15: Castilla - La Mancha,Public"
     	'ESP16'  = "ESP - stratum 16: Castilla - La Mancha,Private"
     	'ESP17'  = "ESP - stratum 17: Cataluña,Public"
     	'ESP18'  = "ESP - stratum 18: Cataluña,Private"
     	'ESP19'  = "ESP - stratum 19: Extremadura,Public"
     	'ESP20'  = "ESP - stratum 20: Extremadura,Private"
     	'ESP21'  = "ESP - stratum 21: Galicia,Public"
     	'ESP22'  = "ESP - stratum 22: Galicia,Private"
     	'ESP23'  = "ESP - stratum 23: La Rioja,Public"
     	'ESP24'  = "ESP - stratum 24: La Rioja,Private"
     	'ESP25'  = "ESP - stratum 25: Madrid,Public"
     	'ESP26'  = "ESP - stratum 26: Madrid,Private"
     	'ESP27'  = "ESP - stratum 27: Murcia,Public"
     	'ESP28'  = "ESP - stratum 28: Murcia,Private"
     	'ESP29'  = "ESP - stratum 29: Navarra,Public"
     	'ESP30'  = "ESP - stratum 30: Navarra,Private"
     	'ESP31'  = "ESP - stratum 31: País Vasco,Public,Public"
     	'ESP32'  = "ESP - stratum 32: País Vasco,Private,Private AB"
     	'ESP33'  = "ESP - stratum 33: País Vasco,Private,Private D"
     	'ESP34'  = "ESP - stratum 34: Comunidad Valenciana,Public"
     	'ESP35'  = "ESP - stratum 35: Comunidad Valenciana,Private"
     	'ESP36'  = "ESP - stratum 36: Ceuta,Public"
     	'ESP37'  = "ESP - stratum 37: Ceuta,Private"
     	'ESP38'  = "ESP - stratum 38: Melilla,Public"
     	'ESP39'  = "ESP - stratum 39: Melilla,Private"
     	'ESP97'  = "Undisclosed STRATUM - Spain"
     	'EST01'  = "EST - stratum 01: Estonian"
     	'EST02'  = "EST - stratum 02: Russian"
     	'EST03'  = "EST - stratum 03: Mixed"
     	'EST97'  = "Undisclosed STRATUM - Estonia"
     	'FIN01'  = "FIN - stratum 01: Helsinki / Uusimaa / Urban / 1"
     	'FIN02'  = "FIN - stratum 02: Helsinki / Uusimaa / Urban / 2"
     	'FIN03'  = "FIN - stratum 03: Helsinki / Uusimaa / Urban / 3"
     	'FIN04'  = "FIN - stratum 04: Helsinki / Uusimaa / Urban / 4"
     	'FIN05'  = "FIN - stratum 05: Helsinki / Uusimaa / Urban / 5"
     	'FIN06'  = "FIN - stratum 06: Helsinki / Uusimaa / Urban / 6"
     	'FIN07'  = "FIN - stratum 07: Helsinki / Uusimaa / Rural"
     	'FIN08'  = "FIN - stratum 08: Southern Finland / Urban / 1"
     	'FIN09'  = "FIN - stratum 09: Southern Finland / Urban / 2"
     	'FIN10'  = "FIN - stratum 10: Southern Finland / Urban / 3"
     	'FIN11'  = "FIN - stratum 11: Southern Finland / Urban / 4"
     	'FIN12'  = "FIN - stratum 12: Southern Finland / Urban / 5"
     	'FIN13'  = "FIN - stratum 13: Southern Finland / Urban / 6"
     	'FIN14'  = "FIN - stratum 14: Southern Finland / Rural"
     	'FIN15'  = "FIN - stratum 15: Western Finland / Urban / 1"
     	'FIN16'  = "FIN - stratum 16: Western Finland / Urban / 2"
     	'FIN17'  = "FIN - stratum 17: Western Finland / Urban / 3"
     	'FIN18'  = "FIN - stratum 18: Western Finland / Urban / 4"
     	'FIN19'  = "FIN - stratum 19: Western Finland / Urban / 5"
     	'FIN20'  = "FIN - stratum 20: Western Finland / Urban / 6"
     	'FIN21'  = "FIN - stratum 21: Western Finland / Rural"
     	'FIN22'  = "FIN - stratum 22: Northern and Eastern Finland / Urban / 1"
     	'FIN23'  = "FIN - stratum 23: Northern and Eastern Finland / Urban / 2, 3, 4"
     	'FIN24'  = "FIN - stratum 24: Northern and Eastern Finland / Urban / 5"
     	'FIN25'  = "FIN - stratum 25: Northern and Eastern Finland / Urban / 6"
     	'FIN26'  = "FIN - stratum 26: Northern and Eastern Finland / Rural / 5"
     	'FIN27'  = "FIN - stratum 27: Northern and Eastern Finland / Rural / 6"
     	'FIN28'  = "FIN - stratum 28: Swedish speaking / Urban"
     	'FIN29'  = "FIN - stratum 29: Swedish speaking / Rural"
     	'FIN97'  = "Undisclosed STRATUM - Finland"
     	'FRA01'  = "FRA - stratum 01: France métropolitaine / Lycée GT / Large school"
     	'FRA02'  = "FRA - stratum 02: France métropolitaine / Collège / Large school"
     	'FRA03'  = "FRA - stratum 03: France métropolitaine / Lycée PRO / Large school"
     	'FRA04'  = "FRA - stratum 04: France métropolitaine / Lycée agricole / Large school"
     	'FRA05'  = "FRA - stratum 05: France métropolitaine / Small school"
     	'FRA06'  = "FRA - stratum 06: France métropolitaine / Very Small school"
     	'FRA07'  = "FRA - stratum 07: Guadeloupe Guyane Martinique / Lycée GT / Large school"
     	'FRA08'  = "FRA - stratum 08: Guadeloupe Guyane Martinique / Collège / Large school"
     	'FRA09'  = "FRA - stratum 09: Guadeloupe Guyane Martinique / Lycée PRO / Large school"
     	'FRA10'  = "FRA - stratum 10: Guadeloupe Guyane Martinique / Lycée agricole / Large school"
     	'FRA11'  = "FRA - stratum 11: Guadeloupe Guyane Martinique / Small school"
     	'FRA12'  = "FRA - stratum 12: Guadeloupe Guyane Martinique / Very Small school"
     	'FRA13'  = "FRA - stratum 13: La Réunion / Lycée GT / Large school"
     	'FRA14'  = "FRA - stratum 14: La Réunion / Collège / Large school"
     	'FRA15'  = "FRA - stratum 15: La Réunion / Lycée PRO / Large school"
     	'FRA16'  = "FRA - stratum 16: La Réunion / Lycée agricole / Large school"
     	'FRA17'  = "FRA - stratum 17: La Réunion / Small school"
     	'FRA18'  = "FRA - stratum 18: La Réunion / Very Small school"
     	'FRA19'  = "FRA - stratum 19: Mayotte / Lycée GT / Large school"
     	'FRA20'  = "FRA - stratum 20: Mayotte / Collège / Large school"
     	'FRA21'  = "FRA - stratum 21: Mayotte / Lycée PRO + Lycée agricole / Large school"
     	'FRA22'  = "FRA - stratum 22: Mayotte / Small school + Very Small School"
     	'FRA97'  = "Undisclosed STRATUM - France"
     	'GEO01'  = "GEO - stratum 01: Large city / Private"
     	'GEO02'  = "GEO - stratum 02: Large city / Public"
     	'GEO03'  = "GEO - stratum 03: City / Private"
     	'GEO04'  = "GEO - stratum 04: City / Public"
     	'GEO05'  = "GEO - stratum 05: Small city and town / Private"
     	'GEO06'  = "GEO - stratum 06: Small city and town / Public"
     	'GEO07'  = "GEO - stratum 07: Village / Private"
     	'GEO08'  = "GEO - stratum 08: Village / Public"
     	'GEO09'  = "GEO - stratum 09: Remote village / Public"
     	'GEO97'  = "Undisclosed STRATUM - Georgia"
     	'GRC01'  = "GRC - stratum 01: Rural"
     	'GRC02'  = "GRC - stratum 02: Suburban"
     	'GRC03'  = "GRC - stratum 03: Urban"
     	'GRC97'  = "Undisclosed STRATUM - Greece"
     	'GTM01'  = "GTM - stratum 01: Rural/ Oficial (Public)"
     	'GTM02'  = "GTM - stratum 02: Rural/ Cooperativa"
     	'GTM03'  = "GTM - stratum 03: Rural/ Municipal"
     	'GTM04'  = "GTM - stratum 04: Rural/ Privado (Private)"
     	'GTM05'  = "GTM - stratum 05: Urbana/ Oficial (Public)"
     	'GTM06'  = "GTM - stratum 06: Urbana/ Cooperativa"
     	'GTM07'  = "GTM - stratum 07: Urbana/ Municipal"
     	'GTM08'  = "GTM - stratum 08: Urbana/ Privado (Private)"
     	'GTM97'  = "Undisclosed STRATUM - Guatemala"
     	'HKG01'  = "HKG - stratum 01: Government"
     	'HKG02'  = "HKG - stratum 02: Aided or Caput"
     	'HKG03'  = "HKG - stratum 03: Private or International"
     	'HKG04'  = "HKG - stratum 04: Direct Subsidy Scheme"
     	'HKG05'  = "HKG - stratum 05: Vocational Training Programme"
     	'HKG97'  = "Undisclosed STRATUM - Hong Kong (China)"
     	'HRV01'  = "HRV - stratum 01: Four or five year vocational programme"
     	'HRV02'  = "HRV - stratum 02: Vocational-industrial-crafts programme"
     	'HRV03'  = "HRV - stratum 03: Mixed type"
     	'HRV04'  = "HRV - stratum 04: Art-vocational programme"
     	'HRV05'  = "HRV - stratum 05: Gymnasium"
     	'HRV06'  = "HRV - stratum 06: Primary schools (lower secondary education)"
     	'HRV97'  = "Undisclosed STRATUM - Croatia"
     	'HUN01'  = "HUN - stratum 01: Primary School"
     	'HUN02'  = "HUN - stratum 02: Grammar School 1 (4-5 years long)"
     	'HUN03'  = "HUN - stratum 03: Grammar School 2 (6-7 years long)"
     	'HUN04'  = "HUN - stratum 04: Grammar School 3 (8-9 years long)"
     	'HUN05'  = "HUN - stratum 05: Vocational secondary school"
     	'HUN06'  = "HUN - stratum 06: Vocational school"
     	'HUN97'  = "Undisclosed STRATUM - Hungary"
     	'IDN01'  = "IDN - stratum 01: DKI JAKARTA"
     	'IDN02'  = "IDN - stratum 02: DI YOGYAKARTA"
     	'IDN03'  = "IDN - stratum 03: BANGKA BELITUNG"
     	'IDN04'  = "IDN - stratum 04: NATIONAL"
     	'IDN97'  = "Undisclosed STRATUM - Indonesia"
     	'IRL01'  = "IRL - stratum 01: Community-comp/up to 45"
     	'IRL02'  = "IRL - stratum 02: Community-comp/46 - 85"
     	'IRL03'  = "IRL - stratum 03: Community-comp/86 or more"
     	'IRL04'  = "IRL - stratum 04: Secondary/up to 45"
     	'IRL05'  = "IRL - stratum 05: Secondary /46 - 85"
     	'IRL06'  = "IRL - stratum 06: Secondary /86 or more"
     	'IRL07'  = "IRL - stratum 07: Vocational/up to 45"
     	'IRL08'  = "IRL - stratum 08: Vocational/46 - 85"
     	'IRL09'  = "IRL - stratum 09: Vocational/86 or more"
     	'IRL97'  = "Undisclosed STRATUM - Ireland"
     	'ISL01'  = "ISL - stratum 01: Reykjavík/1-8"
     	'ISL02'  = "ISL - stratum 02: Reykjavík/9-16"
     	'ISL03'  = "ISL - stratum 03: Reykjavík/17-35"
     	'ISL04'  = "ISL - stratum 04: Reykjavík/>35"
     	'ISL05'  = "ISL - stratum 05: Nágrenni Reykjavíkur/1-8"
     	'ISL07'  = "ISL - stratum 07: Nágrenni Reykjavíkur/17-35"
     	'ISL08'  = "ISL - stratum 08: Nágrenni Reykjavíkur/>35"
     	'ISL09'  = "ISL - stratum 09: Suðurnes/1-8"
     	'ISL10'  = "ISL - stratum 10: Suðurnes/9-16"
     	'ISL11'  = "ISL - stratum 11: Suðurnes/17-35"
     	'ISL12'  = "ISL - stratum 12: Suðurnes/>35"
     	'ISL13'  = "ISL - stratum 13: Vestur- og  Norðvesturland/1-8"
     	'ISL14'  = "ISL - stratum 14: Vestur- og  Norðvesturland/9-16"
     	'ISL15'  = "ISL - stratum 15: Vestur- og  Norðvesturland/17-35"
     	'ISL16'  = "ISL - stratum 16: Vestur- og  Norðvesturland/>35"
     	'ISL17'  = "ISL - stratum 17: Austur- og Norðausturland/1-8"
     	'ISL18'  = "ISL - stratum 18: Austur- og Norðausturland/9-16"
     	'ISL19'  = "ISL - stratum 19: Austur- og Norðausturland/17-35"
     	'ISL20'  = "ISL - stratum 20: Austur- og Norðausturland/>35"
     	'ISL21'  = "ISL - stratum 21: Suðurland/1-8"
     	'ISL22'  = "ISL - stratum 22: Suðurland/9-16"
     	'ISL23'  = "ISL - stratum 23: Suðurland/17-35"
     	'ISL24'  = "ISL - stratum 24: Suðurland/>35"
     	'ISL97'  = "Undisclosed STRATUM - Iceland"
     	'ISR01'  = "ISR - stratum 01: Hebrew Secular"
     	'ISR02'  = "ISR - stratum 02: Hebrew-Religious- Female"
     	'ISR03'  = "ISR - stratum 03: Hebrew-Religious-Mixed"
     	'ISR04'  = "ISR - stratum 04: Hebrew-Religious-male"
     	'ISR05'  = "ISR - stratum 05: Arabic-Arabs"
     	'ISR06'  = "ISR - stratum 06: Arabic-Druze"
     	'ISR07'  = "ISR - stratum 07: Arabic-Bedouin"
     	'ISR08'  = "ISR - stratum 08: Hebrew Ultra-Orthodox–Female"
     	'ISR09'  = "ISR - stratum 09: Hebrew Ultra-Orthodox–Male"
     	'ISR10'  = "ISR - stratum 10: Hebrew Ultra-Orthodox–Mix"
     	'ISR11'  = "ISR - stratum 11: Apprenticeship institutions – Hebrew"
     	'ISR12'  = "ISR - stratum 12: Apprenticeship institutions – Arabic"
     	'ISR97'  = "Undisclosed STRATUM - Israel"
     	'ITA01'  = "ITA - stratum 01: BOLZANO / LICEO"
     	'ITA02'  = "ITA - stratum 02: BOLZANO / ISTITUTO TECNICO"
     	'ITA03'  = "ITA - stratum 03: BOLZANO / ISTITUTO PROFESSIONALE"
     	'ITA04'  = "ITA - stratum 04: BOLZANO / SCUOLA MEDIA"
     	'ITA05'  = "ITA - stratum 05: BOLZANO / CENTRO DI FORMAZIONE PROFESSIONALE"
     	'ITA06'  = "ITA - stratum 06: TRENTO / LICEO"
     	'ITA07'  = "ITA - stratum 07: TRENTO / ISTITUTO TECNICO"
     	'ITA08'  = "ITA - stratum 08: TRENTO / ISTITUTO PROFESSIONALE"
     	'ITA09'  = "ITA - stratum 09: TRENTO / SCUOLA MEDIA"
     	'ITA10'  = "ITA - stratum 10: TRENTO / CENTRO DI FORMAZIONE PROFESSIONALE"
     	'ITA11'  = "ITA - stratum 11: REST OF NORTH EAST / LICEO"
     	'ITA12'  = "ITA - stratum 12: REST OF NORTH EAST / ISTITUTO TECNICO"
     	'ITA13'  = "ITA - stratum 13: REST OF NORTH EAST / ISTITUTO PROFESSIONALE"
     	'ITA14'  = "ITA - stratum 14: REST OF NORTH EAST / SCUOLA MEDIA"
     	'ITA15'  = "ITA - stratum 15: REST OF NORTH EAST / CENTRO DI FORMAZIONE PROFESSIONALE"
     	'ITA16'  = "ITA - stratum 16: NORTH WEST / LICEO"
     	'ITA17'  = "ITA - stratum 17: NORTH WEST / ISTITUTO TECNICO"
     	'ITA18'  = "ITA - stratum 18: NORTH WEST / ISTITUTO PROFESSIONALE"
     	'ITA19'  = "ITA - stratum 19: NORTH WEST / SCUOLA MEDIA"
     	'ITA20'  = "ITA - stratum 20: NORTH WEST / CENTRO DI FORMAZIONE PROFESSIONALE"
     	'ITA21'  = "ITA - stratum 21: CENTRE / LICEO"
     	'ITA22'  = "ITA - stratum 22: CENTRE / ISTITUTO TECNICO"
     	'ITA23'  = "ITA - stratum 23: CENTRE / ISTITUTO PROFESSIONALE"
     	'ITA24'  = "ITA - stratum 24: CENTRE / SCUOLA MEDIA"
     	'ITA25'  = "ITA - stratum 25: CENTRE / CENTRO DI FORMAZIONE PROFESSIONALE"
     	'ITA26'  = "ITA - stratum 26: SOUTH / LICEO"
     	'ITA27'  = "ITA - stratum 27: SOUTH / ISTITUTO TECNICO"
     	'ITA28'  = "ITA - stratum 28: SOUTH / ISTITUTO PROFESSIONALE"
     	'ITA29'  = "ITA - stratum 29: SOUTH / SCUOLA MEDIA"
     	'ITA30'  = "ITA - stratum 30: SOUTH / CENTRO DI FORMAZIONE PROFESSIONALE"
     	'ITA31'  = "ITA - stratum 31: SOUTH AND ISLAND / LICEO"
     	'ITA32'  = "ITA - stratum 32: SOUTH AND ISLAND / ISTITUTO TECNICO"
     	'ITA33'  = "ITA - stratum 33: SOUTH AND ISLAND / ISTITUTO PROFESSIONALE"
     	'ITA34'  = "ITA - stratum 34: SOUTH AND ISLAND / SCUOLA MEDIA"
     	'ITA35'  = "ITA - stratum 35: SOUTH AND ISLAND / CENTRO DI FORMAZIONE PROFESSIONALE"
     	'ITA97'  = "Undisclosed STRATUM - Italy"
     	'JAM01'  = "JAM - stratum 01: Region 1/Urban"
     	'JAM02'  = "JAM - stratum 02: Region 1/Rural"
     	'JAM03'  = "JAM - stratum 03: Region 2/Urban"
     	'JAM04'  = "JAM - stratum 04: Region 2/Rural"
     	'JAM05'  = "JAM - stratum 05: Region 3/Urban"
     	'JAM06'  = "JAM - stratum 06: Region 3/Rural"
     	'JAM07'  = "JAM - stratum 07: Region 4/Urban"
     	'JAM08'  = "JAM - stratum 08: Region 4/Rural"
     	'JAM09'  = "JAM - stratum 09: Region 5/Urban"
     	'JAM10'  = "JAM - stratum 10: Region 5/Rural"
     	'JAM11'  = "JAM - stratum 11: Region 6/Urban"
     	'JAM12'  = "JAM - stratum 12: Region 6/Rural"
     	'JAM13'  = "JAM - stratum 13: Region 7/Urban"
     	'JAM14'  = "JAM - stratum 14: Region 7/Rural"
     	'JAM15'  = "JAM - stratum 15: ISCED2"
     	'JAM97'  = "Undisclosed STRATUM - Jamaica"
     	'JOR01'  = "JOR - stratum 01: Public_Non MoD"
     	'JOR02'  = "JOR - stratum 02: Private"
     	'JOR03'  = "JOR - stratum 03: Public_MoD"
     	'JOR04'  = "JOR - stratum 04: Syrian"
     	'JOR05'  = "JOR - stratum 05: UNRWA"
     	'JOR06'  = "JOR - stratum 06: USAID_Building"
     	'JOR07'  = "JOR - stratum 07: USAID_Expansion"
     	'JOR97'  = "Undisclosed STRATUM - Jordan"
     	'JPN01'  = "JPN - stratum 01: Public,Academic"
     	'JPN02'  = "JPN - stratum 02: Public,Practical"
     	'JPN03'  = "JPN - stratum 03: Private(including National),Academic"
     	'JPN04'  = "JPN - stratum 04: Private(including National),Practical"
     	'JPN97'  = "Undisclosed STRATUM - Japan"
     	'KAZ01'  = "KAZ - stratum 01: Non-intellectual / Nur-Sultan city"
     	'KAZ02'  = "KAZ - stratum 02: Non-intellectual / Almaty city"
     	'KAZ03'  = "KAZ - stratum 03: Non-intellectual / Akmolinskaya oblast"
     	'KAZ04'  = "KAZ - stratum 04: Non-intellectual / Aktubinskaya oblast"
     	'KAZ05'  = "KAZ - stratum 05: Non-intellectual / Almatinskaya oblast"
     	'KAZ06'  = "KAZ - stratum 06: Non-intellectual / Atyrauskaya oblast"
     	'KAZ07'  = "KAZ - stratum 07: Non-intellectual / West-Kazakhstan oblast"
     	'KAZ08'  = "KAZ - stratum 08: Non-intellectual / Zhambylskaya oblast"
     	'KAZ09'  = "KAZ - stratum 09: Non-intellectual / Karagandinskaya oblast"
     	'KAZ10'  = "KAZ - stratum 10: Non-intellectual / Kostanayskaya oblast"
     	'KAZ11'  = "KAZ - stratum 11: Non-intellectual / Kyzylordinskaya oblast"
     	'KAZ12'  = "KAZ - stratum 12: Non-intellectual / Mangystauskaya oblast"
     	'KAZ13'  = "KAZ - stratum 13: Non-intellectual / Turkestanskaya oblast"
     	'KAZ14'  = "KAZ - stratum 14: Non-intellectual / Pavlodarskaya oblast"
     	'KAZ15'  = "KAZ - stratum 15: Non-intellectual / North-Kazakhstan oblast"
     	'KAZ16'  = "KAZ - stratum 16: Non-intellectual / East-Kazakhstan oblast"
     	'KAZ17'  = "KAZ - stratum 17: Non-intellectual / Shymkent city"
     	'KAZ18'  = "KAZ - stratum 18: Intellectual"
     	'KAZ97'  = "Undisclosed STRATUM - Kazakhstan"
     	'KHM01'  = "KHM - stratum 01: Urban/ College/ Plains"
     	'KHM02'  = "KHM - stratum 02: Urban/ College/ Tonlesap"
     	'KHM03'  = "KHM - stratum 03: Urban/ College/ Plato"
     	'KHM04'  = "KHM - stratum 04: Urban/ College/ Costal"
     	'KHM05'  = "KHM - stratum 05: Urban/ LyceeG7_G12/ Plains"
     	'KHM06'  = "KHM - stratum 06: Urban/ LyceeG7_G12/ Tonlesap"
     	'KHM07'  = "KHM - stratum 07: Urban/ LyceeG7_G12/ Plato"
     	'KHM08'  = "KHM - stratum 08: Urban/ LyceeG7_G12/ Costal"
     	'KHM09'  = "KHM - stratum 09: Urban/ LyceeG10_G12/ LyceeG10_G12"
     	'KHM10'  = "KHM - stratum 10: Rural/ College/ Plains"
     	'KHM11'  = "KHM - stratum 11: Rural/ College/ Tonlesap"
     	'KHM12'  = "KHM - stratum 12: Rural/ College/ Plato"
     	'KHM13'  = "KHM - stratum 13: Rural/ College/ Costal"
     	'KHM14'  = "KHM - stratum 14: Rural/ LyceeG7_G12/ Plains"
     	'KHM15'  = "KHM - stratum 15: Rural/ LyceeG7_G12/ Tonlesap"
     	'KHM16'  = "KHM - stratum 16: Rural/ LyceeG7_G12/ Plato"
     	'KHM17'  = "KHM - stratum 17: Rural/ LyceeG7_G12/ Costal"
     	'KHM18'  = "KHM - stratum 18: Rural/ LyceeG10_G12/ LyceeG10_G12"
     	'KHM97'  = "Undisclosed STRATUM - Cambodia"
     	'KOR01'  = "KOR - stratum 01: Lower Secondary/General"
     	'KOR02'  = "KOR - stratum 02: Upper Secondary/General"
     	'KOR03'  = "KOR - stratum 03: Upper Secondary/Vocational"
     	'KOR04'  = "KOR - stratum 04: Mixed/General"
     	'KOR05'  = "KOR - stratum 05: Mixed/Vocational"
     	'KOR97'  = "Undisclosed STRATUM - Korea"
     	'KSV01'  = "KSV - stratum 01: Prishtinë"
     	'KSV02'  = "KSV - stratum 02: Mitrovicë"
     	'KSV03'  = "KSV - stratum 03: Pejë"
     	'KSV04'  = "KSV - stratum 04: Gjakovë"
     	'KSV05'  = "KSV - stratum 05: Prizren"
     	'KSV06'  = "KSV - stratum 06: Ferizaj"
     	'KSV07'  = "KSV - stratum 07: Gjilan"
     	'KSV08'  = "KSV - stratum 08: Large schools"
     	'KSV97'  = "Undisclosed STRATUM - Kosovo"
     	'LTU01'  = "LTU - stratum 01: Lithuanian / Capital / Gymnasium"
     	'LTU02'  = "LTU - stratum 02: Lithuanian / Capital / Basic school"
     	'LTU03'  = "LTU - stratum 03: Lithuanian / Capital / Progymnasium"
     	'LTU04'  = "LTU - stratum 04: Lithuanian / Capital / Other"
     	'LTU05'  = "LTU - stratum 05: Lithuanian / City / Gymnasium"
     	'LTU06'  = "LTU - stratum 06: Lithuanian / City / Basic school"
     	'LTU07'  = "LTU - stratum 07: Lithuanian / City / Progymnasium"
     	'LTU08'  = "LTU - stratum 08: Lithuanian / City / Other"
     	'LTU09'  = "LTU - stratum 09: Lithuanian / Town / Gymnasium"
     	'LTU10'  = "LTU - stratum 10: Lithuanian / Town / Basic school"
     	'LTU11'  = "LTU - stratum 11: Lithuanian / Town / Progymnasium"
     	'LTU12'  = "LTU - stratum 12: Lithuanian / Town / Other"
     	'LTU13'  = "LTU - stratum 13: Lithuanian / Village / Gymnasium"
     	'LTU14'  = "LTU - stratum 14: Lithuanian / Village / Basic school"
     	'LTU15'  = "LTU - stratum 15: Lithuanian / Village / Progymnasium"
     	'LTU16'  = "LTU - stratum 16: Lithuanian / Village / Other"
     	'LTU17'  = "LTU - stratum 17: Russian / N/A / N/A"
     	'LTU18'  = "LTU - stratum 18: Polish / N/A / N/A"
     	'LTU19'  = "LTU - stratum 19: Russian/Polish / N/A / N/A"
     	'LTU20'  = "LTU - stratum 20: Other multi-language / N/A / N/A"
     	'LTU97'  = "Undisclosed STRATUM - Lithuania"
     	'LVA01'  = "LVA - stratum 01: Riga"
     	'LVA02'  = "LVA - stratum 02: City"
     	'LVA03'  = "LVA - stratum 03: Town"
     	'LVA04'  = "LVA - stratum 04: Rural"
     	'LVA97'  = "Undisclosed STRATUM - Latvia"
     	'MAC01'  = "MAC - stratum 01: Government,Grammar-International,Chinese"
     	'MAC02'  = "MAC - stratum 02: Government,Grammar-International,Chinese and Portuguese"
     	'MAC03'  = "MAC - stratum 03: Government,Technical-Vocational,Chinese"
     	'MAC04'  = "MAC - stratum 04: Private-in-Net,Grammar-International,Chinese"
     	'MAC05'  = "MAC - stratum 05: Private-in-Net,Grammar-International,Chinese and English"
     	'MAC06'  = "MAC - stratum 06: Private-in-Net,Grammar-International,English"
     	'MAC07'  = "MAC - stratum 07: Private-in-Net,Technical-Vocational,Chinese"
     	'MAC08'  = "MAC - stratum 08: Private-not-in-Net,Grammar-International,Chinese"
     	'MAC09'  = "MAC - stratum 09: Private-not-in-Net,Grammar-International,English"
     	'MAC10'  = "MAC - stratum 10: Private-not-in-Net,Grammar-International,Portuguese"
     	'MAC97'  = "Undisclosed STRATUM - Macao (China)"
     	'MAR01'  = "MAR - stratum 01: Tanger-Tetouan-Al Hoceima"
     	'MAR02'  = "MAR - stratum 02: Oriental"
     	'MAR03'  = "MAR - stratum 03: Fès-Meknès"
     	'MAR04'  = "MAR - stratum 04: Rabat-Salé-Kénitra"
     	'MAR05'  = "MAR - stratum 05: Béni Mellal-Khénifra"
     	'MAR06'  = "MAR - stratum 06: Casablanca-Settat"
     	'MAR07'  = "MAR - stratum 07: Marrakech-Safi"
     	'MAR08'  = "MAR - stratum 08: Drâa-Tafilalet"
     	'MAR09'  = "MAR - stratum 09: Souss-Massa"
     	'MAR10'  = "MAR - stratum 10: Guelmim-Oued Noun"
     	'MAR11'  = "MAR - stratum 11: Laayoune-Sakia El Hamra"
     	'MAR12'  = "MAR - stratum 12: Eddakhla-Oued Eddahab"
     	'MAR97'  = "Undisclosed STRATUM - Morocco"
     	'MDA01'  = "MDA - stratum 01: Romanian / Big city / ISCED2"
     	'MDA02'  = "MDA - stratum 02: Romanian / Big city / Mixed"
     	'MDA03'  = "MDA - stratum 03: Romanian / Big city / ISCED3"
     	'MDA04'  = "MDA - stratum 04: Romanian / Urban / ISCED2"
     	'MDA05'  = "MDA - stratum 05: Romanian / Urban / Mixed"
     	'MDA06'  = "MDA - stratum 06: Romanian / Urban / ISCED3"
     	'MDA07'  = "MDA - stratum 07: Romanian / Rural / ISCED2"
     	'MDA08'  = "MDA - stratum 08: Romanian / Rural / Mixed"
     	'MDA09'  = "MDA - stratum 09: Romanian / Rural / ISCED3"
     	'MDA10'  = "MDA - stratum 10: Russian / Big city / ISCED2"
     	'MDA11'  = "MDA - stratum 11: Russian / Big city / Mixed"
     	'MDA12'  = "MDA - stratum 12: Russian / Big city / ISCED3"
     	'MDA13'  = "MDA - stratum 13: Russian / Urban / ISCED2"
     	'MDA14'  = "MDA - stratum 14: Russian / Urban / Mixed"
     	'MDA15'  = "MDA - stratum 15: Russian / Urban / ISCED3"
     	'MDA16'  = "MDA - stratum 16: Russian / Rural / ISCED2"
     	'MDA17'  = "MDA - stratum 17: Russian / Rural / Mixed"
     	'MDA18'  = "MDA - stratum 18: Russian / Rural / ISCED3"
     	'MDA19'  = "MDA - stratum 19: Mixed / Big city / ISCED2"
     	'MDA20'  = "MDA - stratum 20: Mixed / Big city / Mixed"
     	'MDA21'  = "MDA - stratum 21: Mixed / Big city / ISCED3"
     	'MDA22'  = "MDA - stratum 22: Mixed / Urban / ISCED2"
     	'MDA23'  = "MDA - stratum 23: Mixed / Urban / Mixed"
     	'MDA24'  = "MDA - stratum 24: Mixed / Urban / ISCED3"
     	'MDA25'  = "MDA - stratum 25: Mixed / Rural / ISCED2"
     	'MDA26'  = "MDA - stratum 26: Mixed / Rural / Mixed"
     	'MDA27'  = "MDA - stratum 27: Mixed / Rural / ISCED3"
     	'MDA97'  = "Undisclosed STRATUM - Republic of Moldova"
     	'MEX01'  = "MEX - stratum 01: Lower secondary,Public,Large"
     	'MEX02'  = "MEX - stratum 02: Lower secondary,Public,Moderately small"
     	'MEX03'  = "MEX - stratum 03: Lower secondary,Public,Small"
     	'MEX04'  = "MEX - stratum 04: Lower secondary,Private,Large"
     	'MEX05'  = "MEX - stratum 05: Lower secondary,Private,Moderately small"
     	'MEX06'  = "MEX - stratum 06: Lower secondary,Private,Small"
     	'MEX07'  = "MEX - stratum 07: Upper secondary,Public,Large"
     	'MEX08'  = "MEX - stratum 08: Upper secondary,Public,Moderately small"
     	'MEX09'  = "MEX - stratum 09: Upper secondary,Public,Small"
     	'MEX10'  = "MEX - stratum 10: Upper secondary,Private,Large"
     	'MEX11'  = "MEX - stratum 11: Upper secondary,Private,Moderately small"
     	'MEX12'  = "MEX - stratum 12: Upper secondary,Private,Small"
     	'MEX97'  = "Undisclosed STRATUM - Mexico"
     	'MKD01'  = "MKD - stratum 01: Macedonian / General"
     	'MKD02'  = "MKD - stratum 02: Macedonian / Mixed"
     	'MKD03'  = "MKD - stratum 03: Macedonian / Vocational"
     	'MKD04'  = "MKD - stratum 04: Mixed / General"
     	'MKD05'  = "MKD - stratum 05: Mixed / Mixed"
     	'MKD06'  = "MKD - stratum 06: Mixed / Vocational"
     	'MKD07'  = "MKD - stratum 07: Albanian / General"
     	'MKD08'  = "MKD - stratum 08: Albanian / Mixed"
     	'MKD09'  = "MKD - stratum 09: Albanian / Vocational"
     	'MKD97'  = "Undisclosed STRATUM - North Macedonia"
     	'MLT01'  = "MLT - stratum 01: State school"
     	'MLT02'  = "MLT - stratum 02: Church school"
     	'MLT03'  = "MLT - stratum 03: Independent school"
     	'MLT97'  = "Undisclosed STRATUM - Malta"
     	'MNE01'  = "MNE - stratum 01: Primary / Central"
     	'MNE02'  = "MNE - stratum 02: Primary / North"
     	'MNE03'  = "MNE - stratum 03: Primary / South"
     	'MNE04'  = "MNE - stratum 04: Gimnazija / Central"
     	'MNE05'  = "MNE - stratum 05: Gimnazija / North"
     	'MNE06'  = "MNE - stratum 06: Gimnazija / South"
     	'MNE07'  = "MNE - stratum 07: Vocational / Central"
     	'MNE08'  = "MNE - stratum 08: Vocational / North"
     	'MNE09'  = "MNE - stratum 09: Vocational / South"
     	'MNE10'  = "MNE - stratum 10: Mixed / Central"
     	'MNE11'  = "MNE - stratum 11: Mixed / North"
     	'MNE12'  = "MNE - stratum 12: Mixed / South"
     	'MNE97'  = "Undisclosed STRATUM - Montenegro"
     	'MNG01'  = "MNG - stratum 01: Kazakh"
     	'MNG03'  = "MNG - stratum 03: Western-other,Suburban"
     	'MNG04'  = "MNG - stratum 04: Western-other,Rural"
     	'MNG06'  = "MNG - stratum 06: Eastern,Suburban"
     	'MNG07'  = "MNG - stratum 07: Eastern,Rural"
     	'MNG08'  = "MNG - stratum 08: Central,Urban"
     	'MNG09'  = "MNG - stratum 09: Central,Suburban"
     	'MNG10'  = "MNG - stratum 10: Central,Rural"
     	'MNG12'  = "MNG - stratum 12: Gobi,Suburban"
     	'MNG13'  = "MNG - stratum 13: Gobi,Rural"
     	'MNG15'  = "MNG - stratum 15: Khangai,Suburban"
     	'MNG16'  = "MNG - stratum 16: Khangai,Rural"
     	'MNG97'  = "Undisclosed STRATUM - Mongolia"
     	'MYS01'  = "MYS - stratum 01: MOE National Secondary School/Other States"
     	'MYS02'  = "MYS - stratum 02: MOE Religious School/Other States"
     	'MYS03'  = "MYS - stratum 03: MOE Technical School/Other States"
     	'MYS04'  = "MYS - stratum 04: MOE Fully Residential School"
     	'MYS05'  = "MYS - stratum 05: non-MOE MARA Junior Science College/Other States"
     	'MYS06'  = "MYS - stratum 06: non-MOE Other Schools/Other States"
     	'MYS07'  = "MYS - stratum 07: Perlis non-“MOE Fully Residential Schools”"
     	'MYS08'  = "MYS - stratum 08: Wilayah Persekutuan Putrajaya non-“MOE Fully Residential Schools”"
     	'MYS09'  = "MYS - stratum 09: Wilayah Persekutuan Labuan non-“MOE Fully Residential Schools”"
     	'MYS97'  = "Undisclosed STRATUM - Malaysia"
     	'NLD01'  = "NLD - stratum 01: PRO"
     	'NLD02'  = "NLD - stratum 02: VMBO-BL/KL"
     	'NLD03'  = "NLD - stratum 03: VMBO-GL/TL"
     	'NLD04'  = "NLD - stratum 04: PRO/VMBO-BL/KL"
     	'NLD05'  = "NLD - stratum 05: PRO/VMBO-BL/KL/GL/TL"
     	'NLD06'  = "NLD - stratum 06: VMBO-BL/KL/GL/TL"
     	'NLD07'  = "NLD - stratum 07: HAVO"
     	'NLD08'  = "NLD - stratum 08: VWO"
     	'NLD09'  = "NLD - stratum 09: HAVO/VWO"
     	'NLD10'  = "NLD - stratum 10: Private Education"
     	'NLD97'  = "Undisclosed STRATUM - Netherlands"
     	'NOR01'  = "NOR - stratum 01: Lower secondary schools"
     	'NOR02'  = "NOR - stratum 02: Upper secondary schools"
     	'NOR97'  = "Undisclosed STRATUM - Norway"
     	'NZL01'  = "NZL - stratum 01: Small (<25)"
     	'NZL02'  = "NZL - stratum 02: Medium (25-150)"
     	'NZL03'  = "NZL - stratum 03: Large (>150)"
     	'NZL97'  = "Undisclosed STRATUM - New Zealand"
     	'PAN01'  = "PAN - stratum 01: INTERNATIONAL/REGULAR/URBAN/PRIVATE"
     	'PAN02'  = "PAN - stratum 02: INTERNATIONAL/REGULAR/RURAL/PRIVATE"
     	'PAN03'  = "PAN - stratum 03: NATIONAL/REGULAR/URBAN/PUBLIC"
     	'PAN04'  = "PAN - stratum 04: NATIONAL/REGULAR/URBAN/PRIVATE"
     	'PAN05'  = "PAN - stratum 05: NATIONAL/REGULAR/RURAL/PUBLIC"
     	'PAN06'  = "PAN - stratum 06: NATIONAL/REGULAR/RURAL/PRIVATE"
     	'PAN07'  = "PAN - stratum 07: NATIONAL/NON-REGULAR/URBAN/PUBLIC"
     	'PAN08'  = "PAN - stratum 08: NATIONAL/NON-REGULAR/URBAN/PRIVATE"
     	'PAN09'  = "PAN - stratum 09: NATIONAL/NON-REGULAR/RURAL/PUBLIC"
     	'PAN10'  = "PAN - stratum 10: NATIONAL/NON-REGULAR/RURAL/PRIVATE"
     	'PAN11'  = "PAN - stratum 11: NATIONAL/MIXED/URBAN/PRIVATE"
     	'PAN12'  = "PAN - stratum 12: NATIONAL/MIXED/RURAL/PRIVATE"
     	'PAN13'  = "PAN - stratum 13: MIXED/REGULAR/URBAN/PRIVATE"
     	'PAN14'  = "PAN - stratum 14: MIXED/MIXED/URBAN/PRIVATE"
     	'PAN15'  = "PAN - stratum 15: MIXED/MIXED/RURAL/PRIVATE"
     	'PAN97'  = "Undisclosed STRATUM - Panama"
     	'PER01'  = "PER - stratum 01: Public,Urban"
     	'PER02'  = "PER - stratum 02: Public,Rural"
     	'PER03'  = "PER - stratum 03: Private,Urban"
     	'PER04'  = "PER - stratum 04: Private,Rural"
     	'PER97'  = "Undisclosed STRATUM - Peru"
     	'PHL01'  = "PHL - stratum 01: REGION 1"
     	'PHL02'  = "PHL - stratum 02: REGION 2"
     	'PHL03'  = "PHL - stratum 03: REGION 3"
     	'PHL04'  = "PHL - stratum 04: REGION 4A"
     	'PHL05'  = "PHL - stratum 05: REGION 4B"
     	'PHL06'  = "PHL - stratum 06: REGION 5"
     	'PHL07'  = "PHL - stratum 07: REGION 6"
     	'PHL08'  = "PHL - stratum 08: REGION 7"
     	'PHL09'  = "PHL - stratum 09: REGION 8"
     	'PHL10'  = "PHL - stratum 10: REGION 9"
     	'PHL11'  = "PHL - stratum 11: REGION 10"
     	'PHL12'  = "PHL - stratum 12: REGION 11"
     	'PHL13'  = "PHL - stratum 13: REGION 12"
     	'PHL14'  = "PHL - stratum 14: NCR"
     	'PHL15'  = "PHL - stratum 15: CAR"
     	'PHL16'  = "PHL - stratum 16: CARAGA"
     	'PHL97'  = "Undisclosed STRATUM - Philippines"
     	'POL01'  = "POL - stratum 01: Primary"
     	'POL02'  = "POL - stratum 02: Licee"
     	'POL03'  = "POL - stratum 03: Secondary Vocational"
     	'POL04'  = "POL - stratum 04: Lower Vocational"
     	'POL97'  = "Undisclosed STRATUM - Poland"
     	'PRT01'  = "PRT - stratum 01: Alentejo Central"
     	'PRT02'  = "PRT - stratum 02: Alentejo Litoral"
     	'PRT03'  = "PRT - stratum 03: Algarve"
     	'PRT04'  = "PRT - stratum 04: Alto Alentejo"
     	'PRT05'  = "PRT - stratum 05: Alto Minho"
     	'PRT06'  = "PRT - stratum 06: Alto Tâmega"
     	'PRT07'  = "PRT - stratum 07: Área Metropolitana de Lisboa"
     	'PRT08'  = "PRT - stratum 08: Área Metropolitana do Porto"
     	'PRT09'  = "PRT - stratum 09: Ave"
     	'PRT10'  = "PRT - stratum 10: Baixo Alentejo"
     	'PRT11'  = "PRT - stratum 11: Beira Baixa"
     	'PRT12'  = "PRT - stratum 12: Beiras e Serra da Estrela"
     	'PRT13'  = "PRT - stratum 13: Cávado"
     	'PRT14'  = "PRT - stratum 14: Douro"
     	'PRT15'  = "PRT - stratum 15: Lezíria do Tejo"
     	'PRT16'  = "PRT - stratum 16: Médio Tejo"
     	'PRT17'  = "PRT - stratum 17: Oeste"
     	'PRT18'  = "PRT - stratum 18: Região Autónoma da Madeira"
     	'PRT19'  = "PRT - stratum 19: Região Autónoma dos Açores"
     	'PRT20'  = "PRT - stratum 20: Região de Aveiro"
     	'PRT21'  = "PRT - stratum 21: Região de Coimbra"
     	'PRT22'  = "PRT - stratum 22: Região de Leiria"
     	'PRT23'  = "PRT - stratum 23: Tâmega e Sousa"
     	'PRT24'  = "PRT - stratum 24: Terras de Trás-os-Montes"
     	'PRT25'  = "PRT - stratum 25: Viseu Dão Lafões"
     	'PRT97'  = "Undisclosed STRATUM - Portugal"
     	'PRY01'  = "PRY - stratum 01: Oficial / Urban / Small"
     	'PRY02'  = "PRY - stratum 02: Oficial / Urban / Medium"
     	'PRY03'  = "PRY - stratum 03: Oficial / Urban / Large"
     	'PRY04'  = "PRY - stratum 04: Oficial / Rural / Small"
     	'PRY05'  = "PRY - stratum 05: Oficial / Rural / Medium"
     	'PRY06'  = "PRY - stratum 06: Oficial / Rural / Large"
     	'PRY07'  = "PRY - stratum 07: Private / Urban / Small"
     	'PRY08'  = "PRY - stratum 08: Private / Urban / Medium"
     	'PRY09'  = "PRY - stratum 09: Private / Urban / Large"
     	'PRY10'  = "PRY - stratum 10: Private / Rural / Small"
     	'PRY11'  = "PRY - stratum 11: Private / Rural / Medium"
     	'PRY12'  = "PRY - stratum 12: Private / Rural / Large"
     	'PRY13'  = "PRY - stratum 13: Subsidized / Urban / Small"
     	'PRY14'  = "PRY - stratum 14: Subsidized / Urban / Medium"
     	'PRY15'  = "PRY - stratum 15: Subsidized / Urban / Large"
     	'PRY16'  = "PRY - stratum 16: Subsidized / Rural / Small"
     	'PRY17'  = "PRY - stratum 17: Subsidized / Rural / Medium"
     	'PRY18'  = "PRY - stratum 18: Subsidized / Rural / Large"
     	'PRY97'  = "Undisclosed STRATUM - Paraguay"
     	'PSE01'  = "PSE - stratum 01: Public,Area C"
     	'PSE02'  = "PSE - stratum 02: Public,JICA Intervention"
     	'PSE03'  = "PSE - stratum 03: Public,Others"
     	'PSE04'  = "PSE - stratum 04: Private,Area C"
     	'PSE05'  = "PSE - stratum 05: Private,JICA Intervention"
     	'PSE06'  = "PSE - stratum 06: Private,Others"
     	'PSE97'  = "Undisclosed STRATUM - Palestinian Authority"
     	'QAT01'  = "QAT - stratum 01: Government"
     	'QAT02'  = "QAT - stratum 02: Community"
     	'QAT03'  = "QAT - stratum 03: International"
     	'QAT04'  = "QAT - stratum 04: Private"
     	'QAT97'  = "Undisclosed STRATUM - Qatar"
     	'QAZ01'  = "QAZ - stratum 01: Urban / Azerbaijani / Public"
     	'QAZ02'  = "QAZ - stratum 02: Urban / Azerbaijani / Private"
     	'QAZ03'  = "QAZ - stratum 03: Suburban / Azerbaijani / Public"
     	'QAZ05'  = "QAZ - stratum 05: Urban / Russian / Public"
     	'QAZ97'  = "Undisclosed STRATUM - Baku (Azerbaijan)"
     	'QCY01'  = "QCY - stratum 01: ISCED2 / General / Public"
     	'QCY02'  = "QCY - stratum 02: Mixed ISCED / General / Public"
     	'QCY03'  = "QCY - stratum 03: Mixed ISCED / General / Private"
     	'QCY04'  = "QCY - stratum 04: Mixed ISCED / Mixed / Public"
     	'QCY05'  = "QCY - stratum 05: ISCED3 / General / Public"
     	'QCY06'  = "QCY - stratum 06: ISCED3 / General / Private"
     	'QCY07'  = "QCY - stratum 07: ISCED3 / Vocational / Public"
     	'QCY08'  = "QCY - stratum 08: ISCED3 / Mixed / Public"
     	'QCY97'  = "Undisclosed STRATUM - Cyprus"
     	'QSC01'  = "QSC - stratum 01: Publicly Funded Non-FE / lowest 20%"
     	'QSC02'  = "QSC - stratum 02: Publicly Funded Non-FE / 2nd lowest20%"
     	'QSC03'  = "QSC - stratum 03: Publicly Funded Non-FE / middle 20%"
     	'QSC04'  = "QSC - stratum 04: Publicly Funded Non-FE / 2nd highest 20%"
     	'QSC05'  = "QSC - stratum 05: Publicly Funded Non-FE / highest 20%"
     	'QSC06'  = "QSC - stratum 06: Publicly Funded Non-FE / missing"
     	'QSC07'  = "QSC - stratum 07: Publicly Funded FE / missing"
     	'QSC08'  = "QSC - stratum 08: Independent / missing"
     	'QSC97'  = "Undisclosed STRATUM - United Kingdom (Scotland)"
     	'QUK01'  = "QUK - stratum 01: England / Academy / Greater London"
     	'QUK02'  = "QUK - stratum 02: England / Academy / Midlands"
     	'QUK03'  = "QUK - stratum 03: England / Academy / North"
     	'QUK04'  = "QUK - stratum 04: England / Academy / South"
     	'QUK05'  = "QUK - stratum 05: England / Independent / Greater London"
     	'QUK06'  = "QUK - stratum 06: England / Independent / Midlands"
     	'QUK07'  = "QUK - stratum 07: England / Independent / North"
     	'QUK08'  = "QUK - stratum 08: England / Independent / South"
     	'QUK09'  = "QUK - stratum 09: England / Maintained / Greater London"
     	'QUK10'  = "QUK - stratum 10: England / Maintained / Midlands"
     	'QUK11'  = "QUK - stratum 11: England / Maintained / North"
     	'QUK12'  = "QUK - stratum 12: England / Maintained / South"
     	'QUK13'  = "QUK - stratum 13: England / Selective / Greater London"
     	'QUK14'  = "QUK - stratum 14: England / Selective / Midlands"
     	'QUK15'  = "QUK - stratum 15: England / Selective / North"
     	'QUK16'  = "QUK - stratum 16: England / Selective / South"
     	'QUK17'  = "QUK - stratum 17: Northern Ireland / Grammar / Belfast"
     	'QUK18'  = "QUK - stratum 18: Northern Ireland / Grammar / North Eastern"
     	'QUK19'  = "QUK - stratum 19: Northern Ireland / Grammar / South Eastern"
     	'QUK20'  = "QUK - stratum 20: Northern Ireland / Grammar / Southern"
     	'QUK21'  = "QUK - stratum 21: Northern Ireland / Grammar / Western"
     	'QUK22'  = "QUK - stratum 22: Northern Ireland / Non grammar / Belfast"
     	'QUK23'  = "QUK - stratum 23: Northern Ireland / Non grammar / North Eastern"
     	'QUK24'  = "QUK - stratum 24: Northern Ireland / Non grammar / South Eastern"
     	'QUK25'  = "QUK - stratum 25: Northern Ireland / Non grammar / Southern"
     	'QUK26'  = "QUK - stratum 26: Northern Ireland / Non grammar / Western"
     	'QUK27'  = "QUK - stratum 27: Wales / Independent / Central South Wales"
     	'QUK28'  = "QUK - stratum 28: Wales / Independent / North Wales"
     	'QUK29'  = "QUK - stratum 29: Wales / Independent / South East Wales"
     	'QUK30'  = "QUK - stratum 30: Wales / Independent / South West and Mid Wales"
     	'QUK31'  = "QUK - stratum 31: Wales / Maintained / Central South Wales"
     	'QUK32'  = "QUK - stratum 32: Wales / Maintained / North Wales"
     	'QUK33'  = "QUK - stratum 33: Wales / Maintained / South East Wales"
     	'QUK34'  = "QUK - stratum 34: Wales / Maintained / South West and Mid Wales"
     	'QUK97'  = "Undisclosed STRATUM - United Kingdom (Excl. Scotland)"
     	'ROU01'  = "ROU - stratum 01: ISCED_2 / Romanian"
     	'ROU02'  = "ROU - stratum 02: ISCED_2 / Hungarian"
     	'ROU03'  = "ROU - stratum 03: ISCED_2 / Mixed"
     	'ROU04'  = "ROU - stratum 04: ISCED_3 / Romanian"
     	'ROU05'  = "ROU - stratum 05: ISCED_3 / Hungarian"
     	'ROU06'  = "ROU - stratum 06: ISCED_3 / Mixed"
     	'ROU97'  = "Undisclosed STRATUM - Romania"
     	'SAU01'  = "SAU - stratum 01: Public/Male/North"
     	'SAU02'  = "SAU - stratum 02: Public/Male/Middle"
     	'SAU03'  = "SAU - stratum 03: Public/Male/South"
     	'SAU04'  = "SAU - stratum 04: Public/Male/East"
     	'SAU05'  = "SAU - stratum 05: Public/Male/West"
     	'SAU06'  = "SAU - stratum 06: Public/Female/North"
     	'SAU07'  = "SAU - stratum 07: Public/Female/Middle"
     	'SAU08'  = "SAU - stratum 08: Public/Female/South"
     	'SAU09'  = "SAU - stratum 09: Public/Female/East"
     	'SAU10'  = "SAU - stratum 10: Public/Female/West"
     	'SAU11'  = "SAU - stratum 11: Private/Male/North"
     	'SAU12'  = "SAU - stratum 12: Private/Male/Middle"
     	'SAU13'  = "SAU - stratum 13: Private/Male/South"
     	'SAU14'  = "SAU - stratum 14: Private/Male/East"
     	'SAU15'  = "SAU - stratum 15: Private/Male/West"
     	'SAU16'  = "SAU - stratum 16: Private/Female/North"
     	'SAU17'  = "SAU - stratum 17: Private/Female/Middle"
     	'SAU18'  = "SAU - stratum 18: Private/Female/South"
     	'SAU19'  = "SAU - stratum 19: Private/Female/East"
     	'SAU20'  = "SAU - stratum 20: Private/Female/West"
     	'SAU21'  = "SAU - stratum 21: International/Male/North"
     	'SAU22'  = "SAU - stratum 22: International/Male/Middle"
     	'SAU23'  = "SAU - stratum 23: International/Male/South"
     	'SAU24'  = "SAU - stratum 24: International/Male/East"
     	'SAU25'  = "SAU - stratum 25: International/Male/West"
     	'SAU26'  = "SAU - stratum 26: International/Female/North"
     	'SAU27'  = "SAU - stratum 27: International/Female/Middle"
     	'SAU28'  = "SAU - stratum 28: International/Female/South"
     	'SAU29'  = "SAU - stratum 29: International/Female/East"
     	'SAU30'  = "SAU - stratum 30: International/Female/West"
     	'SAU97'  = "Undisclosed STRATUM - Saudi Arabia"
     	'SGP01'  = "SGP - stratum 01: Public / Secondary"
     	'SGP02'  = "SGP - stratum 02: Public / Post-secondary"
     	'SGP03'  = "SGP - stratum 03: Private / Secondary"
     	'SGP97'  = "Undisclosed STRATUM - Singapore"
     	'SLV01'  = "SLV - stratum 01: AHUACHAPAN / Rural"
     	'SLV02'  = "SLV - stratum 02: AHUACHAPAN / Urban"
     	'SLV03'  = "SLV - stratum 03: SONSONATE / Rural"
     	'SLV04'  = "SLV - stratum 04: SONSONATE / Urban"
     	'SLV05'  = "SLV - stratum 05: SANTA ANA / Rural"
     	'SLV06'  = "SLV - stratum 06: SANTA ANA / Urban"
     	'SLV07'  = "SLV - stratum 07: LA LIBERTAD / Rural"
     	'SLV08'  = "SLV - stratum 08: LA LIBERTAD / Urban"
     	'SLV09'  = "SLV - stratum 09: CHALATENANGO / Rural"
     	'SLV10'  = "SLV - stratum 10: CHALATENANGO / Urban"
     	'SLV11'  = "SLV - stratum 11: SAN SALVADOR / Rural"
     	'SLV12'  = "SLV - stratum 12: SAN SALVADOR / Urban"
     	'SLV13'  = "SLV - stratum 13: CUSCATLAN / Rural"
     	'SLV14'  = "SLV - stratum 14: CUSCATLAN / Urban"
     	'SLV15'  = "SLV - stratum 15: LA PAZ / Rural"
     	'SLV16'  = "SLV - stratum 16: LA PAZ / Urban"
     	'SLV17'  = "SLV - stratum 17: CABAÑAS / Rural"
     	'SLV18'  = "SLV - stratum 18: CABAÑAS / Urban"
     	'SLV19'  = "SLV - stratum 19: SAN VICENTE / Rural"
     	'SLV20'  = "SLV - stratum 20: SAN VICENTE / Urban"
     	'SLV21'  = "SLV - stratum 21: USULUTAN / Rural"
     	'SLV22'  = "SLV - stratum 22: USULUTAN / Urban"
     	'SLV23'  = "SLV - stratum 23: SAN MIGUEL / Rural"
     	'SLV24'  = "SLV - stratum 24: SAN MIGUEL / Urban"
     	'SLV25'  = "SLV - stratum 25: MORAZAN / Rural"
     	'SLV26'  = "SLV - stratum 26: MORAZAN / Urban"
     	'SLV27'  = "SLV - stratum 27: LA UNIÓN / Rural"
     	'SLV28'  = "SLV - stratum 28: LA UNIÓN / Urban"
     	'SLV97'  = "Undisclosed STRATUM - El Salvador"
     	'SRB01'  = "SRB - stratum 01: Primary"
     	'SRB02'  = "SRB - stratum 02: Voj Gym"
     	'SRB03'  = "SRB - stratum 03: Voj Tech"
     	'SRB04'  = "SRB - stratum 04: Voj Oth"
     	'SRB05'  = "SRB - stratum 05: Voj Mlt"
     	'SRB06'  = "SRB - stratum 06: Bel Gym"
     	'SRB07'  = "SRB - stratum 07: Bel Tech"
     	'SRB08'  = "SRB - stratum 08: Bel Oth"
     	'SRB09'  = "SRB - stratum 09: Bel Mlt"
     	'SRB10'  = "SRB - stratum 10: West Gym"
     	'SRB11'  = "SRB - stratum 11: West Tech"
     	'SRB12'  = "SRB - stratum 12: West Oth"
     	'SRB13'  = "SRB - stratum 13: West Mlt"
     	'SRB14'  = "SRB - stratum 14: East Gym"
     	'SRB15'  = "SRB - stratum 15: East Tech"
     	'SRB16'  = "SRB - stratum 16: East Oth"
     	'SRB17'  = "SRB - stratum 17: East Mlt"
     	'SRB18'  = "SRB - stratum 18: South Gym"
     	'SRB19'  = "SRB - stratum 19: South Tech"
     	'SRB20'  = "SRB - stratum 20: South Oth"
     	'SRB21'  = "SRB - stratum 21: South Mlt"
     	'SRB97'  = "Undisclosed STRATUM - Serbia"
     	'SVK01'  = "SVK - stratum 01: ZŠ,Bratislava"
     	'SVK02'  = "SVK - stratum 02: ZŠ,Trnava"
     	'SVK03'  = "SVK - stratum 03: ZŠ,Nitra"
     	'SVK04'  = "SVK - stratum 04: ZŠ,Trencin"
     	'SVK05'  = "SVK - stratum 05: ZŠ,Banska Bystrica"
     	'SVK06'  = "SVK - stratum 06: ZŠ,Zilina"
     	'SVK07'  = "SVK - stratum 07: ZŠ,Presov"
     	'SVK08'  = "SVK - stratum 08: ZŠ,Kosice"
     	'SVK09'  = "SVK - stratum 09: GYM,Bratislava"
     	'SVK10'  = "SVK - stratum 10: GYM,Trnava"
     	'SVK11'  = "SVK - stratum 11: GYM,Nitra"
     	'SVK12'  = "SVK - stratum 12: GYM,Trencin"
     	'SVK13'  = "SVK - stratum 13: GYM,Banska Bystrica"
     	'SVK14'  = "SVK - stratum 14: GYM,Zilina"
     	'SVK15'  = "SVK - stratum 15: GYM,Presov"
     	'SVK16'  = "SVK - stratum 16: GYM,Kosice"
     	'SVK17'  = "SVK - stratum 17: SŠ,Bratislava"
     	'SVK18'  = "SVK - stratum 18: SŠ,Trnava"
     	'SVK19'  = "SVK - stratum 19: SŠ,Nitra"
     	'SVK20'  = "SVK - stratum 20: SŠ,Trencin"
     	'SVK21'  = "SVK - stratum 21: SŠ,Banska Bystrica"
     	'SVK22'  = "SVK - stratum 22: SŠ,Zilina"
     	'SVK23'  = "SVK - stratum 23: SŠ,Presov"
     	'SVK24'  = "SVK - stratum 24: SŠ,Kosice"
     	'SVK97'  = "Undisclosed STRATUM - Slovak Republic"
     	'SVN01'  = "SVN - stratum 01: GIMg = gymnasia general"
     	'SVN02'  = "SVN - stratum 02: GIMs = gymnasia specialist"
     	'SVN03'  = "SVN - stratum 03: SSI = technical educational programmes"
     	'SVN04'  = "SVN - stratum 04: SPI = vocational of medium duration"
     	'SVN05'  = "SVN - stratum 05: NPI = vocational of short duration"
     	'SVN06'  = "SVN - stratum 06: OS = elementary school"
     	'SVN07'  = "SVN - stratum 07: IO = adult educational programmes"
     	'SVN97'  = "Undisclosed STRATUM - Slovenia"
     	'SWE01'  = "SWE - stratum 01: PUB,LOWER_SEC,METRO"
     	'SWE02'  = "SWE - stratum 02: PUB,LOWER_SEC,LARGE"
     	'SWE03'  = "SWE - stratum 03: PUB,LOWER_SEC,OTHER"
     	'SWE04'  = "SWE - stratum 04: PUB,UPPER_SEC"
     	'SWE05'  = "SWE - stratum 05: IND,LOWER_SEC,METRO"
     	'SWE06'  = "SWE - stratum 06: IND,LOWER_SEC,LARGE"
     	'SWE07'  = "SWE - stratum 07: IND,LOWER_SEC,OTHER"
     	'SWE08'  = "SWE - stratum 08: IND,UPPER_SEC"
     	'SWE97'  = "Undisclosed STRATUM - Sweden"
     	'TAP01'  = "TAP - stratum 01: Junior high (1)/Urban(1)"
     	'TAP02'  = "TAP - stratum 02: Junior high (1)/Suburban(2)"
     	'TAP03'  = "TAP - stratum 03: Junior high (1)/Rural(3)"
     	'TAP04'  = "TAP - stratum 04: Regular senior secondary (2)/Urban(1)"
     	'TAP05'  = "TAP - stratum 05: Regular senior secondary (2)/Suburban(2)"
     	'TAP06'  = "TAP - stratum 06: Regular senior secondary (2)/ Rural(3)"
     	'TAP07'  = "TAP - stratum 07: Skill-based senior secondary (3)/Urban(1)"
     	'TAP08'  = "TAP - stratum 08: Skill-based senior secondary (3)/Suburban(2)"
     	'TAP09'  = "TAP - stratum 09: Skill-based senior secondary (3)/Rural(3)"
     	'TAP10'  = "TAP - stratum 10: Comprehensive senior secondary (4)/Urban(1)"
     	'TAP11'  = "TAP - stratum 11: Comprehensive senior secondary (4)/Suburban(2)"
     	'TAP12'  = "TAP - stratum 12: Comprehensive senior secondary (4)/Rural(3)"
     	'TAP13'  = "TAP - stratum 13: Comprehensive junior-senior high (5)/Urban(1)"
     	'TAP14'  = "TAP - stratum 14: Comprehensive junior-senior high (5)/Suburban(2)"
     	'TAP15'  = "TAP - stratum 15: Comprehensive junior-senior high (5)/Rural(3)"
     	'TAP16'  = "TAP - stratum 16: Five-year junior college (6)/Urban(1)"
     	'TAP17'  = "TAP - stratum 17: Five-year junior college (6)/Suburban(2)"
     	'TAP18'  = "TAP - stratum 18: Five-year junior college (6)/Rural(3)"
     	'TAP97'  = "Undisclosed STRATUM - Chinese Taipei"
     	'THA01'  = "THA - stratum 01: OBEC/ISCED2 only"
     	'THA02'  = "THA - stratum 02: OBEC/Mixed"
     	'THA03'  = "THA - stratum 03: OBEC/ISCED3 only"
     	'THA04'  = "THA - stratum 04: OPEC/ISCED2 only"
     	'THA05'  = "THA - stratum 05: OPEC/Mixed"
     	'THA06'  = "THA - stratum 06: DBMA/ISCED2 only"
     	'THA07'  = "THA - stratum 07: DBMA/Mixed"
     	'THA08'  = "THA - stratum 08: DLCA/ISCED2 only"
     	'THA09'  = "THA - stratum 09: DLCA/Mixed"
     	'THA10'  = "THA - stratum 10: DLCA/ISCED3 only"
     	'THA11'  = "THA - stratum 11: HESI/ISCED2 only, Mixed, & ISCED3 only"
     	'THA12'  = "THA - stratum 12: OVEC/ISCED3 only"
     	'THA13'  = "THA - stratum 13: SSMS/Mixed"
     	'THA14'  = "THA - stratum 14: SSMS/ISCED3 only"
     	'THA97'  = "Undisclosed STRATUM - Thailand"
     	'TUR01'  = "TUR - stratum 01: Lower-Secondary School"
     	'TUR02'  = "TUR - stratum 02: Science High School - A"
     	'TUR03'  = "TUR - stratum 03: Science High School - B"
     	'TUR04'  = "TUR - stratum 04: Science High School - C"
     	'TUR05'  = "TUR - stratum 05: Social Sciences High School - A"
     	'TUR06'  = "TUR - stratum 06: Social Sciences High School - B"
     	'TUR07'  = "TUR - stratum 07: Social Sciences High School - C"
     	'TUR08'  = "TUR - stratum 08: Anatolian High School- A"
     	'TUR09'  = "TUR - stratum 09: Anatolian High School- B"
     	'TUR10'  = "TUR - stratum 10: Anatolian High School- C"
     	'TUR11'  = "TUR - stratum 11: Anatolian High School- D"
     	'TUR12'  = "TUR - stratum 12: Anatolian High School- E"
     	'TUR13'  = "TUR - stratum 13: Anatolian High School- F"
     	'TUR14'  = "TUR - stratum 14: Anatolian High School- G"
     	'TUR15'  = "TUR - stratum 15: Anatolian High School- H"
     	'TUR16'  = "TUR - stratum 16: Anatolian High School- I"
     	'TUR17'  = "TUR - stratum 17: Anatolian High School- J"
     	'TUR18'  = "TUR - stratum 18: Anatolian High School- K"
     	'TUR19'  = "TUR - stratum 19: Anatolian Imam and Preacher High School - A"
     	'TUR20'  = "TUR - stratum 20: Anatolian Imam and Preacher High School - B"
     	'TUR21'  = "TUR - stratum 21: Anatolian Imam and Preacher High School - C"
     	'TUR22'  = "TUR - stratum 22: Anatolian Imam and Preacher High School - D"
     	'TUR23'  = "TUR - stratum 23: Anatolian Imam and Preacher High School - E"
     	'TUR24'  = "TUR - stratum 24: Anatolian Imam and Preacher High School - F"
     	'TUR25'  = "TUR - stratum 25: Anatolian Imam and Preacher High School - G"
     	'TUR26'  = "TUR - stratum 26: Anatolian Imam and Preacher High School - H"
     	'TUR27'  = "TUR - stratum 27: Anatolian Sport High School/ Anatolian Fine Arts High School"
     	'TUR28'  = "TUR - stratum 28: Vocational and Technical Anatolian High School - A"
     	'TUR29'  = "TUR - stratum 29: Vocational and Technical Anatolian High School - B"
     	'TUR30'  = "TUR - stratum 30: Vocational and Technical Anatolian High School - C"
     	'TUR31'  = "TUR - stratum 31: Vocational and Technical Anatolian High School - D"
     	'TUR32'  = "TUR - stratum 32: Vocational and Technical Anatolian High School - E"
     	'TUR33'  = "TUR - stratum 33: Vocational and Technical Anatolian High School - F"
     	'TUR34'  = "TUR - stratum 34: Vocational and Technical Anatolian High School - G"
     	'TUR35'  = "TUR - stratum 35: Vocational and Technical Anatolian High School - H"
     	'TUR36'  = "TUR - stratum 36: Vocational and Technical Anatolian High School - I"
     	'TUR97'  = "Undisclosed STRATUM - Türkiye"
     	'UKR01'  = "UKR - stratum 01: Urban/Vinnytsia"
     	'UKR02'  = "UKR - stratum 02: Urban/ Volyn’"
     	'UKR03'  = "UKR - stratum 03: Urban/ Dnipropetrovsk"
     	'UKR04'  = "UKR - stratum 04: Urban/ Donetsk"
     	'UKR05'  = "UKR - stratum 05: Urban/ Zhytomyr"
     	'UKR06'  = "UKR - stratum 06: Urban/ Zakarpattia"
     	'UKR07'  = "UKR - stratum 07: Urban/ Zaporizhzhia"
     	'UKR08'  = "UKR - stratum 08: Urban/ Ivano-Frankivsk"
     	'UKR09'  = "UKR - stratum 09: Urban/ Kyiv region"
     	'UKR10'  = "UKR - stratum 10: Urban/ Kirovohrad"
     	'UKR11'  = "UKR - stratum 11: Urban/ Luhans’k"
     	'UKR12'  = "UKR - stratum 12: Urban/ L’viv"
     	'UKR13'  = "UKR - stratum 13: Urban/ Mykolaiv"
     	'UKR14'  = "UKR - stratum 14: Urban/ Odesa"
     	'UKR15'  = "UKR - stratum 15: Urban/ Poltava"
     	'UKR16'  = "UKR - stratum 16: Urban/ Rivne"
     	'UKR17'  = "UKR - stratum 17: Urban/ Sumy"
     	'UKR18'  = "UKR - stratum 18: Urban/ Ternopil’"
     	'UKR19'  = "UKR - stratum 19: Urban/ Kharkiv"
     	'UKR20'  = "UKR - stratum 20: Urban/ Kherson"
     	'UKR21'  = "UKR - stratum 21: Urban/ Khmel’nyts’kyi"
     	'UKR22'  = "UKR - stratum 22: Urban/ Cherkasy"
     	'UKR23'  = "UKR - stratum 23: Urban/ Chernivtsi"
     	'UKR24'  = "UKR - stratum 24: Urban/ Chernihiv"
     	'UKR25'  = "UKR - stratum 25: Urban/ Kyiv City"
     	'UKR26'  = "UKR - stratum 26: Rural/Vinnytsia"
     	'UKR27'  = "UKR - stratum 27: Rural/ Volyn’"
     	'UKR28'  = "UKR - stratum 28: Rural/ Dnipropetrovsk"
     	'UKR29'  = "UKR - stratum 29: Rural/ Donetsk"
     	'UKR30'  = "UKR - stratum 30: Rural/ Zhytomyr"
     	'UKR31'  = "UKR - stratum 31: Rural/ Zakarpattia"
     	'UKR32'  = "UKR - stratum 32: Rural/ Zaporizhzhia"
     	'UKR33'  = "UKR - stratum 33: Rural/ Ivano-Frankivsk"
     	'UKR34'  = "UKR - stratum 34: Rural/ Kyiv Region"
     	'UKR35'  = "UKR - stratum 35: Rural/ Kirovohrad"
     	'UKR36'  = "UKR - stratum 36: Rural/ Luhans’k"
     	'UKR37'  = "UKR - stratum 37: Rural/ L’viv"
     	'UKR38'  = "UKR - stratum 38: Rural/ Mykolaiv"
     	'UKR39'  = "UKR - stratum 39: Rural/ Odesa"
     	'UKR40'  = "UKR - stratum 40: Rural/ Poltava"
     	'UKR41'  = "UKR - stratum 41: Rural/ Rivne"
     	'UKR42'  = "UKR - stratum 42: Rural/ Sumy"
     	'UKR43'  = "UKR - stratum 43: Rural/ Ternopil’"
     	'UKR44'  = "UKR - stratum 44: Rural/ Kharkiv"
     	'UKR45'  = "UKR - stratum 45: Rural/ Kherson"
     	'UKR46'  = "UKR - stratum 46: Rural/ Khmel’nyts’kyi"
     	'UKR47'  = "UKR - stratum 47: Rural/ Cherkasy"
     	'UKR48'  = "UKR - stratum 48: Rural/ Chernivtsi"
     	'UKR49'  = "UKR - stratum 49: Rural/Chernihiv"
     	'UKR97'  = "Undisclosed STRATUM - Ukraine"
     	'URY01'  = "URY - stratum 01: Public General Secondary Schools & Military School / Lower secondary only"
     	'URY02'  = "URY - stratum 02: Public General Secondary Schools & Military School / Mixed"
     	'URY03'  = "URY - stratum 03: Public General Secondary Schools & Military School / Upper secondary only"
     	'URY04'  = "URY - stratum 04: Private General Secondary Schools / Lower secondary only"
     	'URY05'  = "URY - stratum 05: Private General Secondary Schools / Mixed"
     	'URY06'  = "URY - stratum 06: Private General Secondary Schools / Upper secondary only"
     	'URY07'  = "URY - stratum 07: Public Technical Secondary Schools / Lower secondary only"
     	'URY08'  = "URY - stratum 08: Public Technical Secondary Schools / Mixed"
     	'URY09'  = "URY - stratum 09: Public Technical Secondary Schools / Upper secondary only"
     	'URY10'  = "URY - stratum 10: Rural Schools with Lower Secondary Degree / Lower secondary only"
     	'URY97'  = "Undisclosed STRATUM - Uruguay"
     	'USA01'  = "USA - stratum 01: Northeast-Private"
     	'USA02'  = "USA - stratum 02: Northeast-Public"
     	'USA03'  = "USA - stratum 03: Midwest-Private"
     	'USA04'  = "USA - stratum 04: Midwest-Public"
     	'USA05'  = "USA - stratum 05: South-Private"
     	'USA06'  = "USA - stratum 06: South-Public"
     	'USA07'  = "USA - stratum 07: West-Private"
     	'USA08'  = "USA - stratum 08: West-Public"
     	'USA97'  = "Undisclosed STRATUM - United States"
     	'UZB01'  = "UZB - stratum 01: Republic of Karakalpakstan/Urban"
     	'UZB02'  = "UZB - stratum 02: Republic of Karakalpakstan/Rural"
     	'UZB03'  = "UZB - stratum 03: Andijan/Urban"
     	'UZB04'  = "UZB - stratum 04: Andijan/Rural"
     	'UZB05'  = "UZB - stratum 05: Bukhara/Urban"
     	'UZB06'  = "UZB - stratum 06: Bukhara/Rural"
     	'UZB07'  = "UZB - stratum 07: Jizzakh/Urban"
     	'UZB08'  = "UZB - stratum 08: Jizzakh/Rural"
     	'UZB09'  = "UZB - stratum 09: Kashkadarya/Urban"
     	'UZB10'  = "UZB - stratum 10: Kashkadarya/Rural"
     	'UZB11'  = "UZB - stratum 11: Navoi/Urban"
     	'UZB12'  = "UZB - stratum 12: Navoi/Rural"
     	'UZB13'  = "UZB - stratum 13: Namangan/Urban"
     	'UZB14'  = "UZB - stratum 14: Namangan/Rural"
     	'UZB15'  = "UZB - stratum 15: Samarkand/Urban"
     	'UZB16'  = "UZB - stratum 16: Samarkand/Rural"
     	'UZB17'  = "UZB - stratum 17: Surkhandarya/Urban"
     	'UZB18'  = "UZB - stratum 18: Surkhandarya/Rural"
     	'UZB19'  = "UZB - stratum 19: Sirdarya/Urban"
     	'UZB20'  = "UZB - stratum 20: Sirdarya/Rural"
     	'UZB21'  = "UZB - stratum 21: Tashkent/Urban"
     	'UZB22'  = "UZB - stratum 22: Tashkent/Rural"
     	'UZB23'  = "UZB - stratum 23: Fergana/Urban"
     	'UZB24'  = "UZB - stratum 24: Fergana/Rural"
     	'UZB25'  = "UZB - stratum 25: Khorezm/Urban"
     	'UZB26'  = "UZB - stratum 26: Khorezm/Rural"
     	'UZB27'  = "UZB - stratum 27: Tashkent city/Urban"
     	'UZB97'  = "Undisclosed STRATUM - Uzbekistan"
     	'VNM01'  = "VNM - stratum 01: Northern Vietnam / >50% public funding / Urban"
     	'VNM02'  = "VNM - stratum 02: Northern Vietnam / >50% public funding / Rural"
     	'VNM03'  = "VNM - stratum 03: Northern Vietnam / >50% public funding / Remote area"
     	'VNM04'  = "VNM - stratum 04: Northern Vietnam / <50% public funding / Urban"
     	'VNM05'  = "VNM - stratum 05: Northern Vietnam / <50% public funding / Rural and Remote area"
     	'VNM06'  = "VNM - stratum 06: Central Vietnam / >50% public funding / Urban"
     	'VNM07'  = "VNM - stratum 07: Central Vietnam / >50% public funding / Rural"
     	'VNM08'  = "VNM - stratum 08: Central Vietnam / >50% public funding / Remote area"
     	'VNM09'  = "VNM - stratum 09: Central Vietnam / <50% public funding / Urban"
     	'VNM10'  = "VNM - stratum 10: Central Vietnam / <50% public funding / Rural and Remote area"
     	'VNM11'  = "VNM - stratum 11: Southern Vietnam / >50% public funding / Urban"
     	'VNM12'  = "VNM - stratum 12: Southern Vietnam / >50% public funding / Rural"
     	'VNM13'  = "VNM - stratum 13: Southern Vietnam / >50% public funding / Remote area"
     	'VNM14'  = "VNM - stratum 14: Southern Vietnam / <50% public funding / Urban"
     	'VNM15'  = "VNM - stratum 15: Southern Vietnam / <50% public funding / Rural"
     	'VNM97'  = "Undisclosed STRATUM - Viet Nam"
     ;
     value $ SUBNATIOF
     	'0080000'  = "Albania"
     	'0310000'  = "Baku (Azerbaijan)"
     	'0320000'  = "Argentina: Rest of the country"
     	'0320100'  = "Argentina: CABA"
     	'0320200'  = "Argentina: Cordoba"
     	'0320300'  = "Argentina: Mendoza"
     	'0360000'  = "Australia"
     	'0400000'  = "Austria"
     	'0560000'  = "Belgium: Rest of the country"
     	'0560100'  = "Belgium: Flemish community"
     	'0760000'  = "Brazil"
     	'0960000'  = "Brunei Darussalam"
     	'1000000'  = "Bulgaria"
     	'1160000'  = "Cambodia"
     	'1240000'  = "Canada"
     	'1520000'  = "Chile"
     	'1580000'  = "Chinese Taipei"
     	'1700000'  = "Colombia"
     	'1880000'  = "Costa Rica"
     	'1910000'  = "Croatia"
     	'1960000'  = "Cyprus"
     	'2030000'  = "Czech Republic"
     	'2080000'  = "Denmark"
     	'2140000'  = "Dominican Republic"
     	'2220000'  = "El Salvador"
     	'2330000'  = "Estonia"
     	'2460000'  = "Finland"
     	'2500000'  = "France"
     	'2680000'  = "Georgia"
     	'2750000'  = "Palestinian Authority"
     	'2760000'  = "Germany"
     	'3000000'  = "Greece"
     	'3200000'  = "Guatemala"
     	'3440000'  = "Hong Kong (China)"
     	'3480000'  = "Hungary"
     	'3520000'  = "Iceland"
     	'3600000'  = "Indonesia"
     	'3720000'  = "Ireland"
     	'3760000'  = "Israel"
     	'3800000'  = "Italy"
     	'3830000'  = "Kosovo"
     	'3880000'  = "Jamaica"
     	'3920000'  = "Japan"
     	'3980000'  = "Kazakhstan"
     	'4000000'  = "Jordan"
     	'4100000'  = "Korea"
     	'4280000'  = "Latvia"
     	'4400000'  = "Lithuania"
     	'4460000'  = "Macao (China)"
     	'4580000'  = "Malaysia"
     	'4700000'  = "Malta"
     	'4840000'  = "Mexico"
     	'4960000'  = "Mongolia"
     	'4980000'  = "Republic of Moldova"
     	'4990000'  = "Montenegro"
     	'5040000'  = "Morocco"
     	'5280000'  = "Netherlands"
     	'5540000'  = "New Zealand"
     	'5780000'  = "Norway"
     	'5910000'  = "Panama"
     	'6000000'  = "Paraguay"
     	'6040000'  = "Peru"
     	'6080000'  = "Philippines"
     	'6160000'  = "Poland"
     	'6200000'  = "Portugal"
     	'6340000'  = "Qatar"
     	'6420000'  = "Romania"
     	'6820000'  = "Saudi Arabia"
     	'6880000'  = "Serbia"
     	'7020000'  = "Singapore"
     	'7030000'  = "Slovak Republic"
     	'7040000'  = "Viet Nam"
     	'7050000'  = "Slovenia"
     	'7240000'  = "Spain"
     	'7520000'  = "Sweden"
     	'7560000'  = "Switzerland"
     	'7640000'  = "Thailand"
     	'7840000'  = "United Arab Emirates: Rest of the country"
     	'7840100'  = "United Arab Emirates: Abu Dhabi"
     	'7840200'  = "United Arab Emirates: Dubai"
     	'7840300'  = "United Arab Emirates: Sharjah"
     	'7920000'  = "Türkiye"
     	'8070000'  = "North Macedonia"
     	'8260000'  = "Great Britain: Rest of the country"
     	'8262000'  = "Great Britain: Scotland"
     	'8400000'  = "United States"
     	'8580000'  = "Uruguay"
     	'8600000'  = "Uzbekistan"
     	'9010000'  = "Ukraine"
     	'9999997'  = "Not Applicable"
     	'9999998'  = "Invalid"
     	'9999999'  = "Missing"
     ;
run;
data &DataFile;
     set DataLib.&DataFile;
     format 
     DMA121Q02RA DMA162Q02RCF.
     DMA134Q01RA DMA162Q02RCF.
     DMA128Q01RA DMA162Q02RCF.
     DMA121Q02RB DMA162Q02RCF.
     DMA128Q01RC DMA162Q02RCF.
     DMA126Q02RB DMA162Q02RCF.
     DMA134Q01RD DMA162Q02RCF.
     DMA162Q02RC DMA162Q02RCF.
     DMA128Q01RB DMA162Q02RCF.
     DMA161Q03RB DMA162Q02RCF.
     DMA126Q02RF DMA162Q02RCF.
     DMA126Q02RI DMA162Q02RCF.
     DMA161Q01RC DMA162Q02RCF.
     DMA126Q02RJ DMA162Q02RCF.
     DMA134Q01RC DMA162Q02RCF.
     DMA126Q02RH DMA162Q02RCF.
     DMA126Q02RL DMA162Q02RCF.
     DMA161Q01RB DMA162Q02RCF.
     DMA161Q03RA DMA162Q02RCF.
     DMA126Q02RA DMA162Q02RCF.
     DMA126Q02RD DMA162Q02RCF.
     DMA160Q02RB DMA162Q02RCF.
     DMA126Q02RE DMA162Q02RCF.
     DMA126Q02RK DMA162Q02RCF.
     DMA134Q01RB DMA162Q02RCF.
     DMA161Q01RA DMA162Q02RCF.
     DMA121Q02RC DMA162Q02RCF.
     DMA162Q02RB DMA162Q02RCF.
     DMA128Q01RD DMA162Q02RCF.
     DMA162Q02RA DMA162Q02RCF.
     DMA160Q02RA DMA162Q02RCF.
     DMA126Q02RC DMA162Q02RCF.
     DMA126Q02RG DMA162Q02RCF.
     CR560Q08VS CR570Q10VSF.
     CM953Q04V CR570Q10VSF.
     CMA130Q01A CR570Q10VSF.
     CMA131Q01VS CR570Q10VSF.
     CM571Q01V CR570Q10VSF.
     CMA146Q01VS CR570Q10VSF.
     CF069Q01VS CR570Q10VSF.
     CR569Q03A CR570Q10VSF.
     CMA131Q04V CR570Q10VSF.
     CR570Q02V CR570Q10VSF.
     CR545Q02V CR570Q10VSF.
     CR566Q14VS CR570Q10VSF.
     CMA130Q03V CR570Q10VSF.
     CMA111Q03V CR570Q10VSF.
     CR559Q08A CR570Q10VSF.
     CR570Q01A CR570Q10VSF.
     CR569Q04V CR570Q10VSF.
     CF095Q02VS CR570Q10VSF.
     CM905Q01A CR570Q10VSF.
     CR541Q09V CR570Q10VSF.
     CR544Q12VS CR570Q10VSF.
     CR567Q10VS CR570Q10VSF.
     CR432Q05VS CR570Q10VSF.
     CMA134Q02VS CR570Q10VSF.
     CMA139Q01A CR570Q10VSF.
     CMA136Q03A CR570Q10VSF.
     CM954Q04A CR570Q10VSF.
     CR570Q05A CR570Q10VSF.
     CR456Q01A CR570Q10VSF.
     CMA135Q03VS CR570Q10VSF.
     CR570Q02VS CR570Q10VSF.
     CMA102Q03VS CR570Q10VSF.
     CM474Q01A CR570Q10VSF.
     CMA123Q01V CR570Q10VSF.
     CMA148Q03V CR570Q10VSF.
     CM155Q02A CR570Q10VSF.
     CR453Q05VS CR570Q10VSF.
     CR568Q15V CR570Q10VSF.
     CR559Q01A CR570Q10VSF.
     CMA142Q02VS CR570Q10VSF.
     CR453Q05A CR570Q10VSF.
     CMA114Q01VS CR570Q10VSF.
     CF308Q03V CR570Q10VSF.
     CMA127Q02V CR570Q10VSF.
     CF082Q01V CR570Q10VSF.
     CR570Q08A CR570Q10VSF.
     CF401Q01VS CR570Q10VSF.
     CM905Q02A CR570Q10VSF.
     CMA154Q03A CR570Q10VSF.
     CR567Q04V CR570Q10VSF.
     CF054Q01V CR570Q10VSF.
     CR460Q06V CR570Q10VSF.
     CR541Q04A CR570Q10VSF.
     CMA108Q02A CR570Q10VSF.
     CMA128Q03VS CR570Q10VSF.
     CM00GQ01VS CR570Q10VSF.
     CMA160Q03A CR570Q10VSF.
     CR567Q06VS CR570Q10VSF.
     CR567Q10V CR570Q10VSF.
     CMA141Q02VS CR570Q10VSF.
     CMA114Q03VS CR570Q10VSF.
     CF097Q01V CR570Q10VSF.
     CMA146Q01V CR570Q10VSF.
     CF300Q02A CR570Q10VSF.
     CMA108Q01V CR570Q10VSF.
     CM559Q01V CR570Q10VSF.
     CMA141Q04VS CR570Q10VSF.
     CM953Q02V CR570Q10VSF.
     CMA161Q02V CR570Q10VSF.
     CF201Q01V CR570Q10VSF.
     CM998Q02V CR570Q10VSF.
     CR220Q02VS CR570Q10VSF.
     CM948Q01VS CR570Q10VSF.
     CR560Q03A CR570Q10VSF.
     CMA143Q03VS CR570Q10VSF.
     CM948Q03VS CR570Q10VSF.
     CMA141Q01A CR570Q10VSF.
     CR404Q06VS CR570Q10VSF.
     CM803Q01V CR570Q10VSF.
     CM462Q01VS CR570Q10VSF.
     CR556Q03V CR570Q10VSF.
     CMA143Q01V CR570Q10VSF.
     CM408Q01V CR570Q10VSF.
     CF307Q01VS CR570Q10VSF.
     CMA160Q01V CR570Q10VSF.
     CMA153Q01A CR570Q10VSF.
     CR055Q01A CR570Q10VSF.
     CR553Q05VS CR570Q10VSF.
     CMA146Q03A CR570Q10VSF.
     CM446Q02A CR570Q10VSF.
     CR562Q07V CR570Q10VSF.
     CR547Q07A CR570Q10VSF.
     CR563Q12V CR570Q10VSF.
     CR562Q07A CR570Q10VSF.
     CM803Q01A CR570Q10VSF.
     CF012Q01V CR570Q10VSF.
     CR550Q09A CR570Q10VSF.
     CR111Q02BA CR570Q10VSF.
     CR544Q04VS CR570Q10VSF.
     CMA129Q02A CR570Q10VSF.
     CR055Q05A CR570Q10VSF.
     CMA105Q03A CR570Q10VSF.
     CMA129Q03V CR570Q10VSF.
     CM603Q01VS CR570Q10VSF.
     CF012Q01VS CR570Q10VSF.
     CMA149Q02VS CR570Q10VSF.
     CR550Q04VS CR570Q10VSF.
     CF068Q01A CR570Q10VSF.
     CR562Q03VS CR570Q10VSF.
     CR111Q02BV CR570Q10VSF.
     CR569Q02VS CR570Q10VSF.
     CR569Q06A CR570Q10VSF.
     CR553Q01A CR570Q10VSF.
     CMA143Q04A CR570Q10VSF.
     CF024Q02VS CR570Q10VSF.
     CM564Q01A CR570Q10VSF.
     CMA153Q02V CR570Q10VSF.
     CMA162Q03A CR570Q10VSF.
     CR552Q01VS CR570Q10VSF.
     CR544Q07VS CR570Q10VSF.
     CR552Q08V CR570Q10VSF.
     CR466Q02V CR570Q10VSF.
     CR552Q09VS CR570Q10VSF.
     CMA151Q02A CR570Q10VSF.
     CMA144Q01A CR570Q10VSF.
     CMA147Q02V CR570Q10VSF.
     CMA142Q01A CR570Q10VSF.
     CR552Q01V CR570Q10VSF.
     CR541Q05VS CR570Q10VSF.
     CR220Q06A CR570Q10VSF.
     CR543Q03V CR570Q10VSF.
     CR219Q02A CR570Q10VSF.
     CR543Q15A CR570Q10VSF.
     CMA161Q04V CR570Q10VSF.
     CR544Q10VS CR570Q10VSF.
     CMA135Q02VS CR570Q10VSF.
     CR563Q09VS CR570Q10VSF.
     CM955Q03A CR570Q10VSF.
     CR563Q12A CR570Q10VSF.
     CM273Q01A CR570Q10VSF.
     CMA150Q03V CR570Q10VSF.
     CM571Q01A CR570Q10VSF.
     CR566Q03V CR570Q10VSF.
     CR456Q06VS CR570Q10VSF.
     CR567Q13VS CR570Q10VSF.
     CF103Q01V CR570Q10VSF.
     CM955Q02VS CR570Q10VSF.
     CM919Q01A CR570Q10VSF.
     CR567Q04VS CR570Q10VSF.
     CMA116Q01A CR570Q10VSF.
     CM273Q01V CR570Q10VSF.
     CMA134Q02V CR570Q10VSF.
     CF033Q02VS CR570Q10VSF.
     CF058Q01V CR570Q10VSF.
     CR567Q11V CR570Q10VSF.
     CMA134Q01A CR570Q10VSF.
     CF303Q01V CR570Q10VSF.
     CF303Q03V CR570Q10VSF.
     CMA138Q02VS CR570Q10VSF.
     CR556Q01V CR570Q10VSF.
     CF308Q02V CR570Q10VSF.
     CMA162Q01A CR570Q10VSF.
     CF103Q01A CR570Q10VSF.
     CMA150Q03VS CR570Q10VSF.
     CR567Q03V CR570Q10VSF.
     CF303Q02A CR570Q10VSF.
     CF097Q01VS CR570Q10VSF.
     CR569Q06VS CR570Q10VSF.
     CM954Q01VS CR570Q10VSF.
     CR567Q11VS CR570Q10VSF.
     CMA116Q02A CR570Q10VSF.
     CR544Q13VS CR570Q10VSF.
     CF106Q02V CR570Q10VSF.
     CR556Q03A CR570Q10VSF.
     CMA131Q02V CR570Q10VSF.
     CF106Q02A CR570Q10VSF.
     CMA136Q03VS CR570Q10VSF.
     CMA128Q03A CR570Q10VSF.
     CM559Q01A CR570Q10VSF.
     CMA137Q01V CR570Q10VSF.
     CM943Q02V CR570Q10VSF.
     CMA111Q01VS CR570Q10VSF.
     CM954Q01A CR570Q10VSF.
     CF051Q01V CR570Q10VSF.
     CM828Q02A CR570Q10VSF.
     CM943Q01VS CR570Q10VSF.
     CMA103Q04V CR570Q10VSF.
     CM033Q01V CR570Q10VSF.
     CMA103Q05VS CR570Q10VSF.
     CM943Q02VS CR570Q10VSF.
     CR220Q01V CR570Q10VSF.
     CM828Q03V CR570Q10VSF.
     CM828Q03VS CR570Q10VSF.
     CMA130Q03VS CR570Q10VSF.
     CR544Q14VS CR570Q10VSF.
     CMA147Q01VS CR570Q10VSF.
     CR560Q06V CR570Q10VSF.
     CMA116Q02VS CR570Q10VSF.
     CM948Q03A CR570Q10VSF.
     CMA131Q02A CR570Q10VSF.
     CM155Q01VS CR570Q10VSF.
     CR543Q01V CR570Q10VSF.
     CR404Q03V CR570Q10VSF.
     CR544Q10A CR570Q10VSF.
     CR404Q07V CR570Q10VSF.
     CR460Q01V CR570Q10VSF.
     CMA110Q01A CR570Q10VSF.
     CR549Q06VS CR570Q10VSF.
     CR549Q04VS CR570Q10VSF.
     CR561Q06A CR570Q10VSF.
     CR460Q01A CR570Q10VSF.
     CF303Q02V CR570Q10VSF.
     CMA112Q03VS CR570Q10VSF.
     CR460Q06A CR570Q10VSF.
     CR561Q07V CR570Q10VSF.
     CR561Q04A CR570Q10VSF.
     CM992Q01VS CR570Q10VSF.
     CMA157Q02VS CR570Q10VSF.
     CMA123Q02V CR570Q10VSF.
     CMA119Q03VS CR570Q10VSF.
     CR561Q01A CR570Q10VSF.
     CMA119Q02A CR570Q10VSF.
     CMA133Q02A CR570Q10VSF.
     CR542Q01V CR570Q10VSF.
     CMA105Q04VS CR570Q10VSF.
     CMA157Q02V CR570Q10VSF.
     CM564Q02VS CR570Q10VSF.
     CR460Q06VS CR570Q10VSF.
     CM411Q01A CR570Q10VSF.
     CMA115Q01A CR570Q10VSF.
     CM982Q04V CR570Q10VSF.
     CR540Q06A CR570Q10VSF.
     CR561Q04V CR570Q10VSF.
     CMA105Q05V CR570Q10VSF.
     CR568Q14VS CR570Q10VSF.
     CR568Q14V CR570Q10VSF.
     CR455Q04V CR570Q10VSF.
     CR561Q03V CR570Q10VSF.
     CR542Q08A CR570Q10VSF.
     CMA112Q02V CR570Q10VSF.
     CR542Q01A CR570Q10VSF.
     CM992Q02A CR570Q10VSF.
     CMA144Q01VS CR570Q10VSF.
     CM982Q04VS CR570Q10VSF.
     CR540Q04V CR570Q10VSF.
     CR564Q05V CR570Q10VSF.
     CM949Q02VS CR570Q10VSF.
     CR549Q05V CR570Q10VSF.
     CR540Q01A CR570Q10VSF.
     CMA125Q02V CR570Q10VSF.
     CMA113Q03V CR570Q10VSF.
     CMA129Q01VS CR570Q10VSF.
     CR558Q10VS CR570Q10VSF.
     CR055Q01V CR570Q10VSF.
     CR455Q03A CR570Q10VSF.
     CR455Q02VS CR570Q10VSF.
     CR102Q05A CR570Q10VSF.
     CR111Q06VS CR570Q10VSF.
     CR102Q05VS CR570Q10VSF.
     CMA156Q01VS CR570Q10VSF.
     CMA113Q03VS CR570Q10VSF.
     CR550Q10V CR570Q10VSF.
     CM915Q02VS CR570Q10VSF.
     CMA126Q02A CR570Q10VSF.
     CMA133Q01V CR570Q10VSF.
     CR562Q02A CR570Q10VSF.
     CMA117Q04V CR570Q10VSF.
     CMA126Q04VS CR570Q10VSF.
     CM00GQ01A CR570Q10VSF.
     CR569Q01A CR570Q10VSF.
     CMA125Q02VS CR570Q10VSF.
     CF033Q01VS CR570Q10VSF.
     CMA120Q01V CR570Q10VSF.
     CMA128Q03V CR570Q10VSF.
     CR553Q01V CR570Q10VSF.
     CR553Q04VS CR570Q10VSF.
     CR547Q09V CR570Q10VSF.
     CR556Q09A CR570Q10VSF.
     CR570Q05V CR570Q10VSF.
     CR456Q06V CR570Q10VSF.
     CMA143Q02V CR570Q10VSF.
     CM00KQ02VS CR570Q10VSF.
     CF102Q01VS CR570Q10VSF.
     CR453Q04V CR570Q10VSF.
     CR565Q01VS CR570Q10VSF.
     CR453Q06V CR570Q10VSF.
     CM909Q01V CR570Q10VSF.
     CR565Q02VS CR570Q10VSF.
     CR565Q01A CR570Q10VSF.
     CR552Q03V CR570Q10VSF.
     CMA143Q01VS CR570Q10VSF.
     CR556Q01VS CR570Q10VSF.
     CMA138Q01VS CR570Q10VSF.
     CR556Q04VS CR570Q10VSF.
     CR404Q03VS CR570Q10VSF.
     CM909Q01VS CR570Q10VSF.
     CF082Q02V CR570Q10VSF.
     CR556Q12VS CR570Q10VSF.
     CF308Q03VS CR570Q10VSF.
     CF308Q02VS CR570Q10VSF.
     CR220Q06VS CR570Q10VSF.
     CR568Q08VS CR570Q10VSF.
     CR453Q06VS CR570Q10VSF.
     CM034Q01V CR570Q10VSF.
     CR466Q06VS CR570Q10VSF.
     CR541Q04V CR570Q10VSF.
     CR560Q03V CR570Q10VSF.
     CMA116Q02V CR570Q10VSF.
     CMA130Q03A CR570Q10VSF.
     CR543Q01A CR570Q10VSF.
     CMA149Q01A CR570Q10VSF.
     CR543Q04VS CR570Q10VSF.
     CR453Q04A CR570Q10VSF.
     CMA139Q01VS CR570Q10VSF.
     CR219Q01V CR570Q10VSF.
     CR544Q04V CR570Q10VSF.
     CR545Q04A CR570Q10VSF.
     CMA113Q02V CR570Q10VSF.
     CM273Q01VS CR570Q10VSF.
     CR545Q06A CR570Q10VSF.
     CMA102Q01A CR570Q10VSF.
     CMA114Q04VS CR570Q10VSF.
     CMA153Q02A CR570Q10VSF.
     CMA150Q01A CR570Q10VSF.
     CMA116Q01VS CR570Q10VSF.
     CR446Q06A CR570Q10VSF.
     CMA103Q02V CR570Q10VSF.
     CMA108Q02V CR570Q10VSF.
     CMA103Q01A CR570Q10VSF.
     CR570Q10VS CR570Q10VSF.
     CM955Q01A CR570Q10VSF.
     CM905Q02V CR570Q10VSF.
     CF068Q01V CR570Q10VSF.
     CMA158Q01VS CR570Q10VSF.
     CMA158Q02A CR570Q10VSF.
     CR566Q04VS CR570Q10VSF.
     CF201Q01VS CR570Q10VSF.
     CF401Q02A CR570Q10VSF.
     CMA131Q04VS CR570Q10VSF.
     CR566Q09VS CR570Q10VSF.
     CMA126Q04A CR570Q10VSF.
     CM949Q01V CR570Q10VSF.
     CR456Q02VS CR570Q10VSF.
     CR544Q06VS CR570Q10VSF.
     CMA132Q02A CR570Q10VSF.
     CR552Q08VS CR570Q10VSF.
     CM462Q01A CR570Q10VSF.
     CR543Q09A CR570Q10VSF.
     CMA131Q03A CR570Q10VSF.
     CR562Q07VS CR570Q10VSF.
     CR432Q01V CR570Q10VSF.
     CR460Q05A CR570Q10VSF.
     CMA128Q01V CR570Q10VSF.
     CR570Q04VS CR570Q10VSF.
     CF303Q03VS CR570Q10VSF.
     CR432Q01A CR570Q10VSF.
     CM411Q02A CR570Q10VSF.
     CF102Q02A CR570Q10VSF.
     CMA111Q03VS CR570Q10VSF.
     CMA136Q02VS CR570Q10VSF.
     CMA108Q03A CR570Q10VSF.
     CMA161Q04A CR570Q10VSF.
     CMA134Q01V CR570Q10VSF.
     CMA141Q04A CR570Q10VSF.
     CM955Q02V CR570Q10VSF.
     CF303Q04V CR570Q10VSF.
     CMA113Q01A CR570Q10VSF.
     CR566Q14A CR570Q10VSF.
     CM919Q01V CR570Q10VSF.
     CMA127Q01A CR570Q10VSF.
     CMA137Q03VS CR570Q10VSF.
     CMA161Q03A CR570Q10VSF.
     CF303Q03A CR570Q10VSF.
     CF051Q01VS CR570Q10VSF.
     CR543Q03VS CR570Q10VSF.
     CR570Q01VS CR570Q10VSF.
     CMA113Q01VS CR570Q10VSF.
     CF303Q01A CR570Q10VSF.
     CM906Q02A CR570Q10VSF.
     CM955Q02A CR570Q10VSF.
     CF024Q02V CR570Q10VSF.
     CM411Q02V CR570Q10VSF.
     CR569Q04VS CR570Q10VSF.
     CF058Q01A CR570Q10VSF.
     CMA141Q03VS CR570Q10VSF.
     CF307Q01A CR570Q10VSF.
     CMA111Q02VS CR570Q10VSF.
     CM033Q01VS CR570Q10VSF.
     CR432Q06V CR570Q10VSF.
     CMA154Q01VS CR570Q10VSF.
     CR455Q05VS CR570Q10VSF.
     CMA135Q01A CR570Q10VSF.
     CMA121Q02V CR570Q10VSF.
     CMA146Q02VS CR570Q10VSF.
     CM955Q03V CR570Q10VSF.
     CF097Q01A CR570Q10VSF.
     CR550Q07V CR570Q10VSF.
     CM954Q04V CR570Q10VSF.
     CF300Q03V CR570Q10VSF.
     CR566Q03A CR570Q10VSF.
     CR460Q05VS CR570Q10VSF.
     CF105Q01A CR570Q10VSF.
     CF105Q01V CR570Q10VSF.
     CR569Q01V CR570Q10VSF.
     CMA127Q03A CR570Q10VSF.
     CMA138Q02V CR570Q10VSF.
     CR556Q03VS CR570Q10VSF.
     CM955Q01V CR570Q10VSF.
     CR456Q02A CR570Q10VSF.
     CM943Q02A CR570Q10VSF.
     CR562Q02V CR570Q10VSF.
     CR544Q13A CR570Q10VSF.
     CM955Q03VS CR570Q10VSF.
     CMA131Q02VS CR570Q10VSF.
     CR562Q05V CR570Q10VSF.
     CM953Q02A CR570Q10VSF.
     CR563Q03V CR570Q10VSF.
     CMA111Q01V CR570Q10VSF.
     CM919Q01VS CR570Q10VSF.
     CMA131Q01V CR570Q10VSF.
     CM949Q01VS CR570Q10VSF.
     CMA161Q02VS CR570Q10VSF.
     CR570Q10V CR570Q10VSF.
     CM828Q02VS CR570Q10VSF.
     CMA146Q01A CR570Q10VSF.
     CR545Q04V CR570Q10VSF.
     CM954Q01V CR570Q10VSF.
     CR556Q04A CR570Q10VSF.
     CR563Q03A CR570Q10VSF.
     CMA130Q01VS CR570Q10VSF.
     CM828Q03A CR570Q10VSF.
     CMA126Q04V CR570Q10VSF.
     CM155Q02VS CR570Q10VSF.
     CMA130Q02VS CR570Q10VSF.
     CR544Q14V CR570Q10VSF.
     CR220Q05A CR570Q10VSF.
     CF203Q01VS CR570Q10VSF.
     CR220Q06V CR570Q10VSF.
     CMA103Q01V CR570Q10VSF.
     CF300Q03VS CR570Q10VSF.
     CM953Q02VS CR570Q10VSF.
     CM948Q02V CR570Q10VSF.
     CMA121Q03V CR570Q10VSF.
     CMA103Q02A CR570Q10VSF.
     CR567Q13A CR570Q10VSF.
     CMA103Q02VS CR570Q10VSF.
     CMA147Q03V CR570Q10VSF.
     CR559Q04A CR570Q10VSF.
     CR453Q01A CR570Q10VSF.
     CR559Q03V CR570Q10VSF.
     CR563Q09A CR570Q10VSF.
     CR559Q06VS CR570Q10VSF.
     CMA103Q05A CR570Q10VSF.
     CF402Q02A CR570Q10VSF.
     CMA131Q01A CR570Q10VSF.
     CR545Q04VS CR570Q10VSF.
     CR446Q06VS CR570Q10VSF.
     CR556Q05V CR570Q10VSF.
     CM446Q01V CR570Q10VSF.
     CM411Q02VS CR570Q10VSF.
     CMA139Q02VS CR570Q10VSF.
     CMA101Q01VS CR570Q10VSF.
     CMA105Q03V CR570Q10VSF.
     CMA154Q02VS CR570Q10VSF.
     CMA109Q03A CR570Q10VSF.
     CR455Q02V CR570Q10VSF.
     CR558Q10A CR570Q10VSF.
     CMA144Q03VS CR570Q10VSF.
     CR558Q09VS CR570Q10VSF.
     CR558Q06A CR570Q10VSF.
     CMA135Q02A CR570Q10VSF.
     CR549Q05A CR570Q10VSF.
     CR568Q06VS CR570Q10VSF.
     CR541Q11VS CR570Q10VSF.
     CMA154Q03V CR570Q10VSF.
     CR558Q12VS CR570Q10VSF.
     CMA135Q03V CR570Q10VSF.
     CMA105Q01VS CR570Q10VSF.
     CR547Q07VS CR570Q10VSF.
     CM803Q01VS CR570Q10VSF.
     CMA123Q02A CR570Q10VSF.
     CR102Q07V CR570Q10VSF.
     CF307Q05VS CR570Q10VSF.
     CF012Q02V CR570Q10VSF.
     CMA120Q02V CR570Q10VSF.
     CM949Q02A CR570Q10VSF.
     CMA105Q01V CR570Q10VSF.
     CR549Q10A CR570Q10VSF.
     CR544Q06A CR570Q10VSF.
     CF307Q02VS CR570Q10VSF.
     CR558Q02V CR570Q10VSF.
     CR556Q09VS CR570Q10VSF.
     CMA105Q02A CR570Q10VSF.
     CMA109Q01VS CR570Q10VSF.
     CMA105Q02VS CR570Q10VSF.
     CMA144Q03A CR570Q10VSF.
     CMA109Q02V CR570Q10VSF.
     CMA144Q03V CR570Q10VSF.
     CR102Q05V CR570Q10VSF.
     CR556Q10VS CR570Q10VSF.
     CMA109Q03VS CR570Q10VSF.
     CMA158Q02VS CR570Q10VSF.
     CR455Q04A CR570Q10VSF.
     CF105Q02VS CR570Q10VSF.
     CF054Q01VS CR570Q10VSF.
     CF403Q01V CR570Q10VSF.
     CMA101Q02V CR570Q10VSF.
     CR561Q08A CR570Q10VSF.
     CR540Q03A CR570Q10VSF.
     CF303Q04A CR570Q10VSF.
     CR540Q04VS CR570Q10VSF.
     CR568Q05A CR570Q10VSF.
     CF095Q01V CR570Q10VSF.
     CMA115Q02V CR570Q10VSF.
     CR568Q05VS CR570Q10VSF.
     CR556Q12V CR570Q10VSF.
     CMA119Q01A CR570Q10VSF.
     CMA158Q02V CR570Q10VSF.
     CR542Q05A CR570Q10VSF.
     CF308Q01A CR570Q10VSF.
     CR542Q08V CR570Q10VSF.
     CF308Q02A CR570Q10VSF.
     CM992Q01A CR570Q10VSF.
     CM411Q01VS CR570Q10VSF.
     CMA110Q01V CR570Q10VSF.
     CMA112Q01A CR570Q10VSF.
     CF202Q01A CR570Q10VSF.
     CMA105Q05VS CR570Q10VSF.
     CR541Q09VS CR570Q10VSF.
     CMA112Q01VS CR570Q10VSF.
     CR542Q05V CR570Q10VSF.
     CMA110Q02V CR570Q10VSF.
     CMA119Q01V CR570Q10VSF.
     CR561Q04VS CR570Q10VSF.
     CR564Q01A CR570Q10VSF.
     CMA115Q02VS CR570Q10VSF.
     CR564Q02V CR570Q10VSF.
     CR540Q06V CR570Q10VSF.
     CR564Q03VS CR570Q10VSF.
     CMA112Q03V CR570Q10VSF.
     CR540Q05VS CR570Q10VSF.
     CM420Q01V CR570Q10VSF.
     CR568Q06A CR570Q10VSF.
     CR564Q01V CR570Q10VSF.
     CMA115Q01V CR570Q10VSF.
     CMA117Q03VS CR570Q10VSF.
     CMA112Q03A CR570Q10VSF.
     CR102Q04A CR570Q10VSF.
     CR540Q01VS CR570Q10VSF.
     CR460Q05V CR570Q10VSF.
     CR564Q02VS CR570Q10VSF.
     CR455Q05V CR570Q10VSF.
     CMA149Q02A CR570Q10VSF.
     CMA162Q02VS CR570Q10VSF.
     CR564Q03V CR570Q10VSF.
     CR558Q06V CR570Q10VSF.
     CMA129Q02VS CR570Q10VSF.
     CR563Q07V CR570Q10VSF.
     CM155Q04VS CR570Q10VSF.
     CR566Q04V CR570Q10VSF.
     CR055Q03V CR570Q10VSF.
     CM992Q02V CR570Q10VSF.
     CR111Q01VS CR570Q10VSF.
     CMA133Q01VS CR570Q10VSF.
     CR570Q06V CR570Q10VSF.
     CMA117Q02A CR570Q10VSF.
     CR466Q02A CR570Q10VSF.
     CR564Q05A CR570Q10VSF.
     CMA156Q01A CR570Q10VSF.
     CR558Q09V CR570Q10VSF.
     CR466Q06V CR570Q10VSF.
     CF082Q02A CR570Q10VSF.
     CM915Q02A CR570Q10VSF.
     CR550Q10VS CR570Q10VSF.
     CM564Q02V CR570Q10VSF.
     CR542Q09A CR570Q10VSF.
     CR558Q04VS CR570Q10VSF.
     CR563Q02V CR570Q10VSF.
     CR550Q06V CR570Q10VSF.
     CF307Q01V CR570Q10VSF.
     CR558Q12V CR570Q10VSF.
     CMA126Q03V CR570Q10VSF.
     CM408Q01VS CR570Q10VSF.
     CR556Q10V CR570Q10VSF.
     CR562Q05A CR570Q10VSF.
     CM954Q02VS CR570Q10VSF.
     CR562Q06VS CR570Q10VSF.
     CR556Q04V CR570Q10VSF.
     CM906Q01V CR570Q10VSF.
     CMA128Q01A CR570Q10VSF.
     CMA128Q01VS CR570Q10VSF.
     CF402Q01V CR570Q10VSF.
     CMA128Q02A CR570Q10VSF.
     CM992Q03VS CR570Q10VSF.
     CR569Q04A CR570Q10VSF.
     CF051Q01A CR570Q10VSF.
     CMA120Q01VS CR570Q10VSF.
     CMA146Q03VS CR570Q10VSF.
     CM954Q04VS CR570Q10VSF.
     CM603Q01A CR570Q10VSF.
     CR547Q10VS CR570Q10VSF.
     CF402Q01A CR570Q10VSF.
     CMA162Q02A CR570Q10VSF.
     CMA124Q01V CR570Q10VSF.
     CR553Q07A CR570Q10VSF.
     CF401Q01V CR570Q10VSF.
     CR456Q01V CR570Q10VSF.
     CR547Q02VS CR570Q10VSF.
     CMA142Q01VS CR570Q10VSF.
     CMA134Q03VS CR570Q10VSF.
     CM603Q01V CR570Q10VSF.
     CMA108Q01A CR570Q10VSF.
     CR446Q03A CR570Q10VSF.
     CR565Q09V CR570Q10VSF.
     CMA124Q01A CR570Q10VSF.
     CR565Q08A CR570Q10VSF.
     CM564Q01V CR570Q10VSF.
     CMA132Q01V CR570Q10VSF.
     CMA160Q01A CR570Q10VSF.
     CMA145Q02V CR570Q10VSF.
     CMA151Q01V CR570Q10VSF.
     CMA154Q02A CR570Q10VSF.
     CM939Q02A CR570Q10VSF.
     CMA143Q03A CR570Q10VSF.
     CMA151Q02VS CR570Q10VSF.
     CR565Q02A CR570Q10VSF.
     CR552Q06A CR570Q10VSF.
     CR404Q10V CR570Q10VSF.
     CR552Q03VS CR570Q10VSF.
     CM936Q02VS CR570Q10VSF.
     CMA143Q02A CR570Q10VSF.
     CM936Q02V CR570Q10VSF.
     CMA160Q02A CR570Q10VSF.
     CM800Q01V CR570Q10VSF.
     CM496Q02A CR570Q10VSF.
     CR556Q05VS CR570Q10VSF.
     CR552Q09V CR570Q10VSF.
     CMA141Q01V CR570Q10VSF.
     CMA143Q04VS CR570Q10VSF.
     CMA145Q01VS CR570Q10VSF.
     CR556Q09V CR570Q10VSF.
     CR404Q03A CR570Q10VSF.
     CM420Q01VS CR570Q10VSF.
     CMA147Q04V CR570Q10VSF.
     CR556Q12A CR570Q10VSF.
     CF102Q02VS CR570Q10VSF.
     CR568Q14A CR570Q10VSF.
     CR559Q03VS CR570Q10VSF.
     CR568Q05V CR570Q10VSF.
     CR568Q06V CR570Q10VSF.
     CM909Q03V CR570Q10VSF.
     CM953Q04VS CR570Q10VSF.
     CR219Q01A CR570Q10VSF.
     CR466Q03VS CR570Q10VSF.
     CMA147Q03A CR570Q10VSF.
     CMA156Q01V CR570Q10VSF.
     CR568Q13V CR570Q10VSF.
     CF033Q02A CR570Q10VSF.
     CR541Q01VS CR570Q10VSF.
     CMA121Q03VS CR570Q10VSF.
     CMA147Q02A CR570Q10VSF.
     CR560Q06A CR570Q10VSF.
     CM496Q01VS CR570Q10VSF.
     CMA147Q01A CR570Q10VSF.
     CR541Q09A CR570Q10VSF.
     CR560Q10VS CR570Q10VSF.
     CR541Q10V CR570Q10VSF.
     CR220Q04V CR570Q10VSF.
     CMA148Q03VS CR570Q10VSF.
     CF303Q04VS CR570Q10VSF.
     CMA151Q01A CR570Q10VSF.
     CR543Q13V CR570Q10VSF.
     CM948Q01V CR570Q10VSF.
     CR219Q01VS CR570Q10VSF.
     CMA114Q01V CR570Q10VSF.
     CMA130Q02A CR570Q10VSF.
     CR543Q10A CR570Q10VSF.
     CR220Q04A CR570Q10VSF.
     CR543Q13VS CR570Q10VSF.
     CR220Q02A CR570Q10VSF.
     CMA102Q02VS CR570Q10VSF.
     CR453Q04VS CR570Q10VSF.
     CMA102Q02V CR570Q10VSF.
     CR545Q02VS CR570Q10VSF.
     CMA153Q02VS CR570Q10VSF.
     CMA130Q01V CR570Q10VSF.
     CR545Q07A CR570Q10VSF.
     CR545Q06V CR570Q10VSF.
     CR453Q01VS CR570Q10VSF.
     CR550Q04V CR570Q10VSF.
     CR544Q13V CR570Q10VSF.
     CMA127Q02A CR570Q10VSF.
     CMA162Q01VS CR570Q10VSF.
     CM953Q03VS CR570Q10VSF.
     CMA138Q01A CR570Q10VSF.
     CMA111Q01A CR570Q10VSF.
     CMA154Q02V CR570Q10VSF.
     CM953Q03A CR570Q10VSF.
     CR563Q07A CR570Q10VSF.
     CMA126Q02V CR570Q10VSF.
     CM442Q02V CR570Q10VSF.
     CR545Q02A CR570Q10VSF.
     CR446Q06V CR570Q10VSF.
     CR550Q05VS CR570Q10VSF.
     CMA140Q03V CR570Q10VSF.
     CF308Q04V CR570Q10VSF.
     CR552Q08A CR570Q10VSF.
     CF106Q02VS CR570Q10VSF.
     CM00KQ02V CR570Q10VSF.
     CMA140Q03VS CR570Q10VSF.
     CMA161Q01VS CR570Q10VSF.
     CMA152Q02V CR570Q10VSF.
     CM949Q01A CR570Q10VSF.
     CR543Q10V CR570Q10VSF.
     CR544Q07V CR570Q10VSF.
     CM155Q02V CR570Q10VSF.
     CR570Q05VS CR570Q10VSF.
     CM305Q01VS CR570Q10VSF.
     CF069Q01A CR570Q10VSF.
     CR550Q07A CR570Q10VSF.
     CMA116Q03V CR570Q10VSF.
     CMA152Q01A CR570Q10VSF.
     CR541Q04VS CR570Q10VSF.
     CR550Q06VS CR570Q10VSF.
     CMA116Q03VS CR570Q10VSF.
     CF300Q01VS CR570Q10VSF.
     CR566Q06V CR570Q10VSF.
     CR550Q07VS CR570Q10VSF.
     CMA102Q03V CR570Q10VSF.
     CMA131Q04A CR570Q10VSF.
     CR566Q12A CR570Q10VSF.
     CMA150Q01VS CR570Q10VSF.
     CR567Q03VS CR570Q10VSF.
     CF024Q02A CR570Q10VSF.
     CM420Q01A CR570Q10VSF.
     CM305Q01V CR570Q10VSF.
     CR567Q11A CR570Q10VSF.
     CMA134Q03A CR570Q10VSF.
     CM446Q02V CR570Q10VSF.
     CM00GQ01V CR570Q10VSF.
     CR456Q01VS CR570Q10VSF.
     CMA142Q02A CR570Q10VSF.
     CR567Q13V CR570Q10VSF.
     CM954Q02V CR570Q10VSF.
     CMA137Q01A CR570Q10VSF.
     CR567Q08VS CR570Q10VSF.
     CR567Q04A CR570Q10VSF.
     CF082Q01A CR570Q10VSF.
     CMA102Q03A CR570Q10VSF.
     CMA121Q01A CR570Q10VSF.
     CM305Q01A CR570Q10VSF.
     CR219Q02V CR570Q10VSF.
     CR562Q06V CR570Q10VSF.
     CMA127Q02VS CR570Q10VSF.
     CMA102Q01VS CR570Q10VSF.
     CR552Q01A CR570Q10VSF.
     CMA108Q01VS CR570Q10VSF.
     CMA149Q03V CR570Q10VSF.
     CM905Q01VS CR570Q10VSF.
     CR543Q04V CR570Q10VSF.
     CR566Q05VS CR570Q10VSF.
     CMA161Q04VS CR570Q10VSF.
     CR570Q04V CR570Q10VSF.
     CMA134Q02A CR570Q10VSF.
     CR541Q03VS CR570Q10VSF.
     CMA161Q03VS CR570Q10VSF.
     CMA150Q02A CR570Q10VSF.
     CMA146Q02V CR570Q10VSF.
     CF403Q01A CR570Q10VSF.
     CF009Q02A CR570Q10VSF.
     CF201Q01A CR570Q10VSF.
     CR567Q06A CR570Q10VSF.
     CR556Q01A CR570Q10VSF.
     CMA141Q04V CR570Q10VSF.
     CM906Q01VS CR570Q10VSF.
     CF303Q01N CR570Q10VSF.
     CMA111Q02V CR570Q10VSF.
     CMA111Q03A CR570Q10VSF.
     CMA136Q02V CR570Q10VSF.
     CMA137Q01VS CR570Q10VSF.
     CR569Q02V CR570Q10VSF.
     CR553Q04V CR570Q10VSF.
     CR563Q10A CR570Q10VSF.
     CR543Q03A CR570Q10VSF.
     CR553Q02A CR570Q10VSF.
     CM905Q01V CR570Q10VSF.
     CF103Q01VS CR570Q10VSF.
     CR563Q03VS CR570Q10VSF.
     CM571Q01VS CR570Q10VSF.
     CF308Q01V CR570Q10VSF.
     CR543Q04A CR570Q10VSF.
     CR432Q05V CR570Q10VSF.
     CF033Q01V CR570Q10VSF.
     CM906Q02V CR570Q10VSF.
     CMA113Q01V CR570Q10VSF.
     CF303Q01Q CR570Q10VSF.
     CR563Q09V CR570Q10VSF.
     CF308Q04A CR570Q10VSF.
     CM967Q03VS CR570Q10VSF.
     CF308Q04VS CR570Q10VSF.
     CR567Q10A CR570Q10VSF.
     CMA161Q03V CR570Q10VSF.
     CR553Q04A CR570Q10VSF.
     CF308Q01VS CR570Q10VSF.
     CF307Q05A CR570Q10VSF.
     CR547Q03VS CR570Q10VSF.
     CM447Q01V CR570Q10VSF.
     CMA141Q03V CR570Q10VSF.
     CR541Q03V CR570Q10VSF.
     CF402Q02V CR570Q10VSF.
     CMA108Q03VS CR570Q10VSF.
     CMA148Q02A CR570Q10VSF.
     CR102Q07A CR570Q10VSF.
     CMA135Q01VS CR570Q10VSF.
     CMA141Q02V CR570Q10VSF.
     CR553Q02VS CR570Q10VSF.
     CMA141Q03A CR570Q10VSF.
     CMA134Q01VS CR570Q10VSF.
     CMA120Q01A CR570Q10VSF.
     CR569Q03VS CR570Q10VSF.
     CF105Q02A CR570Q10VSF.
     CF105Q02V CR570Q10VSF.
     CR547Q10V CR570Q10VSF.
     CM462Q01V CR570Q10VSF.
     CF402Q01VS CR570Q10VSF.
     CF303Q01P CR570Q10VSF.
     CR569Q06V CR570Q10VSF.
     CR570Q04A CR570Q10VSF.
     CMA111Q02A CR570Q10VSF.
     CMA146Q02A CR570Q10VSF.
     CMA146Q03V CR570Q10VSF.
     CF054Q01A CR570Q10VSF.
     CF106Q01A CR570Q10VSF.
     CR552Q04V CR570Q10VSF.
     CMA128Q02VS CR570Q10VSF.
     CMA131Q03VS CR570Q10VSF.
     CMA128Q02V CR570Q10VSF.
     CR553Q05V CR570Q10VSF.
     CMA143Q02VS CR570Q10VSF.
     CMA150Q02V CR570Q10VSF.
     CR567Q03A CR570Q10VSF.
     CR432Q01VS CR570Q10VSF.
     CMA127Q01VS CR570Q10VSF.
     CMA113Q03A CR570Q10VSF.
     CR549Q13VS CR570Q10VSF.
     CR541Q05V CR570Q10VSF.
     CM998Q02VS CR570Q10VSF.
     CMA124Q03V CR570Q10VSF.
     CR220Q02V CR570Q10VSF.
     CF033Q02V CR570Q10VSF.
     CMA142Q02V CR570Q10VSF.
     CMA149Q03A CR570Q10VSF.
     CR553Q07V CR570Q10VSF.
     CR102Q04V CR570Q10VSF.
     CR566Q05A CR570Q10VSF.
     CM954Q02A CR570Q10VSF.
     CF300Q02V CR570Q10VSF.
     CMA158Q01V CR570Q10VSF.
     CR543Q09VS CR570Q10VSF.
     CMA158Q03A CR570Q10VSF.
     CR566Q09V CR570Q10VSF.
     CR566Q12V CR570Q10VSF.
     CM906Q02VS CR570Q10VSF.
     CR567Q08A CR570Q10VSF.
     CF082Q02VS CR570Q10VSF.
     CMA154Q01V CR570Q10VSF.
     CMA162Q03V CR570Q10VSF.
     CR567Q08V CR570Q10VSF.
     CMA152Q01V CR570Q10VSF.
     CR566Q12VS CR570Q10VSF.
     CMA141Q02A CR570Q10VSF.
     CM447Q01A CR570Q10VSF.
     CM446Q02VS CR570Q10VSF.
     CR567Q06V CR570Q10VSF.
     CMA126Q02VS CR570Q10VSF.
     CM155Q01A CR570Q10VSF.
     CF012Q01A CR570Q10VSF.
     CR570Q02A CR570Q10VSF.
     CM949Q02V CR570Q10VSF.
     CF401Q02VS CR570Q10VSF.
     CMA102Q01V CR570Q10VSF.
     CR562Q03V CR570Q10VSF.
     CR550Q06A CR570Q10VSF.
     CM943Q01V CR570Q10VSF.
     CR547Q09A CR570Q10VSF.
     CF203Q01V CR570Q10VSF.
     CR456Q02V CR570Q10VSF.
     CR566Q09A CR570Q10VSF.
     CR550Q05A CR570Q10VSF.
     CM943Q01A CR570Q10VSF.
     CMA127Q03V CR570Q10VSF.
     CF300Q01V CR570Q10VSF.
     CM828Q02V CR570Q10VSF.
     CMA161Q02A CR570Q10VSF.
     CMA126Q03VS CR570Q10VSF.
     CMA126Q03A CR570Q10VSF.
     CMA103Q04VS CR570Q10VSF.
     CMA114Q04V CR570Q10VSF.
     CR545Q03V CR570Q10VSF.
     CMA161Q01A CR570Q10VSF.
     CR456Q06A CR570Q10VSF.
     CMA136Q03V CR570Q10VSF.
     CMA135Q01V CR570Q10VSF.
     CR541Q03A CR570Q10VSF.
     CR566Q05V CR570Q10VSF.
     CR566Q04A CR570Q10VSF.
     CF300Q01A CR570Q10VSF.
     CMA160Q03V CR570Q10VSF.
     CR545Q07V CR570Q10VSF.
     CMA121Q02A CR570Q10VSF.
     CM474Q01VS CR570Q10VSF.
     CMA134Q03V CR570Q10VSF.
     CF009Q02V CR570Q10VSF.
     CMA135Q04V CR570Q10VSF.
     CMA152Q01VS CR570Q10VSF.
     CMA108Q03V CR570Q10VSF.
     CMA130Q02V CR570Q10VSF.
     CMA158Q01A CR570Q10VSF.
     CR055Q02A CR570Q10VSF.
     CM998Q02A CR570Q10VSF.
     CM967Q01V CR570Q10VSF.
     CMA135Q03A CR570Q10VSF.
     CMA152Q02VS CR570Q10VSF.
     CR220Q05VS CR570Q10VSF.
     CR570Q08V CR570Q10VSF.
     CM155Q01V CR570Q10VSF.
     CR432Q06VS CR570Q10VSF.
     CM967Q01A CR570Q10VSF.
     CM034Q01A CR570Q10VSF.
     CMA152Q02A CR570Q10VSF.
     CR570Q08VS CR570Q10VSF.
     CF203Q01A CR570Q10VSF.
     CR560Q03VS CR570Q10VSF.
     CR550Q05V CR570Q10VSF.
     CR570Q01V CR570Q10VSF.
     CMA103Q01VS CR570Q10VSF.
     CM948Q02VS CR570Q10VSF.
     CMA139Q01V CR570Q10VSF.
     CR560Q08A CR570Q10VSF.
     CM982Q01V CR570Q10VSF.
     CR565Q09VS CR570Q10VSF.
     CM464Q01V CR570Q10VSF.
     CR552Q04VS CR570Q10VSF.
     CR446Q03V CR570Q10VSF.
     CR563Q07VS CR570Q10VSF.
     CMA147Q03VS CR570Q10VSF.
     CR559Q04VS CR570Q10VSF.
     CR544Q14A CR570Q10VSF.
     CMA103Q04A CR570Q10VSF.
     CR544Q07A CR570Q10VSF.
     CR545Q03A CR570Q10VSF.
     CM953Q03V CR570Q10VSF.
     CR559Q06A CR570Q10VSF.
     CR545Q03VS CR570Q10VSF.
     CM442Q02A CR570Q10VSF.
     CR220Q01VS CR570Q10VSF.
     CR559Q08VS CR570Q10VSF.
     CMA103Q05V CR570Q10VSF.
     CR568Q13A CR570Q10VSF.
     CMA148Q02VS CR570Q10VSF.
     CM936Q01VS CR570Q10VSF.
     CR545Q06VS CR570Q10VSF.
     CR544Q12V CR570Q10VSF.
     CM442Q02VS CR570Q10VSF.
     CMA145Q02A CR570Q10VSF.
     CM953Q04A CR570Q10VSF.
     CR545Q07VS CR570Q10VSF.
     CMA121Q03A CR570Q10VSF.
     CM936Q02A CR570Q10VSF.
     CF300Q02VS CR570Q10VSF.
     CR544Q06V CR570Q10VSF.
     CR055Q03A CR570Q10VSF.
     CMA135Q04A CR570Q10VSF.
     CF300Q03A CR570Q10VSF.
     CR565Q08V CR570Q10VSF.
     CMA107Q03VS CR570Q10VSF.
     CMA107Q03A CR570Q10VSF.
     CR565Q05A CR570Q10VSF.
     CR565Q03VS CR570Q10VSF.
     CR565Q03A CR570Q10VSF.
     CMA140Q01VS CR570Q10VSF.
     CM915Q01VS CR570Q10VSF.
     CM496Q02VS CR570Q10VSF.
     CR565Q05VS CR570Q10VSF.
     CR566Q03VS CR570Q10VSF.
     CMA148Q02V CR570Q10VSF.
     CMA129Q03A CR570Q10VSF.
     CM982Q01A CR570Q10VSF.
     CR055Q03VS CR570Q10VSF.
     CR565Q09A CR570Q10VSF.
     CR563Q10V CR570Q10VSF.
     CMA124Q01VS CR570Q10VSF.
     CMA162Q03VS CR570Q10VSF.
     CR547Q02V CR570Q10VSF.
     CR541Q10VS CR570Q10VSF.
     CMA124Q02A CR570Q10VSF.
     CMA124Q02V CR570Q10VSF.
     CR547Q09VS CR570Q10VSF.
     CR055Q01VS CR570Q10VSF.
     CR568Q13VS CR570Q10VSF.
     CMA125Q03VS CR570Q10VSF.
     CMA124Q03A CR570Q10VSF.
     CMA149Q02V CR570Q10VSF.
     CMA124Q03VS CR570Q10VSF.
     CR055Q05V CR570Q10VSF.
     CF106Q01V CR570Q10VSF.
     CR460Q01VS CR570Q10VSF.
     CR549Q13V CR570Q10VSF.
     CF012Q02VS CR570Q10VSF.
     CR547Q03A CR570Q10VSF.
     CF303Q02VS CR570Q10VSF.
     CM967Q03V CR570Q10VSF.
     CR549Q12VS CR570Q10VSF.
     CR547Q06V CR570Q10VSF.
     CMA148Q01VS CR570Q10VSF.
     CM982Q02V CR570Q10VSF.
     CF058Q01VS CR570Q10VSF.
     CMA157Q01V CR570Q10VSF.
     CMA117Q04A CR570Q10VSF.
     CMA120Q02A CR570Q10VSF.
     CMA123Q02VS CR570Q10VSF.
     CMA120Q02VS CR570Q10VSF.
     CR568Q10V CR570Q10VSF.
     CMA105Q01A CR570Q10VSF.
     CR568Q10A CR570Q10VSF.
     CM423Q01A CR570Q10VSF.
     CM992Q03V CR570Q10VSF.
     CM423Q01V CR570Q10VSF.
     CM909Q02VS CR570Q10VSF.
     CR558Q12A CR570Q10VSF.
     CMA113Q02VS CR570Q10VSF.
     CMA120Q03VS CR570Q10VSF.
     CMA121Q01VS CR570Q10VSF.
     CMA154Q03VS CR570Q10VSF.
     CMA157Q02A CR570Q10VSF.
     CR558Q04V CR570Q10VSF.
     CM423Q01VS CR570Q10VSF.
     CMA109Q01V CR570Q10VSF.
     CMA102Q02A CR570Q10VSF.
     CR558Q06VS CR570Q10VSF.
     CMA117Q03V CR570Q10VSF.
     CR558Q09A CR570Q10VSF.
     CR549Q04V CR570Q10VSF.
     CMA109Q02A CR570Q10VSF.
     CMA131Q03V CR570Q10VSF.
     CMA109Q02VS CR570Q10VSF.
     CMA125Q01A CR570Q10VSF.
     CR558Q10V CR570Q10VSF.
     CMA117Q02VS CR570Q10VSF.
     CMA117Q02V CR570Q10VSF.
     CMA110Q03VS CR570Q10VSF.
     CMA109Q03V CR570Q10VSF.
     CMA139Q02V CR570Q10VSF.
     CR455Q03V CR570Q10VSF.
     CR564Q04A CR570Q10VSF.
     CR568Q15VS CR570Q10VSF.
     CMA101Q01A CR570Q10VSF.
     CR455Q04VS CR570Q10VSF.
     CMA117Q01A CR570Q10VSF.
     CM919Q02V CR570Q10VSF.
     CMA117Q01V CR570Q10VSF.
     CR455Q05A CR570Q10VSF.
     CF068Q01VS CR570Q10VSF.
     CMA101Q02A CR570Q10VSF.
     CMA149Q03VS CR570Q10VSF.
     CR540Q01V CR570Q10VSF.
     CR542Q09VS CR570Q10VSF.
     CM408Q01A CR570Q10VSF.
     CF082Q01VS CR570Q10VSF.
     CR540Q03VS CR570Q10VSF.
     CMA137Q03V CR570Q10VSF.
     CR540Q04A CR570Q10VSF.
     CM982Q04A CR570Q10VSF.
     CMA105Q04V CR570Q10VSF.
     CMA112Q02VS CR570Q10VSF.
     CR540Q05V CR570Q10VSF.
     CMA112Q02Q CR570Q10VSF.
     CMA115Q02A CR570Q10VSF.
     CM919Q02A CR570Q10VSF.
     CR540Q06VS CR570Q10VSF.
     CMA112Q02P CR570Q10VSF.
     CF095Q01A CR570Q10VSF.
     CR561Q03VS CR570Q10VSF.
     CMA112Q02A CR570Q10VSF.
     CMA105Q05A CR570Q10VSF.
     CR542Q02V CR570Q10VSF.
     CMA162Q02V CR570Q10VSF.
     CM909Q03A CR570Q10VSF.
     CMA133Q02V CR570Q10VSF.
     CR542Q05VS CR570Q10VSF.
     CM992Q01V CR570Q10VSF.
     CMA119Q02V CR570Q10VSF.
     CMA119Q02VS CR570Q10VSF.
     CM192Q01A CR570Q10VSF.
     CM192Q01V CR570Q10VSF.
     CR542Q09V CR570Q10VSF.
     CF031Q01V CR570Q10VSF.
     CMA119Q03V CR570Q10VSF.
     CM559Q01VS CR570Q10VSF.
     CR561Q01VS CR570Q10VSF.
     CR544Q04A CR570Q10VSF.
     CR570Q10A CR570Q10VSF.
     CR542Q08VS CR570Q10VSF.
     CMA110Q01VS CR570Q10VSF.
     CR561Q03A CR570Q10VSF.
     CF031Q01VS CR570Q10VSF.
     CMA119Q01VS CR570Q10VSF.
     CR544Q10V CR570Q10VSF.
     CMA119Q03A CR570Q10VSF.
     CF031Q01A CR570Q10VSF.
     CR563Q02A CR570Q10VSF.
     CR561Q06V CR570Q10VSF.
     CM192Q01VS CR570Q10VSF.
     CMA112Q01V CR570Q10VSF.
     CR561Q07A CR570Q10VSF.
     CR542Q02VS CR570Q10VSF.
     CR542Q02A CR570Q10VSF.
     CR561Q08V CR570Q10VSF.
     CMA132Q01VS CR570Q10VSF.
     CR556Q05A CR570Q10VSF.
     CR541Q01V CR570Q10VSF.
     CMA107Q02VS CR570Q10VSF.
     CR561Q01V CR570Q10VSF.
     CR542Q01VS CR570Q10VSF.
     CR564Q01VS CR570Q10VSF.
     CR561Q07VS CR570Q10VSF.
     CMA110Q02A CR570Q10VSF.
     CMA112Q02N CR570Q10VSF.
     CF105Q01VS CR570Q10VSF.
     CR564Q03A CR570Q10VSF.
     CR561Q06VS CR570Q10VSF.
     CMA117Q01VS CR570Q10VSF.
     CMA105Q03VS CR570Q10VSF.
     CR564Q04V CR570Q10VSF.
     CR540Q05A CR570Q10VSF.
     CR432Q05A CR570Q10VSF.
     CR561Q08VS CR570Q10VSF.
     CMA150Q02VS CR570Q10VSF.
     CMA115Q01VS CR570Q10VSF.
     CR549Q04A CR570Q10VSF.
     CMA161Q01V CR570Q10VSF.
     CMA137Q03A CR570Q10VSF.
     CMA110Q02VS CR570Q10VSF.
     CMA105Q04A CR570Q10VSF.
     CR563Q10VS CR570Q10VSF.
     CMA139Q02A CR570Q10VSF.
     CR540Q03V CR570Q10VSF.
     CR549Q06A CR570Q10VSF.
     CMA101Q01V CR570Q10VSF.
     CF095Q01VS CR570Q10VSF.
     CMA101Q02VS CR570Q10VSF.
     CR549Q10V CR570Q10VSF.
     CF401Q01A CR570Q10VSF.
     CMA117Q04VS CR570Q10VSF.
     CMA110Q03V CR570Q10VSF.
     CR549Q12A CR570Q10VSF.
     CR564Q02A CR570Q10VSF.
     CR549Q12V CR570Q10VSF.
     CMA110Q03A CR570Q10VSF.
     CMA129Q01V CR570Q10VSF.
     CF095Q02A CR570Q10VSF.
     CM992Q02VS CR570Q10VSF.
     CR568Q15A CR570Q10VSF.
     CR102Q04VS CR570Q10VSF.
     CMA108Q02VS CR570Q10VSF.
     CR055Q05VS CR570Q10VSF.
     CF033Q01A CR570Q10VSF.
     CM564Q02A CR570Q10VSF.
     CR455Q03VS CR570Q10VSF.
     CR564Q04VS CR570Q10VSF.
     CR541Q11A CR570Q10VSF.
     CR055Q02V CR570Q10VSF.
     CR564Q05VS CR570Q10VSF.
     CMA129Q03VS CR570Q10VSF.
     CM982Q03VS CR570Q10VSF.
     CM447Q01VS CR570Q10VSF.
     CM411Q01V CR570Q10VSF.
     CR111Q01A CR570Q10VSF.
     CR543Q15V CR570Q10VSF.
     CR455Q02A CR570Q10VSF.
     CM155Q04V CR570Q10VSF.
     CR111Q02BVS CR570Q10VSF.
     CM982Q03V CR570Q10VSF.
     CR111Q06A CR570Q10VSF.
     CF095Q02V CR570Q10VSF.
     CMA132Q02V CR570Q10VSF.
     CMA125Q01V CR570Q10VSF.
     CR563Q02VS CR570Q10VSF.
     CMA105Q02V CR570Q10VSF.
     CM982Q03A CR570Q10VSF.
     CF102Q01A CR570Q10VSF.
     CR466Q03V CR570Q10VSF.
     CMA117Q03A CR570Q10VSF.
     CMA140Q02V CR570Q10VSF.
     CR543Q09V CR570Q10VSF.
     CMA125Q01VS CR570Q10VSF.
     CMA135Q02V CR570Q10VSF.
     CR550Q09V CR570Q10VSF.
     CMA148Q03A CR570Q10VSF.
     CR550Q10A CR570Q10VSF.
     CMA109Q01A CR570Q10VSF.
     CM915Q02V CR570Q10VSF.
     CR549Q05VS CR570Q10VSF.
     CR550Q04A CR570Q10VSF.
     CMA121Q01V CR570Q10VSF.
     CMA140Q03A CR570Q10VSF.
     CR558Q04A CR570Q10VSF.
     CM909Q03VS CR570Q10VSF.
     CR549Q06V CR570Q10VSF.
     CMA123Q01A CR570Q10VSF.
     CR558Q02VS CR570Q10VSF.
     CF308Q03A CR570Q10VSF.
     CR547Q07V CR570Q10VSF.
     CMA120Q03V CR570Q10VSF.
     CMA125Q02A CR570Q10VSF.
     CMA120Q03A CR570Q10VSF.
     CMA123Q01VS CR570Q10VSF.
     CR562Q02VS CR570Q10VSF.
     CMA116Q01V CR570Q10VSF.
     CR562Q03A CR570Q10VSF.
     CR549Q10VS CR570Q10VSF.
     CR558Q02A CR570Q10VSF.
     CM155Q04A CR570Q10VSF.
     CR562Q05VS CR570Q10VSF.
     CR102Q07VS CR570Q10VSF.
     CR562Q06A CR570Q10VSF.
     CMA114Q03V CR570Q10VSF.
     CM906Q01A CR570Q10VSF.
     CMA148Q01V CR570Q10VSF.
     CR552Q04A CR570Q10VSF.
     CF106Q01VS CR570Q10VSF.
     CR569Q01VS CR570Q10VSF.
     CF012Q02A CR570Q10VSF.
     CR569Q02A CR570Q10VSF.
     CMA157Q01VS CR570Q10VSF.
     CF307Q05V CR570Q10VSF.
     CM446Q01A CR570Q10VSF.
     CR569Q03V CR570Q10VSF.
     CR547Q06A CR570Q10VSF.
     CM919Q02VS CR570Q10VSF.
     CM982Q02A CR570Q10VSF.
     CR547Q06VS CR570Q10VSF.
     CMA107Q02A CR570Q10VSF.
     CR565Q02V CR570Q10VSF.
     CM992Q03A CR570Q10VSF.
     CR547Q03V CR570Q10VSF.
     CR543Q15VS CR570Q10VSF.
     CR549Q13A CR570Q10VSF.
     CR553Q02V CR570Q10VSF.
     CMA135Q04VS CR570Q10VSF.
     CM967Q03A CR570Q10VSF.
     CF307Q02V CR570Q10VSF.
     CR553Q01VS CR570Q10VSF.
     CR547Q10A CR570Q10VSF.
     CMA129Q01A CR570Q10VSF.
     CR568Q10VS CR570Q10VSF.
     CMA136Q02A CR570Q10VSF.
     CM949Q03A CR570Q10VSF.
     CR553Q05A CR570Q10VSF.
     CR111Q01V CR570Q10VSF.
     CF202Q01V CR570Q10VSF.
     CM446Q01VS CR570Q10VSF.
     CR553Q07VS CR570Q10VSF.
     CM967Q01VS CR570Q10VSF.
     CM033Q01A CR570Q10VSF.
     CMA124Q02VS CR570Q10VSF.
     CMA125Q03V CR570Q10VSF.
     CMA127Q03VS CR570Q10VSF.
     CM955Q01VS CR570Q10VSF.
     CMA143Q03V CR570Q10VSF.
     CM982Q01VS CR570Q10VSF.
     CMA154Q01A CR570Q10VSF.
     CM00KQ02A CR570Q10VSF.
     CR570Q06VS CR570Q10VSF.
     CR547Q02A CR570Q10VSF.
     CR565Q05V CR570Q10VSF.
     CMA153Q01V CR570Q10VSF.
     CMA153Q01VS CR570Q10VSF.
     CR446Q03VS CR570Q10VSF.
     CMA158Q03V CR570Q10VSF.
     CR055Q02VS CR570Q10VSF.
     CM915Q01A CR570Q10VSF.
     CR219Q02VS CR570Q10VSF.
     CM939Q02V CR570Q10VSF.
     CR453Q01V CR570Q10VSF.
     CMA129Q02V CR570Q10VSF.
     CR565Q08VS CR570Q10VSF.
     CMA107Q03V CR570Q10VSF.
     CMA138Q01V CR570Q10VSF.
     CMA140Q01V CR570Q10VSF.
     CM939Q02VS CR570Q10VSF.
     CR559Q04V CR570Q10VSF.
     CR453Q05V CR570Q10VSF.
     CM949Q03V CR570Q10VSF.
     CMA151Q01VS CR570Q10VSF.
     CMA150Q01V CR570Q10VSF.
     CM564Q01VS CR570Q10VSF.
     CR565Q03V CR570Q10VSF.
     CM915Q01V CR570Q10VSF.
     CR111Q06V CR570Q10VSF.
     CMA151Q02V CR570Q10VSF.
     CMA107Q02V CR570Q10VSF.
     CMA132Q01A CR570Q10VSF.
     CF402Q02VS CR570Q10VSF.
     CF202Q01VS CR570Q10VSF.
     CR568Q08V CR570Q10VSF.
     CR552Q06VS CR570Q10VSF.
     CR566Q06A CR570Q10VSF.
     CR552Q03A CR570Q10VSF.
     CMA158Q03VS CR570Q10VSF.
     CR552Q06V CR570Q10VSF.
     CM982Q02VS CR570Q10VSF.
     CR541Q10A CR570Q10VSF.
     CMA107Q01A CR570Q10VSF.
     CM496Q02V CR570Q10VSF.
     CMA145Q02VS CR570Q10VSF.
     CMA160Q02V CR570Q10VSF.
     CR466Q02VS CR570Q10VSF.
     CR404Q10A CR570Q10VSF.
     CR404Q07A CR570Q10VSF.
     CMA143Q01A CR570Q10VSF.
     CR566Q14V CR570Q10VSF.
     CR404Q07VS CR570Q10VSF.
     CM034Q01VS CR570Q10VSF.
     CM909Q02A CR570Q10VSF.
     CM800Q01A CR570Q10VSF.
     CMA160Q02VS CR570Q10VSF.
     CF303Q01VS CR570Q10VSF.
     CMA121Q02VS CR570Q10VSF.
     CR404Q06A CR570Q10VSF.
     CR404Q06V CR570Q10VSF.
     CM936Q01A CR570Q10VSF.
     CM909Q02V CR570Q10VSF.
     CMA157Q01A CR570Q10VSF.
     CMA133Q01A CR570Q10VSF.
     CMA145Q01A CR570Q10VSF.
     CR556Q10A CR570Q10VSF.
     CM936Q01V CR570Q10VSF.
     CMA145Q01V CR570Q10VSF.
     CM948Q03V CR570Q10VSF.
     CR563Q12VS CR570Q10VSF.
     CMA132Q02VS CR570Q10VSF.
     CR559Q08V CR570Q10VSF.
     CMA147Q04VS CR570Q10VSF.
     CR552Q09A CR570Q10VSF.
     CR559Q06V CR570Q10VSF.
     CF102Q02V CR570Q10VSF.
     CMA140Q02A CR570Q10VSF.
     CMA144Q01V CR570Q10VSF.
     CMA147Q04A CR570Q10VSF.
     CMA133Q02VS CR570Q10VSF.
     CMA127Q01V CR570Q10VSF.
     CR559Q03A CR570Q10VSF.
     CR466Q03A CR570Q10VSF.
     CF069Q01V CR570Q10VSF.
     CMA114Q03A CR570Q10VSF.
     CF401Q02V CR570Q10VSF.
     CR568Q08A CR570Q10VSF.
     CR559Q01V CR570Q10VSF.
     CMA148Q01A CR570Q10VSF.
     CR559Q01VS CR570Q10VSF.
     CM464Q01VS CR570Q10VSF.
     CMA142Q01V CR570Q10VSF.
     CMA114Q04A CR570Q10VSF.
     CMA116Q03A CR570Q10VSF.
     CF307Q02A CR570Q10VSF.
     CMA150Q03A CR570Q10VSF.
     CMA149Q01VS CR570Q10VSF.
     CMA147Q02VS CR570Q10VSF.
     CR432Q06A CR570Q10VSF.
     CR560Q08V CR570Q10VSF.
     CM909Q01A CR570Q10VSF.
     CR550Q09VS CR570Q10VSF.
     CMA162Q01V CR570Q10VSF.
     CR560Q06VS CR570Q10VSF.
     CM464Q01A CR570Q10VSF.
     CM948Q02A CR570Q10VSF.
     CR453Q06A CR570Q10VSF.
     CR541Q05A CR570Q10VSF.
     CR566Q06VS CR570Q10VSF.
     CMA160Q01VS CR570Q10VSF.
     CMA147Q01V CR570Q10VSF.
     CMA140Q02VS CR570Q10VSF.
     CM949Q03VS CR570Q10VSF.
     CF102Q01V CR570Q10VSF.
     CR560Q10A CR570Q10VSF.
     CR560Q10V CR570Q10VSF.
     CR541Q11V CR570Q10VSF.
     CM496Q01V CR570Q10VSF.
     CMA149Q01V CR570Q10VSF.
     CR565Q01V CR570Q10VSF.
     CR543Q01VS CR570Q10VSF.
     CR466Q06A CR570Q10VSF.
     CF403Q01VS CR570Q10VSF.
     CMA107Q01VS CR570Q10VSF.
     CR220Q04VS CR570Q10VSF.
     CMA160Q03VS CR570Q10VSF.
     CR220Q05V CR570Q10VSF.
     CMA138Q02A CR570Q10VSF.
     CMA114Q01A CR570Q10VSF.
     CM948Q01A CR570Q10VSF.
     CF009Q02VS CR570Q10VSF.
     CR220Q01A CR570Q10VSF.
     CM905Q02VS CR570Q10VSF.
     CMA113Q02A CR570Q10VSF.
     CR543Q10VS CR570Q10VSF.
     CMA107Q01V CR570Q10VSF.
     CR543Q13A CR570Q10VSF.
     CM496Q01A CR570Q10VSF.
     CMA141Q01VS CR570Q10VSF.
     CR544Q12A CR570Q10VSF.
     CR570Q06A CR570Q10VSF.
     CMA125Q03A CR570Q10VSF.
     CMA140Q01A CR570Q10VSF.
     CMA143Q04V CR570Q10VSF.
     CR541Q01A CR570Q10VSF.
     CM474Q01V CR570Q10VSF.
     CM800Q01VS CR570Q10VSF.
     CR404Q10VS CR570Q10VSF.
     CMA112Q02WD CMA112Q02WDF.
     CMA112Q02HD CMA112Q02WDF.
     CMA107Q01F CR590Q66TTF.
     CR404Q10F CR590Q66TTF.
     CMA107Q01TT CR590Q66TTF.
     CR404Q10TT CR590Q66TTF.
     CR404Q07F CR590Q66TTF.
     CM936Q02F CR590Q66TTF.
     CR404Q07TT CR590Q66TTF.
     CR566Q05TT CR590Q66TTF.
     CM936Q02TT CR590Q66TTF.
     CMA145Q02F CR590Q66TTF.
     CMA145Q02TT CR590Q66TTF.
     CR404Q06F CR590Q66TTF.
     CR404Q06TT CR590Q66TTF.
     CMA158Q02F CR590Q66TTF.
     CM800Q01F CR590Q66TTF.
     CR404Q03F CR590Q66TTF.
     CM800Q01TT CR590Q66TTF.
     CR404Q03TT CR590Q66TTF.
     CMA145Q01F CR590Q66TTF.
     CM496Q02F CR590Q66TTF.
     CMA145Q01TT CR590Q66TTF.
     CM936Q01F CR590Q66TTF.
     CR559Q08TT CR590Q66TTF.
     CM936Q01TT CR590Q66TTF.
     CR559Q06F CR590Q66TTF.
     CR559Q06TT CR590Q66TTF.
     CMA138Q02TT CR590Q66TTF.
     CMA147Q04F CR590Q66TTF.
     CMA147Q04TT CR590Q66TTF.
     CR559Q03F CR590Q66TTF.
     CM496Q02TT CR590Q66TTF.
     CR559Q03TT CR590Q66TTF.
     CR559Q04F CR590Q66TTF.
     CR559Q04TT CR590Q66TTF.
     CMA147Q03F CR590Q66TTF.
     CM948Q03F CR590Q66TTF.
     CMA147Q03TT CR590Q66TTF.
     CR559Q01F CR590Q66TTF.
     CM954Q02F CR590Q66TTF.
     CR559Q01TT CR590Q66TTF.
     CM948Q03TT CR590Q66TTF.
     CR560Q08F CR590Q66TTF.
     CR560Q08TT CR590Q66TTF.
     CMA147Q02F CR590Q66TTF.
     CR560Q06F CR590Q66TTF.
     CM464Q01F CR590Q66TTF.
     CR560Q06TT CR590Q66TTF.
     CM905Q01TT CR590Q66TTF.
     CR560Q03TT CR590Q66TTF.
     CM464Q01TT CR590Q66TTF.
     CM948Q02F CR590Q66TTF.
     CMA147Q01F CR590Q66TTF.
     CM948Q02TT CR590Q66TTF.
     CMA147Q01TT CR590Q66TTF.
     CR560Q10F CR590Q66TTF.
     CR560Q10TT CR590Q66TTF.
     CR220Q06F CR590Q66TTF.
     CF009Q02F CR590Q66TTF.
     CR220Q06TT CR590Q66TTF.
     CMA130Q03F CR590Q66TTF.
     CR220Q05F CR590Q66TTF.
     CMA130Q03TT CR590Q66TTF.
     CR220Q05TT CR590Q66TTF.
     CM948Q01F CR590Q66TTF.
     CR220Q04F CR590Q66TTF.
     CM948Q01TT CR590Q66TTF.
     CR220Q04TT CR590Q66TTF.
     CMA130Q02F CR590Q66TTF.
     CM496Q01F CR590Q66TTF.
     CMA130Q02TT CR590Q66TTF.
     CR220Q02TT CR590Q66TTF.
     CM828Q03F CR590Q66TTF.
     CR220Q01F CR590Q66TTF.
     CR220Q01TT CR590Q66TTF.
     CR545Q07F CR590Q66TTF.
     CMA130Q01F CR590Q66TTF.
     CM828Q03TT CR590Q66TTF.
     CMA130Q01TT CR590Q66TTF.
     CM953Q04F CR590Q66TTF.
     CR545Q06F CR590Q66TTF.
     CR545Q06TT CR590Q66TTF.
     CM953Q04TT CR590Q66TTF.
     CR545Q04F CR590Q66TTF.
     CR545Q04TT CR590Q66TTF.
     CM496Q01TT CR590Q66TTF.
     CMA103Q05TT CR590Q66TTF.
     CR545Q03F CR590Q66TTF.
     CMA140Q03F CR590Q66TTF.
     CR545Q03TT CR590Q66TTF.
     CMA103Q04F CR590Q66TTF.
     CMA103Q04TT CR590Q66TTF.
     CM953Q03F CR590Q66TTF.
     CR545Q02F CR590Q66TTF.
     CR545Q02TT CR590Q66TTF.
     CR590Q66TT CR590Q66TTF.
     CR590Q26TT CR590Q66TTF.
     CR590Q62TT CR590Q66TTF.
     CM954Q04F CR590Q66TTF.
     CR590Q17TT CR590Q66TTF.
     CM954Q04TT CR590Q66TTF.
     CM828Q02F CR590Q66TTF.
     CF201Q01F CR590Q66TTF.
     CR590Q63TT CR590Q66TTF.
     CR590Q29TT CR590Q66TTF.
     CR590Q11TT CR590Q66TTF.
     CMA103Q01F CR590Q66TTF.
     CM828Q02TT CR590Q66TTF.
     CR590Q40TT CR590Q66TTF.
     CMA103Q01TT CR590Q66TTF.
     CR590Q49TT CR590Q66TTF.
     CM953Q02TT CR590Q66TTF.
     CMA148Q02TT CR590Q66TTF.
     CR566Q03TT CR590Q66TTF.
     CR590Q21TT CR590Q66TTF.
     CR566Q09F CR590Q66TTF.
     CR590Q36TT CR590Q66TTF.
     CMA152Q02F CR590Q66TTF.
     CR590Q08TT CR590Q66TTF.
     CMA152Q02TT CR590Q66TTF.
     CR590Q64TT CR590Q66TTF.
     CR590Q53TT CR590Q66TTF.
     CM943Q02F CR590Q66TTF.
     CR590Q54TT CR590Q66TTF.
     CR590Q39TT CR590Q66TTF.
     CMA152Q01F CR590Q66TTF.
     CM943Q02TT CR590Q66TTF.
     CMA152Q01TT CR590Q66TTF.
     CR562Q02F CR590Q66TTF.
     CR590Q32TT CR590Q66TTF.
     CF069Q01F CR590Q66TTF.
     CR590Q31TT CR590Q66TTF.
     CM155Q01F CR590Q66TTF.
     CR590Q07TT CR590Q66TTF.
     CM559Q01F CR590Q66TTF.
     CR590Q50TT CR590Q66TTF.
     CR590Q06TT CR590Q66TTF.
     CF300Q02F CR590Q66TTF.
     CMA131Q04F CR590Q66TTF.
     CMA131Q04TT CR590Q66TTF.
     CM559Q01TT CR590Q66TTF.
     CMA131Q02F CR590Q66TTF.
     CF401Q02TT CR590Q66TTF.
     CF401Q01TT CR590Q66TTF.
     CM943Q01TT CR590Q66TTF.
     CR566Q14F CR590Q66TTF.
     CF024Q02TT CR590Q66TTF.
     CF082Q02TT CR590Q66TTF.
     CF082Q01F CR590Q66TTF.
     CF300Q03F CR590Q66TTF.
     CF300Q03TT CR590Q66TTF.
     CR590Q15TT CR590Q66TTF.
     CF300Q02TT CR590Q66TTF.
     CR590Q19TT CR590Q66TTF.
     CMA131Q02TT CR590Q66TTF.
     CF300Q01F CR590Q66TTF.
     CF300Q01TT CR590Q66TTF.
     CR590Q44TT CR590Q66TTF.
     CF069Q01TT CR590Q66TTF.
     CR590Q48TT CR590Q66TTF.
     CR566Q12F CR590Q66TTF.
     CF203Q01F CR590Q66TTF.
     CF203Q01TT CR590Q66TTF.
     CMA131Q01F CR590Q66TTF.
     CMA131Q01TT CR590Q66TTF.
     CR590Q14TT CR590Q66TTF.
     CF106Q01TT CR590Q66TTF.
     CF082Q01TT CR590Q66TTF.
     CR590Q55TT CR590Q66TTF.
     CF307Q05TT CR590Q66TTF.
     CR590Q38TT CR590Q66TTF.
     CF307Q02F CR590Q66TTF.
     CF307Q02TT CR590Q66TTF.
     CR590Q23TT CR590Q66TTF.
     CMA154Q03F CR590Q66TTF.
     CR590Q34TT CR590Q66TTF.
     CF307Q01F CR590Q66TTF.
     CM954Q01F CR590Q66TTF.
     CMA113Q01F CR590Q66TTF.
     CF033Q02F CR590Q66TTF.
     CF033Q02TT CR590Q66TTF.
     CF033Q01TT CR590Q66TTF.
     CR590Q05TT CR590Q66TTF.
     CMA111Q02F CR590Q66TTF.
     CR590Q60TT CR590Q66TTF.
     CF102Q02F CR590Q66TTF.
     CR590Q41TT CR590Q66TTF.
     CR590Q09TT CR590Q66TTF.
     CF102Q01TT CR590Q66TTF.
     CR590Q57TT CR590Q66TTF.
     CF105Q02TT CR590Q66TTF.
     CR590Q13TT CR590Q66TTF.
     CF105Q01F CR590Q66TTF.
     CF024Q02F CR590Q66TTF.
     CMA154Q01TT CR590Q66TTF.
     CF403Q01TT CR590Q66TTF.
     CM954Q01TT CR590Q66TTF.
     CR590Q56TT CR590Q66TTF.
     CF105Q02F CR590Q66TTF.
     CMA131Q03TT CR590Q66TTF.
     CR590Q22TT CR590Q66TTF.
     CR590Q37TT CR590Q66TTF.
     CF303Q01F CR590Q66TTF.
     CF402Q01TT CR590Q66TTF.
     CMA162Q03F CR590Q66TTF.
     CF095Q02TT CR590Q66TTF.
     CF401Q01F CR590Q66TTF.
     CR590Q02TT CR590Q66TTF.
     CF095Q01TT CR590Q66TTF.
     CR590Q61TT CR590Q66TTF.
     CR590Q35TT CR590Q66TTF.
     CF068Q01F CR590Q66TTF.
     CF068Q01TT CR590Q66TTF.
     CM446Q01TT CR590Q66TTF.
     CMA162Q02F CR590Q66TTF.
     CR590Q24TT CR590Q66TTF.
     CF012Q01F CR590Q66TTF.
     CR590Q20TT CR590Q66TTF.
     CR590Q33TT CR590Q66TTF.
     CR590Q30TT CR590Q66TTF.
     CM955Q03TT CR590Q66TTF.
     CR590Q59TT CR590Q66TTF.
     CR553Q01F CR590Q66TTF.
     CF308Q04TT CR590Q66TTF.
     CR590Q03TT CR590Q66TTF.
     CMA162Q01F CR590Q66TTF.
     CMA162Q01TT CR590Q66TTF.
     CF308Q03TT CR590Q66TTF.
     CF308Q02F CR590Q66TTF.
     CF308Q01F CR590Q66TTF.
     CF308Q01TT CR590Q66TTF.
     CF103Q01TT CR590Q66TTF.
     CMA127Q03F CR590Q66TTF.
     CMA135Q03F CR590Q66TTF.
     CMA135Q03TT CR590Q66TTF.
     CF202Q01F CR590Q66TTF.
     CF202Q01TT CR590Q66TTF.
     CM420Q01F CR590Q66TTF.
     CF012Q02F CR590Q66TTF.
     CMA135Q02F CR590Q66TTF.
     CMA135Q02TT CR590Q66TTF.
     CF054Q01F CR590Q66TTF.
     CF054Q01TT CR590Q66TTF.
     CM420Q01TT CR590Q66TTF.
     CF303Q04F CR590Q66TTF.
     CM905Q02TT CR590Q66TTF.
     CF303Q04TT CR590Q66TTF.
     CMA135Q01F CR590Q66TTF.
     CF303Q03F CR590Q66TTF.
     CF303Q03TT CR590Q66TTF.
     CF303Q02TT CR590Q66TTF.
     CM305Q01TT CR590Q66TTF.
     CM034Q01F CR590Q66TTF.
     CMA111Q03F CR590Q66TTF.
     CMA111Q03TT CR590Q66TTF.
     CMA162Q03TT CR590Q66TTF.
     CMA127Q01F CR590Q66TTF.
     CF303Q01TT CR590Q66TTF.
     CMA127Q01TT CR590Q66TTF.
     CMA111Q02TT CR590Q66TTF.
     CM00GQ01TT CR590Q66TTF.
     CF097Q01F CR590Q66TTF.
     CF097Q01TT CR590Q66TTF.
     CR543Q03TT CR590Q66TTF.
     CF402Q02TT CR590Q66TTF.
     CM905Q01F CR590Q66TTF.
     CMA111Q01F CR590Q66TTF.
     CF201Q01TT CR590Q66TTF.
     CR590Q25TT CR590Q66TTF.
     CMA111Q01TT CR590Q66TTF.
     CF009Q02TT CR590Q66TTF.
     CMA138Q02F CR590Q66TTF.
     CMA154Q01F CR590Q66TTF.
     CMA121Q03F CR590Q66TTF.
     CR432Q06F CR590Q66TTF.
     CF102Q01F CR590Q66TTF.
     CF102Q02TT CR590Q66TTF.
     CR432Q06TT CR590Q66TTF.
     CMA121Q03TT CR590Q66TTF.
     CMA154Q02TT CR590Q66TTF.
     CM034Q01TT CR590Q66TTF.
     CF082Q02F CR590Q66TTF.
     CF051Q01F CR590Q66TTF.
     CMA121Q02F CR590Q66TTF.
     CMA121Q02TT CR590Q66TTF.
     CR432Q05TT CR590Q66TTF.
     CR590Q01TT CR590Q66TTF.
     CR432Q01TT CR590Q66TTF.
     CMA138Q01F CR590Q66TTF.
     CR102Q07F CR590Q66TTF.
     CR102Q07TT CR590Q66TTF.
     CMA121Q01F CR590Q66TTF.
     CM564Q02TT CR590Q66TTF.
     CMA158Q01TT CR590Q66TTF.
     CR102Q05F CR590Q66TTF.
     CR102Q04F CR590Q66TTF.
     CR102Q04TT CR590Q66TTF.
     CMA149Q03F CR590Q66TTF.
     CF105Q01TT CR590Q66TTF.
     CR460Q06F CR590Q66TTF.
     CM998Q02F CR590Q66TTF.
     CR460Q06TT CR590Q66TTF.
     CMA139Q02F CR590Q66TTF.
     CR460Q05TT CR590Q66TTF.
     CMA149Q02F CR590Q66TTF.
     CMA139Q02TT CR590Q66TTF.
     CMA116Q01TT CR590Q66TTF.
     CMA149Q02TT CR590Q66TTF.
     CM998Q02TT CR590Q66TTF.
     CR460Q01F CR590Q66TTF.
     CF106Q02F CR590Q66TTF.
     CR219Q02F CR590Q66TTF.
     CR219Q02TT CR590Q66TTF.
     CMA149Q01F CR590Q66TTF.
     CMA149Q01TT CR590Q66TTF.
     CR219Q01F CR590Q66TTF.
     CR567Q11F CR590Q66TTF.
     CM155Q02F CR590Q66TTF.
     CR219Q01TT CR590Q66TTF.
     CMA137Q01F CR590Q66TTF.
     CMA139Q01F CR590Q66TTF.
     CR567Q04TT CR590Q66TTF.
     CR567Q08TT CR590Q66TTF.
     CM155Q02TT CR590Q66TTF.
     CR567Q13F CR590Q66TTF.
     CM408Q01TT CR590Q66TTF.
     CR567Q13TT CR590Q66TTF.
     CMA135Q01TT CR590Q66TTF.
     CR567Q06F CR590Q66TTF.
     CMA161Q04F CR590Q66TTF.
     CR567Q06TT CR590Q66TTF.
     CR567Q04F CR590Q66TTF.
     CMA161Q04TT CR590Q66TTF.
     CMA137Q01TT CR590Q66TTF.
     CR544Q12TT CR590Q66TTF.
     CR567Q11TT CR590Q66TTF.
     CMA141Q04F CR590Q66TTF.
     CMA141Q04TT CR590Q66TTF.
     CMA127Q02F CR590Q66TTF.
     CMA161Q03F CR590Q66TTF.
     CR567Q10F CR590Q66TTF.
     CR567Q10TT CR590Q66TTF.
     CMA161Q03TT CR590Q66TTF.
     CMA141Q03F CR590Q66TTF.
     CR567Q03F CR590Q66TTF.
     CMA141Q03TT CR590Q66TTF.
     CR567Q03TT CR590Q66TTF.
     CM943Q01F CR590Q66TTF.
     CR590Q46TT CR590Q66TTF.
     CR562Q03F CR590Q66TTF.
     CM955Q02F CR590Q66TTF.
     CM905Q02F CR590Q66TTF.
     CR566Q12TT CR590Q66TTF.
     CMA141Q02F CR590Q66TTF.
     CR566Q09TT CR590Q66TTF.
     CR563Q12F CR590Q66TTF.
     CMA141Q02TT CR590Q66TTF.
     CM955Q02TT CR590Q66TTF.
     CMA131Q03F CR590Q66TTF.
     CR566Q06F CR590Q66TTF.
     CMA161Q02F CR590Q66TTF.
     CR566Q06TT CR590Q66TTF.
     CMA141Q01F CR590Q66TTF.
     CMA141Q01TT CR590Q66TTF.
     CR566Q14TT CR590Q66TTF.
     CM462Q01F CR590Q66TTF.
     CF012Q01TT CR590Q66TTF.
     CR590Q51TT CR590Q66TTF.
     CR566Q05F CR590Q66TTF.
     CMA135Q04F CR590Q66TTF.
     CMA158Q03F CR590Q66TTF.
     CMA158Q03TT CR590Q66TTF.
     CR566Q04F CR590Q66TTF.
     CR566Q04TT CR590Q66TTF.
     CR566Q03F CR590Q66TTF.
     CMA161Q01F CR590Q66TTF.
     CMA158Q02TT CR590Q66TTF.
     CM955Q01F CR590Q66TTF.
     CMA127Q02TT CR590Q66TTF.
     CMA161Q01TT CR590Q66TTF.
     CR570Q06F CR590Q66TTF.
     CR570Q06TT CR590Q66TTF.
     CM462Q01TT CR590Q66TTF.
     CR570Q05F CR590Q66TTF.
     CR570Q05TT CR590Q66TTF.
     CMA158Q01F CR590Q66TTF.
     CR570Q04F CR590Q66TTF.
     CR543Q10F CR590Q66TTF.
     CR570Q04TT CR590Q66TTF.
     CMA137Q03TT CR590Q66TTF.
     CMA108Q03F CR590Q66TTF.
     CMA108Q03TT CR590Q66TTF.
     CR570Q02F CR590Q66TTF.
     CR570Q02TT CR590Q66TTF.
     CMA150Q03F CR590Q66TTF.
     CM953Q02F CR590Q66TTF.
     CR590Q47TT CR590Q66TTF.
     CMA113Q02F CR590Q66TTF.
     CR570Q10F CR590Q66TTF.
     CMA150Q03TT CR590Q66TTF.
     CR570Q10TT CR590Q66TTF.
     CMA103Q02TT CR590Q66TTF.
     CR570Q08TT CR590Q66TTF.
     CM00GQ01F CR590Q66TTF.
     CR570Q01F CR590Q66TTF.
     CMA103Q02F CR590Q66TTF.
     CR570Q01TT CR590Q66TTF.
     CM273Q01F CR590Q66TTF.
     CMA108Q02F CR590Q66TTF.
     CM949Q03F CR590Q66TTF.
     CMA108Q02TT CR590Q66TTF.
     CMA150Q02F CR590Q66TTF.
     CM953Q03TT CR590Q66TTF.
     CR563Q12TT CR590Q66TTF.
     CMA150Q02TT CR590Q66TTF.
     CR563Q03F CR590Q66TTF.
     CR563Q03TT CR590Q66TTF.
     CM273Q01TT CR590Q66TTF.
     CMA108Q01TT CR590Q66TTF.
     CR563Q02F CR590Q66TTF.
     CR563Q02TT CR590Q66TTF.
     CM446Q02F CR590Q66TTF.
     CR563Q07TT CR590Q66TTF.
     CMA102Q03TT CR590Q66TTF.
     CMA150Q01F CR590Q66TTF.
     CR563Q10F CR590Q66TTF.
     CMA150Q01TT CR590Q66TTF.
     CR563Q10TT CR590Q66TTF.
     CMA102Q02F CR590Q66TTF.
     CR563Q09TT CR590Q66TTF.
     CMA102Q02TT CR590Q66TTF.
     CMA137Q03F CR590Q66TTF.
     CMA154Q02F CR590Q66TTF.
     CMA103Q05F CR590Q66TTF.
     CR544Q14F CR590Q66TTF.
     CR544Q14TT CR590Q66TTF.
     CM949Q03TT CR590Q66TTF.
     CMA102Q01F CR590Q66TTF.
     CMA102Q01TT CR590Q66TTF.
     CMA154Q03TT CR590Q66TTF.
     CR544Q13F CR590Q66TTF.
     CR544Q13TT CR590Q66TTF.
     CF402Q02F CR590Q66TTF.
     CMA114Q04F CR590Q66TTF.
     CMA114Q04TT CR590Q66TTF.
     CR544Q12F CR590Q66TTF.
     CM305Q01F CR590Q66TTF.
     CR545Q07TT CR590Q66TTF.
     CR544Q10F CR590Q66TTF.
     CR544Q10TT CR590Q66TTF.
     CMA123Q02F CR590Q66TTF.
     CM954Q02TT CR590Q66TTF.
     CMA123Q02TT CR590Q66TTF.
     CR544Q07F CR590Q66TTF.
     CM155Q01TT CR590Q66TTF.
     CR544Q07TT CR590Q66TTF.
     CMA114Q03F CR590Q66TTF.
     CR544Q06F CR590Q66TTF.
     CR544Q06TT CR590Q66TTF.
     CMA123Q01F CR590Q66TTF.
     CR220Q02F CR590Q66TTF.
     CMA123Q01TT CR590Q66TTF.
     CR567Q08F CR590Q66TTF.
     CR544Q04F CR590Q66TTF.
     CR544Q04TT CR590Q66TTF.
     CM949Q02TT CR590Q66TTF.
     CMA113Q03F CR590Q66TTF.
     CR543Q15TT CR590Q66TTF.
     CM442Q02F CR590Q66TTF.
     CR543Q13F CR590Q66TTF.
     CR543Q13TT CR590Q66TTF.
     CR543Q10TT CR590Q66TTF.
     CMA113Q02TT CR590Q66TTF.
     CMA127Q03TT CR590Q66TTF.
     CR543Q09F CR590Q66TTF.
     CR543Q09TT CR590Q66TTF.
     CMA114Q01F CR590Q66TTF.
     CR543Q04F CR590Q66TTF.
     CR543Q04TT CR590Q66TTF.
     CMA139Q01TT CR590Q66TTF.
     CMA114Q01TT CR590Q66TTF.
     CR543Q03F CR590Q66TTF.
     CM442Q02TT CR590Q66TTF.
     CMA113Q01TT CR590Q66TTF.
     CMA160Q01TT CR590Q66TTF.
     CR543Q01F CR590Q66TTF.
     CR543Q01TT CR590Q66TTF.
     CMA116Q03F CR590Q66TTF.
     CR541Q11F CR590Q66TTF.
     CMA116Q03TT CR590Q66TTF.
     CM447Q01F CR590Q66TTF.
     CR541Q10F CR590Q66TTF.
     CMA148Q03F CR590Q66TTF.
     CR541Q10TT CR590Q66TTF.
     CR560Q03F CR590Q66TTF.
     CMA148Q03TT CR590Q66TTF.
     CMA116Q02F CR590Q66TTF.
     CMA116Q02TT CR590Q66TTF.
     CR541Q09TT CR590Q66TTF.
     CM949Q01F CR590Q66TTF.
     CMA147Q02TT CR590Q66TTF.
     CR541Q05F CR590Q66TTF.
     CR541Q05TT CR590Q66TTF.
     CM949Q01TT CR590Q66TTF.
     CMA116Q01F CR590Q66TTF.
     CR541Q04F CR590Q66TTF.
     CM447Q01TT CR590Q66TTF.
     CR541Q04TT CR590Q66TTF.
     CMA148Q02F CR590Q66TTF.
     CMA135Q04TT CR590Q66TTF.
     CR541Q03F CR590Q66TTF.
     CR541Q03TT CR590Q66TTF.
     CMA142Q02F CR590Q66TTF.
     CMA142Q02TT CR590Q66TTF.
     CR541Q01TT CR590Q66TTF.
     CM408Q01F CR590Q66TTF.
     CR590Q42TT CR590Q66TTF.
     CR568Q13F CR590Q66TTF.
     CR568Q13TT CR590Q66TTF.
     CMA142Q01F CR590Q66TTF.
     CMA142Q01TT CR590Q66TTF.
     CR568Q10F CR590Q66TTF.
     CR568Q10TT CR590Q66TTF.
     CM474Q01F CR590Q66TTF.
     CR568Q08F CR590Q66TTF.
     CR568Q08TT CR590Q66TTF.
     CR552Q01F CR590Q66TTF.
     CMA148Q01TT CR590Q66TTF.
     CF307Q01TT CR590Q66TTF.
     CMA144Q03F CR590Q66TTF.
     CMA162Q02TT CR590Q66TTF.
     CR568Q15F CR590Q66TTF.
     CR568Q15TT CR590Q66TTF.
     CR568Q06F CR590Q66TTF.
     CMA161Q02TT CR590Q66TTF.
     CR568Q06TT CR590Q66TTF.
     CR568Q05F CR590Q66TTF.
     CR568Q05TT CR590Q66TTF.
     CR466Q03TT CR590Q66TTF.
     CMA144Q01F CR590Q66TTF.
     CMA144Q01TT CR590Q66TTF.
     CR568Q14TT CR590Q66TTF.
     CM909Q03F CR590Q66TTF.
     CR559Q08F CR590Q66TTF.
     CF308Q02TT CR590Q66TTF.
     CMA133Q02TT CR590Q66TTF.
     CR556Q12TT CR590Q66TTF.
     CM909Q03TT CR590Q66TTF.
     CMA157Q02F CR590Q66TTF.
     CMA157Q02TT CR590Q66TTF.
     CR590Q04TT CR590Q66TTF.
     CR556Q10F CR590Q66TTF.
     CR556Q10TT CR590Q66TTF.
     CR556Q09F CR590Q66TTF.
     CR556Q09TT CR590Q66TTF.
     CMA133Q01F CR590Q66TTF.
     CMA157Q01TT CR590Q66TTF.
     CF051Q01TT CR590Q66TTF.
     CMA133Q01TT CR590Q66TTF.
     CR556Q05F CR590Q66TTF.
     CR552Q06F CR590Q66TTF.
     CR556Q05TT CR590Q66TTF.
     CM474Q01TT CR590Q66TTF.
     CMA143Q04F CR590Q66TTF.
     CMA143Q01TT CR590Q66TTF.
     CMA143Q04TT CR590Q66TTF.
     CR556Q04TT CR590Q66TTF.
     CM564Q02F CR590Q66TTF.
     CR556Q03F CR590Q66TTF.
     CM909Q02F CR590Q66TTF.
     CR556Q03TT CR590Q66TTF.
     CR590Q27TT CR590Q66TTF.
     CMA143Q03F CR590Q66TTF.
     CMA143Q03TT CR590Q66TTF.
     CMA160Q03F CR590Q66TTF.
     CR556Q01TT CR590Q66TTF.
     CMA160Q03TT CR590Q66TTF.
     CR552Q08F CR590Q66TTF.
     CR552Q08TT CR590Q66TTF.
     CMA143Q02F CR590Q66TTF.
     CMA143Q02TT CR590Q66TTF.
     CR552Q04F CR590Q66TTF.
     CR552Q04TT CR590Q66TTF.
     CM919Q01F CR590Q66TTF.
     CR552Q03F CR590Q66TTF.
     CR552Q03TT CR590Q66TTF.
     CMA143Q01F CR590Q66TTF.
     CR552Q06TT CR590Q66TTF.
     CM803Q01F CR590Q66TTF.
     CM446Q02TT CR590Q66TTF.
     CMA160Q02F CR590Q66TTF.
     CMA160Q02TT CR590Q66TTF.
     CR552Q09F CR590Q66TTF.
     CMA102Q03F CR590Q66TTF.
     CR552Q09TT CR590Q66TTF.
     CMA151Q02F CR590Q66TTF.
     CMA151Q02TT CR590Q66TTF.
     CR552Q01TT CR590Q66TTF.
     CM803Q01TT CR590Q66TTF.
     CR453Q06F CR590Q66TTF.
     CM909Q01F CR590Q66TTF.
     CR453Q06TT CR590Q66TTF.
     CMA151Q01F CR590Q66TTF.
     CR453Q05F CR590Q66TTF.
     CR453Q05TT CR590Q66TTF.
     CMA151Q01TT CR590Q66TTF.
     CM909Q01TT CR590Q66TTF.
     CMA160Q01F CR590Q66TTF.
     CR453Q04F CR590Q66TTF.
     CR432Q05F CR590Q66TTF.
     CR453Q04TT CR590Q66TTF.
     CR453Q01F CR590Q66TTF.
     CR453Q01TT CR590Q66TTF.
     CF308Q04F CR590Q66TTF.
     CMA153Q02F CR590Q66TTF.
     CMA153Q02TT CR590Q66TTF.
     CR446Q06F CR590Q66TTF.
     CR446Q06TT CR590Q66TTF.
     CR446Q03F CR590Q66TTF.
     CR446Q03TT CR590Q66TTF.
     CMA153Q01F CR590Q66TTF.
     CM955Q01TT CR590Q66TTF.
     CM564Q01F CR590Q66TTF.
     CMA153Q01TT CR590Q66TTF.
     CR456Q06F CR590Q66TTF.
     CM00KQ02F CR590Q66TTF.
     CR456Q06TT CR590Q66TTF.
     CMA134Q03F CR590Q66TTF.
     CMA136Q03F CR590Q66TTF.
     CMA134Q03TT CR590Q66TTF.
     CR456Q02F CR590Q66TTF.
     CR456Q02TT CR590Q66TTF.
     CMA136Q03TT CR590Q66TTF.
     CR456Q01F CR590Q66TTF.
     CM564Q01TT CR590Q66TTF.
     CM00KQ02TT CR590Q66TTF.
     CR456Q01TT CR590Q66TTF.
     CMA134Q02F CR590Q66TTF.
     CM909Q02TT CR590Q66TTF.
     CR553Q07F CR590Q66TTF.
     CM955Q03F CR590Q66TTF.
     CMA134Q02TT CR590Q66TTF.
     CR553Q07TT CR590Q66TTF.
     CR553Q05F CR590Q66TTF.
     CR553Q05TT CR590Q66TTF.
     CF058Q01TT CR590Q66TTF.
     CMA134Q01F CR590Q66TTF.
     CMA134Q01TT CR590Q66TTF.
     CMA136Q02F CR590Q66TTF.
     CR553Q04F CR590Q66TTF.
     CR553Q04TT CR590Q66TTF.
     CMA136Q02TT CR590Q66TTF.
     CR553Q01TT CR590Q66TTF.
     CF058Q01F CR590Q66TTF.
     CR553Q02F CR590Q66TTF.
     CR553Q02TT CR590Q66TTF.
     CR563Q07F CR590Q66TTF.
     CMA128Q03F CR590Q66TTF.
     CMA128Q03TT CR590Q66TTF.
     CM906Q02F CR590Q66TTF.
     CR569Q06F CR590Q66TTF.
     CR569Q06TT CR590Q66TTF.
     CM906Q02TT CR590Q66TTF.
     CMA146Q03F CR590Q66TTF.
     CR569Q04F CR590Q66TTF.
     CR569Q04TT CR590Q66TTF.
     CMA146Q03TT CR590Q66TTF.
     CR569Q03F CR590Q66TTF.
     CR541Q09F CR590Q66TTF.
     CR569Q03TT CR590Q66TTF.
     CMA128Q02F CR590Q66TTF.
     CMA128Q02TT CR590Q66TTF.
     CR569Q02F CR590Q66TTF.
     CR569Q02TT CR590Q66TTF.
     CR569Q01F CR590Q66TTF.
     CR556Q01F CR590Q66TTF.
     CMA128Q01F CR590Q66TTF.
     CR569Q01TT CR590Q66TTF.
     CMA128Q01TT CR590Q66TTF.
     CMA146Q02F CR590Q66TTF.
     CMA146Q02TT CR590Q66TTF.
     CR562Q07F CR590Q66TTF.
     CR562Q07TT CR590Q66TTF.
     CR562Q06F CR590Q66TTF.
     CR562Q06TT CR590Q66TTF.
     CM906Q01F CR590Q66TTF.
     CR562Q05F CR590Q66TTF.
     CMA126Q04F CR590Q66TTF.
     CR562Q05TT CR590Q66TTF.
     CMA126Q04TT CR590Q66TTF.
     CM906Q01TT CR590Q66TTF.
     CR562Q03TT CR590Q66TTF.
     CMA146Q01F CR590Q66TTF.
     CR562Q02TT CR590Q66TTF.
     CMA126Q03F CR590Q66TTF.
     CMA146Q01TT CR590Q66TTF.
     CMA126Q03TT CR590Q66TTF.
     CF103Q01F CR590Q66TTF.
     CM411Q02F CR590Q66TTF.
     CM571Q01F CR590Q66TTF.
     CR550Q07F CR590Q66TTF.
     CR550Q07TT CR590Q66TTF.
     CR556Q04F CR590Q66TTF.
     CR550Q06F CR590Q66TTF.
     CR550Q06TT CR590Q66TTF.
     CMA126Q02F CR590Q66TTF.
     CMA126Q02TT CR590Q66TTF.
     CR550Q05F CR590Q66TTF.
     CM571Q01TT CR590Q66TTF.
     CR550Q05TT CR590Q66TTF.
     CR550Q04F CR590Q66TTF.
     CR550Q04TT CR590Q66TTF.
     CMA140Q03TT CR590Q66TTF.
     CR550Q10F CR590Q66TTF.
     CM411Q02TT CR590Q66TTF.
     CR550Q10TT CR590Q66TTF.
     CR550Q09F CR590Q66TTF.
     CM915Q02F CR590Q66TTF.
     CR550Q09TT CR590Q66TTF.
     CR466Q06F CR590Q66TTF.
     CR466Q06TT CR590Q66TTF.
     CR466Q03F CR590Q66TTF.
     CMA156Q01F CR590Q66TTF.
     CMA140Q02F CR590Q66TTF.
     CM915Q02TT CR590Q66TTF.
     CMA156Q01TT CR590Q66TTF.
     CR590Q58TT CR590Q66TTF.
     CMA140Q02TT CR590Q66TTF.
     CR466Q02F CR590Q66TTF.
     CR466Q02TT CR590Q66TTF.
     CMA132Q02F CR590Q66TTF.
     CR111Q06F CR590Q66TTF.
     CMA132Q02TT CR590Q66TTF.
     CR111Q06TT CR590Q66TTF.
     CR111Q02BF CR590Q66TTF.
     CR111Q02BTT CR590Q66TTF.
     CR111Q01F CR590Q66TTF.
     CMA132Q01F CR590Q66TTF.
     CR111Q01TT CR590Q66TTF.
     CF012Q02TT CR590Q66TTF.
     CMA140Q01F CR590Q66TTF.
     CR055Q03F CR590Q66TTF.
     CMA140Q01TT CR590Q66TTF.
     CR055Q03TT CR590Q66TTF.
     CMA129Q03F CR590Q66TTF.
     CR055Q02F CR590Q66TTF.
     CR055Q02TT CR590Q66TTF.
     CM915Q01F CR590Q66TTF.
     CMA129Q03TT CR590Q66TTF.
     CMA157Q01F CR590Q66TTF.
     CR541Q11TT CR590Q66TTF.
     CM915Q01TT CR590Q66TTF.
     CR055Q01F CR590Q66TTF.
     CR055Q01TT CR590Q66TTF.
     CR055Q05TT CR590Q66TTF.
     CMA125Q03F CR590Q66TTF.
     CMA129Q02TT CR590Q66TTF.
     CMA125Q03TT CR590Q66TTF.
     CR549Q13F CR590Q66TTF.
     CR549Q13TT CR590Q66TTF.
     CM603Q01F CR590Q66TTF.
     CMA129Q01F CR590Q66TTF.
     CMA129Q01TT CR590Q66TTF.
     CR549Q12F CR590Q66TTF.
     CR549Q12TT CR590Q66TTF.
     CR460Q05F CR590Q66TTF.
     CMA117Q04F CR590Q66TTF.
     CR549Q10F CR590Q66TTF.
     CR549Q10TT CR590Q66TTF.
     CMA125Q02F CR590Q66TTF.
     CMA117Q04TT CR590Q66TTF.
     CM919Q02TT CR590Q66TTF.
     CM603Q01TT CR590Q66TTF.
     CR549Q06F CR590Q66TTF.
     CMA125Q02TT CR590Q66TTF.
     CR549Q06TT CR590Q66TTF.
     CR549Q05F CR590Q66TTF.
     CM992Q03F CR590Q66TTF.
     CR549Q05TT CR590Q66TTF.
     CMA117Q03F CR590Q66TTF.
     CMA117Q03TT CR590Q66TTF.
     CR549Q04F CR590Q66TTF.
     CR549Q04TT CR590Q66TTF.
     CM992Q03TT CR590Q66TTF.
     CMA125Q01F CR590Q66TTF.
     CR564Q05F CR590Q66TTF.
     CR564Q05TT CR590Q66TTF.
     CR590Q52TT CR590Q66TTF.
     CMA125Q01TT CR590Q66TTF.
     CMA117Q02TT CR590Q66TTF.
     CM033Q01F CR590Q66TTF.
     CR564Q04F CR590Q66TTF.
     CR564Q04TT CR590Q66TTF.
     CR564Q03F CR590Q66TTF.
     CMA117Q01F CR590Q66TTF.
     CR564Q03TT CR590Q66TTF.
     CMA117Q01TT CR590Q66TTF.
     CR564Q02F CR590Q66TTF.
     CM919Q02F CR590Q66TTF.
     CMA110Q03F CR590Q66TTF.
     CR564Q02TT CR590Q66TTF.
     CMA110Q03TT CR590Q66TTF.
     CMA112Q03F CR590Q66TTF.
     CR564Q01TT CR590Q66TTF.
     CMA112Q03TT CR590Q66TTF.
     CM992Q02F CR590Q66TTF.
     CR561Q08F CR590Q66TTF.
     CF308Q03F CR590Q66TTF.
     CR556Q12F CR590Q66TTF.
     CMA149Q03TT CR590Q66TTF.
     CR561Q08TT CR590Q66TTF.
     CR561Q07F CR590Q66TTF.
     CM992Q02TT CR590Q66TTF.
     CR561Q07TT CR590Q66TTF.
     CMA110Q02F CR590Q66TTF.
     CR561Q06F CR590Q66TTF.
     CR561Q06TT CR590Q66TTF.
     CM033Q01TT CR590Q66TTF.
     CMA112Q02F CR590Q66TTF.
     CR563Q09F CR590Q66TTF.
     CR570Q08F CR590Q66TTF.
     CMA112Q02TT CR590Q66TTF.
     CR561Q04TT CR590Q66TTF.
     CR590Q43TT CR590Q66TTF.
     CM411Q01F CR590Q66TTF.
     CF033Q01F CR590Q66TTF.
     CM919Q01TT CR590Q66TTF.
     CMA112Q01F CR590Q66TTF.
     CR561Q03F CR590Q66TTF.
     CR561Q03TT CR590Q66TTF.
     CMA112Q01TT CR590Q66TTF.
     CR561Q01F CR590Q66TTF.
     CR561Q01TT CR590Q66TTF.
     CMA110Q01F CR590Q66TTF.
     CMA119Q03F CR590Q66TTF.
     CMA110Q01TT CR590Q66TTF.
     CMA119Q03TT CR590Q66TTF.
     CR542Q09F CR590Q66TTF.
     CF031Q01F CR590Q66TTF.
     CR542Q09TT CR590Q66TTF.
     CR542Q08F CR590Q66TTF.
     CM992Q01F CR590Q66TTF.
     CR542Q08TT CR590Q66TTF.
     CR543Q15F CR590Q66TTF.
     CMA119Q02F CR590Q66TTF.
     CMA119Q02TT CR590Q66TTF.
     CR561Q04F CR590Q66TTF.
     CR542Q05F CR590Q66TTF.
     CM192Q01F CR590Q66TTF.
     CR542Q05TT CR590Q66TTF.
     CM992Q01TT CR590Q66TTF.
     CR542Q02F CR590Q66TTF.
     CMA110Q02TT CR590Q66TTF.
     CR542Q02TT CR590Q66TTF.
     CR568Q14F CR590Q66TTF.
     CMA105Q05F CR590Q66TTF.
     CMA119Q01F CR590Q66TTF.
     CF031Q01TT CR590Q66TTF.
     CM411Q01TT CR590Q66TTF.
     CMA119Q01TT CR590Q66TTF.
     CR542Q01F CR590Q66TTF.
     CR542Q01TT CR590Q66TTF.
     CF095Q01F CR590Q66TTF.
     CMA105Q05TT CR590Q66TTF.
     CR540Q06F CR590Q66TTF.
     CR540Q06TT CR590Q66TTF.
     CR590Q16TT CR590Q66TTF.
     CMA115Q02F CR590Q66TTF.
     CM192Q01TT CR590Q66TTF.
     CMA115Q02TT CR590Q66TTF.
     CR540Q05F CR590Q66TTF.
     CR540Q05TT CR590Q66TTF.
     CR540Q04F CR590Q66TTF.
     CR540Q04TT CR590Q66TTF.
     CR564Q01F CR590Q66TTF.
     CMA105Q04F CR590Q66TTF.
     CMA115Q01F CR590Q66TTF.
     CMA115Q01TT CR590Q66TTF.
     CMA133Q02F CR590Q66TTF.
     CR540Q03F CR590Q66TTF.
     CM982Q04F CR590Q66TTF.
     CR540Q03TT CR590Q66TTF.
     CMA108Q01F CR590Q66TTF.
     CM446Q01F CR590Q66TTF.
     CMA105Q04TT CR590Q66TTF.
     CR540Q01F CR590Q66TTF.
     CM982Q04TT CR590Q66TTF.
     CR540Q01TT CR590Q66TTF.
     CMA144Q03TT CR590Q66TTF.
     CF095Q02F CR590Q66TTF.
     CMA101Q02F CR590Q66TTF.
     CMA101Q02TT CR590Q66TTF.
     CR455Q05F CR590Q66TTF.
     CF303Q02F CR590Q66TTF.
     CR455Q05TT CR590Q66TTF.
     CR590Q18TT CR590Q66TTF.
     CR102Q05TT CR590Q66TTF.
     CR455Q04F CR590Q66TTF.
     CMA101Q01F CR590Q66TTF.
     CR455Q04TT CR590Q66TTF.
     CMA101Q01TT CR590Q66TTF.
     CR455Q03F CR590Q66TTF.
     CMA105Q03F CR590Q66TTF.
     CR455Q03TT CR590Q66TTF.
     CMA117Q02F CR590Q66TTF.
     CMA109Q03F CR590Q66TTF.
     CR455Q02F CR590Q66TTF.
     CR455Q02TT CR590Q66TTF.
     CMA105Q03TT CR590Q66TTF.
     CMA109Q03TT CR590Q66TTF.
     CMA148Q01F CR590Q66TTF.
     CMA121Q01TT CR590Q66TTF.
     CR558Q10F CR590Q66TTF.
     CR558Q10TT CR590Q66TTF.
     CF403Q01F CR590Q66TTF.
     CMA109Q02F CR590Q66TTF.
     CMA109Q02TT CR590Q66TTF.
     CM982Q03F CR590Q66TTF.
     CR558Q09F CR590Q66TTF.
     CR558Q09TT CR590Q66TTF.
     CR558Q06F CR590Q66TTF.
     CR558Q06TT CR590Q66TTF.
     CM982Q03TT CR590Q66TTF.
     CMA109Q01F CR590Q66TTF.
     CMA105Q02F CR590Q66TTF.
     CMA109Q01TT CR590Q66TTF.
     CR558Q04F CR590Q66TTF.
     CR558Q04TT CR590Q66TTF.
     CMA105Q02TT CR590Q66TTF.
     CMA114Q03TT CR590Q66TTF.
     CR558Q12F CR590Q66TTF.
     CMA120Q03F CR590Q66TTF.
     CR558Q12TT CR590Q66TTF.
     CMA120Q03TT CR590Q66TTF.
     CMA138Q01TT CR590Q66TTF.
     CF402Q01F CR590Q66TTF.
     CR558Q02F CR590Q66TTF.
     CR590Q10TT CR590Q66TTF.
     CR558Q02TT CR590Q66TTF.
     CMA105Q01F CR590Q66TTF.
     CMA105Q01TT CR590Q66TTF.
     CMA120Q02F CR590Q66TTF.
     CR547Q07F CR590Q66TTF.
     CR547Q07TT CR590Q66TTF.
     CMA120Q02TT CR590Q66TTF.
     CR432Q01F CR590Q66TTF.
     CM423Q01F CR590Q66TTF.
     CR547Q06F CR590Q66TTF.
     CM949Q02F CR590Q66TTF.
     CR547Q06TT CR590Q66TTF.
     CR547Q03F CR590Q66TTF.
     CR547Q03TT CR590Q66TTF.
     CMA120Q01F CR590Q66TTF.
     CM982Q02F CR590Q66TTF.
     CM967Q03F CR590Q66TTF.
     CF307Q05F CR590Q66TTF.
     CMA120Q01TT CR590Q66TTF.
     CMA129Q02F CR590Q66TTF.
     CR055Q05F CR590Q66TTF.
     CR547Q10F CR590Q66TTF.
     CR547Q10TT CR590Q66TTF.
     CM967Q03TT CR590Q66TTF.
     CM155Q04F CR590Q66TTF.
     CM423Q01TT CR590Q66TTF.
     CF106Q01F CR590Q66TTF.
     CM982Q02TT CR590Q66TTF.
     CR590Q28TT CR590Q66TTF.
     CF401Q02F CR590Q66TTF.
     CMA124Q03F CR590Q66TTF.
     CM155Q04TT CR590Q66TTF.
     CF106Q02TT CR590Q66TTF.
     CMA124Q03TT CR590Q66TTF.
     CR590Q65TT CR590Q66TTF.
     CR547Q09F CR590Q66TTF.
     CR547Q09TT CR590Q66TTF.
     CMA124Q02F CR590Q66TTF.
     CMA124Q02TT CR590Q66TTF.
     CR547Q02F CR590Q66TTF.
     CM967Q01F CR590Q66TTF.
     CR547Q02TT CR590Q66TTF.
     CMA132Q01TT CR590Q66TTF.
     CR565Q09F CR590Q66TTF.
     CM967Q01TT CR590Q66TTF.
     CMA124Q01F CR590Q66TTF.
     CR565Q09TT CR590Q66TTF.
     CR541Q01F CR590Q66TTF.
     CMA124Q01TT CR590Q66TTF.
     CR460Q01TT CR590Q66TTF.
     CM982Q01F CR590Q66TTF.
     CR565Q08F CR590Q66TTF.
     CR565Q08TT CR590Q66TTF.
     CR565Q05F CR590Q66TTF.
     CMA107Q03F CR590Q66TTF.
     CR565Q05TT CR590Q66TTF.
     CR590Q45TT CR590Q66TTF.
     CMA107Q03TT CR590Q66TTF.
     CM939Q02F CR590Q66TTF.
     CM982Q01TT CR590Q66TTF.
     CR565Q03F CR590Q66TTF.
     CR565Q03TT CR590Q66TTF.
     CMA113Q03TT CR590Q66TTF.
     CM939Q02TT CR590Q66TTF.
     CMA107Q02F CR590Q66TTF.
     CR565Q02F CR590Q66TTF.
     CR565Q02TT CR590Q66TTF.
     CMA107Q02TT CR590Q66TTF.
     CR565Q01F CR590Q66TTF.
     CR565Q01TT CR590Q66TTF.
     CMA107Q01S CR590Q66SF.
     CR404Q07S CR590Q66SF.
     CMA145Q02S CR590Q66SF.
     CR404Q06S CR590Q66SF.
     CR404Q03S CR590Q66SF.
     CMA145Q01S CR590Q66SF.
     CM936Q01S CR590Q66SF.
     CR559Q06S CR590Q66SF.
     CM800Q01S CR590Q66SF.
     CMA147Q04S CR590Q66SF.
     CR559Q03S CR590Q66SF.
     CR559Q04S CR590Q66SF.
     CM496Q02S CR590Q66SF.
     CMA147Q03S CR590Q66SF.
     CR559Q01S CR590Q66SF.
     CM948Q03S CR590Q66SF.
     CR560Q08S CR590Q66SF.
     CMA147Q02S CR590Q66SF.
     CR560Q06S CR590Q66SF.
     CR560Q03S CR590Q66SF.
     CM948Q02S CR590Q66SF.
     CR560Q10S CR590Q66SF.
     CMA147Q01S CR590Q66SF.
     CM464Q01S CR590Q66SF.
     CR220Q06S CR590Q66SF.
     CR220Q05S CR590Q66SF.
     CMA130Q03S CR590Q66SF.
     CR220Q04S CR590Q66SF.
     CM948Q01S CR590Q66SF.
     CM155Q04S CR590Q66SF.
     CR220Q02S CR590Q66SF.
     CMA130Q02S CR590Q66SF.
     CR220Q01S CR590Q66SF.
     CR545Q07S CR590Q66SF.
     CM828Q03S CR590Q66SF.
     CR545Q06S CR590Q66SF.
     CMA103Q04S CR590Q66SF.
     CR545Q02S CR590Q66SF.
     CM953Q03S CR590Q66SF.
     CR590Q66S CR590Q66SF.
     CR590Q62S CR590Q66SF.
     CR590Q17S CR590Q66SF.
     CMA103Q02S CR590Q66SF.
     CR590Q63S CR590Q66SF.
     CR590Q29S CR590Q66SF.
     CR590Q11S CR590Q66SF.
     CR590Q40S CR590Q66SF.
     CR590Q49S CR590Q66SF.
     CR590Q21S CR590Q66SF.
     CR590Q36S CR590Q66SF.
     CR590Q08S CR590Q66SF.
     CR590Q64S CR590Q66SF.
     CR590Q53S CR590Q66SF.
     CR590Q54S CR590Q66SF.
     CR590Q39S CR590Q66SF.
     CR590Q51S CR590Q66SF.
     CM943Q02S CR590Q66SF.
     CR590Q32S CR590Q66SF.
     CR590Q31S CR590Q66SF.
     CM496Q01S CR590Q66SF.
     CR590Q07S CR590Q66SF.
     CR590Q50S CR590Q66SF.
     CR590Q06S CR590Q66SF.
     CMA131Q04S CR590Q66SF.
     CR590Q46S CR590Q66SF.
     CR590Q58S CR590Q66SF.
     CR590Q16S CR590Q66SF.
     CR590Q56S CR590Q66SF.
     CF082Q02S CR590Q66SF.
     CR590Q09S CR590Q66SF.
     CM559Q01S CR590Q66SF.
     CR590Q28S CR590Q66SF.
     CR590Q30S CR590Q66SF.
     CF300Q03S CR590Q66SF.
     CR590Q15S CR590Q66SF.
     CF300Q02S CR590Q66SF.
     CR590Q19S CR590Q66SF.
     CF300Q01S CR590Q66SF.
     CMA131Q02S CR590Q66SF.
     CR590Q44S CR590Q66SF.
     CF069Q01S CR590Q66SF.
     CR590Q48S CR590Q66SF.
     CR590Q26S CR590Q66SF.
     CM954Q04S CR590Q66SF.
     CR590Q65S CR590Q66SF.
     CF106Q02S CR590Q66SF.
     CR590Q14S CR590Q66SF.
     CMA131Q01S CR590Q66SF.
     CF307Q05S CR590Q66SF.
     CR590Q38S CR590Q66SF.
     CF307Q02S CR590Q66SF.
     CR590Q23S CR590Q66SF.
     CR590Q34S CR590Q66SF.
     CR590Q47S CR590Q66SF.
     CM943Q01S CR590Q66SF.
     CR590Q22S CR590Q66SF.
     CF033Q02S CR590Q66SF.
     CR590Q01S CR590Q66SF.
     CF033Q01S CR590Q66SF.
     CR590Q05S CR590Q66SF.
     CMA154Q02S CR590Q66SF.
     CR590Q60S CR590Q66SF.
     CR590Q41S CR590Q66SF.
     CF102Q01S CR590Q66SF.
     CR590Q57S CR590Q66SF.
     CF105Q02S CR590Q66SF.
     CR590Q13S CR590Q66SF.
     CF105Q01S CR590Q66SF.
     CR590Q25S CR590Q66SF.
     CMA154Q01S CR590Q66SF.
     CR590Q45S CR590Q66SF.
     CM954Q01S CR590Q66SF.
     CR590Q42S CR590Q66SF.
     CM155Q01S CR590Q66SF.
     CR590Q37S CR590Q66SF.
     CR590Q10S CR590Q66SF.
     CF095Q02S CR590Q66SF.
     CR590Q02S CR590Q66SF.
     CF095Q01S CR590Q66SF.
     CR590Q61S CR590Q66SF.
     CF031Q01S CR590Q66SF.
     CR590Q35S CR590Q66SF.
     CR590Q52S CR590Q66SF.
     CM919Q02S CR590Q66SF.
     CR590Q43S CR590Q66SF.
     CF012Q02S CR590Q66SF.
     CM446Q01S CR590Q66SF.
     CR590Q24S CR590Q66SF.
     CF012Q01S CR590Q66SF.
     CR590Q20S CR590Q66SF.
     CR590Q33S CR590Q66SF.
     CR590Q59S CR590Q66SF.
     CR590Q27S CR590Q66SF.
     CF308Q03S CR590Q66SF.
     CR590Q04S CR590Q66SF.
     CMA162Q01S CR590Q66SF.
     CM919Q01S CR590Q66SF.
     CMA135Q04S CR590Q66SF.
     CF308Q01S CR590Q66SF.
     CMA127Q03S CR590Q66SF.
     CF202Q01S CR590Q66SF.
     CMA135Q02S CR590Q66SF.
     CF303Q03S CR590Q66SF.
     CMA135Q01S CR590Q66SF.
     CF303Q02S CR590Q66SF.
     CMA111Q02S CR590Q66SF.
     CF097Q01S CR590Q66SF.
     CMA111Q01S CR590Q66SF.
     CF009Q02S CR590Q66SF.
     CMA121Q03S CR590Q66SF.
     CMA138Q02S CR590Q66SF.
     CR432Q06S CR590Q66SF.
     CM905Q01S CR590Q66SF.
     CM420Q01S CR590Q66SF.
     CR102Q07S CR590Q66SF.
     CM034Q01S CR590Q66SF.
     CMA138Q01S CR590Q66SF.
     CR460Q06S CR590Q66SF.
     CR460Q05S CR590Q66SF.
     CMA149Q02S CR590Q66SF.
     CMA139Q01S CR590Q66SF.
     CR567Q08S CR590Q66SF.
     CR567Q13S CR590Q66SF.
     CMA137Q03S CR590Q66SF.
     CR567Q06S CR590Q66SF.
     CR567Q04S CR590Q66SF.
     CMA137Q01S CR590Q66SF.
     CR567Q11S CR590Q66SF.
     CMA141Q04S CR590Q66SF.
     CR567Q10S CR590Q66SF.
     CMA141Q03S CR590Q66SF.
     CMA141Q02S CR590Q66SF.
     CR566Q06S CR590Q66SF.
     CMA141Q01S CR590Q66SF.
     CR566Q14S CR590Q66SF.
     CMA161Q02S CR590Q66SF.
     CR566Q05S CR590Q66SF.
     CM408Q01S CR590Q66SF.
     CR566Q04S CR590Q66SF.
     CR570Q06S CR590Q66SF.
     CR570Q05S CR590Q66SF.
     CMA158Q01S CR590Q66SF.
     CR570Q04S CR590Q66SF.
     CR570Q02S CR590Q66SF.
     CMA108Q03S CR590Q66SF.
     CR570Q08S CR590Q66SF.
     CR570Q01S CR590Q66SF.
     CMA108Q02S CR590Q66SF.
     CM00GQ01S CR590Q66SF.
     CMA150Q02S CR590Q66SF.
     CR563Q03S CR590Q66SF.
     CMA108Q01S CR590Q66SF.
     CR563Q02S CR590Q66SF.
     CR563Q07S CR590Q66SF.
     CMA102Q03S CR590Q66SF.
     CR563Q10S CR590Q66SF.
     CMA150Q01S CR590Q66SF.
     CMA102Q01S CR590Q66SF.
     CF307Q01S CR590Q66SF.
     CR544Q12S CR590Q66SF.
     CR544Q10S CR590Q66SF.
     CMA123Q02S CR590Q66SF.
     CR544Q06S CR590Q66SF.
     CM273Q01S CR590Q66SF.
     CR544Q04S CR590Q66SF.
     CMA113Q03S CR590Q66SF.
     CR543Q13S CR590Q66SF.
     CR543Q10S CR590Q66SF.
     CR543Q09S CR590Q66SF.
     CM949Q02S CR590Q66SF.
     CR543Q04S CR590Q66SF.
     CMA114Q01S CR590Q66SF.
     CR543Q03S CR590Q66SF.
     CMA113Q01S CR590Q66SF.
     CR543Q01S CR590Q66SF.
     CR541Q10S CR590Q66SF.
     CM442Q02S CR590Q66SF.
     CR541Q05S CR590Q66SF.
     CMA116Q01S CR590Q66SF.
     CF308Q02S CR590Q66SF.
     CR541Q03S CR590Q66SF.
     CMA148Q02S CR590Q66SF.
     CR541Q01S CR590Q66SF.
     CM949Q01S CR590Q66SF.
     CMA142Q01S CR590Q66SF.
     CR568Q10S CR590Q66SF.
     CM447Q01S CR590Q66SF.
     CR568Q08S CR590Q66SF.
     CR568Q15S CR590Q66SF.
     CMA148Q01S CR590Q66SF.
     CR568Q05S CR590Q66SF.
     CMA144Q01S CR590Q66SF.
     CR568Q14S CR590Q66SF.
     CM909Q03S CR590Q66SF.
     CMA157Q02S CR590Q66SF.
     CR556Q10S CR590Q66SF.
     CR556Q05S CR590Q66SF.
     CMA133Q01S CR590Q66SF.
     CR556Q04S CR590Q66SF.
     CMA143Q04S CR590Q66SF.
     CR556Q03S CR590Q66SF.
     CR590Q03S CR590Q66SF.
     CMA143Q03S CR590Q66SF.
     CR556Q01S CR590Q66SF.
     CMA160Q03S CR590Q66SF.
     CF308Q04S CR590Q66SF.
     CM909Q02S CR590Q66SF.
     CMA143Q02S CR590Q66SF.
     CR552Q06S CR590Q66SF.
     CMA143Q01S CR590Q66SF.
     CM564Q02S CR590Q66SF.
     CR552Q09S CR590Q66SF.
     CR552Q01S CR590Q66SF.
     CMA151Q02S CR590Q66SF.
     CR453Q05S CR590Q66SF.
     CM909Q01S CR590Q66SF.
     CR453Q01S CR590Q66SF.
     CM803Q01S CR590Q66SF.
     CMA153Q02S CR590Q66SF.
     CM474Q01S CR590Q66SF.
     CR446Q03S CR590Q66SF.
     CMA134Q03S CR590Q66SF.
     CMA136Q03S CR590Q66SF.
     CR456Q01S CR590Q66SF.
     CR553Q07S CR590Q66SF.
     CR553Q05S CR590Q66SF.
     CR553Q01S CR590Q66SF.
     CM564Q01S CR590Q66SF.
     CR553Q02S CR590Q66SF.
     CR569Q04S CR590Q66SF.
     CR569Q03S CR590Q66SF.
     CR569Q02S CR590Q66SF.
     CR569Q01S CR590Q66SF.
     CR562Q07S CR590Q66SF.
     CMA146Q02S CR590Q66SF.
     CR562Q05S CR590Q66SF.
     CMA126Q04S CR590Q66SF.
     CR562Q02S CR590Q66SF.
     CM906Q01S CR590Q66SF.
     CMA146Q01S CR590Q66SF.
     CMA126Q03S CR590Q66SF.
     CR550Q06S CR590Q66SF.
     CR550Q05S CR590Q66SF.
     CR550Q04S CR590Q66SF.
     CMA140Q03S CR590Q66SF.
     CR466Q06S CR590Q66SF.
     CM571Q01S CR590Q66SF.
     CR466Q03S CR590Q66SF.
     CM915Q02S CR590Q66SF.
     CMA140Q02S CR590Q66SF.
     CMA132Q02S CR590Q66SF.
     CR111Q01S CR590Q66SF.
     CMA140Q01S CR590Q66SF.
     CM411Q02S CR590Q66SF.
     CMA139Q02S CR590Q66SF.
     CMA129Q03S CR590Q66SF.
     CR055Q01S CR590Q66SF.
     CM915Q01S CR590Q66SF.
     CR549Q13S CR590Q66SF.
     CMA125Q03S CR590Q66SF.
     CMA129Q01S CR590Q66SF.
     CR549Q12S CR590Q66SF.
     CR549Q10S CR590Q66SF.
     CR549Q06S CR590Q66SF.
     CR549Q04S CR590Q66SF.
     CMA117Q02S CR590Q66SF.
     CR564Q04S CR590Q66SF.
     CR564Q03S CR590Q66SF.
     CMA117Q01S CR590Q66SF.
     CR564Q02S CR590Q66SF.
     CM603Q01S CR590Q66SF.
     CR564Q01S CR590Q66SF.
     CR561Q08S CR590Q66SF.
     CM992Q02S CR590Q66SF.
     CMA110Q02S CR590Q66SF.
     CR561Q04S CR590Q66SF.
     CMA112Q01S CR590Q66SF.
     CR561Q03S CR590Q66SF.
     CR561Q01S CR590Q66SF.
     CR542Q09S CR590Q66SF.
     CMA110Q01S CR590Q66SF.
     CR542Q08S CR590Q66SF.
     CMA119Q02S CR590Q66SF.
     CR542Q05S CR590Q66SF.
     CM992Q01S CR590Q66SF.
     CMA119Q01S CR590Q66SF.
     CR542Q01S CR590Q66SF.
     CMA105Q05S CR590Q66SF.
     CR540Q06S CR590Q66SF.
     CR590Q18S CR590Q66SF.
     CMA115Q02S CR590Q66SF.
     CR540Q05S CR590Q66SF.
     CM411Q01S CR590Q66SF.
     CMA115Q01S CR590Q66SF.
     CR540Q03S CR590Q66SF.
     CR540Q01S CR590Q66SF.
     CM033Q01S CR590Q66SF.
     CMA101Q02S CR590Q66SF.
     CR455Q05S CR590Q66SF.
     CM982Q04S CR590Q66SF.
     CR455Q04S CR590Q66SF.
     CM192Q01S CR590Q66SF.
     CMA109Q03S CR590Q66SF.
     CM305Q01S CR590Q66SF.
     CMA105Q03S CR590Q66SF.
     CMA109Q02S CR590Q66SF.
     CR558Q09S CR590Q66SF.
     CR558Q06S CR590Q66SF.
     CMA109Q01S CR590Q66SF.
     CMA105Q02S CR590Q66SF.
     CM982Q03S CR590Q66SF.
     CR590Q55S CR590Q66SF.
     CMA120Q03S CR590Q66SF.
     CR558Q02S CR590Q66SF.
     CMA105Q01S CR590Q66SF.
     CR547Q06S CR590Q66SF.
     CR547Q03S CR590Q66SF.
     CMA120Q01S CR590Q66SF.
     CM967Q03S CR590Q66SF.
     CM982Q02S CR590Q66SF.
     CR547Q10S CR590Q66SF.
     CR547Q02S CR590Q66SF.
     CR565Q09S CR590Q66SF.
     CM423Q01S CR590Q66SF.
     CM967Q01S CR590Q66SF.
     CMA124Q01S CR590Q66SF.
     CR565Q08S CR590Q66SF.
     CR565Q03S CR590Q66SF.
     CM982Q01S CR590Q66SF.
     CM939Q02S CR590Q66SF.
     CMA107Q02S CR590Q66SF.
     CR565Q01S CR590Q66SF.
     CMA130Q01S DMA146Q03CF.
     CR545Q03S DMA146Q03CF.
     CMA152Q01S DMA146Q03CF.
     CMA131Q03S DMA146Q03CF.
     CF402Q02S DMA146Q03CF.
     CMA162Q03S DMA146Q03CF.
     CMA162Q02S DMA146Q03CF.
     CF303Q01S DMA146Q03CF.
     CMA121Q02S DMA146Q03CF.
     CMA121Q01S DMA146Q03CF.
     CM955Q03S DMA146Q03CF.
     CMA161Q03S DMA146Q03CF.
     CR566Q09S DMA146Q03CF.
     CMA158Q02S DMA146Q03CF.
     CMA161Q01S DMA146Q03CF.
     CR544Q14S DMA146Q03CF.
     CMA123Q01S DMA146Q03CF.
     CMA114Q03S DMA146Q03CF.
     CMA149Q01S DMA146Q03CF.
     CMA113Q02S DMA146Q03CF.
     CMA116Q03S DMA146Q03CF.
     CMA144Q03S DMA146Q03CF.
     CR556Q12S DMA146Q03CF.
     CMA160Q02S DMA146Q03CF.
     CMA151Q01S DMA146Q03CF.
     CMA160Q01S DMA146Q03CF.
     CMA134Q02S DMA146Q03CF.
     CMA134Q01S DMA146Q03CF.
     CMA128Q03S DMA146Q03CF.
     DMA146Q03C DMA146Q03CF.
     CMA128Q01S DMA146Q03CF.
     CMA126Q02S DMA146Q03CF.
     CMA132Q01S DMA146Q03CF.
     CMA117Q04S DMA146Q03CF.
     CMA112Q03S DMA146Q03CF.
     CMA112Q02S DMA146Q03CF.
     CMA105Q04S DMA146Q03CF.
     CR558Q10S DMA146Q03CF.
     CR547Q07S DMA146Q03CF.
     CMA120Q02S DMA146Q03CF.
     LANGTEST_COG LANGTEST_COGF.
     CF303Q01W CF303Q01WF.
     CR545Q03SD CR570Q04SDF.
     CR545Q03SC CR570Q04SDF.
     CR545Q03SB CR570Q04SDF.
     CR545Q03SA CR570Q04SDF.
     CF307Q01SC CR570Q04SDF.
     CF307Q01SA CR570Q04SDF.
     CF308Q04SD CR570Q04SDF.
     CF308Q04SB CR570Q04SDF.
     CF308Q04SA CR570Q04SDF.
     CF308Q02SC CR570Q04SDF.
     CF308Q02SB CR570Q04SDF.
     CF308Q02SA CR570Q04SDF.
     CF308Q01SC CR570Q04SDF.
     CF308Q01SB CR570Q04SDF.
     CF308Q01SA CR570Q04SDF.
     CR567Q08SD CR570Q04SDF.
     CR567Q08SC CR570Q04SDF.
     CR567Q08SB CR570Q04SDF.
     CR567Q08SA CR570Q04SDF.
     CR567Q11SF CR570Q04SDF.
     CR567Q11SD CR570Q04SDF.
     CR567Q11SC CR570Q04SDF.
     CR567Q11SA CR570Q04SDF.
     CR567Q08SE CR570Q04SDF.
     CR570Q04SD CR570Q04SDF.
     CR570Q04SC CR570Q04SDF.
     CR570Q04SB CR570Q04SDF.
     CR570Q04SA CR570Q04SDF.
     CF307Q01SB CR570Q04SDF.
     CR544Q14SB CR570Q04SDF.
     CR544Q14SA CR570Q04SDF.
     CR544Q14SE CR570Q04SDF.
     CR544Q14SD CR570Q04SDF.
     CR544Q14SC CR570Q04SDF.
     CR556Q12SB CR570Q04SDF.
     CR556Q12SA CR570Q04SDF.
     CF308Q04SC CR570Q04SDF.
     CR556Q12SD CR570Q04SDF.
     CR556Q12SC CR570Q04SDF.
     CR549Q12SD CR570Q04SDF.
     CR549Q12SB CR570Q04SDF.
     CR549Q12SA CR570Q04SDF.
     CR549Q13SD CR570Q04SDF.
     CR549Q13SC CR570Q04SDF.
     CR549Q13SB CR570Q04SDF.
     CR561Q04SC CR570Q04SDF.
     CR561Q04SB CR570Q04SDF.
     CR561Q04SA CR570Q04SDF.
     CR558Q10SA CR570Q04SDF.
     CR558Q02SC CR570Q04SDF.
     CR558Q02SB CR570Q04SDF.
     CR558Q02SA CR570Q04SDF.
     CR558Q10SD CR570Q04SDF.
     CR558Q10SC CR570Q04SDF.
     CR558Q10SB CR570Q04SDF.
     CR547Q07SE CR570Q04SDF.
     CR547Q07SD CR570Q04SDF.
     CR547Q07SC CR570Q04SDF.
     CR547Q07SB CR570Q04SDF.
     CR547Q07SA CR570Q04SDF.
     CR547Q07SF CR570Q04SDF.
     CMA103Q05S CMA116Q02SF.
     CMA116Q02S CMA116Q02SF.
     CMA152Q02S CMA152Q02SF.
     CMA128Q02S CMA152Q02SF.
     CMA127Q01S CMA133Q02SF.
     CMA114Q04S CMA133Q02SF.
     CMA133Q02S CMA133Q02SF.
     CMA125Q02S CMA125Q02SF.
     CMA135Q03S CMA157Q01SF.
     CMA157Q01S CMA157Q01SF.
     CMA117Q03S CR561Q06SF.
     CR561Q06S CR561Q06SF.
     CMA101Q01S CR561Q06SF.
     CMA124Q02S CR561Q06SF.
     CMA125Q01S CMA125Q01SF.
     CMA129Q02S CMA129Q02SF.
     Option_UH Option_UHF.
     Option_FL Option_UHF.
     Option_CT Option_UHF.
     OECD Option_UHF.
     CNT $CNTF.
     RDESIGN RDESIGNF.
     RCORE_TEST RCORE_TESTF.
     RS1_TEST RS1_TESTF.
     RS2_TEST RS2_TESTF.
     RS2_LEV RS2_LEVF.
     RS1_LEV RS2_LEVF.
     RCO1S_PERF RCORE_PERFF.
     RCORE_PERF RCORE_PERFF.
     DR545Q04C DR570Q10CF.
     DF303Q04C DR570Q10CF.
     DR567Q03C DR570Q10CF.
     DR566Q12C DR570Q10CF.
     DR566Q03C DR570Q10CF.
     DR570Q10C DR570Q10CF.
     DR563Q14C DR570Q10CF.
     DR563Q13C DR570Q10CF.
     DR563Q12C DR570Q10CF.
     DR563Q09C DR570Q10CF.
     DMA102Q02C DR570Q10CF.
     DR544Q13C DR570Q10CF.
     DR544Q07C DR570Q10CF.
     DR543Q15C DR570Q10CF.
     DR541Q11C DR570Q10CF.
     DR541Q09C DR570Q10CF.
     DR541Q04C DR570Q10CF.
     DR568Q13C DR570Q10CF.
     DR568Q06C DR570Q10CF.
     DR556Q09C DR570Q10CF.
     DR552Q08C DR570Q10CF.
     DR552Q04C DR570Q10CF.
     DR552Q11C DR570Q10CF.
     DR552Q03C DR570Q10CF.
     DMA153Q01C DR570Q10CF.
     DR553Q06C DR570Q10CF.
     DR553Q04C DR570Q10CF.
     DR569Q06C DR570Q10CF.
     DR562Q03C DR570Q10CF.
     DR550Q07C DR570Q10CF.
     DR550Q10C DR570Q10CF.
     DR550Q09C DR570Q10CF.
     DR549Q05C DR570Q10CF.
     DR564Q05C DR570Q10CF.
     DR561Q07C DR570Q10CF.
     DR542Q02C DR570Q10CF.
     DR540Q04C DR570Q10CF.
     DR558Q04C DR570Q10CF.
     DR558Q12C DR570Q10CF.
     DR565Q05C DR570Q10CF.
     DR565Q02C DR570Q10CF.
     DM953Q02C DM998Q02CF.
     DM954Q02C DM998Q02CF.
     DM446Q02C DM998Q02CF.
     DF402Q01C DM998Q02CF.
     DM905Q02C DM998Q02CF.
     DM998Q02C DM998Q02CF.
     DM955Q02C DM998Q02CF.
     DM955Q01C DM998Q02CF.
     DM00KQ02C DM998Q02CF.
     DM992Q03C DM998Q02CF.
     DR559Q08C DR562Q06CF.
     DF082Q01C DR562Q06CF.
     DF203Q01C DR562Q06CF.
     DMA154Q03C DR562Q06CF.
     DF102Q02C DR562Q06CF.
     DMA127Q02C DR562Q06CF.
     DMA158Q03C DR562Q06CF.
     DMA150Q03C DR562Q06CF.
     DMA148Q03C DR562Q06CF.
     DMA142Q02C DR562Q06CF.
     DR562Q06C DR562Q06CF.
     DMA156Q01C DR562Q06CF.
     DR111Q06C DR562Q06CF.
     DR111Q02BC DR562Q06CF.
     DMA110Q03C DR562Q06CF.
     DMA124Q03C DR562Q06CF.
     DR547Q09C DR562Q06CF.
     DF401Q01C DM949Q03CF.
     DM949Q03C DM949Q03CF.
     DM906Q02C DM949Q03CF.
     DM155Q02C DM155Q02CF.
     DM462Q01C DM462Q01CF.
     DR404Q10BC DR466Q02CF.
     DR404Q10AC DR466Q02CF.
     DMA103Q01C DR466Q02CF.
     DM828Q02C DR466Q02CF.
     DF401Q02C DR466Q02CF.
     DF106Q01C DR466Q02CF.
     DF403Q01C DR466Q02CF.
     DF068Q01C DR466Q02CF.
     DF103Q01C DR466Q02CF.
     DF058Q01C DR466Q02CF.
     DF054Q01C DR466Q02CF.
     DMA111Q03C DR466Q02CF.
     DR432Q05C DR466Q02CF.
     DR432Q01C DR466Q02CF.
     DR102Q05C DR466Q02CF.
     DR102Q04C DR466Q02CF.
     DMA149Q03C DR466Q02CF.
     DR460Q01C DR466Q02CF.
     DR219Q02C DR466Q02CF.
     DR219Q01EC DR466Q02CF.
     DR219Q01C DR466Q02CF.
     DR219Q01DC DR466Q02CF.
     DR219Q01CC DR466Q02CF.
     DR219Q01BC DR466Q02CF.
     DR219Q01AC DR466Q02CF.
     DR453Q06C DR466Q02CF.
     DR453Q04C DR466Q02CF.
     DR446Q06C DR466Q02CF.
     DR456Q06C DR466Q02CF.
     DR456Q02C DR466Q02CF.
     DR466Q02C DR466Q02CF.
     DR055Q02C DR466Q02CF.
     DR055Q05C DR466Q02CF.
     DR455Q03C DR466Q02CF.
     DR455Q02C DR466Q02CF.
     DM936Q02C DM936Q02CF.
     DM953Q04C DM953Q04CF.
     DF024Q02C DF024Q02CF.
     DF051Q01C DF201Q01CF.
     DF201Q01C DF201Q01CF.
     DMA136Q02C DMA136Q02CF.
     DMA119Q03C DMA119Q03CF.
     DMA107Q03C DMA119Q03CF.
     ADMINMODE ADMINMODEF.
     CNTRYID CNTRYIDF.
     BOOKID BOOKIDF.
     SUBNATIO $SUBNATIOF.
     MPATH MPATHF.
     MS2_ItemSet MS2_ItemSetF.
     MS1_ItemSet MS2_ItemSetF.
     MCORE_ItemSet MS2_ItemSetF.
     MS1_TEST MS2_TESTF.
     MCORE_TEST MS2_TESTF.
     MS2_TEST MS2_TESTF.
     MS1_LEV MS1_LEVF.
     MS2_LEV MS2_LEVF.
     REGION REGIONF.
     DR055Q03C DR055Q03CF.
     NatCen $NatCenF.
     DR404Q07RC DR570Q04RDF.
     DR404Q07RB DR570Q04RDF.
     DR404Q07RA DR570Q04RDF.
     DM155Q04RC DR570Q04RDF.
     DM155Q04RB DR570Q04RDF.
     DM155Q04RA DR570Q04RDF.
     DMA130Q02RB DR570Q04RDF.
     DMA130Q02RA DR570Q04RDF.
     DM496Q01RD DR570Q04RDF.
     DR545Q03RD DR570Q04RDF.
     DR545Q03RC DR570Q04RDF.
     DR545Q03RB DR570Q04RDF.
     DR545Q03RA DR570Q04RDF.
     DM496Q01RC DR570Q04RDF.
     DM496Q01RB DR570Q04RDF.
     DM496Q01RA DR570Q04RDF.
     DMA152Q01RC DR570Q04RDF.
     DMA152Q01RB DR570Q04RDF.
     DMA152Q01RA DR570Q04RDF.
     DF069Q01RC DR570Q04RDF.
     DF069Q01RB DR570Q04RDF.
     DF069Q01RA DR570Q04RDF.
     DF307Q01RC DR570Q04RDF.
     DF307Q01RB DR570Q04RDF.
     DF307Q01RA DR570Q04RDF.
     DMA162Q03RC DR570Q04RDF.
     DMA162Q03RB DR570Q04RDF.
     DMA162Q03RA DR570Q04RDF.
     DF031Q01RD DR570Q04RDF.
     DF031Q01RC DR570Q04RDF.
     DF031Q01RB DR570Q04RDF.
     DF031Q01RA DR570Q04RDF.
     DF012Q02RB DR570Q04RDF.
     DF012Q02RA DR570Q04RDF.
     DF308Q04RD DR570Q04RDF.
     DF308Q04RC DR570Q04RDF.
     DF308Q04RB DR570Q04RDF.
     DF308Q04RA DR570Q04RDF.
     DF308Q02RC DR570Q04RDF.
     DF308Q02RB DR570Q04RDF.
     DF308Q02RA DR570Q04RDF.
     DF308Q01RC DR570Q04RDF.
     DF308Q01RB DR570Q04RDF.
     DF308Q01RA DR570Q04RDF.
     DM420Q01RD DR570Q04RDF.
     DM420Q01RC DR570Q04RDF.
     DF097Q01RC DR570Q04RDF.
     DF097Q01RB DR570Q04RDF.
     DF097Q01RA DR570Q04RDF.
     DM420Q01RB DR570Q04RDF.
     DM905Q01RB DR570Q04RDF.
     DM420Q01RA DR570Q04RDF.
     DM905Q01RA DR570Q04RDF.
     DR567Q08RE DR570Q04RDF.
     DR567Q08RD DR570Q04RDF.
     DR567Q08RC DR570Q04RDF.
     DR567Q08RB DR570Q04RDF.
     DR567Q08RA DR570Q04RDF.
     DM408Q01RD DR570Q04RDF.
     DR567Q11RF DR570Q04RDF.
     DR567Q11RD DR570Q04RDF.
     DR567Q11RC DR570Q04RDF.
     DR567Q11RA DR570Q04RDF.
     DM408Q01RC DR570Q04RDF.
     DM408Q01RB DR570Q04RDF.
     DM408Q01RA DR570Q04RDF.
     DMA158Q02RC DR570Q04RDF.
     DMA158Q02RB DR570Q04RDF.
     DMA158Q02RA DR570Q04RDF.
     DR570Q04RD DR570Q04RDF.
     DR570Q04RC DR570Q04RDF.
     DR570Q04RB DR570Q04RDF.
     DR570Q04RA DR570Q04RDF.
     DR544Q14RE DR570Q04RDF.
     DR544Q14RD DR570Q04RDF.
     DR544Q14RC DR570Q04RDF.
     DR544Q14RB DR570Q04RDF.
     DR544Q14RA DR570Q04RDF.
     DM949Q02RC DR570Q04RDF.
     DM949Q02RB DR570Q04RDF.
     DMA113Q02RD DR570Q04RDF.
     DMA113Q02RC DR570Q04RDF.
     DMA113Q02RB DR570Q04RDF.
     DM949Q02RA DR570Q04RDF.
     DMA113Q02RA DR570Q04RDF.
     DM949Q01RC DR570Q04RDF.
     DM949Q01RB DR570Q04RDF.
     DM949Q01RA DR570Q04RDF.
     DMA144Q03RC DR570Q04RDF.
     DMA144Q03RB DR570Q04RDF.
     DMA144Q03RA DR570Q04RDF.
     DR453Q05RD DR570Q04RDF.
     DR453Q05RC DR570Q04RDF.
     DMA151Q01RD DR570Q04RDF.
     DR453Q05RB DR570Q04RDF.
     DMA151Q01RC DR570Q04RDF.
     DR453Q05RA DR570Q04RDF.
     DMA151Q01RB DR570Q04RDF.
     DMA151Q01RA DR570Q04RDF.
     DMA160Q01RD DR570Q04RDF.
     DMA160Q01RC DR570Q04RDF.
     DMA160Q01RB DR570Q04RDF.
     DMA160Q01RA DR570Q04RDF.
     DR466Q03RC DR570Q04RDF.
     DR466Q03RB DR570Q04RDF.
     DR466Q03RA DR570Q04RDF.
     DR549Q13RD DR570Q04RDF.
     DR549Q13RC DR570Q04RDF.
     DR549Q13RB DR570Q04RDF.
     DR549Q12RD DR570Q04RDF.
     DR549Q12RB DR570Q04RDF.
     DR549Q12RA DR570Q04RDF.
     DMA117Q04RC DR570Q04RDF.
     DM603Q01RC DR570Q04RDF.
     DMA117Q04RB DR570Q04RDF.
     DMA117Q04RA DR570Q04RDF.
     DM603Q01RB DR570Q04RDF.
     DM603Q01RA DR570Q04RDF.
     DMA112Q02R DR570Q04RDF.
     DR561Q04RC DR570Q04RDF.
     DR561Q04RB DR570Q04RDF.
     DR561Q04RA DR570Q04RDF.
     DMA105Q04RC DR570Q04RDF.
     DMA105Q04RB DR570Q04RDF.
     DMA105Q04RA DR570Q04RDF.
     DR455Q05RD DR570Q04RDF.
     DR455Q05RC DR570Q04RDF.
     DR455Q05RB DR570Q04RDF.
     DR455Q05RA DR570Q04RDF.
     DMA105Q03RB DR570Q04RDF.
     DMA105Q03RA DR570Q04RDF.
     DR558Q10RD DR570Q04RDF.
     DR558Q10RC DR570Q04RDF.
     DR558Q10RB DR570Q04RDF.
     DR558Q10RA DR570Q04RDF.
     DM982Q03RB DR570Q04RDF.
     DM982Q03RA DR570Q04RDF.
     DR558Q02RC DR570Q04RDF.
     DR558Q02RB DR570Q04RDF.
     DR558Q02RA DR570Q04RDF.
     DR547Q07RF DR570Q04RDF.
     DR547Q07RE DR570Q04RDF.
     DR547Q07RD DR570Q04RDF.
     DR547Q07RC DR570Q04RDF.
     DR547Q07RB DR570Q04RDF.
     DR547Q07RA DR570Q04RDF.
     DM967Q03RB DR570Q04RDF.
     DM967Q03RA DR570Q04RDF.
     DM155Q04RD DR570Q04RDF.
     DF095Q02RB DR556Q12RDF.
     DF095Q02RA DR556Q12RDF.
     DR556Q12RD DR556Q12RDF.
     DR556Q12RC DR556Q12RDF.
     DR556Q12RB DR556Q12RDF.
     DR556Q12RA DR556Q12RDF.
     DMA107Q01R DR570Q08RF.
     DMA145Q02R DR570Q08RF.
     DR404Q06R DR570Q08RF.
     DR404Q03R DR570Q08RF.
     DM800Q01R DR570Q08RF.
     DMA145Q01R DR570Q08RF.
     DR559Q06R DR570Q08RF.
     DMA147Q04R DR570Q08RF.
     DR559Q03R DR570Q08RF.
     DR559Q04R DR570Q08RF.
     DMA147Q03R DR570Q08RF.
     DR559Q01R DR570Q08RF.
     DR560Q08R DR570Q08RF.
     DMA147Q02R DR570Q08RF.
     DR560Q06R DR570Q08RF.
     DR560Q03R DR570Q08RF.
     DMA147Q01R DR570Q08RF.
     DR220Q06R DR570Q08RF.
     DMA130Q03R DR570Q08RF.
     DR220Q05R DR570Q08RF.
     DR220Q04R DR570Q08RF.
     DM948Q01R DR570Q08RF.
     DR220Q02R DR570Q08RF.
     DR545Q07R DR570Q08RF.
     DR545Q06R DR570Q08RF.
     DR545Q02R DR570Q08RF.
     DM559Q01R DR570Q08RF.
     DM943Q01R DR570Q08RF.
     DF082Q02R DR570Q08RF.
     DF300Q03R DR570Q08RF.
     DMA131Q02R DR570Q08RF.
     DF106Q02R DR570Q08RF.
     DMA131Q01R DR570Q08RF.
     DF307Q05R DR570Q08RF.
     DF033Q01R DR570Q08RF.
     DMA154Q02R DR570Q08RF.
     DF105Q02R DR570Q08RF.
     DF105Q01R DR570Q08RF.
     DMA154Q01R DR570Q08RF.
     DM305Q01R DR570Q08RF.
     DF095Q01R DR570Q08RF.
     DF012Q01R DR570Q08RF.
     DMA162Q01R DR570Q08RF.
     DF308Q03R DR570Q08RF.
     DMA135Q04R DR570Q08RF.
     DMA127Q03R DR570Q08RF.
     DMA135Q02R DR570Q08RF.
     DMA135Q01R DR570Q08RF.
     DF303Q01R DR570Q08RF.
     DMA111Q02R DR570Q08RF.
     DF009Q02R DR570Q08RF.
     DMA138Q02R DR570Q08RF.
     DMA121Q03R DR570Q08RF.
     DMA138Q01R DR570Q08RF.
     DR102Q07R DR570Q08RF.
     DR460Q06R DR570Q08RF.
     DR460Q05R DR570Q08RF.
     DMA139Q02R DR570Q08RF.
     DMA149Q02R DR570Q08RF.
     DMA139Q01R DR570Q08RF.
     DR567Q04R DR570Q08RF.
     DMA137Q01R DR570Q08RF.
     DMA141Q04R DR570Q08RF.
     DR567Q10R DR570Q08RF.
     DMA141Q03R DR570Q08RF.
     DMA141Q02R DR570Q08RF.
     DR566Q06R DR570Q08RF.
     DMA161Q02R DR570Q08RF.
     DR566Q14R DR570Q08RF.
     DR566Q05R DR570Q08RF.
     DR566Q04R DR570Q08RF.
     DR570Q06R DR570Q08RF.
     DR570Q05R DR570Q08RF.
     DMA158Q01R DR570Q08RF.
     DR570Q02R DR570Q08RF.
     DR570Q08R DR570Q08RF.
     DR570Q01R DR570Q08RF.
     DMA108Q02R DR570Q08RF.
     DMA150Q02R DR570Q08RF.
     DR563Q03R DR570Q08RF.
     DR563Q02R DR570Q08RF.
     DR563Q07R DR570Q08RF.
     DMA102Q03R DR570Q08RF.
     DR563Q10R DR570Q08RF.
     DMA150Q01R DR570Q08RF.
     DR544Q12R DR570Q08RF.
     DR544Q10R DR570Q08RF.
     DMA123Q02R DR570Q08RF.
     DR544Q06R DR570Q08RF.
     DR544Q04R DR570Q08RF.
     DMA113Q03R DR570Q08RF.
     DR543Q10R DR570Q08RF.
     DR543Q09R DR570Q08RF.
     DR543Q04R DR570Q08RF.
     DMA114Q01R DR570Q08RF.
     DR543Q03R DR570Q08RF.
     DMA113Q01R DR570Q08RF.
     DR543Q01R DR570Q08RF.
     DR541Q10R DR570Q08RF.
     DR541Q05R DR570Q08RF.
     DMA116Q01R DR570Q08RF.
     DR541Q03R DR570Q08RF.
     DMA148Q02R DR570Q08RF.
     DM447Q01R DR570Q08RF.
     DR541Q01R DR570Q08RF.
     DMA142Q01R DR570Q08RF.
     DR568Q10R DR570Q08RF.
     DR568Q08R DR570Q08RF.
     DMA148Q01R DR570Q08RF.
     DR568Q05R DR570Q08RF.
     DMA144Q01R DR570Q08RF.
     DMA157Q02R DR570Q08RF.
     DR556Q10R DR570Q08RF.
     DMA133Q01R DR570Q08RF.
     DR556Q05R DR570Q08RF.
     DMA143Q04R DR570Q08RF.
     DR556Q04R DR570Q08RF.
     DR556Q03R DR570Q08RF.
     DMA143Q03R DR570Q08RF.
     DR556Q01R DR570Q08RF.
     DM909Q02R DR570Q08RF.
     DMA160Q03R DR570Q08RF.
     DMA143Q02R DR570Q08RF.
     DMA143Q01R DR570Q08RF.
     DR552Q06R DR570Q08RF.
     DR552Q09R DR570Q08RF.
     DMA151Q02R DR570Q08RF.
     DR552Q01R DR570Q08RF.
     DR453Q01R DR570Q08RF.
     DMA153Q02R DR570Q08RF.
     DMA134Q03R DR570Q08RF.
     DMA136Q03R DR570Q08RF.
     DR456Q01R DR570Q08RF.
     DM564Q01R DR570Q08RF.
     DR553Q05R DR570Q08RF.
     DR553Q01R DR570Q08RF.
     DR553Q02R DR570Q08RF.
     DR569Q04R DR570Q08RF.
     DR569Q03R DR570Q08RF.
     DR569Q01R DR570Q08RF.
     DMA146Q02R DR570Q08RF.
     DR562Q07R DR570Q08RF.
     DMA126Q04R DR570Q08RF.
     DR562Q02R DR570Q08RF.
     DMA146Q01R DR570Q08RF.
     DMA126Q03R DR570Q08RF.
     DR550Q05R DR570Q08RF.
     DR550Q04R DR570Q08RF.
     DM571Q01R DR570Q08RF.
     DMA140Q03R DR570Q08RF.
     DM411Q02R DR570Q08RF.
     DMA140Q02R DR570Q08RF.
     DMA132Q02R DR570Q08RF.
     DR111Q01R DR570Q08RF.
     DMA129Q03R DR570Q08RF.
     DR055Q01R DR570Q08RF.
     DM915Q01R DR570Q08RF.
     DMA125Q03R DR570Q08RF.
     DMA129Q01R DR570Q08RF.
     DR549Q10R DR570Q08RF.
     DR549Q06R DR570Q08RF.
     DR549Q04R DR570Q08RF.
     DMA117Q02R DR570Q08RF.
     DR564Q04R DR570Q08RF.
     DR564Q03R DR570Q08RF.
     DMA117Q01R DR570Q08RF.
     DR564Q02R DR570Q08RF.
     DR564Q01R DR570Q08RF.
     DMA110Q02R DR570Q08RF.
     DR561Q03R DR570Q08RF.
     DR561Q01R DR570Q08RF.
     DMA110Q01R DR570Q08RF.
     DR542Q08R DR570Q08RF.
     DR542Q05R DR570Q08RF.
     DMA119Q01R DR570Q08RF.
     DR542Q01R DR570Q08RF.
     DMA105Q05R DR570Q08RF.
     DR540Q06R DR570Q08RF.
     DMA115Q02R DR570Q08RF.
     DR540Q05R DR570Q08RF.
     DM033Q01R DR570Q08RF.
     DMA115Q01R DR570Q08RF.
     DR540Q03R DR570Q08RF.
     DR540Q01R DR570Q08RF.
     DM982Q04R DR570Q08RF.
     DMA101Q02R DR570Q08RF.
     DR455Q04R DR570Q08RF.
     DMA109Q03R DR570Q08RF.
     DMA109Q02R DR570Q08RF.
     DR558Q06R DR570Q08RF.
     DMA109Q01R DR570Q08RF.
     DMA105Q02R DR570Q08RF.
     DMA105Q01R DR570Q08RF.
     DR547Q06R DR570Q08RF.
     DR547Q03R DR570Q08RF.
     DMA120Q01R DR570Q08RF.
     DM423Q01R DR570Q08RF.
     DR547Q02R DR570Q08RF.
     DR565Q09R DR570Q08RF.
     DMA124Q01R DR570Q08RF.
     DR565Q08R DR570Q08RF.
     DR565Q03R DR570Q08RF.
     DM939Q02R DR570Q08RF.
     DR565Q01R DR570Q08RF.
     DF033Q02R DM906Q01RF.
     DM273Q01RD DM906Q01RF.
     DM273Q01RC DM906Q01RF.
     DM273Q01RB DM906Q01RF.
     DM273Q01RA DM906Q01RF.
     DM564Q02R DM906Q01RF.
     DM906Q01R DM906Q01RF.
     DM192Q01RC DM192Q01RCF.
     DM192Q01RB DM192Q01RCF.
     DM192Q01RA DM192Q01RCF.
     DM474Q01R DM474Q01RF.
     DMA161Q04C DMA161Q04CF.
     DF307Q02RD DR566Q09REF.
     DF307Q02RC DR566Q09REF.
     DF307Q02RB DR566Q09REF.
     DF307Q02RA DR566Q09REF.
     DF402Q02RF DR566Q09REF.
     DF402Q02RE DR566Q09REF.
     DF402Q02RD DR566Q09REF.
     DF402Q02RC DR566Q09REF.
     DF402Q02RB DR566Q09REF.
     DF402Q02RA DR566Q09REF.
     DF202Q01RD DR566Q09REF.
     DF202Q01RC DR566Q09REF.
     DF202Q01RB DR566Q09REF.
     DF202Q01RA DR566Q09REF.
     DF303Q02RE DR566Q09REF.
     DF303Q02RD DR566Q09REF.
     DF303Q02RC DR566Q09REF.
     DF303Q02RB DR566Q09REF.
     DF303Q02RA DR566Q09REF.
     DR432Q06RI DR566Q09REF.
     DR432Q06RH DR566Q09REF.
     DR432Q06RG DR566Q09REF.
     DR432Q06RF DR566Q09REF.
     DR432Q06RE DR566Q09REF.
     DR432Q06RD DR566Q09REF.
     DR432Q06RC DR566Q09REF.
     DR432Q06RB DR566Q09REF.
     DR432Q06RA DR566Q09REF.
     DMA149Q01RD DR566Q09REF.
     DMA149Q01RC DR566Q09REF.
     DMA149Q01RB DR566Q09REF.
     DMA149Q01RA DR566Q09REF.
     DMA137Q03RD DR566Q09REF.
     DMA137Q03RC DR566Q09REF.
     DMA137Q03RB DR566Q09REF.
     DMA137Q03RA DR566Q09REF.
     DR566Q09RE DR566Q09REF.
     DR566Q09RD DR566Q09REF.
     DR566Q09RC DR566Q09REF.
     DR566Q09RB DR566Q09REF.
     DR566Q09RA DR566Q09REF.
     DMA108Q03RG DR566Q09REF.
     DMA108Q03RF DR566Q09REF.
     DMA108Q03RE DR566Q09REF.
     DMA108Q03RD DR566Q09REF.
     DMA108Q03RC DR566Q09REF.
     DMA108Q03RB DR566Q09REF.
     DMA108Q03RA DR566Q09REF.
     DMA102Q01RE DR566Q09REF.
     DMA102Q01RD DR566Q09REF.
     DMA102Q01RC DR566Q09REF.
     DMA102Q01RB DR566Q09REF.
     DMA102Q01RA DR566Q09REF.
     DMA114Q03RE DR566Q09REF.
     DMA114Q03RD DR566Q09REF.
     DMA114Q03RC DR566Q09REF.
     DMA114Q03RB DR566Q09REF.
     DMA114Q03RA DR566Q09REF.
     DR446Q03RG DR566Q09REF.
     DR446Q03RF DR566Q09REF.
     DR446Q03RE DR566Q09REF.
     DR446Q03RD DR566Q09REF.
     DR446Q03RC DR566Q09REF.
     DR446Q03RB DR566Q09REF.
     DR446Q03RA DR566Q09REF.
     DMA120Q03RD DR566Q09REF.
     DMA120Q03RC DR566Q09REF.
     DMA120Q03RB DR566Q09REF.
     DMA120Q03RA DR566Q09REF.
     DMA120Q02RE DR566Q09REF.
     DMA120Q02RD DR566Q09REF.
     DMA120Q02RC DR566Q09REF.
     DMA120Q02RB DR566Q09REF.
     DMA120Q02RA DR566Q09REF.
     DR547Q10RM DR566Q09REF.
     DR547Q10RL DR566Q09REF.
     DR547Q10RK DR566Q09REF.
     DR547Q10RJ DR566Q09REF.
     DR547Q10RI DR566Q09REF.
     DR547Q10RH DR566Q09REF.
     DR547Q10RG DR566Q09REF.
     DR547Q10RF DR566Q09REF.
     DR547Q10RE DR566Q09REF.
     DR547Q10RD DR566Q09REF.
     DR547Q10RC DR566Q09REF.
     DR547Q10RB DR566Q09REF.
     DR547Q10RA DR566Q09REF.
     DMA103Q04RB DR590Q66RF.
     DMA103Q04RA DR590Q66RF.
     DR590Q66R DR590Q66RF.
     DR590Q62R DR590Q66RF.
     DR590Q17R DR590Q66RF.
     DR590Q63R DR590Q66RF.
     DR590Q29R DR590Q66RF.
     DR590Q11R DR590Q66RF.
     DR590Q40R DR590Q66RF.
     DR590Q49R DR590Q66RF.
     DR590Q21R DR590Q66RF.
     DR590Q36R DR590Q66RF.
     DR590Q08R DR590Q66RF.
     DR590Q64R DR590Q66RF.
     DR590Q53R DR590Q66RF.
     DR590Q54R DR590Q66RF.
     DR590Q39R DR590Q66RF.
     DR590Q51R DR590Q66RF.
     DR590Q32R DR590Q66RF.
     DR590Q31R DR590Q66RF.
     DR590Q07R DR590Q66RF.
     DR590Q50R DR590Q66RF.
     DR590Q06R DR590Q66RF.
     DR590Q46R DR590Q66RF.
     DR590Q58R DR590Q66RF.
     DR590Q16R DR590Q66RF.
     DR590Q56R DR590Q66RF.
     DR590Q09R DR590Q66RF.
     DR590Q28R DR590Q66RF.
     DR590Q30R DR590Q66RF.
     DR590Q15R DR590Q66RF.
     DR590Q19R DR590Q66RF.
     DR590Q44R DR590Q66RF.
     DR590Q48R DR590Q66RF.
     DR590Q26R DR590Q66RF.
     DR590Q65R DR590Q66RF.
     DR590Q14R DR590Q66RF.
     DR590Q55R DR590Q66RF.
     DR590Q38R DR590Q66RF.
     DR590Q23R DR590Q66RF.
     DR590Q34R DR590Q66RF.
     DR590Q47R DR590Q66RF.
     DR590Q22R DR590Q66RF.
     DR590Q01R DR590Q66RF.
     DR590Q05R DR590Q66RF.
     DR590Q60R DR590Q66RF.
     DR590Q41R DR590Q66RF.
     DR590Q57R DR590Q66RF.
     DR590Q13R DR590Q66RF.
     DR590Q25R DR590Q66RF.
     DR590Q45R DR590Q66RF.
     DR590Q42R DR590Q66RF.
     DR590Q37R DR590Q66RF.
     DR590Q10R DR590Q66RF.
     DR590Q18R DR590Q66RF.
     DR590Q02R DR590Q66RF.
     DR590Q61R DR590Q66RF.
     DR590Q35R DR590Q66RF.
     DR590Q52R DR590Q66RF.
     DR590Q43R DR590Q66RF.
     DR590Q24R DR590Q66RF.
     DR590Q20R DR590Q66RF.
     DR590Q33R DR590Q66RF.
     DR590Q59R DR590Q66RF.
     DR590Q03R DR590Q66RF.
     DR590Q27R DR590Q66RF.
     DR590Q04R DR590Q66RF.
     DMA128Q03RC DMA128Q03RCF.
     DMA128Q03RB DMA128Q03RCF.
     DMA128Q03RA DMA128Q03RCF.
     DMA152Q02RA DMA152Q02RAF.
     DMA103Q05RA DMA103Q05RAF.
     STRATUM $STRATUMF.
     ;
run;
